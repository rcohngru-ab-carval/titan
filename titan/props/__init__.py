import os

from .gen import gen_props

PROPS_FILES = [file for file in os.listdir(os.path.dirname(__file__)) if file.endswith(".props")]
PROPS = {}

for filename in PROPS_FILES:
    entity, _ = filename.split(".")
    file = os.path.join(os.path.dirname(__file__), filename)
    PROPS[entity] = gen_props(open(file, "r").read())