# Connected rock blockers

Implemented: one generated basalt material with room-cell obstacle geometry,
connected shelves, excavation, saved progress and paid build-over.

Each blocker occupies the same 1×1 grid footprint as a standard room. New runs
seed fifteen rocks in four connected formations around the initial station,
alongside the four wrecked rooms. The core's four immediate neighbors remain open.
Old checkpoints keep their recorded field; loading never adds new blockers.

Select a rock and choose **Break & Clear Rock**. A cardinally adjacent station
room provides access. Rocks and wrecks share the single basic salvage rig and
18-second clearance duration. Work supports individual pause/resume and game
pause, and survives Continue. Rocks yield no metal. Normal construction costs
apply after removal; neighboring rock cells remain blocked.

## Art and connection contract

- `basalt-surface-v1.png` is the original built-in image_gen result, unmodified.
  Although requested opaque, it returned partial alpha throughout. An opaque
  stone-colored polygon behind the material prevents scenery showing through.
- `generation-record.json` preserves the exact prompt and processing declaration.
- `manifest.json` records actual dimensions, alpha and SHA-256.
- `rock_view.gd` maps the material continuously in world coordinates across
  connected cells. Four-cell mirrored spans share identical edge texels; the
  source itself is not claimed to be perfectly tileable. Large fields can show
  mirrored repetition.
- All sixteen cardinal neighbor combinations are supported. Internal edges have
  no cliff strips or inset gaps. Only exposed sides get irregular rims and dark
  relief. Diagonal-only neighbors remain separate.
- Removing a cell recomputes its neighbors' exposed boundaries immediately.
  Rock texture coordinates stay fixed, so the surviving formation does not slide.
- Excavation adds fractures and moving silt/cutting effects; the cell remains
  visibly solid and blocked until completion. This is procedural feedback, not a
  physically simulated rock destruction system.
- Gameplay reuses the existing `wrecks` checkpoint field with `kind: basalt`,
  preserving the small clearance system rather than adding a second scheduler.
  Operational room graphs do not include these obstacles.

The existing raw-image export bridge covers `assets/environment`. PNGs use Git
LFS. A packaged release export was not tested in this pass.

## Verification

`tests/test_rock_clearance.gd` passes all sixteen connections and exact shared
edge geometry, cell bounds, new-run layout, blocking/reach, inspector actions,
global/job pause, mutual exclusion with wreck work, disk save/restore, neighbor
exposure, no rock metal payout, and normal paid construction over cleared rock.
The existing wreck clearance and save suites plus synergy, discovery, gameplay
polish and run balance suites pass with no script errors.

`tests/playtest_rock_blockers.gd` captures isolated rocks, a nine-cell mass and an
L shelf beside normal rooms at verified 1280×720, 1600×900 and 2560×1440 sizes.
It checks working/pause pixels and paid construction in an excavated notch.
The fixture isolates settings as well as saves so player fullscreen preferences
cannot change capture sizes. Evidence is in `output/rock-blockers-v1/` and
`output/rock-native.log`; use `index.html` to review it locally.

The native review covers connected surfaces, newly exposed inner edges and
room-scale readability. Density, timing and placement are prototype values that
still need human run-pacing feedback. No procedural map generation is added.
