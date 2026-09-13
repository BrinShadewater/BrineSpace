# Project handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: Existing Bill at 2x source density

## Objective and acceptance

Owner approved rebaking Bill's original higher-resolution sheets at 148px standing
height, retaining his artwork and colours and comparing at the existing world size.
The earlier material simplification was explicitly rejected as muddy and lacking
detail. This experiment isolates density; no redesign or animation repair is mixed in.

## Accepted decisions and constraints

Use the original source sheets and exact shipped 64-colour palette. Keep existing
poses, phase ordering, timing, loop flags, stride metadata, crouching proportions,
and shared endpoints. New pack: 184x184 canvas, pivot (92,172), standingHeight 148.
World calibration remains 65.28 units, giving 2.267 source pixels per world unit.
No enlargement of the finished 74px frames, generation service, new palette fit,
or production asset replacement.

The old `/74` rendering constant assumed 74px standing height; it did not itself
downsample art. The per-pack metadata permits denser art without doubling world size.

## Current state

Latest continuation: **motion-v4**, described below. Density-v3 remains the isolated
density comparison and is preserved unchanged.

Preview output: `output/local-sprite-repair-2026-09-12/density-v3/`.
Reproducible builder: `output/local-sprite-repair-2026-09-12/build_density_trial.py`.
It imports the original builder's extraction helpers without invoking its writing
entry point, doubles canvas/pivot and each pose family's extraction target, and
quantizes directly to the shipped palette. The original 2-pixel island threshold
becomes 8 pixels to preserve its world-area meaning; one dense island pixel removed.

Delivered: 17 states / 102 individual PNGs, 17 strips, spritesheet, manifest,
source hashes and original metadata in provenance, checks, full contact sheet and
four review crops. Comparison GIFs cover idle-east, walk-east, walk-south, run-east,
and interact-east. `density-comparison.png` is a static room-scale comparison.

`native_review.gd` loads both packs through the real CrewSpritePlayer and draws
using crew_standing_height and crew_pivot in a native Godot fixture.
`native-frame-0.png`, `native-frame-2.png`, and `native-frame-4.png` show the active
Research Lab bank and both versions at normal, close, and fit scales. These are
native fixture captures, not captures of production gameplay/occlusion/lighting.

No production character art, bindings, gameplay scripts, or existing engine changes
were edited. The current checkout also contains concurrent room/fire work; it was
left untouched. No commit, export, or upload.

## Verification

- Baseline extraction at 74px reproduces all 102 shipped frames pixel-for-pixel.
- All input hashes unchanged; all 102 dense frames are 184x184 with binary alpha,
  no border clipping, and only colours from the original 64-colour palette.
- All 17 timings, loop flags and counts preserved; kneel/idle/repair shared
  endpoints and reversed stand chain pass. Every output differs from a nearest
  2x enlargement of its corresponding shipped frame.
- Maximum per-frame bounding-box difference after world scaling: 0.883 world
  units (rounding), with identical declared standing-height calibration.
- Generic sprite manifest validator: no errors or warnings.
- `python tools/run_tests.py --only test_crew_standing_height`: PASS.
- Native Godot 4.6.1 loader/render fixture: exit 0, 17 states / 102 frames,
  all dense sizes/heights/pivots verified, three captures saved; clean log at
  `density-v3/native-review.log`.
- Agent inspected all 102 dense poses and the native comparison. Face, harness,
  patch and boots retain substantially more detail at close zoom without the
  rejected muddy colour reduction. Existing pose drift/stride defects remain.

## Motion continuation — V4

Owner requested continuing after the density comparison. The next isolated pass is
`output/local-sprite-repair-2026-09-12/motion-v4/`, built by
`build_motion_trial.py` in the parent folder. It retains the 148px density and all
original colours; no rejected material treatment or generation service is used.

49 frames changed across ten clips, within a complete 17-state/102-frame preview:

- Four idles reuse their own first dense pose, with a one-pixel upper-body breath
  and fixed lower body. Original height variation was 6px south, 8px north, 9px
  east, 3px west; all become 1px. First frames stay unchanged for action endpoints.
- Five walk clips reuse their own first head/collar band while preserving source
  vertical bob. Torso/arm/leg pixels below that band, phase order, and timing stay
  identical. This stabilizes identity; it is not an opposite-step repair.
- Interact-east aligns its upper body to idle, reuses the idle head and legs, and
  retains the authored reaching arm. The leg replacement starts below the glove;
  first/last frames remain identical to idle.
- Four runs plus kneel, repair and stand are pixel-identical to density-v3.

Each changed clip has a paired contact sheet and an original/repaired comparison
GIF. `run_native_review.py` constructs/runs a separate native fixture. It loads
all 102 frames, verifies density/pivot metadata, checks all 102 timed selections
through `frame_at_elapsed`, and saves three native captures. Exit 0; clean log at
`motion-v4/native-review.log`. Pixel checks and the generic manifest validator pass:
unchanged source hashes, original palette only, fixed idle/interaction legs,
unchanged walk pixels below the head band, preserved timing/loops/endpoints,
unaffected clips identical, binary alpha and no border clipping. Agent inspected
all ten paired pose sheets, the interaction close-up, and a native comparison.
Continuous motion/owner acceptance remains separate from these checks.

Source walk audit: `density-v3/walk-source-audit.png` compares original and cleanup
east/west sheets at dense scale. Several side-view phases repeat the same leading
leg rather than providing a clear opposite step. Reordering alone is not a sound
fix. A proper local limb/pose repair remains to be developed; no new gait is claimed.

## Superseding integration

Owner subsequently authorized replacing the complete library. See
[full replacement](BILL_FULL_REPLACEMENT_2026-09-12.md) for the selected dense
revision, complete equipment/action coverage and current validation. The trial-only
status above describes the earlier review milestone.

## Earlier next action

Review the V4 animation comparisons, especially head/collar seams and the stationary
interaction legs. The substantive animation gap is now a believable alternating
side-view stride, requiring more than frame reordering. If a pack is selected for
integration, use a new revision and verify full-game rendering and separate legacy
equipment/extended-action compatibility. Production art and bindings remain unchanged.
