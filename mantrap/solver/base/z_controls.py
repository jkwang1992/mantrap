from abc import ABC
import typing

import numpy as np
import torch

import mantrap.solver
import mantrap.utility.shaping

from .trajopt import TrajOptSolver


class ZControlIntermediate(TrajOptSolver, ABC):

    ###########################################################################
    # Problem formulation - Formulation #######################################
    ###########################################################################
    def num_optimization_variables(self) -> int:
        return 2 * self.planning_horizon

    def optimization_variable_bounds(self) -> typing.Tuple[typing.List, typing.List]:
        lower, upper = self._env.ego.control_limits()
        lb = (np.ones(self.num_optimization_variables()) * lower).tolist()
        ub = (np.ones(self.num_optimization_variables()) * upper).tolist()
        return lb, ub

    ###########################################################################
    # Transformations #########################################################
    ###########################################################################
    def z_to_ego_trajectory(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        ego_controls = torch.from_numpy(z).view(-1, 2).float()
        ego_controls.requires_grad = True
        ego_trajectory = self.env.ego.unroll_trajectory(controls=ego_controls, dt=self.env.dt)
        assert mantrap.utility.shaping.check_ego_trajectory(ego_trajectory, pos_and_vel_only=True)
        return ego_trajectory if not return_leaf else (ego_trajectory, ego_controls)

    def z_to_ego_controls(self, z: np.ndarray, return_leaf: bool = False) -> torch.Tensor:
        ego_controls = torch.from_numpy(z).view(-1, 2).float()
        ego_controls.requires_grad = True
        assert mantrap.utility.shaping.check_ego_controls(ego_controls)
        return ego_controls if not return_leaf else (ego_controls, ego_controls)

    def ego_trajectory_to_z(self, ego_trajectory: torch.Tensor) -> np.ndarray:
        assert mantrap.utility.shaping.check_ego_trajectory(ego_trajectory)
        controls = self.env.ego.roll_trajectory(ego_trajectory, dt=self.env.dt)
        return controls.flatten().detach().numpy()

    def ego_controls_to_z(self, ego_controls: torch.Tensor) -> np.ndarray:
        assert mantrap.utility.shaping.check_ego_controls(ego_controls)
        return ego_controls.flatten().detach().numpy()