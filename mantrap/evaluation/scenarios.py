import numpy as np

from mantrap.agents.agent import Agent
from mantrap.agents import IntegratorDTAgent
from mantrap.simulation.simulation import Simulation
from mantrap.simulation import SocialForcesSimulation
from mantrap.utility.datasets import load_eth


# def scenario_eth(
#     sim_type: Simulation.__class__ = SocialForcesSimulation.__class__,
#     ego_type: Agent.__class__ = IntegratorDTAgent.__class__,
# ):
#     trajectories_data = load_eth(return_id_dict=False)
#     sim = sim_type(ego_type=ego_type, ego_kwargs={"position": np.array([-5, 2.0]), "velocity": np.array([1, 0])},)
#
#     return sim, np.array([5, 0.1])



# def scenario_sf_ego_static_single_ado(
#     sim_type: Simulation.__class__ = SocialForcesSimulation.__class__,
#     ego_type: Agent.__class__ = IntegratorDTAgent.__class__,
# ):
#     sim = sim_type(ego_type=ego_type, ego_kwargs={"position": np.array([-5, 2.0]), "velocity": np.array([1, 0])},)
#     sim.add_ado(position=np.zeros(2), velocity=np.zeros(2), goal_position=np.zeros(2))
#     return sim, np.array([5, 0.1])
#
#
# def scenario_sf_ego_moving_single_ado(
#     sim_type: Simulation.__class__ = SocialForcesSimulation.__class__,
#     ego_type: Agent.__class__ = IntegratorDTAgent.__class__,
# ):
#     sim = sim_type(ego_type=ego_type, ego_kwargs={"position": np.array([-5, 0.1]), "velocity": np.array([1, 0])},)
#     sim.add_ado(position=np.zeros(2), velocity=np.array([0, 0.5]), goal_position=np.array([0, 5]))
#     return sim, np.array([5, 0.1])
#
#
# def scenario_sf_ego_moving_two_ados(
#     sim_type: Simulation.__class__ = SocialForcesSimulation.__class__,
#     ego_type: Agent.__class__ = IntegratorDTAgent.__class__,
# ):
#     sim = sim_type(ego_type=ego_type, ego_kwargs={"position": np.array([-5, 0.1]), "velocity": np.array([1, 0])},)
#     sim.add_ado(position=np.array([0, 1]), velocity=np.array([-1, -0.5]), goal_position=np.ones(2) * (-10))
#     sim.add_ado(position=np.array([1, -1]), velocity=np.array([-1, 0]), goal_position=np.ones(2) * (-10))
#     return sim, np.array([5, 0.1])
#
#
# def scenario_sf_ego_moving_many_ados(
#     sim_type: Simulation.__class__ = SocialForcesSimulation.__class__,
#     ego_type: Agent.__class__ = IntegratorDTAgent.__class__,
# ):
#     sim = sim_type(ego_type=ego_type, ego_kwargs={"position": np.array([-5, 0.1]), "velocity": np.array([1, 0])},)
#     sim.add_ado(position=np.array([7, -7]), velocity=np.array([-1, 1]), goal_position=np.array([-5, 5]))
#     sim.add_ado(position=np.array([3, 8]), velocity=np.array([-0.2, -0.5]), goal_position=np.array([2, -8]))
#     sim.add_ado(position=np.array([1, -1]), velocity=np.array([-1, -0.2]), goal_position=np.ones(2) * (-10))
#     sim.add_ado(position=np.array([5, -5]), velocity=np.array([2, 0.2]), goal_position=np.ones(2) * 10)
#     sim.add_ado(position=np.array([0, 1]), velocity=np.array([-1, 0]), goal_position=np.ones(2) * (-10))
#     return sim, np.array([5, 0.1])
#
#
# def scenario_sf_ego_moving_along_down(
#     sim_type: Simulation.__class__ = SocialForcesSimulation.__class__,
#     ego_type: Agent.__class__ = IntegratorDTAgent.__class__,
# ):
#     sim = sim_type(ego_type=ego_type, ego_kwargs={"position": np.array([-5, 1.0]), "velocity": np.array([1, 0])},)
#     sim.add_ado(position=np.array([-5, -1.0]), velocity=np.array([1, 0]), goal_position=np.array([5, -1.0]))
#     return sim, np.array([0, -5])
