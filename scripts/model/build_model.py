
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

class CartPoleModelBuilder:
    def __init__(self, config_path="config/cartpole-parameters.yaml", initial_position="down"):
        if initial_position not in ("down", "up"):
            raise ValueError("initial_position must be \"down\" or \"up\"")

        self.initial_position = initial_position
        self.config_path = config_path
        with open(self.config_path, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.cart_mass_kg = self.config["physical"]["cart_mass_kg"]
        self.pole_mass_kg = self.config["physical"]["pendulum_point_mass_kg"]
        self.pole_length_m = self.config["physical"]["pivot_to_point_mass_m"]
        self.g_nominal_m_s2 = self.config["physical"]["gravity_m_per_s2"]

    def build_model(self):
        # 2. Read XML
        tree = ET.parse("models/cart-pole.xml")
        root = tree.getroot()

        # 3. Find cart geometry
        cart_geom = root.find(".//geom[@name='cart_geom']")

        # 4. Update mass
        cart_geom.set("mass", str(self.cart_mass_kg))

        # 5. Find pole geometry
        pole_inertial = root.find(".//body[@name='pole']/inertial")
        pole_inertial.set("mass", str(self.pole_mass_kg))
        pole_inertial.set("pos", f"0 0 {-self.pole_length_m}")

        # Visual rod
        pole_rod = root.find(".//geom[@name='pole_rod']")
        pole_rod.set("fromto", f"0 0 0 0 0 {-self.pole_length_m}")

        # Visual point mass
        pole_bob = root.find(".//geom[@name='pole_bob']")
        pole_bob.set("pos", f"0 0 {-self.pole_length_m}")

        # Gravity
        option = root.find("./option")
        option.set("gravity", f"0 0 {-self.g_nominal_m_s2}")

        # Initial configuration: theta = 0 (down) or theta = pi (up)
        upright_angle = self.config["assumptions"]["upright_angle_rad"]
        initial_theta = 0.0 if self.initial_position == "down" else upright_angle
        keyframe = root.find("./keyframe")
        if keyframe is None:
            keyframe = ET.SubElement(root, "keyframe")
        initial_key = keyframe.find("./key[@name='initial']")
        if initial_key is None:
            initial_key = ET.SubElement(keyframe, "key", name="initial")
        initial_key.set("qpos", f"0 {initial_theta}")
        initial_key.set("qvel", "0 0")
        initial_key.set("ctrl", "0")

        # 6. Save generated XML
        tree.write("models/cartpole_generated.xml")
        output_path = Path("models/cartpole_generated.xml")
        return output_path


if __name__ == "__main__":
    model = CartPoleModelBuilder()
    path = model.build_model()
    print(path)
