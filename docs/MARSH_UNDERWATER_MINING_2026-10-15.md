# Marsh underwater mining handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: four-facing mining and full trips

## Objective and acceptance

Owner requested distinct underwater mining animations in all four directions and
a full mining-trip test, after diagnosis showed mining reused salvage motion.
Implemented and tested; [review](../character/marsh-underwater-mining-v1/review/index.html)
is ready for owner visual acceptance. No export, commit or upload.

## Accepted decisions and constraints

Use complete independently authored Marsh bodies, existing ivory/sage material,
anatomical-right temple hardware, graphite gloves, ivory boot tops and 148-pixel
standing ruler. Preserve accepted swimming, salvage, cargo and rest decisions.
Existing work positions, extraction/service duration, mineral rewards, navigation
and save format remain unchanged. No helmet or oxygen requirement for Marsh.

## Current state

- `character/marsh-underwater-mining-v1/manifest.json` is last in the catalog.
  Adds `water-mine-draw`, `water-mine` and `water-mine-stow` in four directions:
  12 states / 52 holds. Selected library now 256 states / 1,326 holds.
  Draw starts at exact accepted tread; draw/work/stow share the same braced pose;
  stow ends at exact tread used by existing pickup. All 244 prior states and
  1,274 holds remain unchanged, including paths, clocks and metadata.
- `sources/` retains reference guides, raw generated sheets and exact prompts.
  Four directional sheets selected; north01 rejected for arms/drill drawn across
  the back. North02 uses coherent forward-facing arms, mostly occluded by the
  rear-view torso. East hardware is visible; west near-side temple stays clean.
  28 complete new body keys; neutral cell0 calibrates scale and is unselected.
- `tools/build_marsh_underwater_mining.py`: fixed neutral-derived scale per
  direction, whole-pose registration to tread, alpha island/fringe cleanup and
  fixed 224×208 exports at pivot (112,172). No part grafts, mirroring or per-pose
  height normalization. Wired into `tools/rebuild_marsh_art.py` after water actions.
- `scripts/marsh_water_actions.gd` checks expedition kind during the existing
  work phase (internally still named `salvage`). Mining uses 400 ms accepted
  braking, 600 ms draw, six pressure/recoil cycles over 3.88 seconds, then 600 ms
  stowing. The existing 5.48-second service remains authoritative. Salvage stays
  on its original water-work branch; loaded return/drain/unload are retained.
- New checks: `tests/test_marsh_underwater_mining.py`,
  `tests/test_marsh_mining_clock.gd` and paired UID, plus crew test-group entry.
  Baseline `tests/crew-art-baseline.json` rebaked and narrowly audited.
- `tools/review_marsh_water_actions.gd` now accepts a fixture expedition kind,
  checks that kind's exact rewards and mining tool-hold coverage, while retaining
  its default salvage behavior. `tools/review_marsh_mining.gd` and paired UID run
  four actual mineral journeys. North uses the established fixture obstacle to
  force a northward final route leg; no actor-facing override.
- `tools/publish_marsh_mining_review.py` produces four correctly retimed source
  chains and four sampled native trip witnesses. Native samples are held 200 ms
  for inspection and explicitly do not reproduce continuous real-time cadence.

## Verification

Evidence/logs: `output/marsh-mining-2026-10-15/`.

- Mining clock test first fails on all 12 new directional selections, then passes
  5,284 checks / zero after implementation. Saved work time selects draw, drill
  and stow deterministically; ordinary salvage and death precedence checked.
- Native full trip matrix: 21,808 checks / zero failures or script errors; four
  complete mining dispatches observe east/south/west/north work respectively.
  All 12 phases, all four draw/five drilling/four stow holds, six pickup holds,
  five loaded drainage holds and four unload holds reached. Exactly one deposit
  load consumed and two metal credited per completed delivery, with no early
  credit or data reward. Marsh completes with zero oxygen and normal rule flags.
  Sixteen actual mid-lift/work/loaded-return/drain disk restores across four trips;
  pause and airlock power-loss clock/source checks retained. 164 native crops
  with paired selected-source PNGs.
- Existing salvage/water clock regression: 6,256 checks / zero. Crew complete
  packs: 4,916 checks / zero. Two Python contract tests pass: all accepted source
  hashes/selection metadata and exact tool/tread/pickup handoffs.
- Native mining crop in each facing and all four packaged boards inspected.
  New source and sampled native WebPs decode; local image links resolve; preview
  JavaScript passes Node syntax checking. Browser interaction not automated.
- Package rebuild byte-exact. Loaded baseline: 4 actors / 2,030 clips / 19,740
  frames; exactly 12 added Marsh clips, every prior loaded frame and other actor
  unchanged against immediate pre-pass freeze. Raster outputs retain LFS rules.
- Every Godot invocation uses scratch APPDATA. All 2,948 fingerprinted non-log
  owner files unchanged; pre-existing editor left running.

## Next action

Owner reviews the mining animation page. No further correction found in this
bounded pass. Full-trip evidence uses production dispatch, pathfinding, actor and
save paths on prescribed station/deposit fixtures. Existing outside-deposit work
positions are retained; this does not establish drill-tip contact with individual
painted nodules, every recall/hazard interruption, owner layout or exported build.
