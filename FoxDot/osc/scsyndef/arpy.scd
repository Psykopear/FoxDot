SynthDef.new(\arpy, {
    |amp=1, sus=1, pan=0, freq=0, fmod=5, bus=0, blur=1, level=0.8|
    var osc, env;
    sus = sus * blur;
    freq = In.kr(bus, 1);
    freq = [freq, freq+fmod];
    freq = (freq / 2);
    amp = (amp * 2.5);
    freq = (freq + [0, 0.5]);
    osc = RLPF.ar(Impulse.ar(freq), 3000,0.5);
    env = EnvGen.ar(Env.perc(attackTime: 0.01,releaseTime: (sus * 0.25),level: amp,curve: 0), doneAction: 0);
    osc = (osc * env);
    osc = RHPF.ar(osc, 400, 1);
    osc = Mix(osc);
    osc = Pan2.ar(osc, pan);
    ReplaceOut.ar(bus, osc)
}).add;
