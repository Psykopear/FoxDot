"""
Load all synthdefs in SuperCollider server
It also adds synth names to globals to be used during performances
"""
import os

from .SynthDef import FileSynthDef
from ..Settings import FOXDOT_ROOT

for file in os.listdir(os.path.join(FOXDOT_ROOT, "osc/scsyndef/")):
    synth_name = os.path.splitext(file)[0]
    synth = FileSynthDef(synth_name)
    synth.add()
    globals()[synth_name] = synth
