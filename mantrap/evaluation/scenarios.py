import numpy as np

from mantrap.agents import IntegratorDTAgent
from mantrap.simulation import SocialForcesSimulation


def sf_ego_static_single_ado():
    sim = SocialForcesSimulation(
        ego_type=IntegratorDTAgent, ego_kwargs={"position": np.array([-5, 0.1]), "velocity": np.array([1, 0])},
    )
    sim.add_ado(position=np.zeros(2), velocity=np.zeros(2), goal_position=np.zeros(2))
    return sim


def sf_ego_moving_single_ado():
    sim = SocialForcesSimulation(
        ego_type=IntegratorDTAgent, ego_kwargs={"position": np.array([-5, 0.1]), "velocity": np.array([1, 0])},
    )
    sim.add_ado(position=np.zeros(2), velocity=np.array([0, 0.5]), goal_position=np.array([0, 5]))
    return sim


def sf_ego_moving_two_ados():
    sim = SocialForcesSimulation(
        ego_type=IntegratorDTAgent, ego_kwargs={"position": np.array([-5, 0.1]), "velocity": np.array([1, 0])},
    )
    sim.add_ado(position=np.array([0, 1]), velocity=np.array([-1, 0]), goal_position=np.ones(2)*(-10))
    sim.add_ado(position=np.array([1, -1]), velocity=np.array([-1, 0]), goal_position=np.ones(2)*(-10))
    return sim


def sf_ego_moving_many_ados():
    sim = SocialForcesSimulation(
        ego_type=IntegratorDTAgent, ego_kwargs={"position": np.array([-5, 0.1]), "velocity": np.array([1, 0])},
    )
    sim.add_ado(position=np.array([7, -7]), velocity=np.array([-1, 1]), goal_position=np.array([-5, 5]))
    sim.add_ado(position=np.array([3, 8]), velocity=np.array([-0.2, -0.5]), goal_position=np.array([2, -8]))
    sim.add_ado(position=np.array([1, -1]), velocity=np.array([-1, 0]), goal_position=np.ones(2)*(-10))
    sim.add_ado(position=np.array([5, -5]), velocity=np.array([2, 0.2]), goal_position=np.ones(2) * 10)
    sim.add_ado(position=np.array([0, 1]), velocity=np.array([-1, 0]), goal_position=np.ones(2) * (-10))
    return sim
