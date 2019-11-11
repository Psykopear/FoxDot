# FoxDot
This is a fork of FoxDot intended for personal use, please go to [the original repository](https://github.com/Qirky/FoxDot) for instructions, issues or PRs.

## Why a fork?
I love FoxDot, and Qirky made a great job architecting the application (I never experienced a crash in 2 years of use).

That said, there are some things that are holding me from developing comfortably:
- the code looks a bit messy and I feel it's hard to read (solution: use a formatter like [Black](missing-link))
- it's hard to keep up with the amount of new development the original author adds to it (solution: freeze at the actual version for now, 1.8)
- I need some samples that would be good for me but maybe not for everyone and since the amount of samples that can be included is limited, I'm going to swap some of the existing ones

Other than this, there are things I want to to that could be merged into the main repository if the author and the community are ok with it:
- I'd like to cleanup the sound design in some synths
- I'd like to rename some synths to make clear their intended use (bass synths, lead synths, ecc). This is a consequence of the previous point, for example I would cut low frequencies in any synth not intended to be used as a bass
- I don't need any of the GUI code since I use an external editor, so I would separate GUI code from the library as two separate packages, of which I would only maintain the library part
- I'd like to start Supercollider from within FoxDot, so I don't have to fire up the instance separately
- Remove python2 compatibility layer, since python2 is going to die [very soon](https://pythonclock.org) and the code adds complexity I don't want to deal with

## Changes
- Apply Black formatter to the codebase for easier reading. I avoided using it on demos and in general wherever there is code used for performances, since I don't think it's useful there.

## Todo
- [x] Format code with Black
- [ ] Remove GUI code (can be recovered from the original repo if needed)
- [ ] Start supercollider server from within FoxDot
- [ ] Adjust present synths' sound design
- [ ] New synths design
- [ ] New drums samples design
- [ ] Control parameters or entrie instruments via an external midi controller
