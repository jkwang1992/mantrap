import pytest
import torch

from mantrap.agents import IntegratorDTAgent
from mantrap.simulation import PotentialFieldSimulation, SocialForcesSimulation
from mantrap.solver.objectives import GoalModule, InteractionAccelerationModule, InteractionPositionModule
from mantrap.solver.objectives.objective_module import ObjectiveModule
from mantrap.utility.primitives import straight_line_primitive


@pytest.mark.parametrize("module_class", [InteractionAccelerationModule, InteractionPositionModule])
class TestObjectiveInteraction:

    @staticmethod
    def test_objective_far_and_near(module_class: ObjectiveModule.__class__):
        sim = PotentialFieldSimulation(IntegratorDTAgent, {"position": torch.tensor([-5, 0.1])})
        sim.add_ado(position=torch.zeros(2))
        x2_near = straight_line_primitive(10, torch.tensor([-5, 0.1]), torch.tensor([5, 0.1]))
        x2_far = straight_line_primitive(10, torch.tensor([-5, 10.0]), torch.tensor([5, 10.0]))

        module = module_class(horizon=10, env=sim)
        assert module.objective(x2_near) > module.objective(x2_far)

    @staticmethod
    def test_multimodal_support(module_class: ObjectiveModule.__class__):
        sim = SocialForcesSimulation(IntegratorDTAgent, {"position": torch.tensor([-5, 0.1])})
        ado_pos, ado_vel, ado_goal = torch.zeros(2), torch.tensor([-1, 0]), torch.tensor([-5, 0])
        sim.add_ado(position=ado_pos, velocity=ado_vel, num_modes=2, weights=[0.1, 0.9], goal=ado_goal)
        x2 = straight_line_primitive(10, sim.ego.position, torch.tensor([5, 0.1]))

        module = module_class(horizon=10, env=sim)
        print(module.objective(x2))

    @staticmethod
    def test_output(module_class: ObjectiveModule.__class__):
        sim = PotentialFieldSimulation(IntegratorDTAgent, {"position": torch.tensor([-5, 0.1])})
        sim.add_ado(position=torch.zeros(2))
        x2 = straight_line_primitive(10, sim.ego.position, torch.tensor([5, 0.1]))

        module = module_class(horizon=10, env=sim)
        assert type(module.objective(x2)) == float
        assert module.gradient(x2).size == x2.numel()  # without setting `grad_wrt`, size should match x2


def test_objective_goal_distribution():
    goal = torch.tensor([4.1, 8.9])
    x2 = torch.rand((10, 2))

    module = GoalModule(goal=goal, horizon=10, weight=1.0)
    module.importance_distribution = torch.zeros(10)
    module.importance_distribution[3] = 1.0

    objective = module.objective(x2)
    assert objective == torch.norm(x2[3, :] - goal)