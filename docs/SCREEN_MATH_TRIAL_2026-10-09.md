# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: exact shared screen calculations

## Objective and acceptance
Test whether repeated animated screen calculations explain the measured library
paint cost, preserving formulas, output commands, animation timing and saved state.
Require a meaningful measured remedy for remaining performance gates.

## Accepted decisions and constraints
Private prototype only; no production admission. Exact clocks/index keys, original
waveform and bar expressions, float64 bar levels, original geometry transformation
and command order. Radar rendering unchanged. Numeric cache bound128 entries;
new clock clears lookup, candidate Grid exit calls cleanup. No retained art/images.

## Current state
D:/bs-release-crew-cache-20261009/screen-math-trial/: reference.gd/candidate.gd,
test.gd, exact control/candidate three-file overlays and workloads/. Unchanged
frozen Grid/RoomContent sources accompany the helper to resolve packaged dependencies.
Candidate Grid adds only session-exit cleanup. Physical verified QA package reused.
Normal source, UIDs, owner layouts and delivery remain unchanged.

## Verification
Contract-first red test fails solely for absent cache API. Green and boundary runs
pass768 exact drawing-command comparisons across eight clocks, four indices, three
screen kinds, two scales, operating/reduced-motion states. Same clock shares waveform
math across geometry;300 unique requests stay at128 entries, tiny exact clock change
discards previous lookup, explicit cleanup empties it. Owner guards unchanged2,938.

Packaged session36329 exits0: four actual debug=false40-room idle/lighting runs,
all speeds/both orders,4,320 samples. Twelve full state pairs match exactly including
playback; no engine/missing-art errors; owner2,938 unchanged. Average frames
30.4012->30.2514ms forward and30.5109->30.3215ms reverse. Content callback savings
only52.56/55.52us per frame. Candidate lookup holds four entries, with143,836 hits
and2,522 waveform builds at the final forward phase. Original gate failures remain.
Command parity does not constitute complete packaged visual/release acceptance.

## Next action
Keep this unadmitted: repeated numerical calculations account for too little of
the remaining budget to prioritize cache complexity. Next distinguish original
screen/effect drawing submissions from setup/geometry allocation. Preserve actual
commands/pixels and animation sampling. Do not repeat this matched benchmark without
a material new change; full hardware, original bugs, endurance and Mac gates open.
