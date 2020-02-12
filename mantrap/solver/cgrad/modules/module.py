from abc import abstractmethod
from collections import deque
import logging
from typing import List, Tuple

import numpy as np
import torch

from mantrap.simulation.simulation import GraphBasedSimulation


class Module:

    def __init__(self, horizon: int, weight: float = 1.0, **module_kwargs):
        self.weight = weight
        self.T = horizon

        # Logging variables for objective and gradient values. For logging the latest variables are stored
        # as class parameters and appended to the log when calling the `logging()` function, in order to avoid
        # appending multiple values within one optimization step.
        self._obj_current, self._grad_current = 0.0, np.zeros(2)
        self._log_obj = deque()
        self._log_grad = deque()

    ###########################################################################
    # Optimization Formulation ################################################
    ###########################################################################

    @abstractmethod
    def objective(self, x2: torch.Tensor) -> float:
        pass

    @abstractmethod
    def gradient(self, x2: torch.Tensor) -> np.ndarray:
        pass

    def _build_partial_gradients(self, x2: torch.Tensor, env: GraphBasedSimulation) -> np.ndarray:
        graphs = env.build_connected_graph(ego_positions=x2)
        ego_positions = [graphs[f"ego_{k}_position"] for k in range(self.T)]
        partial_grads = torch.zeros((self.T, self.T, env.num_ados, 2))
        for k in range(self.T):
            for m in range(env.num_ados):
                ado_output = graphs[f"{env.ado_ghosts[m].gid}_{k}_output"]
                grads_tuple = torch.autograd.grad(ado_output, inputs=ego_positions[:k + 1], retain_graph=True)
                partial_grads[:, :k + 1, m, :] = torch.stack(grads_tuple)
        return partial_grads.detach().numpy()

    ###########################################################################
    # Utility #################################################################
    ###########################################################################

    def _return_objective(self, obj_value: float) -> float:
        logging.debug(f"Module {self.__str__()} with objective value {obj_value}")
        self._obj_current = self.weight * obj_value
        logging.debug(f"Module {self.__str__()} with objective value {self._obj_current}")
        return self._obj_current

    def _return_gradient(self, gradient: np.ndarray) -> np.ndarray:
        logging.debug(f"Module {self.__str__()} with gradient {gradient}")
        self._grad_current = self.weight * gradient
        return self._grad_current

    def logging(self):
        self._log_obj.append(self._obj_current)
        self._log_grad.append(np.linalg.norm(self._grad_current))

    def clean_up(self):
        self._log_obj = deque()
        self._log_grad = deque()

    @property
    def logs(self) -> Tuple[List[float], List[float]]:
        return list(self._log_obj), list(self._log_grad)
