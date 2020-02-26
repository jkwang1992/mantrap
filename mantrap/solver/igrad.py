from typing import List, Tuple

import numpy as np
import torch

from mantrap.simulation.graph_based import GraphBasedSimulation
from mantrap.solver.ipopt_solver import IPOPTSolver
from mantrap.utility.maths import lagrange_interpolation
from mantrap.utility.primitives import square_primitives


class IGradSolver(IPOPTSolver):

    def __init__(self, sim: GraphBasedSimulation, goal: torch.Tensor, **solver_params):
        super(IGradSolver, self).__init__(sim, goal, **solver_params)

        # Number of control points determines the number of points used for interpolation, next to the initial
        # and terminal (goal) point. This is equivalent to the number of optimization variables (x2 -> 2D).
        if "num_control_points" not in self._solver_params.keys():
            self._solver_params["num_control_points"] = 2

    ###########################################################################
    # Initialization ##########################################################
    ###########################################################################
    def z0s_default(self) -> torch.Tensor:
        x20s = square_primitives(start=self.env.ego.position, end=self.goal, dt=self.env.dt, steps=self.T)
        x40s = torch.zeros((self.T, 4))
        for i, x20 in enumerate(x20s):
            x40s[i] = self.env.ego.expand_trajectory(path=x20, dt=self.env.dt)
        return x40s

    ###########################################################################
    # Optimization formulation - Objective ####################################
    ###########################################################################
    @staticmethod
    def objective_defaults() -> List[Tuple[str, float]]:
        return [("interaction", 1.0)]

    ###########################################################################
    # Optimization formulation - Constraints ##################################
    ###########################################################################
    @staticmethod
    def constraints_modules() -> List[str]:
        return ["max_speed"]

    ###########################################################################
    # Utility #################################################################
    ###########################################################################
    def z_to_ego_trajectory(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        mid = torch.tensor(z.astype(np.float64)).view(self.num_control_points, 2).double()
        mid.requires_grad = True

        start_point = self._env.ego.position.unsqueeze(0)
        end_point = self._goal.unsqueeze(0)
        control_points = torch.cat((start_point, mid, end_point))
        path = lagrange_interpolation(control_points, num_samples=self.T, deg=self.num_control_points + 2)

        x4 = self.env.ego.expand_trajectory(path, dt=self.env.dt)[:, 0:4]
        return x4 if not return_leaf else (x4, mid)

    @property
    def num_control_points(self) -> int:
        return self._solver_params["num_control_points"]
