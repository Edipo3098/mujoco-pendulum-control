
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
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
g_nominal = config["physical"]["gravity_m_per_s2"]

print("Configuration loaded successfully.")


# ============================================================
# 2. LINEARIZED STATE MATRIX A
# ============================================================

def upright_state_matrix(mc, mp, length, gravity):
    """
    Linearized state matrix around theta = pi.

    State:
        delta_s = [delta_x, delta_theta,
                   delta_x_dot, delta_theta_dot]

    Open-loop system:
        delta_s_dot = A @ delta_s
    """

    return np.array([
        [0.0, 0.0,                         1.0, 0.0],
        [0.0, 0.0,                         0.0, 1.0],
        [0.0, mp * gravity / mc,           0.0, 0.0],
        [0.0, (mc + mp) * gravity / (mc * length),
                                                   0.0, 0.0]
    ], dtype=float)


# ============================================================
# 3. ANALYTICAL POSITIVE EIGENVALUE
# ============================================================

def positive_eigenvalue(mc, mp, length, gravity):
    """
    Positive eigenvalue of the upright equilibrium.
    """

    return np.sqrt(
        (mc + mp) * gravity / (mc * length)
    )


# ============================================================
# 4. GRAVITY PARAMETER SWEEP
# ============================================================

# Vary gravity while keeping mc, mp and l constant.
gravity_values = np.linspace(
    0.2 * g_nominal,
    2.0 * g_nominal,
    200
)

eigenvalues_numerical = []
eigenvalues_analytical = []

for gravity in gravity_values:

    # Build A with the current gravity.
    A = upright_state_matrix(
        m_c, m_p, l, gravity
    )

    # Numerical eigenvalues of A.
    eigenvalues = np.linalg.eigvals(A)

    # The unstable eigenvalue is the one
    # with the largest real part.
    lambda_positive = np.max(eigenvalues.real)

    eigenvalues_numerical.append(lambda_positive)

    # Analytical eigenvalue.
    lambda_analytical = positive_eigenvalue(
        m_c, m_p, l, gravity
    )

    eigenvalues_analytical.append(lambda_analytical)


eigenvalues_numerical = np.array(eigenvalues_numerical)
eigenvalues_analytical = np.array(eigenvalues_analytical)


# ============================================================
# 5. CHECK NUMERICAL VS ANALYTICAL RESULTS
# ============================================================

error = np.abs(
    eigenvalues_numerical - eigenvalues_analytical
)

lambda_nominal = positive_eigenvalue(
    m_c, m_p, l, g_nominal
)

A_nominal = upright_state_matrix(
    m_c, m_p, l, g_nominal
)

print("\nNominal parameters:")
print(f"Cart mass:        {m_c:.3f} kg")
print(f"Pendulum mass:    {m_p:.3f} kg")
print(f"Pendulum length:  {l:.3f} m")
print(f"Gravity:          {g_nominal:.3f} m/s^2")

print("\nNominal eigenvalues:")
print(np.linalg.eigvals(A_nominal))

print(f"\nPositive eigenvalue: {lambda_nominal:.6f} 1/s")

print(
    "Maximum numerical vs analytical error:",
    f"{np.max(error):.3e} 1/s"
)

assert np.allclose(
    eigenvalues_numerical,
    eigenvalues_analytical,
    rtol=1e-10,
    atol=1e-12
), "Numerical eigenvalues do not match the analytical solution"


# ============================================================
# 6. ANGULAR PERTURBATION RESPONSE
# ============================================================

# For zero initial angular velocity:
#
# delta_theta(t) = delta_theta(0) * cosh(lambda * t)
#
# This response belongs to the LINEARIZED model.

initial_angle_deg = 0.5

time = np.linspace(0.0, 0.55, 500)

gravity_cases = [
    0.5 * g_nominal,
    g_nominal,
    1.5 * g_nominal
]


# ============================================================
# 7. PLOT RESULTS
# ============================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ----- Plot 1: eigenvalue vs gravity -----

axes[0].plot(
    gravity_values,
    eigenvalues_numerical,
    label="Numerical eigenvalue",
    linewidth=2
)

axes[0].plot(
    gravity_values,
    eigenvalues_analytical,
    "--",
    label="Analytical eigenvalue",
    linewidth=2
)

axes[0].scatter(
    [g_nominal],
    [lambda_nominal],
    color="red",
    zorder=5,
    label="Nominal parameters"
)

axes[0].set_title("Positive Eigenvalue vs Gravity")
axes[0].set_xlabel("Gravity (m/s²)")
axes[0].set_ylabel("Positive eigenvalue (1/s)")
axes[0].grid(True)
axes[0].legend()


# ----- Plot 2: angular perturbation growth -----

for gravity in gravity_cases:

    lambda_positive = positive_eigenvalue(
        m_c, m_p, l, gravity
    )

    delta_theta_deg = (
        initial_angle_deg *
        np.cosh(lambda_positive * time)
    )

    axes[1].plot(
        time,
        delta_theta_deg,
        label=f"g = {gravity:.2f} m/s²"
    )

axes[1].set_title("Growth of Angular Perturbation")
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Angular deviation (deg)")
axes[1].grid(True)
axes[1].legend()

fig.suptitle(
    "Cart-Pole - Eigenvalue Sensitivity to Gravity"
)

fig.tight_layout()

plt.show()
