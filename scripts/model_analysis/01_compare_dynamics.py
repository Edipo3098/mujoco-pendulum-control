import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from pathlib import Path
import yaml

# Directorio del script actual
SCRIPT_DIR = Path(__file__).resolve().parent

# Ruta del archivo YAML
CONFIG_PATH = SCRIPT_DIR.parent.parent / "config" / "cartpole-parameters.yaml"

with open(CONFIG_PATH, 'r') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

print("Config loaded successfully.")

m_c = config['physical']['cart_mass_kg']
m_p = config['physical']['pendulum_point_mass_kg']
l =   config['physical']['pivot_to_point_mass_m']
g =  config['physical']['gravity_m_per_s2']

theta_e = config['assumptions']['upright_angle_rad']

def cartpole_dynamics(t, state,mc,mp,L,g):
    x, theta, x_dot, theta_dot = state
    U = 0.0

       # Aceleración del carro
    x_ddot = ( U +mp*np.sin(theta)*(L*theta_dot**2 +g*np.cos(theta)))/(mc +mp*np.sin(theta)**2)
    theta_ddot = (-U*np.cos(theta) -mp*L*theta_dot**2*np.cos(theta)*np.sin(theta)-(mc+mp)*g*np.sin(theta))/(L*(mc+mp*np.sin(theta)**2))

    return [x_dot, theta_dot, x_ddot, theta_ddot]

initial_state = [0, theta_e + np.deg2rad(0), 0, 0]

solution = solve_ivp(cartpole_dynamics, [0, 10], initial_state, args=(m_c, m_p, l, g),t_eval=np.linspace(0,10,1000),rtol=1e-10, atol=1e-10)

if not solution.success:
    raise RuntimeError(solution.message)

time = solution.t
theta = solution.y[1]

# Convertimos el ángulo de radianes a grados
theta_deg = np.rad2deg(theta)
theta_e_deg = np.rad2deg(theta_e)



# Extraemos las velocidades de la solución
x_dot = solution.y[2]
theta_dot = solution.y[3]

# Energía cinética
T = (
    0.5 * (m_c + m_p) * x_dot**2
    + m_p * l * x_dot * theta_dot * np.cos(theta)
    + 0.5 * m_p * l**2 * theta_dot**2
)

# Energía potencial
V = -m_p * g * l * np.cos(theta)

# Energía mecánica total
E = T + V

# Error respecto a la energía inicial
energy_error = E - E[0]

print(f"Initial energy: {E[0]:.12f} J")
print(f"Maximum absolute energy error: {np.max(np.abs(energy_error)):.3e} J")

# Gráfica del error de energía
plt.figure(figsize=(10, 5))
plt.plot(time, energy_error, label="Energy error")

plt.axhline(0, color="red", linestyle="--", label="Ideal energy error")

plt.xlabel("Time (s)")
plt.ylabel("Energy error (J)")
plt.title("Cart-Pole - Mechanical Energy Conservation")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Creamos la gráfica
plt.figure(figsize=(10, 5))

plt.plot(time, theta_deg, label="Nonlinear model")
plt.axhline(
    theta_e_deg,
    linestyle="--",
    color="red",
    label="Upright equilibrium"
)

plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.title("Cart-Pole - Nonlinear Angular Dynamics")

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
