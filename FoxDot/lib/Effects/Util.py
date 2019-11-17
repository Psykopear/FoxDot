from ..Settings import EFFECTS_DIR, SC3_PLUGINS
from ..ServerManager import Server


class Effect:
    server = Server

    def __init__(self, foxdot_name, synthdef, args={}, control=False):
        self.name = foxdot_name
        self.synthdef = synthdef
        self.filename = EFFECTS_DIR + "/{}.scd".format(self.synthdef)
        self.args = args.keys()
        self.vars = ["osc"]
        self.defaults = args
        self.effects = []
        self.control = control

        self.channels = 1 if self.control else 2

    @classmethod
    def set_server(cls, server):
        cls.server = server

    def __repr__(self):
        other_args = ["{}".format(arg) for arg in self.args if arg != self.name]
        other_args = ", other args={}".format(other_args) if other_args else ""
        return "<'{}': keyword='{}'{}>".format(self.synthdef, self.name, other_args)

    def __str__(self):
        return self.__repr__()

    def add(self, string):
        self.effects.append(string)

    def doc(self, string):
        """ Set a docstring for the effects"""
        pass

    def list_effects(self):
        return ";\n".join(self.effects)

    def add_var(self, name):
        if name not in self.vars:
            self.vars.append(name)

    def save(self):
        self.load()

    def load(self):
        """ Load the Effect into the server. """
        if self.server is not None:
            self.server.loadSynthDef(self.filename)


class EffectManager(dict):
    def __init__(self):
        dict.__init__(self)
        self.kw = []
        self.all_kw = []
        self.defaults = {}
        self.order = {N: [] for N in range(3)}

    def __repr__(self):
        return "\n".join([repr(value) for value in self.values()])

    def values(self):
        return [self[key] for key in self.sort_by("synthdef")]

    def sort_by(self, attr):
        """ Returns the keys sorted by attribute name"""
        return sorted(self.keys(), key=lambda effect: getattr(self[effect], attr))

    def new(self, foxdot_arg_name, synthdef, args, order=2):
        self[foxdot_arg_name] = Effect(foxdot_arg_name, synthdef, args, order == 0)

        if order in self.order:
            self.order[order].append(foxdot_arg_name)
        else:
            self.order[order] = [foxdot_arg_name]

        # Store the main keywords together
        self.kw.append(foxdot_arg_name)

        # Store other sub-keys
        for arg in args:
            if arg not in self.all_kw:
                self.all_kw.append(arg)
            # Store the default value
            self.defaults[arg] = args[arg]
        self[foxdot_arg_name].load()
        return self[foxdot_arg_name]

    def kwargs(self):
        """ Returns the title keywords for each effect """
        return tuple(self.kw)

    def all_kwargs(self):
        """ Returns *all* keywords for all effects """
        return tuple(self.all_kw)

    def __iter__(self):
        for key in self.kw:
            yield key, self[key]

    def reload(self):
        """ Re-sends each effect to SC """
        for kw, effect in self:
            effect.load()


class In(Effect):
    def __init__(self):
        Effect.__init__(self, "startSound", "startSound")
        self.load()


class Out(Effect):
    def __init__(self):
        self.max_duration = 8
        Effect.__init__(self, "makeSound", "makeSound")
        self.load()


FxList = EffectManager()

# In and Out
Out()
In()

# Frequency Effects
FxList.new("vib", "vibrato", {"vib": 0, "vibdepth": 0.02}, order=0)
FxList.new("slide", "slideTo", {"slide": 0, "sus": 1, "slidedelay": 0}, order=0)
FxList.new(
    "slidefrom", "slideFrom", {"slidefrom": 0, "sus": 1, "slidedelay": 0}, order=0
)
FxList.new("glide", "glissando", {"glide": 0, "glidedelay": 0.5, "sus": 1}, order=0)
FxList.new("bend", "pitchBend", {"bend": 0, "sus": 1, "benddelay": 0}, order=0)
FxList.new("coarse", "coarse", {"coarse": 0, "sus": 1}, order=0)
FxList.new("striate", "striate", {"striate": 0, "sus": 1, "buf": 0, "rate": 1}, order=0)
FxList.new("pshift", "pitchShift", {"pshift": 0}, order=0)
FxList.new("hpf", "highPassFilter", {"hpf": 0, "hpr": 1}, order=2)
FxList.new("lpf", "lowPassFilter", {"lpf": 0, "lpr": 1}, order=2)
FxList.new("swell", "filterSwell", {"swell": 0, "sus": 1, "hpr": 1}, order=2)
FxList.new(
    "bpf", "bandPassFilter", {"bpf": 0, "bpr": 1, "bpnoise": 0, "sus": 1}, order=2
)

if SC3_PLUGINS:
    FxList.new(
        "crush", "bitcrush", {"bits": 8, "sus": 1, "amp": 1, "crush": 0}, order=1
    )
    FxList.new("dist", "distortion", {"dist": 0, "tmp": 0}, order=1)

# Post envelope effects
FxList.new("chop", "chop", {"chop": 0, "sus": 1}, order=2)
FxList.new("tremolo", "tremolo", {"tremolo": 0, "beat_dur": 1}, order=2)
FxList.new("echo", "combDelay", {"echo": 0, "beat_dur": 1, "echotime": 1}, order=2)
FxList.new("spin", "spinPan", {"spin": 0, "sus": 1}, order=2)
FxList.new("cut", "trimLength", {"cut": 0, "sus": 1}, order=2)
FxList.new("room", "reverb", {"room": 0, "mix": 0.1}, order=2)
FxList.new("formant", "formantFilter", {"formant": 0}, order=2)
FxList.new("shape", "wavesShapeDistortion", {"shape": 0}, order=2)
FxList.new("drive", "overdriveDistortion", {"drive": 0}, order=2)

Effect.server.setFx(FxList)
