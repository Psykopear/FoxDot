"""
Load all synthdefs in SuperCollider server
It also adds synth names to globals to be used during performances
"""
import os

from .SynthDef import FileSynthDef
from ..Settings import FOXDOT_ROOT
from .SCLang import instance


CUSTOM_ARGS = {
    "evilbass": {"cutoff": 1000},
}

for file in os.listdir(os.path.join(FOXDOT_ROOT, "osc/scsyndef/")):
    synth_name = os.path.splitext(file)[0]
    synth = FileSynthDef(synth_name)
    custom_args = CUSTOM_ARGS.get(synth_name)
    if custom_args:
        synth.defaults.update(custom_args)
        for key, value in custom_args.items():
            synth.__setattr__(key, instance(key))
    synth.add()
    globals()[synth_name] = synth
