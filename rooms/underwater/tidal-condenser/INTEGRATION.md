# Tidal Condenser initial art integration

Four registered south-facing skids render through shared tee geometry. Plain
source wall strips replace the source's recessed midpoint treatment. Station,
draft and inspector card consumers select the new 512-square card; the baker
accepts `--tidal`. The immutable source remains RGB 1254 square.

Operating cues: condensation strokes on the lowest chilled coil, local tank
flow traces, pump gauge and console traces. All four hosts stop offline and
freeze on pause. These are restrained operating cues, not simulated fluid fill.

`tests/playtest_tidal_condenser.gd` passes at 1280x720, 1600x900 and 2560x1440:
four rotations, full assembly bounds, per-host motion/offline/pause pixels,
non-overlapping footprints, canonical tee sockets, 1,092 aisle samples and
console-screen containment. All runs exit zero without SCRIPT ERROR/ERROR lines;
inherited Image.load warnings remain. Logs/captures: `output/tidal-condenser/native-*`.
The native 512 card and 1600 active station/draft/inspector frame were reviewed.

Gameplay branch evidence is separate in GAMEPLAY.md. Remaining: native discovery
progression, real-economy visual states, connected/blocked boundaries, production
walker/depth review and export. Source floor within enclosed skid frames and
mostly steel department treatment remain visual tradeoffs for review.

## Connected paths and economy follow-up

Focused pair sweep against the first ten rooms, three adaptations and itself:
1,728 ordered pairs, 828 compatible and 329,664 production foot samples pass.
Neighbor selection and collision are checked separately from pixels. Four real
economy states and paired frames also pass at base rotation/1600x900, without
working-cell overrides. Evidence: `output/tidal-condenser/walker.*`, `economy.*`.

All three canonical ports at four rotations pass 12 production arrivals against
Battery Array. Both unscaled review pages (84 sampled frames) were inspected;
thresholds and equipment approaches remain clear with appropriate door behavior.
Full captures/index: `crossings-1600/`; sheet metadata/hashes and explicit review:
`crossing-review/`. Fixed 30% zoom, 1600x900, 100x100 native crops. No continuous
unsampled motion, other neighbor materials or complete depth claim is implied.
All runs exit zero without SCRIPT ERROR/ERROR lines.

`tools/build_crossing_review_sheet.py` reproduces the review sheets from a capture
index and explicit crop bounds. It preserves source frames, rejects invalid
bounds/paths or an existing output directory, records hashes, and never marks
its output as visually reviewed. Review findings remain a separate record.

## Windows export follow-up

The checked Windows command with all four additional manifests passes in
`output/production-ten/windows-validation-condenser-v1`. The executable runs
from an empty external directory: 14 selected source hashes, 28 raw PNG decodes,
21 rooms visited, 308 connected transitions. These are 2,000 simulated walker
seconds, not long-run economy or hardware-performance coverage. Export/runtime
logs have no SCRIPT ERROR/ERROR lines; artifact hashes are in verification.json.
The start overview was inspected and Tidal Condenser is visible at lower right.
Other rooms partially covered by the objective overlay are not thereby reviewed.
