from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Dict, List, Union

import torch

from mantrap.constants import *
from mantrap.environment.environment import GraphBasedEnvironment
from mantrap.utility.shaping import check_ego_trajectory


class IterativeEnvironment(GraphBasedEnvironment, ABC):

    ###########################################################################
    # Simulation Graph ########################################################
    ###########################################################################
    @abstractmethod
    def build_graph(self, ego_state: torch.Tensor = None, k: int = 0, **graph_kwargs) -> Dict[str, torch.Tensor]:
        raise NotImplementedError

    ###########################################################################
    # Simulation Graph over time-horizon ######################################
    ###########################################################################
    def _build_connected_graph(self, ego_trajectory: Union[List, torch.Tensor], **kwargs) -> Dict[str, torch.Tensor]:
        """Build a connected graph based on the ego's trajectory.

        The graph should span over the time-horizon of the length of the ego's trajectory and contain the state
        (position, velocity) and "controls" of every ghost in the scene as well as the ego's states itself. When
        possible the graph should be differentiable, such that finding some gradient between the outputted ado
        states and the inputted ego trajectory is determinable.

        Iterative environment build up a prediction over a time horizon > 1 stepwise, i.e. predicting the first
        step t0 -> t1, then plugging in the results to the next prediction t1 -> t2, etc, until tN. Also they are
        usually (at least not the ones regarded within the scope of this project) not conditioned on the presence
        of some ego agent, so that instead of a trajectory simply a list of None can be passed, in order to build
        a graph without an ego in the scene.

        :param ego_trajectory: ego's trajectory (t_horizon, 5) or list of None if no ego in the scene.
        :return: dictionary over every state of every agent in the scene for t in [0, t_horizon].
        """
        if not all([x is None for x in ego_trajectory]):
            assert check_ego_trajectory(ego_trajectory, pos_and_vel_only=True)

        # Since the ghosts are used for building the graph, and in during this process updated over the time horizon,
        # they are (deep-)copied in order to be able to re-construct them afterwards.
        ado_ghosts_copy = deepcopy(self._ado_ghosts)

        # Build first graph for the next state, in case no forces are applied on the ego.
        graphs = self.build_graph(ego_state=ego_trajectory[0], k=0, **kwargs)

        # Build the graph iteratively for the whole prediction horizon.
        # Social forces assumes all agents to be controlled by some force vector, i.e. to be double integrators.
        t_horizon = len(ego_trajectory)  # works for list and torch.Tensor (= .shape[0])
        for t in range(1, t_horizon):
            for m_ghost, ghost in enumerate(self._ado_ghosts):
                self._ado_ghosts[m_ghost].agent.update(graphs[f"{ghost.id}_{t - 1}_{GK_CONTROL}"], dt=self.dt)

            # The ego movement is, of cause, unknown, since we try to find it here. Therefore motion primitives are
            # used for the ego motion, as guesses for the final trajectory i.e. starting points for optimization.
            graph_k = self.build_graph(ego_trajectory[t], k=t, **kwargs)
            graphs.update(graph_k)

        # Update graph for a last time using the forces determined in the previous step.
        for m_ghost in range(self.num_ghosts):
            ghost_id = self.ghosts[m_ghost].id
            self._ado_ghosts[m_ghost].agent.update(graphs[f"{ghost_id}_{t_horizon - 1}_{GK_CONTROL}"], dt=self.dt)
            graphs[f"{ghost_id}_{t_horizon}_{GK_POSITION}"] = self.ghosts[m_ghost].agent.position
            graphs[f"{ghost_id}_{t_horizon}_{GK_VELOCITY}"] = self.ghosts[m_ghost].agent.velocity

        # Reset ado ghosts to previous states.
        self._ado_ghosts = ado_ghosts_copy
        return graphs

    def _build_connected_graph_wo_ego(self, t_horizon: int, **kwargs) -> Dict[str, torch.Tensor]:
        """Build a connected graph over `t_horizon` time-steps for ados only.

        The graph should span over the time-horizon of the inputted number of time-steps and contain the state
        (position, velocity) and "controls" of every ghost in the scene as well as the ego's states itself. When
        possible the graph should be differentiable, such that finding some gradient between the outputted ado
        states and the inputted ego trajectory is determinable.

        Since iterative  environments (at least not the ones regarded within the scope of this project) are not
        conditioned on the presence of some ego agent, so that instead of a trajectory simply a list of None
        can be passed, in order to build a graph without an ego in the scene.

        :param t_horizon: number of prediction time-steps.
        :return: dictionary over every state of every ado in the scene for t in [0, t_horizon].
        """
        return self._build_connected_graph(t_horizon=t_horizon, ego_trajectory=[None] * t_horizon, **kwargs)