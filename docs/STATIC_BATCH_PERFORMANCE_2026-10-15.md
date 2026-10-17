# Static prop and structural batching — October 15, 2026

Two ordered structural merges reduce steady large-station draw calls by about
**40 / 1.9%**, preserving exact pixels. Timing remains mixed, so **keep the
candidate private**. Normal game sources, UIDs, gameplay and exports are unchanged.

| Pooled phase | Reference FPS | Candidate FPS | Reference p95 | Candidate p95 |
|---|---:|---:|---:|---:|
| Normal idle | 55.25 | 53.81 | 19.690 ms | 25.996 ms |
| Normal placement | 54.31 | 54.64 | 20.325 ms | 22.699 ms |
| 4× idle | 48.97 | 49.50 | 34.806 ms | 34.763 ms |
| 4× placement | 46.23 | 46.59 | 35.871 ms | 31.774 ms |

4× placement action frames worsen slightly in both orders: **55.606→55.907 ms**
and **56.498→56.719 ms**. Following windows are mixed. **0/8** candidate phases
meet mean and p95 ≤16.667 ms. These are comparisons against the selected private
water V2/stable-ID V3/LOD cohort, excluding the neutral waveform trial, not against
the installed game or an earlier study's different process timings.

## Inventory and chosen changes

The first inventory covered 34 ordinary content canvases / 301 slots. A second
included the active large-room content canvas: 35 canvases / 311 slots, 20 visible
library bases plus ordinary static props. Culling and distant-room caching hide
many slots. Visible candidate prop runs have different texture RIDs; no useful
same-texture run exists without crossing active screens, special props or crew.
No prop grouping or texture atlas was implemented. That would introduce UV,
sampling, depth and memory work for uncertain benefit in this fixture.

Selected structural changes reuse already accepted packet geometry:

- `painted_shell.gd::north`: the exposed vertical returns and corners share one
  local cap packet, preserving left strip → left corner → right strip → right
  corner. Flush before doors, ocean hatches and probe artwork. Two exposed sides
  become four polygon submissions → one; one side two → one. Existing rectangle
  sampling and the cap-batching fallback remain unchanged.
- `room_lighting.gd::draw_equipment_shadows`: the four-outline border packet is
  prefixed to the cached room-shadow packet. Same points, colors, indices and
  blend order; no primitive conversion. The prefix adds 40 vertices / 96 indices
  and **1,344 bytes** per cached geometry under the existing 128-entry / 8 MiB
  limit. Prefix mode joins the cache key; each palette starts with the exact
  border colors. Arrays are owned copies; prop-only projected counts stay intact.
  Empty props, disabled flags and existing oversampling/size/contact fallbacks
  retain the original path without duplicate submission.

Neither change alters animation clocks, props, crew, navigation, doors or warning
logic. No new nodes, textures, native code or atlas. The floor prefix is Windows
gated; north returns use the existing cap-packet flag and arithmetic. Native visual
acceptance below is Windows only; no Mac acceptance is claimed.

## Submission evidence and FPS scope

| Phase | Reference calls/frame | Candidate calls/frame | Delayed viewport CPU reference→candidate |
|---|---:|---:|---:|
| Normal idle | 2,116.73 | 2,076.74 | 4.815→4.878 ms |
| Normal placement | 2,137.39 | 2,094.42 | 4.859→4.775 ms |
| 4× idle | 2,120.34 | 2,076.28 | 4.916→4.824 ms |
| 4× placement | 2,199.50 | 2,154.60 | 5.029→4.950 ms |

Every paired phase reduces draw calls. Placement includes other changing render
work; do not attribute its entire pooled difference to these two packets.
Viewport CPU/GPU query results are delayed and cannot be aligned to current-frame
script costs or added to them. Draw reduction is proven; broad FPS/pacing acceptance
is not.

Physical loaded source hashes cover both affected scripts. Candidate process
counters record ten north-return packets and 94/95 floor prefixes; reference has
zero new counters. These are **process-lifetime diagnostics**, including startup /
warm-up, not per-phase counts. Floor prefix count does not reset with cache clear.
Both lanes keep identical water totals (1,320 batches / 105,099 packets / zero
rejections) and ten stable-navigation calls.

## Placement pacing

Action = fixture frame 30; subsequent window = frames 31–90, excluding action.

| 4× order | Action reference→candidate | Next frame | Following 60 mean | Following 60 p95 | Following >50 ms |
|---|---:|---:|---:|---:|---:|
| Forward | 55.606→55.907 ms | 23.338→23.012 ms | 21.986→21.571 ms | 32.217→36.619 ms | 2→0 |
| Reverse | 56.498→56.719 ms | 22.611→24.302 ms | 22.264→22.264 ms | 40.548→32.858 ms | 0→1 |

