from typing import Dict

import torch

from mantrap.environment import SocialForcesEnvironment
from mantrap.utility.io import dict_value_or_default


class PotentialFieldEnvironment(SocialForcesEnvironment):
    """Simplified version of social forces environment class.

    The simplified model assumes static agents (ados) in the scene, having zero velocity (if not stated otherwise)
    and no incentive to move since goal and position are the same. Hereby, the graph model is cut to the pure
    interaction between ego and ado, no inter-ado interaction and goal pulling force. Since the ados would not move
    at all without an ego agent in the scene, the interaction loss simply comes down the the distance of every position
    of the ados in time to their initial (static) position.
    """

    ###########################################################################
    # Prediction ##############################################################
    ###########################################################################
    def predict_w_controls(self, controls: torch.Tensor, return_more: bool = False, **graph_kwargs) -> torch.Tensor:
        return super(PotentialFieldEnvironment, self).predict_w_controls(controls, return_more, **graph_kwargs)

    def predict_w_trajectory(self, trajectory: torch.Tensor, return_more: bool = False, **graph_kwargs) -> torch.Tensor:
        return super(PotentialFieldEnvironment, self).predict_w_trajectory(trajectory, return_more, **graph_kwargs)

    def predict_wo_ego(self, t_horizon: int, return_more: bool = False, **graph_kwargs) -> torch.Tensor:
        return super(PotentialFieldEnvironment, self).predict_wo_ego(t_horizon, return_more, **graph_kwargs)

    ###########################################################################
    # Scene ###################################################################
    ###########################################################################
    def add_ado(self, **ado_kwargs):
        # enforce static agent - no incentive to move (overwriting goal input !)
        ado_kwargs["goal"] = ado_kwargs["position"]
        ado_kwargs["velocity"] = dict_value_or_default(ado_kwargs, key="velocity", default=torch.zeros(2))
        # enforce uni-modality of agent (environment)
        ado_kwargs["num_modes"] = dict_value_or_default(ado_kwargs, key="num_modes", default=1)

        super(PotentialFieldEnvironment, self).add_ado(**ado_kwargs)

    def build_graph(self, ego_state: torch.Tensor = None, **graph_kwargs) -> Dict[str, torch.Tensor]:
        # Graph initialization - Add ados and ego to graph (position, velocity and goals).
        graph = self.write_state_to_graph(ego_state, **graph_kwargs)
        k = dict_value_or_default(graph_kwargs, key="k", default=0)
        for ghost in self.ghosts:
            graph[f"{ghost.id}_{k}_goal"] = ghost.params["goal"]

        # Make graph with resulting force as an output.
        for ghost in self.ghosts:
            gpos, gvel = graph[f"{ghost.id}_{k}_position"], graph[f"{ghost.id}_{k}_velocity"]
            graph[f"{ghost.id}_{k}_control"] = torch.zeros(2)

            if ego_state is not None:
                ego_pos = graph[f"ego_{k}_position"]
                delta = gpos - ego_pos
                potential_force = torch.sign(delta) * torch.exp(- torch.abs(delta))
                graph[f"{ghost.id}_{k}_control"] = torch.add(graph[f"{ghost.id}_{k}_control"], potential_force)

            # Summarize (standard) graph elements.
            graph[f"{ghost.id}_{k}_output"] = torch.norm(graph[f"{ghost.id}_{k}_control"])

        return graph

    ###########################################################################
    # Simulation parameters ###################################################
    ###########################################################################
    @property
    def environment_name(self) -> str:
        return "potential_field"
