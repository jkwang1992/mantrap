#######################################
# agent parameters ###############
#######################################
agent_speed_max = 4  # maximal agent velocity in [m/s].
agent_acc_max = 4  # maximal agent acceleration in [m/s^2].

#######################################
# simulation parameters ###############
#######################################
sim_dt_default = 0.4
sim_x_axis_default = (-10, 10)
sim_y_axis_default = (-10, 10)

sim_social_forces_defaults = {
    "tau": 0.4,  # [s] relaxation time (assumed to be uniform over all agents).
    "v0": 4.0,  # [m2s-2] repulsive field constant.
    "sigma": 0.9,  # [m] repulsive field exponent constant.
}
sim_social_forces_min_goal_distance = 0.1  # [m] minimal distance to goal to have non-zero goal traction force.
sim_social_forces_max_interaction_distance = 2.0  # [m] maximal distance between agents for interaction force.

#######################################
# solver parameters ###################
#######################################
solver_horizon = 5  # number of future time-steps to be taken into account

ipopt_max_solver_steps = 100  # maximal number of IPOPT solver iterations.
ipopt_max_solver_cpu_time = 1.0  # [s] maximal IPOPT solver CPU time.

constraint_min_distance = 0.5  # [m] minimal distance constraint between ego and every ado ghost

orca_agent_radius = 1.0  # ado collision radius [m].
orca_agent_safe_dt = 10.0  # safe time for agent [s].

#######################################
# visualization parameters ############
#######################################
visualization_agent_radius = 0.1
visualization_preview_horizon = 10

#######################################
# numerical parameters ################
#######################################
eps_numeric = 0.0001
