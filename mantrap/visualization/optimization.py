import matplotlib.animation
import matplotlib.pyplot as plt
import torch

import mantrap.constants
import mantrap.environment
import mantrap.utility.shaping

from .atomics import interactive_save_video
from .prediction import visualize_prediction


def visualize_optimization(
    ego_planned: torch.Tensor,
    ado_actual: torch.Tensor,
    ado_planned: torch.Tensor,
    ado_planned_wo: torch.Tensor,
    env: mantrap.environment.base.GraphBasedEnvironment,
    ego_goal: torch.Tensor = None,
    legend: bool = False,
    frame_interval: float = mantrap.constants.VISUALIZATION_FRAME_DELAY,
    restart_delay: float = mantrap.constants.VISUALIZATION_RESTART_DELAY,
    file_path: str = None,
):
    """Visualize robot/ado trajectories and distributions over full optimization (multiple time-steps).

    Draw trajectories in (quadratic) plot, thereby differentiate the actual trajectories from the
    baseline trajectories (without) using a different line markup. Also add little dots (`plt.Circle`) at the
    agents current positions.

   :param ego_planned: planned/optimized ego trajectory (time-step, t_horizon + 1, 5).
   :param ado_actual: actual ado trajectory (num_ados, time_step, 1, 5).
   :param ado_planned: according ado trajectory conditioned on ego_planned
                       (time-steps, num_ados, num_samples, t_horizon + 1, 1, 5).
   :param ado_planned_wo: ado trajectories without robot
                          (time-steps, num_ados, num_samples, t_horizon + 1, num_modes = 1,  5).
   :param env: simulation environment, just used statically here (e.g. to convert ids to agents, roll out
               trajectories, etc.).
   :param ego_goal: optimization robot goal state.
   :param legend: draw legend in paths plot (might be a mess for many agents).
   :param file_path: storage path, if None return as HTML video object.
   :param frame_interval: video frame displaying time interval [ms].
   :param restart_delay: video restart delay time interval [ms].
    """
    time_steps = ego_planned.shape[0]

    assert all(mantrap.utility.shaping.check_ego_trajectory(ego_planned[k]) for k in range(time_steps))
    assert ado_planned.shape[0] == time_steps
    assert ado_planned_wo.shape[0] == time_steps
    if ego_goal is not None:
        assert mantrap.utility.shaping.check_goal(ego_goal)

    plt.close('all')
    fig, ax = plt.subplots(figsize=(8, 8), constrained_layout=True)

    def update(k):
        plt.axis("off")
        ax.cla()

        # Plot optimization goal state as a red cross.
        if ego_goal is not None:
            assert mantrap.utility.shaping.check_goal(ego_goal)
            ax.plot(ego_goal[0], ego_goal[1], "rx", markersize=15.0, label="goal")

        # Since the environment is in the initial state for t > t0 the ado histories are not accurate.
        # Therefore extend them with the actual trajectories the ados took during optimization.
        ado_histories = []
        for m_ado, ado in enumerate(env.ados):
            ado_history = torch.cat((ado.history[:, 0:2], ado_actual[m_ado, :k, 0, 0:2]))
            ado_histories.append(ado_history)
        ado_histories = torch.stack(ado_histories)

        # All other visualizations are re-used from the prediction plot.
        visualize_prediction(ego_planned=ego_planned[k], ado_planned=ado_planned[k], ado_planned_wo=ado_planned_wo[k],
                             ado_histories=ado_histories, env=env, legend=legend, ax=ax)

        return ax

    anim = matplotlib.animation.FuncAnimation(fig, update, frames=time_steps,
                                              interval=frame_interval, repeat_delay=restart_delay)
    return interactive_save_video(anim, file_path=file_path)