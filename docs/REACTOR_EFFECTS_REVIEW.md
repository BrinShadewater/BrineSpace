# Reactor host motion and pause follow-up

`tests/playtest_reactor_effects.gd` uses the existing isolated-save native station
harness and the current Reactor renderer. It measures all six prop crops in four
rotations at the actual fitted station zoom, not an enlarged detail panel.

## Completed evidence

`output/reactor-effects-native-v1` exits 0 and reports zero assertion failures:

- 48 individual host comparisons: six props, four rotations, on/off pairs at
  visual times 0.2 and 1.1. Only the chamber and console have time-varying cues.
- Four paused pairs explicitly call `main._process(0.9)` while paused and require
  the visual clock and all six host crops to remain unchanged.
- Four resumes call the actual main process while unpaused, require the clock
  to advance, then require chamber and console pixels to change. The fixture
  pauses again before capture to keep the measurement deterministic.
- Escape/W/Space input-isolation checks pass. Full frames are 1600x900; recorded
  fitted grid zoom is approximately 0.428819, not a close-up art inspection.

The completed negative control, `reactor-effects-frozen-negative-v2`, exits 1 with
exactly eight failures: the deliberately frozen chamber fails working motion
and resume in each rotation. The console remains independently animated. Its
failure does not modify the production renderer.

`reactor-effects-frozen-negative-v1` ended with child 0 before any terminal test
summary or measurement results. It is incomplete evidence, not a passing control;
the cause is not established. The terminal process was gone before retrying.

The positive log has no ERROR/SCRIPT ERROR entries; raw-image warnings remain.
The later editor import exits 0 without engine/script errors and generates the
new test's paired `.gd.uid`.

## Visual review and boundaries

Reviewed `reactor-q0-on-a.png` and `reactor-q3-off-a.png`: props remain upright and
inside the low shell in those selected views. Small effect detail is restrained
at this zoom; changed pixels alone are not approval of perceived animation quality.

The fixture sets `powered_room_cells` directly. It does not test Reactor's economy
or prove whole-room darkness; the reviewed offline frame still has room lighting.
Operation binding, lighting policy and power-generation rules need separate
current-state verification before claiming a power-loss visual is correct.

Crew are temporarily disabled for these measurements and their prior active
flags restored afterward. Sidecars explicitly show no active/present crew here.
These are not normal crew-bearing review images or overlap evidence. No player
save, art source, card, wall height or gameplay code is changed.

`reactor-effects.json` records the current renderer/main hashes and each individual
operation comparison. This remains native evidence, not a fresh Windows package
certificate. The pipeline repair-loop now requires an attempted clock advance and
resume check before treating identical frames as pause evidence. The bible's
existing requirement that pause freezes active cues remains unchanged.
