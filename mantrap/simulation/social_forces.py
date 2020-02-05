from collections import namedtuple
import copy
from typing import Any, Dict, List, Tuple, Union

import torch

from mantrap.agents.agent import Agent
from mantrap.agents import DoubleIntegratorDTAgent
from mantrap.constants import (
    sim_x_axis_default,
    sim_y_axis_default,
    sim_dt_default,
    sim_social_forces_default_params,
    sim_social_forces_min_goal_distance,
    sim_social_forces_max_interaction_distance,
)
from mantrap.utility.shaping import check_ego_trajectory, check_trajectories, check_policies, check_weights
from mantrap.utility.stats import Distribution, DirecDelta
from mantrap.utility.utility import build_trajectory_from_positions
from mantrap.simulation.simulation import GraphBasedSimulation


class SocialForcesSimulation(GraphBasedSimulation):

    # Re-Definition of the Ghost object introducing further social-forces specific parameters such as a goal or
    # agent-dependent simulation parameters v0, sigma and tau.
    Ghost = namedtuple("Ghost", "agent goal v0 sigma tau weight gid")

    def __init__(
        self,
        ego_type: Agent.__class__ = None,
        ego_kwargs: Dict[str, Any] = None,
        x_axis: Tuple[float, float] = sim_x_axis_default,
        y_axis: Tuple[float, float] = sim_y_axis_default,
        dt: float = sim_dt_default,
    ):
        super(SocialForcesSimulation, self).__init__(ego_type, ego_kwargs, x_axis=x_axis, y_axis=y_axis, dt=dt)
        self._ado_ghosts = []

    def predict(
        self, t_horizon: int, ego_trajectory: torch.Tensor = None, verbose: bool = False,
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor, torch.Tensor]]:
        """For predicting the ado states in future time-steps up to t* = t_horizon given some ego trajectory
        subsequently build a graph representation of the current scene in order to predict all states in the next scene,
        using the determined forces as control input for the ado state updates. Then, after iterating through all
        time-steps up to t* = t_horizon, build the ado trajectories by using their state histories. In order to account
        for different ado modes, simulate them as "ghost" agents independently.

        :param t_horizon: prediction horizon (number of time-steps of length dt).
        :param ego_trajectory: ego agent trajectory the prediction is conditioned on, (t_horizon, [2, 6]).
        :param verbose: return the actual system inputs (at every time -> trajectory) and probabilities of each mode.
        :return: predicted trajectories for ados in the scene (either one or multiple for each ado).
        """
        if ego_trajectory is not None:
            if ego_trajectory.shape[1] == 2:
                ego_trajectory = build_trajectory_from_positions(ego_trajectory, dt=self.dt, t_start=self.sim_time)
            assert check_ego_trajectory(ego_trajectory, t_horizon=t_horizon), "ego trajectory invalid"

        forces = torch.zeros((self.num_ados, self.num_ado_modes, t_horizon, 2))
        # The social forces model predicts from one time-step to another, therefore the ados are actually updated in
        # each time step, in order to predict the next time-step. To not change the initial state, hence, the ados
        # vector is copied.
        ado_ghosts_copy = copy.deepcopy(self._ado_ghosts)
        for t in range(t_horizon):
            # Build graph based on simulation ados. Build it once and update it every time is surprisingly difficult
            # since the gradients/computations are not updated when one of the leafs is updated, resulting in the
            # same output. However the computational effort of building the graph is negligible (about 1 ms for
            # 2 agents on Mac Pro 2018).
            ego_state = ego_trajectory[t, :] if ego_trajectory is not None else None
            graph_at_t = self.build_graph(ego_state=ego_state)

            # Evaluate graph.
            for i in range(self.num_ado_ghosts):
                i_ado, i_mode = self.ghost_to_ado_index(i)
                forces[i_ado, i_mode, t, :] = graph_at_t[f"{self._ado_ghosts[i].gid}_force"].detach()
                self._ado_ghosts[i].agent.update(forces[i_ado, i_mode, t, :], dt=self.dt)  # assuming m = 1 kg

        # Collect histories of simulated ados (last t_horizon steps are equal to future trajectories).
        # Additionally, extract probability distribution over modes, which basically is the initial distribution.
        trajectories = torch.zeros((self.num_ados, self.num_ado_modes, t_horizon, 6))
        weights = torch.zeros((self.num_ados, self.num_ado_modes))
        for i, ghost in enumerate(self._ado_ghosts):
            i_ado, i_mode = self.ghost_to_ado_index(i)
            trajectories[i_ado, i_mode, :, :] = ghost.agent.history[-t_horizon:, :]
            weights[i_ado, i_mode] = ghost.weight

        # Reset the list of ado ghosts with the list before the prediction loop.
        self._ado_ghosts = ado_ghosts_copy

        assert check_policies(forces, num_ados=self.num_ados, num_modes=self.num_ado_modes, t_horizon=t_horizon)
        assert check_weights(weights, num_ados=self.num_ados, num_modes=self.num_ado_modes)
        assert check_trajectories(trajectories, self.num_ados, t_horizon=t_horizon, modes=self.num_ado_modes)
        return trajectories if not verbose else (trajectories, forces, weights)

    def step(self, ego_policy: torch.Tensor = None) -> Tuple[torch.Tensor, Union[torch.Tensor, None]]:
        ado_states, ego_next_state = super(SocialForcesSimulation, self).step(ego_policy=ego_policy)
        for i in range(len(self._ado_ghosts)):
            i_ado, i_mode = self.ghost_to_ado_index(i)
            self._ado_ghosts[i].agent.reset(ado_states[i_ado, i_mode, 0, :], history=None)  # new state is appended
        return ado_states, ego_next_state

    def add_ado(
        self,
        goal: torch.Tensor,
        num_modes: int,
        v0s: List[Distribution] = None,
        sigmas: List[Distribution] = None,
        weights: List[float] = None,
        **ado_kwargs,
    ):
        """Add ado to the simulation. To create multi-modality and stochastic effects several sets of simulation
        parameters can be assigned to the ado, each representing one of it's modes, and weights by the given
        weight vector, representing the probability of each mode occurring. The ado_kwargs are basis ado parameters
        such as position, velocity, id, etc.
        """
        # Social Forces requires to introduce a goal point, the agent is heading to. Find it in the parameters
        # and add it to the ado parameters dictionary.
        assert goal.size() == torch.Size([2]), "goal position must be two-dimensional (x, y)"

        # In order to introduce multi-modality and stochastic effects the underlying parameters of the social forces
        # simulation are sampled from distributions, each for one mode. If not stated the default parameters are
        # used as hot-encoded (i.e. direc delta) distribution.
        v0s = v0s if v0s is not None else [DirecDelta(sim_social_forces_default_params["v0"])] * num_modes
        sigmas = sigmas if sigmas is not None else [DirecDelta(sim_social_forces_default_params["sigma"])] * num_modes
        weights = weights if weights is not None else (torch.ones(num_modes) / num_modes).tolist()
        assert len(v0s) == len(sigmas) == len(weights), "simulation parameters and number of modes do not match"

        # Create ado and ado ghosts.
        super(SocialForcesSimulation, self).add_ado(type=DoubleIntegratorDTAgent, **ado_kwargs)
        for i in range(num_modes):
            assert v0s[i].__class__.__bases__[0] == Distribution
            assert sigmas[i].__class__.__bases__[0] == Distribution
            ado = copy.deepcopy(self._ados[-1])
            v0 = float(v0s[i].sample())
            sigma = float(sigmas[i].sample())
            tau = sim_social_forces_default_params["tau"]
            gid = ado.id + "_" + str(i)
            self._ado_ghosts.append(self.Ghost(ado, goal=goal, v0=v0, sigma=sigma, tau=tau, weight=weights[i], gid=gid))

    def ghost_to_ado_index(self, ghost_index: int) -> Tuple[int, int]:
        """Ghost of the same "parent" agent are appended to the internal storage of ghosts together, therefore it can
        be backtracked which ghost index belongs to which agent and mode by simple integer division (assuming the same
        number of modes of every ado).
        :return ado index, mode index
        """
        return int(ghost_index / self.num_ado_modes), int(ghost_index % self.num_ado_modes)

    ###########################################################################
    # Simulation Graph ########################################################
    ###########################################################################

    def build_graph(self, ego_state: torch.Tensor, is_intermediate: bool = False, **kwargs) -> Dict[str, torch.Tensor]:

        # Repulsive force introduced by every other agent (depending on relative position and (!) velocity).
        def _repulsive_force(
            alpha_position: torch.Tensor,
            beta_position: torch.Tensor,
            alpha_velocity: torch.Tensor,
            beta_velocity: torch.Tensor,
            v_0: float,
            sigma: float,
        ) -> torch.Tensor:

            # Relative properties and their norms.
            relative_distance = torch.sub(alpha_position, beta_position)
            relative_distance.retain_grad()  # get gradient without being leaf node
            relative_velocity = torch.sub(alpha_velocity, beta_velocity)

            norm_relative_distance = torch.norm(relative_distance)
            norm_relative_velocity = torch.norm(relative_velocity)
            norm_diff_position = torch.sub(relative_distance, relative_velocity * self.dt).norm()

            # Alpha-Beta potential field.
            b1 = torch.add(norm_relative_distance, norm_diff_position)
            b2 = self.dt * norm_relative_velocity
            b = 0.5 * torch.sqrt(torch.sub(torch.pow(b1, 2), torch.pow(b2, 2)))
            v = v_0 * torch.exp(-b / sigma)

            # The repulsive force between agents is the negative gradient of the other (beta -> alpha)
            # potential field. Therefore subtract the gradient of V w.r.t. the relative distance.
            return torch.autograd.grad(v, relative_distance, create_graph=True)[0]

        # Graph initialization - Add ados and ego to graph (position, velocity and goals).
        graph = super(SocialForcesSimulation, self).build_graph(ego_state, is_intermediate, **kwargs)
        for ghost in self.ado_ghosts:
            graph[f"{ghost.gid}_goal"] = ghost.goal

        # Make graph with resulting force as an output.
        for ghost in self._ado_ghosts:
            gpos, gvel = graph[f"{ghost.gid}_position"], graph[f"{ghost.gid}_velocity"]

            # Destination force - Force pulling the ado to its assigned goal position.
            direction = torch.sub(graph[f"{ghost.gid}_goal"], graph[f"{ghost.gid}_position"])
            goal_distance = torch.norm(direction)
            if goal_distance.data < sim_social_forces_min_goal_distance:
                destination_force = torch.zeros(2)
            else:
                direction = torch.div(direction, goal_distance)
                speed = torch.norm(graph[f"{ghost.gid}_velocity"])
                destination_force = torch.sub(direction * speed, graph[f"{ghost.gid}_velocity"]) * 1 / ghost.tau
            graph[f"{ghost.gid}_force"] = destination_force

            # Interactive force - Repulsive potential field by every other agent.
            for other in self._ado_ghosts:
                if ghost.agent.id == other.agent.id:  # ghosts from the same parent agent dont repulse each other
                    continue
                distance = torch.sub(graph[f"{ghost.gid}_position"], graph[f"{other.gid}_position"]).data
                if torch.norm(distance) > sim_social_forces_max_interaction_distance:
                    continue
                else:
                    opos, ovel = graph[f"{other.gid}_position"], graph[f"{other.gid}_velocity"]
                    v_grad = _repulsive_force(gpos, opos, gvel, ovel, v_0=ghost.v0, sigma=ghost.sigma)
                v_grad = v_grad * other.weight  # weight force by probability of the mode
                graph[f"{ghost.gid}_force"] = torch.sub(graph[f"{ghost.gid}_force"], v_grad)

            # Interactive force w.r.t. ego - Repulsive potential field.
            if ego_state is not None:
                ego_pos, ego_vel = graph["ego_position"], graph["ego_velocity"]
                v_grad = _repulsive_force(gpos, ego_pos, gvel, ego_vel, v_0=ghost.v0, sigma=ghost.sigma)
                graph[f"{ghost.gid}_force"] = torch.sub(graph[f"{ghost.gid}_force"], v_grad)

            # Summarize (standard) graph elements.
            graph[f"{ghost.gid}_force_norm"] = torch.norm(graph[f"{ghost.gid}_force"])

        # Check healthiness of graph by looking for specific keys in the graph that are required.
        assert all([f"{ghost.gid}_force_norm" for ghost in self._ado_ghosts])
        return graph

    ###########################################################################
    # Ado properties ##########################################################
    ###########################################################################

    @property
    def ado_ghosts_agents(self) -> List[Agent]:
        return [ghost.agent for ghost in self._ado_ghosts]

    @property
    def ado_ghosts(self) -> List[Ghost]:
        return self._ado_ghosts

    @property
    def num_ado_ghosts(self) -> int:
        return len(self._ado_ghosts)

    @property
    def num_ado_modes(self) -> int:
        """The number of modes results from the ratio between the number of ado ghosts (pseudo ados, i.e. different
        versions of an ado differentiating by a their parameters) and the number of ados. Thereby we assume that
        all ados have the same number of modes (which is usually the case by construction). """
        if self.num_ados == 0:
            num_ado_modes = 0
        else:
            assert len(self._ado_ghosts) % self.num_ados == 0
            num_ado_modes = int(len(self._ado_ghosts) / self.num_ados)
        return num_ado_modes
