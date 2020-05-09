import typing

import torch

import mantrap.utility.shaping

from .base import PureObjectiveModule


class GoalModule(PureObjectiveModule):
    """Objective based on goal distance of every point of planned robot trajectory.

    Next to avoiding interaction with other agents the robot should reach the goal state in a finite amount of
    time. Therefore the distance of every trajectory point to the goal state is taken to account, which is
    minimized the faster the robot gets to the goal.

    .. math:: objective = \\sum_{T} || pos_t - goal ||_2

    However, it is more important for the last rather than the first trajectory points to be close to the goal.
    Using some strictly-increasing distribution to weight the importance of the distance at every point in time
    did not lead to the expect result, while complicating the optimization. When we want to trade-off the
    goal cost with other cost, simply adapting its weight is sufficient as well.

    Additionally a cost for the velocity at the goal state can be included in this objective, a cost for non-zero
    velocity to be exact. This cost is weighted continuously based on the distance to the goal, i.e. the closer
    the a large speed (= velocity L2 norm) occurs, the higher its cost.

    .. math:: objective = \\sum_{T} w_t(d_{goal}(t)) || v_t ||_2

    :param goal: goal state/position for robot agent (2).
    :param optimize_speed: include cost for zero velocity at goal state.
    """

    def __init__(self, goal: torch.Tensor, optimize_speed: bool = False, **module_kwargs):
        super(GoalModule, self).__init__(**module_kwargs)

        assert mantrap.utility.shaping.check_goal(goal)
        self._goal = goal
        self._include_velocity = optimize_speed

    def _compute_objective(self, ego_trajectory: torch.Tensor, ado_ids: typing.List[str] = None
                           ) -> typing.Union[torch.Tensor, None]:
        """Determine objective value core method.

        To compute the goal-based objective simply take the L2 norm between all positions on the ego trajectory
        and the goal. To encounter the fact, that it is more important for the last position (last = position at
        the end of the planning horizon) to be close to the goal position than the first position, multiply with
        a strictly increasing importance distribution, cubic in this case.

        When the goal-velocity is included here, compute the speed as L2 norm per trajectory state. Then weight
        the speeds at every time by its distance to the goal, as explained in the description of this module.

        :param ego_trajectory: planned ego trajectory (t_horizon, 5).
        :param ado_ids: ghost ids which should be taken into account for computation.
        """
        goal_distances = torch.norm(ego_trajectory[:, 0:2] - self._goal, dim=1)
        cost = torch.mean(goal_distances)

        if self._include_velocity:
            speeds = torch.norm(ego_trajectory[:, 2:4], dim=1)
            cost += speeds.dot(torch.exp(- goal_distances * 0.5))

        return cost

    def _gradient_condition(self) -> bool:
        """Condition for back-propagating through the objective/constraint in order to obtain the
        objective's gradient vector/jacobian (numerically). If returns True and the ego_trajectory
        itself requires a gradient, the objective/constraint value, stored from the last computation
        (`_current_`-variables) has to require a gradient as well.

        Since the objective value computation depends on the ego_trajectory (and the ego goal) only, this
        should always hold.
        """
        return True

    ###########################################################################
    # Objective Properties ####################################################
    ###########################################################################
    @property
    def name(self) -> str:
        return "goal"