SynthDef(\evilbass, {
    |bus=0, amp=1, freq=400, sus=0.5|
    var subfreq = freq / 4;
    // Envelopes
    var subenv = EnvGen.kr(Env.perc(0, sus), doneAction:2);
    var env = EnvGen.kr(Env.perc(0, sus));
    // Component synthesis
    var pluck = Pluck.ar(PinkNoise.ar, 1, 0.2, subfreq.reciprocal) * subenv * 2;
    var tri = VarSaw.ar(freq) * env;
    var sin = SinOsc.ar(freq) * env;
    var sub = (SinOsc.ar([subfreq, subfreq - 2, subfreq + 2]).sum * subenv).tanh;
    var click = RLPF.ar(Impulse.ar(0), [2000, 8000], 1).sum * 10;
    // Initial signal
    var sig = pluck + tri + sub + click;
    freq = freq / 2;
    // Resonant LPFs
    sig = RLPF.ar(sig, XLine.ar(freq * 100, freq * 10, 0.15));
    sig = sig + (MoogFF.ar(sig, freq * 20, 2.5) * 0.1);
    // EQ resulting signal
    sig = BPeakEQ.ar(sig, 400, 0.5, -9);
    sig = BPeakEQ.ar(sig, 2000, 0.5, 6);
    sig = BHiShelf.ar(sig, 8000, 1, 3);
    sig = BPeakEQ.ar(sig, 200, 1, 3);
    // Apply another envelope to dampen a bit more
    sig = sig * XLine.kr(1, 0.6, 0.1);
    // Tanh distortion / limiting
    sig = (sig * 1).tanh;
    // Another round of signal coloring, using another RLPF
    // and sine components
    sig = sig + RLPF.ar(sig, XLine.ar(freq * 100, freq * 10, 0.15)) + sin + sub;
    // Another round of tanh distortion / limiting
    sig = (sig / 2.3).tanh;
    // Another resonant LPF
    sig = MoogFF.ar(sig, XLine.ar(freq*150, freq*30, 0.1), 0.1);
    ReplaceOut.ar(bus, sig!2*0.5*amp)}
).add;
