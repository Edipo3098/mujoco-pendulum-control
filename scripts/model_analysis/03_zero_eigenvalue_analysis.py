
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
import yaml


# ============================================================
# 1. LOAD PHYSICAL PARAMETERS
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent

CONFIG_PATH = PROJECT_ROOT / "config" / "cartpole-parameters.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)

m_c = config["physical"]["cart_mass_kg"]
m_p = config["physical"]["pendulum_point_mass_kg"]
l = config["physical"]["pivot_to_point_mass_m"]
g = config["physical"]["gravity_m_per_s2"]

theta_e = config["assumptions"]["upright_angle_rad"]

print("Configuration loaded successfully.")


# ============================================================
# 2. LINEARIZED MODEL AROUND UPRIGHT EQUILIBRIUM
# ============================================================

def upright_state_matrix(mc, mp, length, gravity):
    """
    State order:
        [delta_x, delta_theta,
         delta_x_dot, delta_theta_dot]
    """

    return np.array([
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, mp * gravity / mc, 0.0, 0.0],
        [0.0, (mc + mp) * gravity / (mc * length), 0.0, 0.0]
    ], dtype=float)


def linear_dynamics(t, delta_state, A):
    return A @ delta_state


A = upright_state_matrix(m_c, m_p, l, g)


# ============================================================
# 3. EIGENVALUE ANALYSIS
# ============================================================

eigenvalues = np.linalg.eigvals(A)

print("\nState matrix A:")
print(A)

print("\nEigenvalues:")
print(eigenvalues)

zero_eigenvalues = np.isclose(
    eigenvalues,
    0.0,
    atol=1e-10
)

algebraic_multiplicity = np.count_nonzero(zero_eigenvalues)

print(A.shape[0], np.linalg.matrix_rank(A))
# Dimension of the kernel of A
geometric_multiplicity = A.shape[0] - np.linalg.matrix_rank(A)

print("\nZero eigenvalue analysis:")
print("Algebraic multiplicity:", algebraic_multiplicity)
print("Geometric multiplicity:", geometric_multiplicity)

assert algebraic_multiplicity == 2
assert geometric_multiplicity == 1


# ============================================================
# 4. EIGENVECTOR AND GENERALIZED EIGENVECTOR
# ============================================================

# Eigenvector corresponding to lambda = 0.
# A @ v0 = 0
v0 = np.array([1.0, 0.0, 0.0, 0.0])

# Generalized eigenvector.
# A @ v1 = v0
v1 = np.array([0.0, 0.0, 1.0, 0.0])

np.testing.assert_allclose(
    A @ v0,
    np.zeros(4),
    atol=1e-12
)

np.testing.assert_allclose(
    A @ v1,
    v0,
    atol=1e-12
)

print("\nEigenvector v0:")
print(v0)

print("\nGeneralized eigenvector v1:")
print(v1)


# ============================================================
# 5. SIMULATION PARAMETERS
# ============================================================

t_start = 0.0
t_end = 5.0

time_eval = np.linspace(t_start, t_end, 1000)

# Each case contains:
# (description, initial cart position, initial cart velocity)

cases = [
    ("Position perturbation", 0.2, 0.0),
    ("Velocity perturbation", 0.0, 0.2),
    ("Combined perturbation", 0.2, 0.2)
]


# ============================================================
# 6. NUMERICAL SIMULATION
# ============================================================

results = []

for description, x0, x_dot0 in cases:

    # Initial perturbation relative to upright equilibrium.
    # Angular perturbation and angular velocity are zero.
    initial_delta_state = np.array([
        x0,
        0.0,
        x_dot0,
        0.0
    ])

    solution = solve_ivp(
        linear_dynamics,
        (t_start, t_end),
        initial_delta_state,
        args=(A,),
        t_eval=time_eval,
        rtol=1e-10,
        atol=1e-12
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    # Analytical solution for these initial conditions.
    x_analytical = x0 + x_dot0 * solution.t
    x_dot_analytical = np.full_like(solution.t, x_dot0)

    np.testing.assert_allclose(
        solution.y[0],
        x_analytical,
        atol=1e-9
    )

    np.testing.assert_allclose(
        solution.y[2],
        x_dot_analytical,
        atol=1e-9
    )

    print(f"\n{description}")
    print(f"Initial position: {x0:.3f} m")
    print(f"Initial velocity: {x_dot0:.3f} m/s")
    print(f"Final position: {solution.y[0, -1]:.3f} m")
    print(f"Final velocity: {solution.y[2, -1]:.3f} m/s")

    results.append({
        "description": description,
        "time": solution.t,
        "state": solution.y,
        "x_analytical": x_analytical,
        "x_dot_analytical": x_dot_analytical
    })


# ============================================================
# 7. VISUALIZATION
# ============================================================

fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

for result in results:

    time = result["time"]
    state = result["state"]
    label = result["description"]

    # Cart position: numerical and analytical
    line, = axes[0].plot(
        time,
        state[0],
        label=f"{label} - numerical"
    )

    axes[0].plot(
        time,
        result["x_analytical"],
        linestyle="--",
        color=line.get_color(),
        alpha=0.7,
        label=f"{label} - analytical"
    )

    # Cart velocity
    axes[1].plot(
        time,
        state[2],
        label=label
    )


axes[0].set_title("Cart Position")
axes[0].set_ylabel("Position (m)")
axes[0].grid(True)
axes[0].legend()

axes[1].set_title("Cart Velocity")
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Velocity (m/s)")
axes[1].grid(True)
axes[1].legend()

fig.suptitle(
    "Cart-Pole - Zero Eigenvalues and Free Cart Motion"
)

fig.tight_layout()

plt.show()
