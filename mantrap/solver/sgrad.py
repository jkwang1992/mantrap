from typing import List, Tuple

import numpy as np
import torch

from mantrap.solver.ipopt_solver import IPOPTSolver
from mantrap.utility.primitives import square_primitives
from mantrap.utility.shaping import check_ego_controls, check_ego_trajectory


class SGradSolver(IPOPTSolver):
    """Shooting NLP using IPOPT solver.

    .. math:: z = controls
    .. math:: J(z) = J_{goal} + J_{interaction}
    .. math:: C(z) = [C_{max-speed}, C_{min-distance}]
    """

    ###########################################################################
    # Initialization ##########################################################
    ###########################################################################
    def initialize(self, **solver_params):
        pass

    def z0s_default(self, just_one: bool = False) -> torch.Tensor:
        x20s = square_primitives(start=self.env.ego.position, end=self.goal, dt=self.env.dt, steps=self.T + 1)

        u0s = torch.zeros((x20s.shape[0], self.T, 2))
        for i, x20 in enumerate(x20s):
            x40 = self.env.ego.expand_trajectory(path=x20, dt=self.env.dt)
            u0s[i] = self.env.ego.roll_trajectory(trajectory=x40, dt=self.env.dt)

        return u0s if not just_one else u0s[1].reshape(self.T, 2)

    ###########################################################################
    # Problem formulation - Formulation #######################################
    ###########################################################################
    def num_optimization_variables(self) -> int:
        return self.T

    ###########################################################################
    # Optimization formulation - Objective ####################################
    ###########################################################################
    @staticmethod
    def objective_defaults() -> List[Tuple[str, float]]:
        return [("goal", 1.0), ("interaction", 1.0)]

    ###########################################################################
    # Optimization formulation - Constraints ##################################
    ###########################################################################
    @staticmethod
    def constraints_defaults() -> List[str]:
        return ["max_speed", "min_distance"]

    ###########################################################################
    # Utility #################################################################
    ###########################################################################
    def z_to_ego_trajectory(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        u2 = torch.from_numpy(z).view(self.T, 2)
        u2.requires_grad = True
        x5 = self.env.ego.unroll_trajectory(controls=u2, dt=self.env.dt)
        assert check_ego_trajectory(x5, t_horizon=self.T + 1, pos_and_vel_only=True)
        return x5 if not return_leaf else (x5, u2)

    def z_to_ego_controls(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        u2 = torch.from_numpy(z).view(self.T, 2)
        u2.requires_grad = True
        assert check_ego_controls(u2, t_horizon=self.T)
        return u2 if not return_leaf else (u2, u2)

    ###########################################################################
    # Logging parameters ######################################################
    ###########################################################################
    @property
    def solver_name(self) -> str:
        return "sgrad"
