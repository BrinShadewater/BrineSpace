# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: normal-budget stale drone cleanup trial

## Objective and acceptance
Remove the attributed stale lookup retention without changing selected art,
animation/gameplay or causing duplicate decode/upload work. Full release gates
remain open, particularly frame pacing and large-station memory.

## Accepted decisions and constraints
Private trial only; do not admit to normal source from one matched run. Both lanes
use the same original large-room renderer and physically selected flood helper.
No source-code reload. Owner saves are isolated and fingerprinted.

## Current state
Driver `output/compressed-crew-2026-10-06/run-drone-stale-gameplay.py` and comparator
`compare-drone-stale-gameplay.py`; artifacts in
`output/drone-stale-lease-2026-10-07/gameplay/`.
Private Motion candidate uses the normal 256 MiB decoded cache budget, frame-end
over-budget stale pruning, weak image restoration and expired weak metadata
pruning. Private SessionArtCache clears weak metadata and disconnects the trim
signal after the final owner. Original Motion/SessionArtCache/flood bytes restored.

## Verification
One native current-source 40-room 1920x1080 pair: idle/pan/zoom at 1/2/4x,
60 frames per phase, nine phases per lane. Full crew/drone/door/light/zoom/power
state, retained drone image metadata and viewport dimensions match in all phases.
Both clean logs/exits; 98 uploads each, counts equal at every phase. Owner 2,936
files unchanged; restoration guard passes; both processes terminal.

At zoom2x control reports 4,452.80465 MiB vs candidate 4,391.55474 MiB:
exactly 64,225,188 bytes (61.24991 MiB) less. Decoded lookup retention falls
771,277,716 -> 723,108,752 bytes; stale portion 48,168,964 -> 0. Other eight
texture endpoints equal, including final 4,146.74499 MiB. This corroborates the
previous two-source attribution and is transient memory improvement, not a
large-scene budget pass. Recently used images still exceed the decoded cache
budget; pruning must preserve them.

Frame performance mixed: median phase means 37.44593 -> 37.41690 ms; zoom2x
p95 77.205 -> 69.130 ms, but zoom1x 49.853 -> 51.759 and zoom4x 65.868 -> 66.875.
No consistent FPS claim. Neither run encounters >100 ms; earlier reproduced
104 ms stall remains unresolved, not closed by this pair. This is editor/source
native evidence, not debug=false packaged acceptance or a motion-pixel matrix.

## Next action
Run mixed-recency order and final-owner signal/weak-table cleanup regression
coverage, measure trim cost, and repeat with reversed order before admission.
Keep working on the larger zoom redraw stall and exact crew memory provider;
61 MiB transient savings does not resolve the remaining multi-GiB memory gate.
