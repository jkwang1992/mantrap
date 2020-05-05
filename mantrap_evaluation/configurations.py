"""
Environment:
X environment types
X initial conditions
- ego agent type
- simulation time-step

Solver
X solver types
X environment types
X evaluation environment types
X planning horizon: greed (T=1), medium (T=1s), long (T=2s)
- objectives: (goal, interaction), goal only, interaction only
- objectives weight distribution (for non-single permutations)
- constraints: (max_speed, min_distance), max_speed only
X filter: no_filter, uni-modal, attention radius
- IPOPT configuration: automatic Jacobian estimate, manual Jacobian estimate

Specific Comparisons
- control effort objective vs  max control constraint only
"""
import itertools

import mantrap

import mantrap_evaluation.datasets

configurations = list(itertools.product(*[
    mantrap.solver.SOLVERS_DICT.keys(),  # solver type
    mantrap_evaluation.datasets.SCENARIOS.keys(),  # scenario
    mantrap.environment.ENVIRONMENTS_DICT.keys(),  # environment type
    mantrap.agents.AGENTS_DICT.keys(),  # ego_type
    mantrap.filter.FILTER_DICT.keys(),  # filter types
    [1, 3, 5],  # planning horizon
    [None],  # evaluation environments,
    [mantrap.constants.ENV_DT_DEFAULT],  # time-steps,
    [True, False]  # multi-processing
]))

config_keys = [
    "solver", "scenario", "env_type", "ego_type", "filter", "t_planning", "eval_env", "dt", "multiprocessing"
]
