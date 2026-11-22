
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
