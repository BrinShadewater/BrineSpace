# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: distant-room raster prototype

## Objective and acceptance

Owner approved prototyping distant-zoom room images on a few expensive rooms,
with crew, doors and warnings live, then measuring the benefit. This is a private
feasibility experiment, not an installed rendering change or release acceptance.
Small machinery animations may freeze at distant zoom; close views retain full detail.

## Accepted decisions and constraints

Hydroponics Farm, Storage Depot and Tidal Power Plant only; Moonbay unchanged.
Use original authored artwork and current owner's Studio layouts. Two transparent
512-square cached render targets per eligible room: base and furnishings, with
station doors drawn live between them. The door loop keeps original rotations,
threshold colours and opening fractions. Fixed central equipment is disjoint from
the perimeter door bands; furniture remains after doors, as in the original path.
Crew, drones, selection, warning/hazard overlays, lighting and simulation remain
outside the raster cache. Machinery screens/effects and the stable Tidal rotor freeze.

Enter at zoom <=0.24; return to full detail above 0.28, with hysteresis. Cache
images cover a canonical 768-square floor plus 128-unit padding on every side.
Dry rooms only; intermediate tidal chamber fill/drain, special props, excessive
painted bounds and explicit slot tint use the original renderer. No gameplay,
asset, save-format, default quality-setting or monolith refactor changes.

## Current state

**Normal source and the Windows candidate are unchanged by this task.** Prototype
drivers/fragments: `output/room-lod-20261014/`. Private derived source, overlay packs,
logs, images and JSON: `C:/bs-room-lod-20261014/`. No commit or publication.

The baseline is a physical copy of Windows build `brinespace-2fb8e8659a3be093`,
plus the previously accepted companion topology cleanup in both comparison lanes.
Frozen GridCanvas, RoomContentCanvas, LargeRoomCanvas and common large-room drawing
match the wall-batched delivery bytes. Candidate differs only in private copies of
LargeRoomCanvas and large-room Common. Normal companion source is frozen unchanged.
Actual release mode (`debug=false`), source/companion-instance hash checks, muted
secondary display, input disabled, fixed window size and minimize/resize rejection.
GPU work serial; every job has scratch APPDATA, resolved directory and owner guards.

The reuse key takes complete appearance minus the equipment clock, station-door
fractions and Tidal rotor angle, plus layout revision, operating state and Reduced
Motion. Shared prop-array identity also invalidates capture, including replacement
without a revision change. Painted registration geometry and flips, with a generous
gutter, drive extreme-placement fallback. Fit checks reuse immutable prop identities.
The private BugReport mount proxy preserves the earlier verified early-load guard.

## Verification

### Matched native timing

Godot 4.7.2 Compatibility, RTX 4070 Ti, 1920x1080; maintained 40-room mixed-large
fixture, four large rooms, active crew/drones, fitted zoom ~0.130814. Each pair
covers idle, pan, zoom and lighting at 1x/2x/4x, 180 frames per phase.

| Comparison | Reference mean | Prototype mean | Reduction | Better p95 phases |
| --- | ---: | ---: | ---: | ---: |
| Reference then prototype | 27.529 ms | 26.309 ms | 4.43% | 10/12 |
| Prototype then reference | 28.589 ms | 26.217 ms | 8.30% | 11/12 |

8,640 measured frames; all 24 full simulation-state/camera pairs match. Timings
vary, notably the second reference's 2x zoom/lighting phases: do not treat 8.30%
as a guaranteed gain. Idle 1x independently improves in both pairs:
24.876 -> 23.369 ms (40.2 -> 42.8 FPS), 24.422 -> 23.155 ms (40.9 -> 43.2 FPS).
Still **0/24 prototype phases pass** the maintained 60 FPS phase gate.

Mean draw calls fall ~2,866 -> 2,670 (~196 / 6.8%). Idle render CPU falls
6.60 -> 6.05 ms and 6.51 -> 6.02 ms; idle live-room callbacks fall
6.21 -> 5.47 ms and 6.11 -> 5.43 ms. These nested/overlapping scopes must not
be added. Worst frames: 75.744 -> 65.986 ms and 83.601 -> 65.444 ms.
P95 improves 21/24 phases, so this is not a universal pacing improvement.

Reported end texture memory rises exactly 12 MiB in each pair (2430.640 ->
2442.640 MiB). Most paired phase deltas are also +12 MiB; one pan phase crosses
an existing texture-cache eviction boundary, so its delta differs. Cache creation
occurs during warmup: these measurements do not establish cold-entry hitch cost.
Evidence: `analysis.json`, `pilot-{reference,candidate}.json`,
`reverse-{candidate,reference}.json`, paired identity/owner files and trace logs.

### Appearance and behavior

Initial native frozen comparisons at fitted/0.24 zoom show expected raster sampling
and held machinery-frame differences; adjacent reference repeats and prototype
repeats are exact. At zoom 0.30 and 0.50, full-renderer fallback is pixel-exact
against reference in both directions. All frozen state snapshots match. Fitted and
0.24 station images plus a Storage crop were visually reviewed: recognizable artwork,
no obvious missing room content or perimeter clipping in the tested layout.
This is distant-view review, not a claim of pixel identity at distant zoom.

Final native contract passes **58 checks / zero failures**: live door opening changes
rendered pixels without room recapture (with an exact frozen repeat before opening),
clock reuse, operating/layout/cache-identity invalidation, immutable source dictionaries,
offline shade, wet/tidal-fill fallback, distant/close hysteresis, explicit tint fallback
and an extreme painted extent. Layout revision is restored after the scratch probe.
The repeated final image probe confirms the same distant sampling differences and
pixel-exact close fallback; all frozen state snapshots match. See `verified-visual.json`.
The final fitted screenshot was reviewed too.

The first smoke exposed an offscreen viewport transform set before attaching its
canvas; corrected by setting it after tree attachment. That errored smoke is
excluded. Subsequent smoke, visual and timing runs contain no engine/script errors.
Independent read-only review led to prop-identity invalidation and painted-bounds
fallback before the measured packs were frozen.

All 11 saved owner guards preserve 2,948 files. `final-audit.json` records unchanged
normal runtime source hashes and identical candidate pack hashes across the timed
and final visual runs. Accepted logs contain no engine/script errors. No game/QA
process from this task remains running; scoped documentation whitespace check passes.

## Next action

The prototype and its checks are complete. The measured reduction warrants
considering a wider, carefully selected room set;
it does not imply proportional scaling or enough savings for 60 FPS. Do not install
the spike unchanged: production work must establish cold cache-entry/threshold hitch
cost, all rotations and wall/filter modes, continuous transitions, arbitrary Studio
prop/effect extents, inherited ancestor tint/material behavior, texture lifetime and
owner visual acceptance. The 64-unit effect gutter is conservative for this fixture,
not proof for arbitrary effects/scales. Ordinary rooms interleave crew and props by
depth; extending this approach must preserve that order rather than placing every
cached prop behind a live actor. No target-PC, Mac, endurance, save/relaunch,
placement/demolition or complete release-workload acceptance in this prototype.
