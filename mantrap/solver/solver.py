from abc import abstractmethod
from collections import defaultdict, deque
import logging
import os
from typing import Dict, List, Tuple

import numpy as np
import torch

from mantrap.constants import solver_horizon
from mantrap.simulation.simulation import GraphBasedSimulation
from mantrap.solver.constraints.constraint_module import ConstraintModule
from mantrap.solver.constraints import CONSTRAINTS
from mantrap.solver.objectives.objective_module import ObjectiveModule
from mantrap.solver.objectives import OBJECTIVES
from mantrap.utility.io import build_os_path
from mantrap.utility.shaping import check_ego_controls


class Solver:

    def __init__(
        self,
        sim: GraphBasedSimulation,
        goal: torch.Tensor,
        t_planning: int = solver_horizon,
        objectives: List[Tuple[str, float]] = None,
        verbose: bool = False,
        **solver_params
    ):
        """Initialise solver class by building objective and constraint modules as defined within the specific
        definition of the (optimisation) problem. The verbose flag enables printing more debugging flags as well
        as plotting the optimisation history at the end.

        :param: sim: simulation environment the solver's forward simulations are based on.
        :param: goal: goal state (position) of the robot (2).
        :param: t_planning: planning horizon, i.e. how many future time-steps shall be taken into account in planning.
        :param: verbose: debugging flag (logging, visualisation -> comp. expensive !).
        :param: objectives: List of objective module names and according weights.
        """
        assert goal.size() == torch.Size([2])
        self._env = sim
        self._goal = goal.float()

        # Dictionary of solver parameters.
        self._solver_params = solver_params
        self._solver_params["t_planning"] = t_planning
        self._solver_params["verbose"] = verbose

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
        self._variables_latest = defaultdict(deque)
        self._iteration = 0

    def solve(self, time_steps: int, **solver_kwargs) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Find the ego trajectory given the internal simulation with the current scene as initial condition.
        Therefore iteratively solve the problem for the scene at t = t_k, update the scene using the internal simulator
        and the derived ego policy and repeat until t_k = `horizon` or until the goal has been reached.
        This method changes the internal environment by forward simulating it over the prediction horizon.

        :param: time_steps: how many time-steps shall be solved (not planning horizon !).
        :return: derived ego trajectory [horizon, 5].
        :return: ado trajectories [horizon, num_ados, modes, T, 5] conditioned on the derived ego trajectory
        :return: planned ego trajectory for every step [horizon, T, 2].
        """
        x5_opt = torch.zeros((time_steps, 5))
        ado_trajectories = torch.zeros((time_steps - 1, self._env.num_ados, self._env.num_ado_modes, self.T, 5))
        x5_opt_planned = torch.zeros((time_steps - 1, self.T, 5))

        # Initialize trajectories with current state and simulation time.
        x5_opt[0, :] = self._env.ego.state_with_time
        ado_trajectories[0] = self.env.predict_wo_ego(t_horizon=self.T).detach()

        logging.info(f"Starting trajectory optimization solving for planning horizon {time_steps} steps ...")
        for k in range(time_steps - 1):
            logging.info(f"solver @ time-step k = {k}")
            self._iteration = k

            ego_controls = self.determine_ego_controls(**solver_kwargs)
            assert check_ego_controls(ego_controls, t_horizon=self.T - 1)
            logging.info(f"solver @k={k}: ego optimized controls = {ego_controls.tolist()}")

            # Forward simulate environment.
            ado_state, ego_state = self._env.step(ego_control=ego_controls[0, :])

            # Logging.
            ado_trajectories[k] = self.env.predict_w_controls(controls=ego_controls).detach()
            x5_opt[k + 1, :] = ego_state.detach()
            x5_opt_planned[k] = self.env.ego.unroll_trajectory(controls=ego_controls, dt=self.env.dt).detach()

            # If the goal state has been reached, break the optimization loop (and shorten trajectories to
            # contain only states up to now (i.e. k + 2 optimization steps instead of max_steps).
            if torch.norm(ego_state[0:2] - self._goal) < 0.1:
                x5_opt = x5_opt[:k + 2, :].detach()
                ado_trajectories = ado_trajectories[:k + 2].detach()
                x5_opt_planned = x5_opt_planned[:k + 2].detach()
                break

        logging.info(f"Finishing up trajectory optimization solving")
        return x5_opt, ado_trajectories, x5_opt_planned

    @abstractmethod
    def determine_ego_controls(self, **solver_kwargs) -> torch.Tensor:
        """Determine the ego control inputs for the internally stated problem and the current state of the environment.
        The implementation crucially depends on the solver class itself and is hence not implemented here.

        :return: ego_controls: control inputs of ego agent for whole planning horizon.
        """
        raise NotImplementedError

    ###########################################################################
    # Problem formulation - Formulation #######################################
    ###########################################################################
    @abstractmethod
    def num_optimization_variables(self) -> int:
        raise NotImplementedError

    ###########################################################################
    # Problem formulation - Objective #########################################
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

    ###########################################################################
    # Problem formulation - Constraints #######################################
    ###########################################################################
    def optimization_variable_bounds(self) -> Tuple[List, List]:
        limits = self._env.ego.control_limits()
        lb = (np.ones(2 * self.num_optimization_variables()) * limits[0]).tolist()
        ub = (np.ones(2 * self.num_optimization_variables()) * limits[1]).tolist()
        return lb, ub

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

    @property
    def is_unconstrained(self) -> bool:
        return len(self._constraint_modules.keys()) == 0

    ###########################################################################
    # Utility #################################################################
    ###########################################################################
    @abstractmethod
    def z_to_ego_trajectory(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        raise NotImplementedError

    @abstractmethod
    def z_to_ego_controls(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        raise NotImplementedError

    def _build_objective_modules(self, modules: List[Tuple[str, float]]) -> Dict[str, ObjectiveModule]:
        assert all([name in OBJECTIVES.keys() for name, _ in modules]), "invalid objective module detected"
        assert all([0.0 <= weight for _, weight in modules]), "invalid solver module weight detected"
        return {m: OBJECTIVES[m](horizon=self.T, weight=w, env=self._env, goal=self.goal) for m, w in modules}

    def _build_constraint_modules(self, modules: List[str]) -> Dict[str, ConstraintModule]:
        assert all([name in CONSTRAINTS.keys() for name in modules]), "invalid constraint module detected"
        return {m: CONSTRAINTS[m](horizon=self.T, env=self._env) for m in modules}

    ###########################################################################
    # Visualization & Logging #################################################
    ###########################################################################
    def intermediate_log(self, iter_count: int, obj_value: float, inf_pr: float):
        self._optimization_log["iter_count"].append(iter_count)
        self._optimization_log["obj_overall"].append(obj_value)
        self._optimization_log["inf_primal"].append(inf_pr)

        # Log recent trial (trajectory solutions that have been tried).
        for key, trials in self._variables_latest.items():
            self._optimization_log[f"{key}_trials"].append(trials)
            self._optimization_log[key].append(trials[-1])
        self._variables_latest = defaultdict(deque)

        # Log objective and constraint modules.
        for module in self._objective_modules.values():
            module.logging()
        for module in self._constraint_modules.values():
            module.logging()

    def logging(self, **kwargs):
        for key, value in kwargs.items():
            self._variables_latest[key].append(value)

    def log_and_clean_up(self, tag: str = None):
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
            obj_dict = {n: f"{xs[0]:.4f} => {xs[-1]:.4f}" for n, xs in self._optimization_log.items() if "obj" in n}
            inf_dict = {n: f"{xs[0]:.4f} => {xs[-1]:.4f}" for n, xs in self._optimization_log.items() if "inf" in n}
            logging.info(f"ipopt optimization [{tag}] finished after {num_optimization_steps} steps")
            logging.info(f"ipopt optimization [{tag}]: {obj_dict}")
            logging.info(f"ipopt optimization [{tag}]: {inf_dict}")

        # Plotting only makes sense if you see some progress in the optimization, i.e. compare and figure out what
        # the current optimization step has changed.
        if self.is_verbose and do_logging:
            from mantrap.evaluation.visualization import visualize_optimization
            name_tag = self.__class__.__name__.lower()
            tag = "optimisation" if tag is None else tag
            output_directory_path = build_os_path(f"test/graphs/{name_tag}", make_dir=True, free=False)
            output_path = os.path.join(output_directory_path, tag)
            visualize_optimization(self._optimization_log, env=self._env, file_path=output_path)

        # Reset optimization logging parameters for next optimization.
        self._optimization_log = defaultdict(deque)
        self._variables_latest = defaultdict(deque)

    ###########################################################################
    # Solver parameters #######################################################
    ###########################################################################
    @property
    def env(self) -> GraphBasedSimulation:
        return self._env

    @env.setter
    def env(self, env: GraphBasedSimulation):
        self._env = env

    @property
    def goal(self) -> torch.Tensor:
        return self._goal

    @property
    def T(self) -> int:
        return self._solver_params["t_planning"]

    @property
    def is_verbose(self) -> bool:
        return self._solver_params["verbose"]