Including action, >50 ms counts are 3→1 forward and 1→2 reverse. Full placement
phase maxima are 57.830→55.907 ms forward and 56.498→57.738 ms reverse. No measured
frame exceeds 100 ms. Mean 4× action 56.052→56.313 ms does not improve.

## Normal-idle burst remains unresolved

Forward normal idle improves 54.48→55.66 FPS; reverse worsens 56.05→52.07.
Frames 71–80 of the reverse candidate average 30.794 ms versus reference 17.432.
Drawing and simulation both slow, across unchanged environment, live-room,
door-validation and surface-validation scopes. Current/sampled drone uploads are
zero there. All valid rows remain in the pooled results; no rerun selected a
preferred sign.

Trace review finds **no changed floor/cap CPU callback** during the burst: all 120
idle frames retain floor count 72, redraw count 13 and no floor/wall callback
stages. All four processes also have identical later floor-rebuild trajectories.
That rules out an observed extra structural invalidation, not downstream rendering
or an external cause. Retained commands still render every frame. Root cause is
unresolved; do not call the regression noise or blame an unobserved process.

## Verification and protection

Godot 4.7.2 `ed1daf0bf`, actual Windows release executable/PCK, Compatibility /
OpenGL, RTX 4070 Ti, 1920×1080; muted visible secondary-display QA. Serial
reference→candidate→candidate→reference, 180 warm frames per process then 120 each
idle/placement at 1×/4×. **1,920 timed frames**, eight exact phase-end simulation /
route state and camera endpoint/path pairs. Existing benchmark observers remain;
no added detailed profiler wrappers. Frame cap and VSync measured off. Process/window
guard has no errors or foreign game process; owner editor PID46624 preserved.

- Correct RED checks observed: north 6→6 calls when three fewer expected;
  border/shadow 2→2 when one fewer expected. A helper CLI parsing mistake occurred
  before Godot and was corrected; it is not acceptance evidence.
- North returns: **768** exact native raster pairs across three wall families,
  four scales/rotations/adjoining-side combinations, two filters and dry/flood
  materials. **192** more cover AI/airlock/probe specials; **12** verify flag-off
  parity. All cases also check the expected submission difference.
- Border/shadow: **128** exact raster cases; 96 save one call, 32 exercise the
  existing scale-oversampling fallback. Empty-prop, floor-border-disabled and
  prefix-disabled lanes add **48** exact cases with no expected call reduction.
- **38 cache checks** cover 128 fades, exact vertex/index/color prefixes, prop-only
  counts, prefix-flag keys, borrowed-array ownership, byte budget, editing,
  eviction and final-owner release. Total focused native raster pairs: **1,148**.
- **Seventeen** cross-process station/first-placement image pairs plus twelve
  repeats exact; three zooms, lighting on/off, first-placement readiness/state.
  Representative zoom-0.5 image inspected.
- Independent read-only review finds no source blocker and confirms the burst has
  no sampled structural repaint. Final audit passes: 24 frozen scripts, only two
  candidate overlays differ. Normal selected sources/UIDs/tests unchanged; all
  **23 owner / ten stable / ten water binary guards** clean. Protected **2,948-file**
  fingerprint equals initial/prior baseline. Earlier profile-incident caveat persists.

Texture counters: start 2,026.62 MB, end 2,044.11 MB forward / 2,046.11 MB reverse
for both lanes; peak 2,776.91 MB. These are not native transient/RSS or long-soak
acceptance. Existing source/DLL hashes remain unchanged. No new native build,
dependency, release/Mac package, commit or upload.

## Evidence and next action

Evidence `C:/bs-static-batch-20261015/`; helpers `output/static-batch-20261015/`.
Authoritative files: `static1-analysis.json`, four timing reports, process guard,
pixel/cache scratch results, image parity, `final-audit.json`. Twenty-three
reference scripts match the preceding selected reference; unchanged current
painted-shell source is explicit file 24. `reference23.pck` preserves prior pack.
Source/installed/native snapshots and runtime identity retain provenance.

The initial 4 GiB copy plan hit the maintained disk guard. Only immutable EXE/PCK
inputs are hard-linked to the preceding frozen runtime, avoiding 3.48 GiB of
duplicate data; descriptors, overlays and profiles stay task-local. New QA writes
reserve 512 MiB and the **20 GiB free-space floor is preserved**. Final identity
and hard-link audit confirms the original inputs stayed unchanged.

Next isolate the normal-idle burst and downstream render timing before admitting
these packets. Keep this candidate independent of private navigation/water/LOD
work. Further prop batching needs a deliberate texture/material or bounded-atlas
design with sampling/depth/memory checks; simple same-texture grouping has no
eligible visible runs in this fixture. Do not repeat that approach without new
inventory evidence.
