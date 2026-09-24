# Native mixed-audio check

September22,2026. No audio assets, gains or gameplay changed.

Ran maintained tests/review_audio_mix.gd using native Godot with the Dummy stereo
backend and fresh isolated preferences/meta/loop paths. It combines normal music
and ambience with scheduled UI/placement/door/power/cargo/terminal/discovery/warning
cues, and seeks near a track boundary. Configured music and master volume are1.0.
Gameplay process/cycle timers are stopped; this is not an expedition audio review.

Exit0, no logged engine errors. Captured1409024stereo frames; peak-14.85dBFS,
zero dropped capture frames, successful WAV write. Independent PCM inspection
confirms no full-scale samples. A silent/missing cue is not excluded solely by a
nonzero mix; the fixture requests events but does not separately prove each audible
voice or assert that the randomized track boundary crossfaded rather than rested.
These measurements provide headroom evidence for this sample, not a perceived
loudness, spatial realism or owner listening acceptance. No gain adjustment justified.

Evidence: output/audio-review-2026-09-22/native.log, mix.wav and summary.json.
Next: owner listening/ordinary expedition audio judgment, with exact reproducible
cue/phase evidence if a problem is heard. Do not normalize all sounds based on the
peak of one mixed sample.
