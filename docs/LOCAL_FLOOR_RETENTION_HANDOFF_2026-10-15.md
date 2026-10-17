# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: local floor repaint

## Objective and acceptance

Owner approved localizing floor/content repaint after placement and removal,
preserving appearance, layering and live actors. Installed a conservative floor
prototype for its repeatable structural-change saving. Average FPS and smooth
60 FPS pacing remain open; no steady-state FPS gain is claimed.

## Accepted decisions and constraints

Preserve connectors, legacy drawing, the two floor-pass groups and room order.
Active lighting fades retain the original full-pass path so pools remain above
all floors in their pass. Special, wet and actor-bearing rooms keep conservative
repaint rules. Crew, doors, warnings, clocks and existing content retention stay
live. No art, gameplay, owner-layout or delivery changes. Private raster LOD stays
private. Native jobs serial, silent secondary display, isolated APPDATA with
copied layouts and real-profile fingerprints. No export/commit/publication.

## Current state

- `scripts/grid_canvas.gd`: identity containers before fade children retain one
  slot per layered floor in the original order. Local dependency changes repaint
  their slots; group migration reorders/reparents them, and removed rooms release
  them. Original full drawing remains available with `--combined-floor-slots`.
  Active fades hide these roots and use the original painting/cleanup. No changed
  drawing commands, filtering, geometry or raster capture.
- `scripts/retained_floor_context.gd` + UID: small specialization of the existing
  wall dependency projection, retaining interior-light dependency. It snapshots
  local structure/power plus room floor state and global layout/render inputs.
- `tests/test_local_floor_context.gd`, `tests/test_local_floor_retention.gd` + UIDs,
  and `tests/index.json`: metadata invalidation and native lifecycle/pixel coverage.
  Existing Grid UID retained. Normal content code is unchanged; localization avoids
  preparing unrelated floor views, while contents keep their existing retention.

Evidence: `C:/bs-local-floor-20261015/`; drivers:
`output/local-floor-20261015/`. Final comparison: **compare1**.
Installed Grid SHA256:
`db7d7635d10be17d510e360cc840a7ede5fcf6bc75778868f7bf2ac91fe61d8a`.
Installed floor context SHA256:
`f021ecd1641109ceb8988a155c306b78cfc1afdf2ff01798b848851812c4e3f6`.
The helper block and replaced floor branch match the measured private candidate;
private LOD differences are excluded from normal integration (`production-source.json`).
Reference overlay SHA256:
`e03f30776063b43fbb604ccbf5bc52a781dec607152db1ac16d00fb0dad6c5b4`.
Candidate overlay SHA256:
`5604dca1faceb55d0c9fe6d914223075600148dca1b96a0ae84d7eedb4913bd9`.
Both lanes contain the accepted navigation/companion/water/Grid changes and the
same private LOD. Windows delivery is unchanged.

## Verification

Actual debug=false runtime passes **72 adjacent exact image comparisons** at
fitted/.25/.5 zoom, including repeat controls and both directions. Six frozen
scenarios: baseline, real placement, rotation, removal, mid-fade and settled light.
All captured gameplay snapshots match. Mid-fade uses no local floor draws;
unchanged repeat captures redraw only two conservative rooms instead of 36–37.
Representative placement image visually reviewed. See `parity2.json` and PNGs.

Installed normal-source checks pass, logs clean:

- `20261015-013203-headless`: local floor context 164 checks; wall context 8,006;
  structural plan 7,294. Local/nonlocal dependencies, nested snapshot ownership,
  interior light, bake state, layout revision and removed metadata are covered.
- `20261015-013229-native`: live-surface/zoom retention, 231 wall-slot checks and
  440 solar rotation/layout/cache checks pass.
- `20261015-013418-native`: new floor fixture passes 23 checks, including exact
  original pixels, four rotations, placement, split migration/removal, fades and
  first-frame creation. Placement repaints five of 26 floors in this fixture.

The new native fixture initially needed an explicit native-lane override because
its headless guard fooled auto-classification. That skipped invocation is not
counted as a pass. Independent final source-only review finds no actionable issue.

Actual release comparison: **6,720 measured frames / 28 exact gameplay-camera
phase pairs**, seven actions at 1x/4x, both orders. Source/overlay identity guards
pass. Process snapshots detect no foreign Godot worker or duplicate game.

| Placement frame | Reference | Candidate |
|---|---:|---:|
| Forward, 1x |72.894 ms|68.002 ms|
| Forward, 4x |79.428 ms|67.108 ms|
| Reverse, 1x |70.816 ms|67.033 ms|
| Reverse, 4x |72.981 ms|67.856 ms|

Removal frames fall from 75.386–78.860 ms to 67.251–71.662 ms. Placement/removal
repaints **6–8 floors instead of 36–37**. Forward floor callbacks total about
11–12 -> 5 ms; whole drawing falls about 30–36 -> 23–28 ms across these events.
The floor total adds parent floor callbacks and separate child callbacks, not
nested per-room detail timers. Live-room drawing itself remains substantial.

Whole-workload means: 22.311 -> 22.196 ms forward, 22.120 -> 22.203 ms reverse.
P95 improves 8/14 and 7/14 phases; >50-ms frames 15->12 and 12->13. Worst frames
79.428->71.662 and 76.118->71.520 ms. **All 28 candidate 60 FPS phase gates fail.**
The repeatable admission is shorter structural-change drawing/hitches, not a
general FPS or pacing claim. Texture peaks remain identical at 2784.653 MiB.
New storage is bounded scene-owned nodes/command lists and dependency metadata;
process RAM cost was not established. Both floor passes still independently
prepare their metadata projection on global invalidation.

All 16 completed owner guards preserve 2,948 files. Exploratory exclusions: the
expected missing-API RED; an editor pack-mount probe that stalled and was stopped;
and a parity fixture that passed baseline images but searched for placement at
its final close zoom. The corrected parity2 resets to fitted zoom before placement.
No excluded timing is merged with compare1. No task-owned QA process remains.

## Next action

The approved prototype, normal integration and validation are complete. Placement
still takes roughly 67–68 ms in this workload. Remaining structural work includes
navigation, live-room/door preparation and other retained-layer rebuilds. Profile
those together before introducing more retention. Actual current-source Windows/
Mac, endurance, save/relaunch and 60 FPS release acceptance remain open.
