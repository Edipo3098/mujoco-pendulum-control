
from pathlib import Path
import time

import mujoco
import mujoco.viewer
import numpy as np

import yaml
import xml.etree.ElementTree as ET

# --------------------------------------------------
# 1. Load the Cart-Pole model
# --------------------------------------------------
# 1. Read YAML


with open("config/cartpole-parameters.yaml", "r") as file:
    config = yaml.safe_load(file)

cart_mass = config["physical"]["cart_mass_kg"]

# 2. Read XML
tree = ET.parse("models/cart-pole.xml")
root = tree.getroot()

# 3. Find cart geometry
cart_geom = root.find(".//geom[@name='cart_geom']")

# 4. Update mass
cart_geom.set("mass", str(cart_mass))

# 5. Save generated XML
tree.write("models/cartpole_generated.xml")

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "cartpole_generated.xml"

model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
data = mujoco.MjData(model)

print("MuJoCo version:", mujoco.__version__)
print("Degrees of freedom:", model.nv)
print("Actuators:", model.nu)


# --------------------------------------------------
# 2. Define initial conditions
# --------------------------------------------------

# State: [x, theta, x_dot, theta_dot]
# theta = 0   -> pendulum down
# theta = pi  -> pendulum upright

x0 = 0.0
theta0 = np.pi + np.deg2rad(1.0)

x_dot0 = 0.0
theta_dot0 = 0.0

# Initial positions
data.joint("slider").qpos[0] = x0
data.joint("hinge").qpos[0] = theta0

# Initial velocities
data.joint("slider").qvel[0] = x_dot0
data.joint("hinge").qvel[0] = theta_dot0

# Control force
actuator_id = mujoco.mj_name2id(
    model,
    mujoco.mjtObj.mjOBJ_ACTUATOR,
    "cart_force"
)

# Update the physics state
mujoco.mj_forward(model, data)


# --------------------------------------------------
# 3. Run simulation
# --------------------------------------------------

SIMULATION_TIME = 5.0
dt = model.opt.timestep
steps = int(SIMULATION_TIME / dt)

print(f"Simulation timestep: {dt} s")
print(f"Simulation duration: {SIMULATION_TIME} s")

with mujoco.viewer.launch_passive(model, data) as viewer:

    # Configure initial camera
    with viewer.lock():
        viewer.cam.type = mujoco.mjtCamera.mjCAMERA_FREE

        # Point the camera at the Cart-Pole
        viewer.cam.lookat[:] = [0.0, 0.0, 1.0]

        # Camera distance (zoom)
        viewer.cam.distance = 4.0

        # Horizontal rotation
        viewer.cam.azimuth = 90.0

        # Vertical rotation

    for i in range(steps):

        if not viewer.is_running():
            break

        step_start = time.perf_counter()

        # Physics integration
        mujoco.mj_step(model, data)

        # Update visualization every 10 steps
        if i % 10 == 0:
            viewer.sync()

        # Print state every 200 steps
        if i % 200 == 0:
            x = data.qpos[0]
            theta = data.qpos[1]
            x_dot = data.qvel[0]
            theta_dot = data.qvel[1]

            print(
                f"t={data.time:.2f}s | "
                f"x={x:.4f}m | "
                f"theta={theta:.4f}rad | "
                f"x_dot={x_dot:.4f}m/s | "
                f"theta_dot={theta_dot:.4f}rad/s"
            )

        # Approximate real-time simulation
        elapsed = time.perf_counter() - step_start
        time.sleep(max(0.0, dt - elapsed))

print("Simulation finished.")
