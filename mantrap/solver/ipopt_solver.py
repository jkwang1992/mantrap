from abc import abstractmethod
from collections import defaultdict, deque
import logging
import os
from typing import Dict, List, Tuple, Union

import ipopt
import numpy as np
import torch

from mantrap.constants import ipopt_max_solver_steps, ipopt_max_solver_cpu_time
from mantrap.simulation.graph_based import GraphBasedSimulation
from mantrap.solver.constraints.constraint_module import ConstraintModule
from mantrap.solver.constraints import CONSTRAINTS
from mantrap.solver.objectives.objective_module import ObjectiveModule
from mantrap.solver.objectives import OBJECTIVES
from mantrap.solver.solver import Solver
from mantrap.utility.io import build_os_path


class IPOPTSolver(Solver):

    def __init__(
        self,
        sim: GraphBasedSimulation,
        goal: torch.Tensor,
        objectives: List[Tuple[str, float]] = None,
        **solver_params
    ):
        super(IPOPTSolver, self).__init__(sim, goal, **solver_params)

        # The objective and constraint functions (and their gradients) are packed into objectives, for a more compact
        # representation, the ease of switching between different objective functions and to simplify logging and
        # visualization.
        objective_modules = self.objective_defaults() if objectives is None else objectives
        self._objective_modules = self._build_objective_modules(modules=objective_modules)
        self._constraint_modules = self._build_constraint_modules(modules=self.constraints_modules())

        # Logging variables. Using default-dict(deque) whenever a new entry is created, it does not have to be checked
        # whether the related key is already existing, since if it is not existing, it is created with a queue as
        # starting value, to which the new entry is appended. With an appending complexity O(1) instead of O(N) the
        # deque is way more efficient than the list type for storing simple floating point numbers in a sequence.
        self._optimization_log = defaultdict(deque)
        self._param_latest = dict()

    def solve_single_optimization(
        self,
        z0: torch.Tensor = None,
        max_iter: int = ipopt_max_solver_steps,
        max_cpu_time: float = ipopt_max_solver_cpu_time,
        approx_jacobian: bool = False,
        approx_hessian: bool = True,
        check_derivative: bool = False,
        return_controls: bool = False,
        iteration_tag: str = ""
    ):
        """Solve optimization problem by finding constraint bounds, constructing ipopt optimization problem and
        solve it using the parameters defined in the function header."""
        lb, ub, cl, cu = self.constraint_bounds()

        # Formulate optimization problem as in standardized IPOPT format.
        z0 = z0 if z0 is not None else self.z0_default()
        u0_flat = z0.flatten().numpy().tolist()
        assert len(u0_flat) == len(lb) == len(ub)

        nlp = ipopt.problem(n=len(u0_flat), m=len(cl), problem_obj=self, lb=lb, ub=ub, cl=cl, cu=cu)
        nlp.addOption("max_iter", max_iter)
        nlp.addOption("max_cpu_time", max_cpu_time)
        if approx_jacobian:
            nlp.addOption("jacobian_approximation", "finite-difference-values")
        if approx_hessian:
            nlp.addOption("hessian_approximation", "limited-memory")

        print_level = 5 if self.is_verbose or check_derivative else 0  # the larger the value, the more print output.
        nlp.addOption("print_level", print_level)
        if self.is_verbose:
            nlp.addOption("print_timing_statistics", "yes")
        if check_derivative:
            nlp.addOption("derivative_test", "first-order")
            nlp.addOption("derivative_test_tol", 1e-4)

        # Solve optimization problem for "optimal" ego trajectory `x_optimized`.
        z_optimized, info = nlp.solve(u0_flat)
        x5_optimized = self.z_to_ego_trajectory(z_optimized)
        z2_optimized = torch.from_numpy(z_optimized).view(-1, 2)

        # Plot optimization progress.
        self.log_and_clean_up(tag=iteration_tag)
        return x5_optimized if not return_controls else (x5_optimized, z2_optimized)

    def determine_ego_controls(self, **solver_kwargs) -> torch.Tensor:
        logging.info("solver starting ipopt optimization procedure")
        _, z_opt = self.solve_single_optimization(**solver_kwargs, return_controls=True)
        return self.z_to_ego_controls(z_opt.detach().numpy())

    ###########################################################################
    # Initialization ##########################################################
    ###########################################################################
    @abstractmethod
    def z0_default(self) -> torch.Tensor:
        raise NotImplementedError

    ###########################################################################
    # Optimization formulation - Objective ####################################
    # IPOPT requires to use numpy arrays for computation, therefore switch ####
    # everything from torch to numpy here #####################################
    ###########################################################################
    @staticmethod
    def objective_defaults() -> List[Tuple[str, float]]:
        raise NotImplementedError

    def objective(self, z: np.ndarray) -> float:
        x4 = self.z_to_ego_trajectory(z)
        objective = np.sum([m.objective(x4) for m in self._objective_modules.values()])

        logging.debug(f"Objective function = {objective}")
        self.logging(z=torch.from_numpy(z).view(-1, 2), x4=x4)
        return float(objective)

    def gradient(self, z: np.ndarray) -> np.ndarray:
        x4, grad_wrt = self.z_to_ego_trajectory(z, return_leaf=True)
        gradient = np.sum([m.gradient(x4, grad_wrt=grad_wrt) for m in self._objective_modules.values()], axis=0)

        logging.debug(f"Gradient function = {gradient}")
        self.logging(z=torch.from_numpy(z).view(-1, 2), x4=x4)
        return gradient

    ###########################################################################
    # Optimization formulation - Constraints ##################################
    ###########################################################################
    @abstractmethod
    def constraint_bounds(self) -> Tuple[List, List, List, List]:
        raise NotImplementedError

    @staticmethod
    def constraints_modules() -> List[str]:
        raise NotImplementedError

    def constraints(self, z: np.ndarray) -> np.ndarray:
        if self.is_unconstrained:
            constraints = np.array([])
        else:
            x4 = self.z_to_ego_trajectory(z)
            constraints = np.concatenate([m.constraint(x4) for m in self._constraint_modules.values()])

        logging.debug(f"Constraints vector = {constraints}")
        return constraints

    def jacobian(self, z: np.ndarray) -> np.ndarray:
        if self.is_unconstrained:
            jacobian = np.array([])
        else:
            x4, grad_wrt = self.z_to_ego_trajectory(z, return_leaf=True)
            jacobian = np.concatenate([m.jacobian(x4, grad_wrt=grad_wrt) for m in self._constraint_modules.values()])

        logging.debug(f"Constraint jacobian function computed")
        return jacobian

    # wrong hessian should just affect rate of convergence, not convergence in general
    # (given it is semi-positive definite which is the case for the identity matrix)
    # hessian = np.eye(3*self.O)
    def hessian(self, z, lagrange=None, obj_factor=None) -> np.ndarray:
        raise NotImplementedError

    ###########################################################################
    # Utility #################################################################
    ###########################################################################
    @abstractmethod
    def z_to_ego_trajectory(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        raise NotImplementedError

    @abstractmethod
    def z_to_ego_controls(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        raise NotImplementedError

    def logging(self, **kwargs):
        self._param_latest.update(kwargs)

    def _build_objective_modules(self, modules: List[Tuple[str, float]]) -> Dict[str, ObjectiveModule]:
        assert all([name in OBJECTIVES.keys() for name, _ in modules]), "invalid objective module detected"
        assert all([0.0 <= weight for _, weight in modules]), "invalid solver module weight detected"
        return {m: OBJECTIVES[m](horizon=self.T, weight=w, env=self._env, goal=self.goal) for m, w in modules}

    @staticmethod
    def _build_constraint_modules(modules: List[str]) -> Dict[str, ConstraintModule]:
        assert all([name in CONSTRAINTS.keys() for name in modules]), "invalid constraint module detected"
        return {m: CONSTRAINTS[m]() for m in modules}

    ###########################################################################
    # Visualization ###########################################################
    ###########################################################################
    def intermediate(self, alg_mod, iter_count, obj_value, inf_pr, inf_du, mu, d_norm, *args):
        self._optimization_log["iter_count"].append(iter_count)
        self._optimization_log["obj_overall"].append(obj_value)
        self._optimization_log["inf_primal"].append(inf_pr)
        self._optimization_log["grad_lagrange"].append(d_norm)
        for key, value in self._param_latest.items():
            self._optimization_log[key].append(value)
        for module in self._objective_modules.values():
            module.logging()
        for module in self._constraint_modules.values():
            module.logging()

    def constraints_fulfilled(self) -> Union[bool, None]:
        if len(self._optimization_log) == 0:
            return None
        return self._optimization_log["inf_primal"][-1] < 1e-6

    @property
    def is_unconstrained(self) -> bool:
        return len(self._constraint_modules.keys()) == 0

    def log_and_clean_up(self, tag: str = ""):
        """Clean up optimization logs and reset optimization parameters.
        IPOPT determines the CPU time including the intermediate function, therefore if we would plot at every step,
        we would loose valuable optimization time. Therefore the optimization progress is plotted all at once at the
        end of the optimization process."""
        self._optimization_log = {k: list(data) for k, data in self._optimization_log.items() if not type(data) == list}

        # Transfer objective modules logs to main logging dictionary and clean up objectives.
        for module_name, module in self._objective_modules.items():
            obj_log, grad_log = module.logs
            self._optimization_log[f"obj_{module_name}"] = obj_log
            self._optimization_log[f"grad_{module_name}"] = grad_log
            module.clean_up()

        # Transfer constraint modules logs to main logging dictionary and clean up objectives.
        for module_name, module in self._constraint_modules.items():
            self._optimization_log[f"inf_{module_name}"] = module.logs
            module.clean_up()

        # Logging.
        do_logging = len(self._optimization_log) > 0 and all([len(v) > 2 for v in self._optimization_log.values()])
        if do_logging:
            num_optimization_steps = self._optimization_log["iter_count"][-1]
            obj_dict = {name: f"{xs[0]} ==> {xs[-1]}" for name, xs in self._optimization_log.items() if "obj" in name}
            inf_dict = {name: f"{xs[0]} ==> {xs[-1]}" for name, xs in self._optimization_log.items() if "inf" in name}
            logging.info(f"solver ipopt optimization finished after {num_optimization_steps} steps")
            logging.info(f"solver ipopt optimization: {obj_dict}")
            logging.info(f"solver ipopt optimization: {inf_dict}")

        # Plotting only makes sense if you see some progress in the optimization, i.e. compare and figure out what
        # the current optimization step has changed.
        if self.is_verbose and do_logging:
            from mantrap.evaluation.visualization import visualize_optimization
            name_tag = self.__class__.__name__.lower()
            output_directory_path = build_os_path(f"test/graphs/{name_tag}", make_dir=True, free=True)
            output_path = os.path.join(output_directory_path, tag)
            visualize_optimization(self._optimization_log, env=self._env, file_path=output_path)

        # Reset optimization logging parameters for next optimization.
        self._optimization_log = defaultdict(deque)
        self._param_latest = dict()
