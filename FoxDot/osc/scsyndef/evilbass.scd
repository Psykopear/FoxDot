SynthDef(\evilbass, {
    |bus=0, amp=1, freq=400, sus=0.1, cutoff=2000|
    var subfreq = freq / 2;
    var subsubfreq = subfreq / 2;
    var env = EnvGen.kr(Env.perc(0, sus, curve:-4), doneAction:2);

    // Component synthesis
    var pluck = Pluck.ar(PinkNoise.ar, 1, 0.1, subsubfreq.reciprocal) * env;
    var tri = VarSaw.ar(subfreq) * env;
    var sin = SinOsc.ar(subfreq / 2) * env * 0.8;
    var sub = (SinOsc.ar([subsubfreq, subsubfreq - 2, subsubfreq + 2]).sum * env).tanh;
    var click = RLPF.ar(Impulse.ar(0), [2000, 8000], 1).sum * 5;

    var sig = pluck + tri + sub + click;

    // Resonant LPFs
    sig = RLPF.ar(sig, XLine.ar(subsubfreq * 100, subsubfreq, 0.15));
    sig = sig + (MoogFF.ar(sig, subsubfreq * 20, 2.5) * 0.1);
    // EQ resulting signal
    sig = BPeakEQ.ar(sig, 400, 0.5, -12);
    sig = BPeakEQ.ar(sig, cutoff, 0.5, 6);
    sig = BHiShelf.ar(sig, 8000, 1, 3);

    // Apply another envelope to dampen a bit more
    sig = sig * XLine.kr(1, 0.6, 0.1);

    // Tanh distortion / limiting
    sig = (sig * 2.3).tanh;

    // Another round of signal coloring, using another RLPF and sine components
    sig = sig + RLPF.ar(sig, XLine.ar(subsubfreq * 50, subsubfreq * 10, 1)) + sub + sin;

    // Another round of tanh distortion / limiting
    sig = (sig / 2.3).tanh;

    // Another resonant LPF
    sig = MoogFF.ar(sig, XLine.ar(subsubfreq*150, subsubfreq*30, 0.1), 0.1);
    ReplaceOut.ar(bus, sig!2*amp*0.5)
}).add;
