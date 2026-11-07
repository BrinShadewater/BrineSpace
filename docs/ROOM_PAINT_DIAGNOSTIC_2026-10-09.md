# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: normal-rendering content paint attribution

## Objective and acceptance
Identify sustained room rendering work without disabling visuals or animation
advancement. Timings establish a target, not an accepted gain or release certification.

## Accepted decisions and constraints
Frozen crew-cache inputs; normal quality, all layers enabled, actual debug=false
package. Isolated profiles and owner guards. Preserve animation pixels/timing,
reference identity and saved playback. No broad monolith refactor.

## Current state
Private timing-only RoomContent overlay at D:/bs-release-crew-cache-20261009/
room-paint-diagnostic-v2/. Unchanged frozen Grid is included to resolve its dependency
consistently. Per-frame bounded numeric paint counters distinguish simple library
painting, state binding/restoration and slot-kind draw bodies. Reset at existing
prepare/advance boundaries; no image retention or altered painting. Existing verified
physical QA package reused; previous runtime fixture retained with source identity.
Normal source and delivery packages unchanged.

## Verification
First room-paint-diagnostic/ run stops at its constructor guard before measurement;
retained log/unchanged owner fingerprint. Corrected guard checks canvases after warmup.
Session47523 exits0:540 idle samples at1/2/4x, zero engine/missing-art failures,
owner2,938 unchanged. All six comparisons against both normal-rendering diagnostic
orders match exactly, including crew/companion animation playback.

Content drawing means2.309/2.301/2.592ms. Simple library screen/effect path paints
110 slots per frame and costs1.470/1.472/1.483ms. Occupant pass~0.275-0.279ms;
crew draws~0.190-0.234ms; other prop bodies~0.202-0.422ms. State binding~0.093-0.096ms
and restoration~0.047-0.050ms. Counts are not durations, body intervals exclude
binding/restoration, and categories are nested inside content drawing.
workloads/analysis.json records full counters and exact state acceptance.

## Next action
Investigate repeated screen/effect calculations in _paint_simple_library and
PreparedScreens.draw. Screen geometry is already prepared; per-clock waveform,
bar and radar calculations repeat across props. Attribute within that path and
trial exact reusable calculations only where identical inputs guarantee identical
outputs. Keep effects, order and pixels; validate numerical/pixel parity and
matched actual workloads before admission. General frame gates/Mac/endurance open.
