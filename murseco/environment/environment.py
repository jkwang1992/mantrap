from typing import Any, Dict, List, Tuple, Union

from murseco.obstacle.abstract import DiscreteTimeObstacle
from murseco.obstacle.static import StaticObstacle
from murseco.utility.types import EnvActor
from murseco.utility.io import JSONSerializer


class Environment(JSONSerializer):
    def __init__(self, xaxis: Tuple[float, float], yaxis: Tuple[float, float], actors: List[EnvActor] = None):
        super(Environment, self).__init__("environment/environment/Environment")

        assert xaxis[0] < xaxis[1], "xaxis has to be in the format (x_min, x_max)"
        assert yaxis[0] < yaxis[1], "yaxis has to be in the format (y_min, y_max)"

        self.xaxis = tuple(xaxis)
        self.yaxis = tuple(yaxis)
        self.actors = [] if actors is None else actors

    def _add_actor(self, element: Any, category: str, tframe: str) -> str:
        """Add actor to list of actors and create its id from random.

        :argument element: actor object to add to list.
        :argument category: type of actor (obstacle, robot)
        :argument tframe: time frame description (ct, dt, none)
        :return id: obstacle assigned identifier string.
        """
        assert category in ("robot", "obstacle"), "agent type description must be one out of (robot, obstacle)"
        assert tframe in ("ct", "dt", "none"), "time frame description must be one out of (ct, dt, none)"
        actor = EnvActor(category=category, tframe=tframe, element=element)
        self.actors.append(actor)
        return actor.identifier

    def add_discrete_time_obstacle(self, obstacle: DiscreteTimeObstacle) -> str:
        return self._add_actor(obstacle, "obstacle", "dt")

    def add_continuous_time_obstacle(self, obstacle: Any) -> str:
        return self._add_actor(obstacle, "obstacle", "ct")

    def add_static_obstacle(self, obstacle: StaticObstacle) -> str:
        return self._add_actor(obstacle, "obstacle", "none")

    def add_robot(self, robot: Any) -> str:
        return self._add_actor(robot, "robot", "none")

    def forward(self):
        """Forward step all agents in the environment, i.e. tn = tn + 1 in discrete time."""
        for obstacle in self.obstacles_dt:
            obstacle.element.forward()

    @property
    def obstacles(self) -> List[EnvActor]:
        return [actor for actor in self.actors if actor.category == "obstacle"]

    @property
    def obstacles_dt(self) -> List[EnvActor]:
        return [obstacle for obstacle in self.obstacles if obstacle.tframe == "dt"]

    @property
    def obstacles_ct(self) -> List[EnvActor]:
        return [obstacle for obstacle in self.obstacles if obstacle.tframe == "ct"]

    @property
    def robot(self) -> Union[None, EnvActor]:
        robots = [actor for actor in self.actors if actor.category == "robot"]
        assert len(robots) < 2, "maximal one robot is allowed in the scene"
        return robots[0] if len(robots) == 1 else None

    def summary(self) -> Dict[str, Any]:
        summary = super(Environment, self).summary()
        summary.update({"xaxis": self.xaxis, "yaxis": self.yaxis, "actors": [a.summary() for a in self.actors]})
        return summary

    @classmethod
    def from_summary(cls, json_text: Dict[str, Any]):
        actors = [EnvActor.from_summary(actor_text) for actor_text in json_text["actors"]]
        return cls(json_text["xaxis"], json_text["yaxis"], actors)
