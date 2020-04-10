import torch


def check_ego_state(x: torch.Tensor, enforce_temporal: bool = False) -> bool:
    if enforce_temporal:
        is_correct = x.size() == torch.Size([5])
    else:
        is_correct = x.size() == torch.Size([4]) or x.size() == torch.Size([5])
    return is_correct


def check_ego_action(x: torch.Tensor) -> bool:
    return x.size() == torch.Size([2])


def check_weights(x: torch.Tensor, num_ados: int = None, num_modes: int = None) -> bool:
    is_correct = True
    is_correct = is_correct and len(x.shape) == 2  # (num_ados, num_modes)
    if num_ados is not None:
        is_correct = is_correct and x.shape[0] == num_ados
    if num_modes is not None:
        is_correct = is_correct and x.shape[1] == num_modes
    return is_correct


def check_ego_path(x: torch.Tensor, num_primitives: int = None, t_horizon: int = None) -> bool:
    is_correct = True
    if num_primitives is not None:
        is_correct = is_correct and len(x.shape) == 3  # (num_primitives, t_horizon, 2)
        is_correct = is_correct and x.shape[2] == 2
        is_correct = is_correct and x.shape[0] == num_primitives
        if t_horizon is not None:
            is_correct = is_correct and x.shape[1] == t_horizon
    else:
        is_correct = is_correct and len(x.shape) == 2  # (t_horizon, 2)
        is_correct = is_correct and x.shape[1] == 2
        if t_horizon is not None:
            is_correct = is_correct and x.shape[0] == t_horizon
    return is_correct


def check_ego_controls(x: torch.Tensor, t_horizon: int = None) -> bool:
    is_correct = True
    is_correct = is_correct and len(x.shape) == 2  # (t_horizon, dims)
    if t_horizon is not None:
        is_correct = is_correct and x.shape[0] == t_horizon
    return is_correct


def check_ego_trajectory(x: torch.Tensor, t_horizon: int = None, pos_only: bool = False, pos_and_vel_only: bool = False
) -> bool:
    is_correct = True
    is_correct = is_correct and len(x.shape) == 2  # (t_horizon, 5)
    if pos_only:
        is_correct = is_correct and x.shape[1] >= 2  # (x, y, vx, vy)
    elif pos_and_vel_only:
        is_correct = is_correct and x.shape[1] >= 4  # (x, y, vx, vy)
    else:
        is_correct = is_correct and x.shape[1] == 5  # (x, y, vx, vy, t)
    if t_horizon is not None:
        is_correct = is_correct and x.shape[0] == t_horizon
    return is_correct


def check_ado_states(x: torch.Tensor, num_ados: int = None, enforce_temporal: bool = False) -> bool:
    is_correct = True
    is_correct = is_correct and len(x.shape) == 2  # (num_ados, 4/5)
    if num_ados is not None:
        is_correct = is_correct and x.shape[0] == num_ados
    if enforce_temporal:
        is_correct = is_correct and x.shape[1] == 5
    else:
        is_correct = is_correct and x.shape[1] == 4 or x.shape[1] == 5
    return is_correct


def check_ado_controls(x: torch.Tensor, t_horizon: int = None, num_ados: int = None, num_modes: int = None):
    is_correct = True
    is_correct = is_correct and len(x.shape) == 4  # (num_ados, num_modes, t_horizon, dims)
    if t_horizon is not None:
        is_correct = is_correct and x.shape[2] == t_horizon
    if num_ados is not None:
        is_correct = is_correct and x.shape[0] == num_ados
    if num_modes is not None:
        is_correct = is_correct and x.shape[1] == num_modes
    return is_correct


def check_ado_trajectories(
    x: torch.Tensor,
    ados: int = None,
    modes: int = None,
    t_horizon: int = None,
    pos_only: bool = False,
    pos_and_vel_only: bool = False
) -> bool:
    is_correct = True
    is_correct = is_correct and len(x.shape) == 4  # (num_ados,num_modes,t_horizon, 5)

    if pos_only:
        is_correct = is_correct and x.shape[3] >= 2  # (x, y)
    elif pos_and_vel_only:
        is_correct = is_correct and x.shape[3] >= 4  # (x, y, vx, vy)
    else:
        is_correct = is_correct and x.shape[3] == 5  # (x, y, vx, vy, t)

    if ados is not None:
        is_correct = is_correct and x.shape[0] == ados
    if modes is not None:
        is_correct = is_correct and x.shape[1] == modes
    if t_horizon is not None:
        is_correct = is_correct and x.shape[2] == t_horizon
    return is_correct
