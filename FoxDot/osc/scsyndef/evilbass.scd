(
    SynthDef(\evilbass, {
        |bus=0, amp=1, freq=400, sus=0.1, cutoff=2000| var subfreq = freq / 2;
        var env = EnvGen.kr(Env.perc(0, sus, curve:-4), doneAction:2);
        // Component synthesis
        var pluck = Pluck.ar(PinkNoise.ar, 1, 0.1, subfreq.reciprocal) * env;
        var tri = VarSaw.ar(freq) * env;
        var sin = SinOsc.ar(freq / 2) * env;
        var sub = (SinOsc.ar([subfreq, subfreq - 2, subfreq + 2]).sum * env).tanh;
        var click = RLPF.ar(Impulse.ar(0), [2000, 8000], 1).sum * 5;

        var sig = pluck + tri + sub + click;

        freq = freq / 2;
        // Resonant LPFs
        sig = RLPF.ar(sig, XLine.ar(freq * 100, freq * 10, 0.15));
        sig = sig + (MoogFF.ar(sig, freq * 20, 2.5) * 0.1);
        // EQ resulting signal
        sig = BPeakEQ.ar(sig, 400, 0.5, -9);
        sig = BPeakEQ.ar(sig, cutoff, 0.5, 6);
        sig = BHiShelf.ar(sig, 8000, 1, 3);
        sig = BPeakEQ.ar(sig, 200, 1, 3);
        // Apply another envelope to dampen a bit more
        sig = sig * XLine.kr(1, 0.6, 0.1);
        // Tanh distortion / limiting
        sig = (sig * 2.3).tanh;
        // Another round of signal coloring, using another RLPF
        // and sine components
        sig = sig + RLPF.ar(sig, XLine.ar(freq * 50, freq * 10, 1)) + sub + sin;
        // Another round of tanh distortion / limiting
        sig = (sig / 2.3).tanh;
        // Another resonant LPF
        sig = MoogFF.ar(sig, XLine.ar(freq*150, freq*30, 0.1), 0.1);
        ReplaceOut.ar(bus, sig!2*amp)
    }).add;
)
