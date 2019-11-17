SynthDef.new(\blip, {
    |amp=1, sus=1, pan=0, freq=0, vib=0, fmod=0, rate=0, bus=0, blur=1|
    var env, click, subtle, blip, osc;
    sus = sus * blur;
    freq = In.kr(bus, 1);
    freq = [freq, freq+fmod];
    freq = (freq + [0, LFNoise2.ar(50).range(-2, 2)]);
    freq = (freq * 2);
    // Elements
    click = LFCub.ar((freq * 1.002), iphase: 1.5) * 0.3;
    subtle = LFTri.ar(freq, iphase: Line.ar(2, 0, 0, 2)) * 0.3;
    blip = Blip.ar((freq / 2), rate);
    // Env
    env = XLine.ar(amp, (amp / 10000), (sus * 2)) * 0.3;
    // Oscillator
    osc = (click + subtle) * blip * env;
    osc = (osc * 3).tanh;
    osc = RHPF.ar(osc, 300, 1);
    osc = Mix(osc) * 0.8;
    osc = Pan2.ar(osc, pan);
    ReplaceOut.ar(bus, osc)
}).add;
