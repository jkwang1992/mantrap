from copy import deepcopy
from typing import Dict, List, Union

import torch

from mantrap.agents import DoubleIntegratorDTAgent
from mantrap.constants import *
from mantrap.environment.environment import GraphBasedEnvironment
from mantrap.utility.maths import Distribution, Gaussian


class SocialForcesEnvironment(GraphBasedEnvironment):
    """Social Forces Simulation.
    Pedestrian Dynamics based on to "Social Force Model for Pedestrian Dynamics" (D. Helbling, P. Molnar). The idea
    of Social Forces is to determine interaction forces by taking into account the following entities:

    *Goal force*:
    Each ado has a specific goal state/position in mind, to which it moves to. The goal pulling force
    is modelled as correction term between the direction vector of the current velocity and the goal direction
    (vector between current position and goal).

    .. math:: F_{goal} = 1 / tau_{a} (v_a^0 e_a - v_a)

    *Interaction force*:
    For modelling interaction between multiple agents such as avoiding collisions each agent
    has an with increasing distance exponentially decaying repulsion field. Together with the scalar product of the
    velocity of each agent pair (in order to not alter close but non interfering agents, e.g. moving parallel to
    each other) the interaction term is constructed.

    .. math:: V_{aB} (x) = V0_a exp(−x / \sigma_a)
    .. math:: F_{interaction} = - grad_{r_{ab}} V_{aB}(||r_{ab}||)

    To create multi-modality and stochastic effects several sets of environment parameters can be assigned to the ado,
    each representing one of it's modes.
    """

    ###########################################################################
    # Scene ###################################################################
    ###########################################################################
    def add_ado(
        self,
        num_modes: int = 1,
        goal: torch.Tensor = torch.zeros(2),
        v0s: Union[List[Distribution], List[float]] = None,
        sigmas: Union[List[Distribution], List[float]] = None,
        weights: List[float] = None,
        **ado_kwargs,
    ):
        # Social Forces requires to introduce a goal point, the agent is heading to. Find it in the parameters
        # and add it to the ado parameters dictionary.
        assert goal.size() == torch.Size([2])
        goal = goal.detach().float()

        # In order to introduce multi-modality and stochastic effects the underlying parameters of the social forces
        # environment are sampled from distributions, each for one mode. If not stated the default parameters are
        # used as Gaussian distribution around the default value.
        v0s_default = Gaussian(ENV_SOCIAL_FORCES_DEFAULTS[PARAMS_V0], ENV_SOCIAL_FORCES_DEFAULTS[PARAMS_V0] / 2)
        v0s = v0s if v0s is not None else [v0s_default] * num_modes
        sigma_default = Gaussian(ENV_SOCIAL_FORCES_DEFAULTS[PARAMS_SIGMA], ENV_SOCIAL_FORCES_DEFAULTS[PARAMS_SIGMA] / 2)
        sigmas = sigmas if sigmas is not None else [sigma_default] * num_modes
        assert len(v0s) == len(sigmas)

        # For each mode sample new parameters from the previously defined distribution. If no distribution is defined,
        # but a list of floating point values is passed directly, just use them.
        args_list = []
        for i in range(num_modes):
            if type(v0s[i]) == float:
                assert type(sigmas[i]) == float
                v0 = v0s[i]
                sigma = sigmas[i]
            elif v0s[i].__class__.__bases__[0] == Distribution:
                assert sigmas[i].__class__.__bases__[0] == Distribution
                v0 = abs(float(v0s[i].sample()))
                sigma = abs(float(sigmas[i].sample()))
            else:
                raise ValueError
            tau = ENV_SOCIAL_FORCES_DEFAULTS[PARAMS_TAU]
            args_list.append({PARAMS_V0: v0, PARAMS_SIGMA: sigma, PARAMS_TAU: tau, PARAMS_GOAL: goal})

        # Finally add ado ghosts to environment.
        super(SocialForcesEnvironment, self).add_ado(
            ado_type=DoubleIntegratorDTAgent,
            num_modes=num_modes,
            weights=weights,
            arg_list=args_list,
            **ado_kwargs
        )

    ###########################################################################
    # Simulation Graph ########################################################
    ###########################################################################
    def build_graph(self, ego_state: torch.Tensor = None, k: int = 0, **graph_kwargs) -> Dict[str, torch.Tensor]:

        # Repulsive force introduced by every other agent (depending on relative position and (!) velocity).
        def _repulsive_force(
            alpha_position: torch.Tensor,
            beta_position: torch.Tensor,
            alpha_velocity: torch.Tensor,
            beta_velocity: torch.Tensor,
            p_v_0: float,
            p_sigma: float,
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
            v = p_v_0 * torch.exp(-b / p_sigma)

            # The repulsive force between agents is the negative gradient of the other (beta -> alpha)
            # potential field. Therefore subtract the gradient of V w.r.t. the relative distance.
            force = torch.autograd.grad(v, relative_distance, create_graph=True)[0]
            if torch.any(torch.isnan(force)):  # TODO: why is nan rarely occurring here and how to deal with that ?
                return torch.zeros(2)
            else:
                return force

        # Graph initialization - Add ados and ego to graph (position, velocity and goals).
        graph = self.write_state_to_graph(ego_state, ado_grad=True, k=k, **graph_kwargs)
        for ghost in self.ghosts:
            graph[f"{ghost.id}_{k}_{GK_GOAL}"] = ghost.params[PARAMS_GOAL]

        # Make graph with resulting force as an output.
        for ghost in self._ado_ghosts:
            tau, v0, sigma = ghost.params[PARAMS_TAU], ghost.params[PARAMS_TAU], ghost.params[PARAMS_SIGMA]
            gpos = graph[f"{ghost.id}_{k}_{GK_POSITION}"]
            gvel = graph[f"{ghost.id}_{k}_{GK_VELOCITY}"]

            # Destination force - Force pulling the ado to its assigned goal position.
            direction = torch.sub(graph[f"{ghost.id}_{k}_{GK_GOAL}"], graph[f"{ghost.id}_{k}_{GK_POSITION}"])
            goal_distance = torch.norm(direction)
            if goal_distance.data < ENV_SOCIAL_FORCES_MIN_GOAL_DISTANCE:
                destination_force = torch.zeros(2)
            else:
                direction = torch.div(direction, goal_distance)
                speed = torch.norm(graph[f"{ghost.id}_{k}_{GK_VELOCITY}"])
                destination_force = torch.sub(direction * speed, graph[f"{ghost.id}_{k}_{GK_VELOCITY}"]) * 1 / tau
            graph[f"{ghost.id}_{k}_{GK_CONTROL}"] = destination_force

            # Interactive force - Repulsive potential field by every other agent.
            for other in self.ghosts:
                if ghost.agent.id == other.agent.id:  # ghosts from the same parent agent dont repulse each other
                    continue
                distance = torch.sub(graph[f"{ghost.id}_{k}_{GK_POSITION}"], graph[f"{other.id}_{k}_{GK_POSITION}"])
                if torch.norm(distance) > ENV_SOCIAL_FORCES_MAX_INTERACTION_DISTANCE:
                    continue
                else:
                    opos = graph[f"{other.id}_{k}_{GK_POSITION}"]
                    ovel = graph[f"{other.id}_{k}_{GK_VELOCITY}"]
                    v_grad = _repulsive_force(gpos, opos, gvel, ovel, p_v_0=v0, p_sigma=sigma)
                v_grad = v_grad * other.weight  # weight force by probability of the modes
                graph[f"{ghost.id}_{k}_{GK_CONTROL}"] = torch.sub(graph[f"{ghost.id}_{k}_{GK_CONTROL}"], v_grad)

            # Interactive force w.r.t. ego - Repulsive potential field.
            if ego_state is not None:
                ego_pos = graph[f"ego_{k}_{GK_POSITION}"]
                ego_vel = graph[f"ego_{k}_{GK_VELOCITY}"]
                v_grad = _repulsive_force(gpos, ego_pos, gvel, ego_vel, p_v_0=v0, p_sigma=sigma)
                graph[f"{ghost.id}_{k}_{GK_CONTROL}"] = torch.sub(graph[f"{ghost.id}_{k}_{GK_CONTROL}"], v_grad)

            # Summarize (standard) graph elements.
            graph[f"{ghost.id}_{k}_{GK_OUTPUT}"] = torch.norm(graph[f"{ghost.id}_{k}_{GK_CONTROL}"])

        # Check healthiness of graph by looking for specific keys in the graph that are required.
        assert all([f"{ghost.id}_{k}_{GK_OUTPUT}" for ghost in self._ado_ghosts])
        return graph

    ###########################################################################
    # Simulation Graph over time-horizon ######################################
    ###########################################################################
    def _build_connected_graph(
        self,
        t_horizon: int,
        ego_trajectory: Union[List[None], torch.Tensor],
        **kwargs
    ) -> Dict[str, torch.Tensor]:
        # Since the ghosts are used for building the graph, and in during this process updated over the time horizon,
        # they are (deep-)copied in order to be able to re-construct them afterwards.
        ado_ghosts_copy = deepcopy(self._ado_ghosts)

        # Build first graph for the next state, in case no forces are applied on the ego.
        graphs = self.build_graph(ego_state=ego_trajectory[0], k=0, **kwargs)

        # Build the graph iteratively for the whole prediction horizon.
        # Social forces assumes all agents to be controlled by some force vector, i.e. to be double integrators.
        assert all([ghost.agent.__class__ == DoubleIntegratorDTAgent for ghost in self._ado_ghosts])
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

    def build_connected_graph_wo_ego(self, t_horizon: int, **kwargs) -> Dict[str, torch.Tensor]:
        return self._build_connected_graph(t_horizon=t_horizon, ego_trajectory=[None] * t_horizon, **kwargs)

    ###########################################################################
    # Operators ###############################################################
    ###########################################################################
    def _copy_ados(self, copy: 'GraphBasedEnvironment') -> 'GraphBasedEnvironment':
        for i in range(self.num_ados):
            ghosts_ado = self.ghosts_by_ado_index(ado_index=i)
            ado_id, _ = self.split_ghost_id(ghost_id=ghosts_ado[0].id)
            copy.add_ado(
                position=ghosts_ado[0].agent.position,  # same over all ghosts of same ado
                velocity=ghosts_ado[0].agent.velocity,  # same over all ghosts of same ado
                history=ghosts_ado[0].agent.history,  # same over all ghosts of same ado
                weights=[ghost.weight for ghost in ghosts_ado],
                num_modes=self.num_modes,
                identifier=self.split_ghost_id(ghost_id=ghosts_ado[0].id)[0],
                goal=ghosts_ado[0].params[PARAMS_GOAL],
                v0s=[ghost.params[PARAMS_V0] for ghost in ghosts_ado],
                sigmas=[ghost.params[PARAMS_SIGMA] for ghost in ghosts_ado],
            )
        return copy

    ###########################################################################
    # Simulation parameters ###################################################
    ###########################################################################
    @property
    def environment_name(self) -> str:
        return "social_forces"