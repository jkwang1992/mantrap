from mantrap.solver.igrad import IGradSolver
from mantrap.solver.sgrad import SGradSolver
from mantrap.solver.baselines.orca import ORCASolver
from mantrap.solver.mc_tree_search import MonteCarloTreeSearch

# SOLVER = [IGradSolver, SGradSolver, ORCASolver, MonteCarloTreeSearch]
SOLVER = [SGradSolver, ORCASolver, MonteCarloTreeSearch]
