# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: first-time room setup

## Objective and acceptance

Reduce first-placement setup without changing appearance; measure average FPS,
placement peaks and following frames against the latest accepted water baseline.

## Accepted decisions and constraints

Private distant-room LOD remains private. No production runtime, art, clocks,
quality, renderer or export change. Crew/doors/warnings remain live. Serial native
jobs, isolated APPDATA and owner fingerprints; existing editor left untouched.

## Current state

`C:/bs-first-room-setup-20261015/candidate-room_content_canvas.gd` adds one empty
capture viewport per content layer, taken before capture and replenished on a
later frame. No used-image or room-state recycling; cold fallback unchanged.
Other eighteen overlays match the latest animated-water candidate. Normal runtime
source is untouched. Helpers: `output/first-room-setup-20261015/`. Detailed report:
[FIRST_ROOM_SETUP_PERFORMANCE_2026-10-15.md](FIRST_ROOM_SETUP_PERFORMANCE_2026-10-15.md).

## Verification

3,840 uninstrumented release frames, sixteen exact state/camera/path phase pairs,
both orders. Normal placement 58.281/60.397→54.762/54.974 ms; 4× mixed
76.972/71.503→70.176/71.231 ms. Following sixty frames have no >50 ms frame in
either lane; replacement makes the next frame 25–27 ms. Idle 50.08→50.26 FPS,
essentially unchanged; 0/16 60 FPS gates. Engine texture peak +1.125 MiB, one spare.
83 native ownership/burst checks and thirty actual-release invalidation/live-crew
checks pass. Twelve cross-process station image pairs, twelve repeat pairs and
five first-placement-frame pairs exact; same live-to-ready capture transition.
Independent review found no actionable issue. Twenty-one owner guards preserve
all 2,948 files. No task-owned game remains after checks.

## Next action

Keep the private candidate available for subsequent performance work; do not
install its LOD implementation into normal source without separate acceptance.
Next useful target is remaining placement/topology/navigation work or atlas upload
bursts. No further unchanged benchmark is needed. Packaged Windows/Mac release
certification and broader private LOD appearance/endurance remain separate work.
