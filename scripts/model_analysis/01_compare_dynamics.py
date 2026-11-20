
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from pathlib import Path
import yaml


# ============================================================
# 1. LOAD PHYSICAL PARAMETERS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR.parent.parent / "config" / "cartpole-parameters.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

m_c = config["physical"]["cart_mass_kg"]
m_p = config["physical"]["pendulum_point_mass_kg"]
l = config["physical"]["pivot_to_point_mass_m"]
g = config["physical"]["gravity_m_per_s2"]

theta_e = config["assumptions"]["upright_angle_rad"]

print("Config loaded successfully.")


# ============================================================
# 2. NONLINEAR MODEL
# ============================================================

def cartpole_dynamics(t, state, mc, mp, L, g):
    x, theta, x_dot, theta_dot = state

    U = 0.0

    denominator = mc + mp * np.sin(theta)**2

    x_ddot = (
        U
        + mp * L * theta_dot**2 * np.sin(theta)
        + mp * g * np.sin(theta) * np.cos(theta)
    ) / denominator

    theta_ddot = -(
        U * np.cos(theta)
        + mp * L * theta_dot**2 * np.sin(theta) * np.cos(theta)
        + (mc + mp) * g * np.sin(theta)
    ) / (L * denominator)

    return [x_dot, theta_dot, x_ddot, theta_ddot]


# ============================================================
# 3. LINEARIZED MODEL AROUND UPRIGHT EQUILIBRIUM
# ============================================================

A = np.array([
    [0, 0,             1, 0],
    [0, 0,             0, 1],
    [0, m_p*g/m_c,     0, 0],
    [0, g*(m_c+m_p)/(l*m_c), 0, 0]
], dtype=float)


def cartpole_linear_dynamics(t, delta_state, A):
    return A @ delta_state


# ============================================================
# 4. INITIAL CONDITIONS AND SIMULATION
# ============================================================

# Perturbation around the upright equilibrium
initial_angle_deg = float(os.environ.get("CARTPOLE_INITIAL_ANGLE_DEG", "10.0"))

# Short time interval: linearization is valid locally
t_start = 0.0
t_end = 1.2

time_eval = np.linspace(t_start, t_end, 1000)

# Upright equilibrium
equilibrium_state = np.array([0.0, theta_e, 0.0, 0.0])

# Nonlinear initial state
initial_state = equilibrium_state + np.array([
    0.0,
    np.deg2rad(initial_angle_deg),
    0.0,
    0.0
])

# Linearized initial perturbation
initial_delta_state = initial_state - equilibrium_state


# Nonlinear integration
solution_nonlinear = solve_ivp(
    cartpole_dynamics,
    (t_start, t_end),
    initial_state,
    args=(m_c, m_p, l, g),
    t_eval=time_eval,
    rtol=1e-10,
    atol=1e-12
)

# Linear integration
solution_linear = solve_ivp(
    cartpole_linear_dynamics,
    (t_start, t_end),
    initial_delta_state,
    args=(A,),
    t_eval=time_eval,
    rtol=1e-10,
    atol=1e-12
)

if not solution_nonlinear.success:
    raise RuntimeError(solution_nonlinear.message)

if not solution_linear.success:
    raise RuntimeError(solution_linear.message)

time = solution_nonlinear.t

# Nonlinear state: [x, theta, x_dot, theta_dot]
state_nonlinear = solution_nonlinear.y

# Linear solution contains perturbations.
delta_state_linear = solution_linear.y

# Convert the linear perturbations into physical states.
state_linear = (
    delta_state_linear + equilibrium_state[:, np.newaxis]
)


# ============================================================
# 5. MECHANICAL ENERGY
# ============================================================

def mechanical_energy(state, mc, mp, L, g):
    x, theta, x_dot, theta_dot = state

    T = (
        0.5 * (mc + mp) * x_dot**2
        + mp * L * x_dot * theta_dot * np.cos(theta)
        + 0.5 * mp * L**2 * theta_dot**2
    )

    V = -mp * g * L * np.cos(theta)

    return T + V


def linearized_energy(delta_state, mc, mp, L, g):
    dx, dtheta, dx_dot, dtheta_dot = delta_state

    # Quadratic Taylor approximation of mechanical energy
    # around theta = pi, zero velocities.
    T = (
        0.5 * (mc + mp) * dx_dot**2
        - mp * L * dx_dot * dtheta_dot
        + 0.5 * mp * L**2 * dtheta_dot**2
    )

    V = (
        mp * g * L
        - 0.5 * mp * g * L * dtheta**2
    )

    return T + V


