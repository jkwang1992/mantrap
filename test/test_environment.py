import numpy as np

from murseco.environment.environment import Environment
from murseco.obstacle.single_mode import SingleModeDTVObstacle
from murseco.robot.cardinal import CardinalDTRobot
from murseco.utility.arrayops import rand_invsymmpos
import murseco.utility.io
from murseco.utility.visualization import plot_env_samples


def test_environment_identifier():
    env = Environment((0, 10), (0, 10))
    for i in range(10):
        env.add_obstacle(SingleModeDTVObstacle(covariance=rand_invsymmpos(2, 2)))
    identifiers = [o.identifier for o in env.obstacles]
    assert len(np.unique(identifiers)) == 10


def test_environment_json():
    env_1 = Environment((-10, 10), (-10, 10))
    env_1.add_obstacle(SingleModeDTVObstacle(history=np.array([1.4, 4.2])))
    env_1.add_obstacle(SingleModeDTVObstacle(history=np.array([5.4, -2.94])))
    env_1.add_robot(CardinalDTRobot(np.array([1.31, 4.3]), 4, 1.0, np.ones((4, 1)) * 2))
    cache_path = murseco.utility.io.path_from_home_directory("test/cache/env_test.json")
    env_1.to_json(cache_path)
    env_2 = Environment.from_json(cache_path)
    assert env_1.summary() == env_2.summary()


def test_environment_visualization_samples():
    env = Environment((-10, 10), (-10, 10))
    env.add_obstacle(SingleModeDTVObstacle(mu=np.array([1, 0]), covariance=np.diag([1e-4, 0.2])))
    env.add_robot(CardinalDTRobot(np.array([1.31, 4.3]), thorizon=4, velocity=1.0, policy=np.ones((4, 1)) * 2))
    plot_env_samples(env, murseco.utility.io.path_from_home_directory("test/cache/env_samples.png"))
