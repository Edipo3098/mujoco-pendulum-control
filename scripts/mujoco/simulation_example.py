from scripts.model.build_model import CartPoleModelBuilder
from scripts.mujoco.simulation import CartPoleSimulator
import numpy as np
import time


builder = CartPoleModelBuilder(initial_position="up")
path = builder.build_model()

sim = CartPoleSimulator(path)

INITIAL_POSITION = "up"     # "up" o "down"
PERTURBATION_DEG = 1.0     # Grados respecto al equilibrio

theta_equilibrium = np.pi if INITIAL_POSITION == "up" else 0.0
sim.reset(theta0=theta_equilibrium + np.deg2rad(PERTURBATION_DEG))  # Start with the pole in the upright position

dt = sim.model.opt.timestep
print("Simulation timestep:", dt, "seconds")
SIMULATION_TIME = 10.0 # secods
PLAYBACK_SPEED = 0.5  # 50% of real-time speed
steps = int(SIMULATION_TIME / dt)
sim.render()
for i in range(steps):
    if not sim.viewer.is_running():
        break
    x, theta, x_dot, theta_dot = sim.step(0.0)
    if i % 10 == 0:
        sim.render()
    time.sleep(dt / PLAYBACK_SPEED)
# Display final simulation state
sim.render()
print("Simulation finished. Close the viewer to exit.")
# Keep the viewer open
while sim.viewer.is_running():
    time.sleep(0.05)
sim.close()