# Physical mechanical energy of the nonlinear trajectory
E_nonlinear = mechanical_energy(
    state_nonlinear, m_c, m_p, l, g
)

# Physical energy formula evaluated on the linear trajectory
E_linear_physical = mechanical_energy(
    state_linear, m_c, m_p, l, g
)

# Quadratic energy approximation associated with linear dynamics
E_linear_quadratic = linearized_energy(
    delta_state_linear, m_c, m_p, l, g
)


# Energy deviations relative to each initial value
error_nonlinear = E_nonlinear - E_nonlinear[0]
error_linear_physical = E_linear_physical - E_linear_physical[0]
error_linear_quadratic = E_linear_quadratic - E_linear_quadratic[0]

print(
    "Nonlinear energy max error:",
    f"{np.max(np.abs(error_nonlinear)):.3e} J"
)

print(
    "Linear quadratic energy max error:",
    f"{np.max(np.abs(error_linear_quadratic)):.3e} J"
)


# ============================================================
# 6. DYNAMICS COMPARISON
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True)

labels = [
    "Cart position (m)",
    "Pendulum angle (deg)",
    "Cart velocity (m/s)",
    "Angular velocity (deg/s)"
]

titles = [
    "Cart Position",
    "Pendulum Angle",
    "Cart Velocity",
    "Angular Velocity"
]

for i, ax in enumerate(axes.flat):
    nonlinear_values = state_nonlinear[i]
    linear_values = state_linear[i]

    # Convert angular values to degrees
    if i in (1, 3):
        nonlinear_values = np.rad2deg(nonlinear_values)
        linear_values = np.rad2deg(linear_values)

    ax.plot(time, nonlinear_values, label="Nonlinear")
    ax.plot(
        time,
        linear_values,
        linestyle="--",
        label="Linearized"
    )

    if i == 1:
        ax.axhline(
            np.rad2deg(theta_e),
            color="red",
            linestyle=":",
            label="Upright equilibrium"
        )

    ax.set_title(titles[i])
    ax.set_ylabel(labels[i])
    ax.grid(True)
    ax.legend()

for ax in axes[1]:
    ax.set_xlabel("Time (s)")

fig.suptitle("Cart-Pole - Nonlinear vs Linear Dynamics")
fig.tight_layout()


# ============================================================
# 7. ENERGY COMPARISON
# ============================================================

fig_energy, energy_axes = plt.subplots(
    2, 1, figsize=(12, 8), sharex=True
)

# Energy values
energy_axes[0].plot(
    time, E_nonlinear,
    label="Nonlinear - physical energy"
)

energy_axes[0].plot(
    time, E_linear_physical,
    linestyle="--",
    label="Linear trajectory - physical energy"
)

energy_axes[0].plot(
    time, E_linear_quadratic,
    linestyle=":",
    label="Linear - quadratic energy"
)

energy_axes[0].set_ylabel("Energy (J)")
energy_axes[0].set_title("Mechanical Energy")
energy_axes[0].grid(True)
energy_axes[0].legend()


# Energy conservation errors
energy_axes[1].plot(
    time, error_nonlinear,
    label="Nonlinear energy error"
)

energy_axes[1].plot(
    time, error_linear_physical,
    linestyle="--",
    label="Physical energy on linear trajectory"
)

energy_axes[1].plot(
    time, error_linear_quadratic,
    linestyle=":",
    label="Linear quadratic energy error"
)

energy_axes[1].axhline(
    0, color="red", linestyle="--",
    label="Zero energy error"
)

energy_axes[1].set_xlabel("Time (s)")
energy_axes[1].set_ylabel("Energy difference (J)")
energy_axes[1].set_title("Energy Conservation Error")
energy_axes[1].grid(True)
energy_axes[1].legend()

fig_energy.suptitle("Cart-Pole - Energy Comparison")
fig_energy.tight_layout()

# Optional: export reproducible images for the experiment results gallery.
output_dir = os.environ.get("CARTPOLE_PLOT_DIR")
if output_dir:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    angle_label = format(initial_angle_deg, "g").replace(".", "p").replace("-", "m")
    fig.savefig(output_path / f"angle_{angle_label}_dynamics.png", dpi=150)
    fig_energy.savefig(output_path / f"angle_{angle_label}_energy.png", dpi=150)

plt.show()
