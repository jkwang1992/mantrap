from typing import Any, Dict, List, Tuple

import numpy as np

from murseco.environment import Environment
from murseco.problem.abstract import AbstractProblem


class D2TSProblem(AbstractProblem):
    """The DiscreteTimeDiscreteSpace (D2TS) Problem defines the optimization problem as following, for the time-step
    0 <= k <= N, the discrete space vector x_k, the system dynamics f(x_k, u_k) and the time and spatially dependent
    probability density function of the risk pdf(x_k, k):

    Cost:
        J(x(t)) = sum_{k=0}^{N-1} l(x_k, u_k) + l_f(x_N)
        l(x_k, u_k) = w_x * ||x_Goal - x_k||_2^2 + w_u * ||u||_2^2
        l_f(x_N) = 0 if ||x_G - x_N||^2 < eps, c_Goal otherwise

    Constraints C:
        x_{k+1} = f(x_k, u_k)
        x_0 = x_Start
        ||u_k||_2 < u_max
        sum_{k=0}^N pdf(x_k, k) < risk_{max}

    Optimization:
        min J(x(t)) subject to constraints C
    """

    def __init__(
        self,
        env: Environment,
        x_goal: np.ndarray,
        thorizon: int = 20,
        w_x: float = 1.0,
        w_u: float = 1.0,
        c_goal: float = 1000.0,
        risk_max: float = 0.1,
        u_max: float = 1.0,
        dt: float = 1.0,
        mproc: bool = True,
        grid_resolution: float = 0.01,
        **kwargs,
    ):
        kwargs.update({"name": "problem/d2ts/D2TSProblem"})
        super(D2TSProblem, self).__init__(
            env=env,
            x_goal=x_goal,
            thorizon=thorizon,
            w_x=w_x,
            w_u=w_u,
            c_goal=c_goal,
            risk_max=risk_max,
            u_max=u_max,
            dt=dt,
            mproc=mproc,
            **kwargs,
        )

        # Temporal and spatial discretization.
        assert env.xaxis == env.yaxis, "discretization assumes equal axes for simplification (and nicer graphs)"
        num_points_per_axis = int((env.xaxis[1] - env.xaxis[0]) / grid_resolution)
        self._tppdf, self._meshgrid = env.tppdf_grid(num_points=num_points_per_axis, mproc=mproc)

    @property
    def grid(self) -> Tuple[List[np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        return self._tppdf, self._meshgrid

    def summary(self) -> Dict[str, Any]:
        summary = super(D2TSProblem, self).summary()
        return summary

    @classmethod
    def from_summary(cls, json_text: Dict[str, Any]):
        summary = super(D2TSProblem, cls).from_summary(json_text)
        return cls(**summary)
