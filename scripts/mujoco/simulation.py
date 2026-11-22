
import mujoco
import mujoco.viewer
from pathlib import Path
import numpy as np
class CartPoleSimulator:
    def __init__(self, model_path):
        ROOT = Path(__file__).resolve().parents[2]
        MODEL_PATH = ROOT / "models" /  model_path
        self.model = mujoco.MjModel.from_xml_path(str(MODEL_PATH))
        self.data = mujoco.MjData(self.model)

        self.viewer = None

        self.actuator_id = mujoco.mj_name2id(
            self.model,
            mujoco.mjtObj.mjOBJ_ACTUATOR,
            "cart_force"
        )

        print("MuJoCo version:", mujoco.__version__)
        print("Degrees of freedom:", self.model.nv)
        print("Actuators:", self.model.nu)

    def reset(self, x0=0.0, theta0=0.0, x_dot0=0.0, theta_dot0=0.0):

        mujoco.mj_resetData(self.model, self.data)
        # Initial positions
        self.data.joint("slider").qpos[0] = x0
        self.data.joint("hinge").qpos[0] = theta0

        # Initial velocities
        self.data.joint("slider").qvel[0] = x_dot0
        self.data.joint("hinge").qvel[0] = theta_dot0
        # Update the physics state
        mujoco.mj_forward(self.model, self.data)
    
    def getState(self):

        x = self.data.joint("slider").qpos[0]
        theta = self.data.joint("hinge").qpos[0]
        x_dot = self.data.joint("slider").qvel[0]
        theta_dot = self.data.joint("hinge").qvel[0]


        return x, theta, x_dot, theta_dot

    def step(self, force):
        # Apply control force
       
        self.data.actuator(self.actuator_id).ctrl[0] = force

        # Step the simulation
        mujoco.mj_step(self.model, self.data)

    def render(self):
        if self.viewer is None:
            self.viewer = mujoco.viewer.launch_passive(
                self.model,
                self.data
            )

            # Initial camera configuration
            with self.viewer.lock():
                self.viewer.cam.lookat[:] = [0.0, 0.0, 1.0]
                self.viewer.cam.distance = 4.0
                self.viewer.cam.azimuth = 90.0
                self.viewer.cam.elevation = -15.0

        if self.viewer.is_running():
            self.viewer.sync()

    def close(self):

        if self.viewer is not None:
            self.viewer.close()
            self.viewer = None


#sim = CartPoleSimulator("cartpole_generated.xml")
#
#sim.reset(
#    x0=0.0,
#    theta0=np.pi + np.deg2rad(1.0)
#)
#import time
#
#
#dt = sim.model.opt.timestep
#print("Simulation timestep:", dt, "seconds")
#
#SIMULATION_TIME = 10.0 # secods
#PLAYBACK_SPEED = 0.5  # 50% of real-time speed
#
#steps = int(SIMULATION_TIME / dt)
#
#sim.render()
#for i in range(steps):
#
#    if not sim.viewer.is_running():
#        break
#
#    sim.step(0.0)
#
#    if i % 10 == 0:
#        sim.render()
#
#    time.sleep(dt / PLAYBACK_SPEED)
#
## Display final simulation state
#sim.render()
#
#print("Simulation finished. Close the viewer to exit.")
#
## Keep the viewer open
#while sim.viewer.is_running():
#    time.sleep(0.05)
#
#sim.close()