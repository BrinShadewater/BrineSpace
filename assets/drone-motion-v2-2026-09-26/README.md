# Drone motion review v2

Continuation of the owner-endorsed muted-cyan pilot. Review assets, not installed
gameplay. The original accepted-v10 bundle and earlier pilot remain preserved.

## Review

Latest addition: choose **Complete job**, an action and a cardinal heading, then
**Replay job**. Mining/welding/repair reach their work contact and stow afterward.
Collection approaches, grips, lifts, carries, lowers, releases and backs away.
Completed jobs keep hovering; deposited ore stays put until explicit replay.
The original work loops remain selectable. See `review/collection-jobs.gif`,
`review/collection-storyboard.png`, and `review/job-transitions.png`.

- `index.html`: interactive patrol, arrow-key movement including diagonals, four work modes, pause/slow playback and independent status-light selection.
- `review/propeller-revision.gif`: enlarged and game-size idle/travel comparison.
- `review/eight-directions.gif`: all eight independently authored travel headings.
- `review/cardinal-work.gif`: all 16 mining, collection, welding and repair contact loops in N/E/S/W.
- `review/size-pass.png`: eight-heading proportions and same-scale travel/action comparisons; findings in `review/SIZE_PASS.md`.
- `review/direction-registration.png`: hub markers for auditing the rotor rig; red dots are diagnostic marks, not exported vehicle lights.

Serve this folder locally: `python -m http.server 8767 --bind 127.0.0.1 --directory "C:/Users/Alex/Documents/Brine Space/assets/drone-motion-v2-2026-09-26"`.
Open `http://127.0.0.1:8767/`. A local review server was left running for this delivery.

## Delivered coverage

| Asset | Coverage |
|---|---|
| Idle and moving propellers | N, NE, E, SE, S, SW, W, NW; 51 frames per loop at 30 fps |
| Mining | N/E/S/W boring-tool movement and separate sediment particles |
| Collection | N/E/S/W gripper activity with held ore |
| Welding | N/E/S/W plate/tool motion and a localized separate arc/bubble layer |
| Repair | N/E/S/W bracket/fastener operation, distinct from welding |
| Work-loop timing | 102 frames at 30 fps per action; local articulation around an authored contact pose |
| Top light | Independent blue operational, red stopped, yellow charging/out-of-power layers; .85-second brightness pulse |

Status colors are previewed independently; selecting a lamp color is not a
simulation of fleet battery/stop behavior. Layer metadata is in `manifest.json`.
With the job supplement: 6084 body frames, 5268 operation-effect frames, 3636 cargo
layer frames, 153 status frames, and 99 atlases. There are 32 original loop clips
and 16 complete jobs. Empty effect/cargo frames are included in these counts.
Do not count those frames as independently generated poses.

## Changes from the first pilot

Propeller centers were offset in the first pilot. Corrected projected axes now
rotate an annular blade region while keeping the intake, casing and axle
highlight stationary. Five shutter samples soften travel-speed rotation.
Top emission dims toward dark blue instead of revealing a white lamp source.
The light clock remains independent of work frames, including held poses.

Eight headings were drawn independently. The first cardinal sheet swapped tool
sides; the partial correction added an extra north-facing arm. Those sources are
retained as rejected evidence. Only the corrected east/west cells are selected.
North, north-east and south-west were authored separately; south-east/north-west
use their reviewed cells. The owner identified the missing north-west work arm;
`northwest-arm-v2.png` restored a clearly visible connected arm and nozzle.
The earlier claim that this was acceptable occlusion was incorrect.
No heading was mirrored to manufacture the opposite side.

The initial arm repair rebuilt only north-west idle/movement (102 frames, two atlases).
All 1683 other body/effect/status frames were hash-checked unchanged. Both arms
are visible in all eight reviewed headings. Rotor centers were adjusted to the
repaired source. For a narrow rebuild use `python assets/drone-motion-v2-2026-09-26/rebuild_heading.py northwest`, followed by `build_direction_review.py` and `validate_pack.py`.

Latest owner follow-up: north-west arm must curve farther right; check limb/propeller
proportions and extend all actions to N/E/S/W. Selected `northwest-curve-v4.png`
has the inward/right bend and slimmer nozzle. Three independently generated work
sheets add the other cardinal facings. Fixed chassis registration and per-heading
scales keep action sizes consistent. No mirrored facings. All 16 combinations are
selectable in the preview; changing heading preserves the current work action.

## Scope and limits

The owner's singular-drone request was used to make all four visual work studies
on this drone. Existing Mining/Salvage/Construction gameplay roles are unchanged;
the optional role-allocation question has not been answered.

Work loops and complete jobs cover North, East, South and West. Jobs start in a
job-ready pose; travel-to-job-ready blending and runtime targeting remain pending.
Mining expects a world deposit
at its tool contact; the sprite does not include a large ore deposit. Collection
has both the earlier held-ore loop and a complete pickup/carry/deposit supplement.
The ore transfer and root trajectory are explicit metadata; the preview does not
modify game inventory. Welding and repair retain their demonstration workpieces.

Export mapping remains .34 world units per library pixel; the 69.12-unit south
hull width is provisional. Source scale recipes are recorded per view, with
chassis registration rather than per-frame bounding-box centering. Some material
and projected-size variation remains across newly authored headings. These are
review candidates, not newly accepted bible references. No room, save, gameplay,
pathfinding, docking or release integration was performed in this revision.

## Rebuild and checks

### Fixed-surface polish

The current manifest points to `polish/frames/` and `polish/atlases/` for body
art. Imagegen-authored matte panel/casing surfaces are registered to eight
headings and sixteen work poses. Only pixels stationary throughout each paired
travel or work/job sequence receive the composite. Original alpha, moving arms,
blades, cargo, effects, pulse and timing are preserved. East/west depth received
a shading refinement within the existing geometry, not a new camera projection.
Original frames and atlases remain available through
`polish/manifest-before-polish.json`; do not overwrite them with polished art.
The generated material source is `polish/heading-polish-v2.png`; v1 was rejected
for excessive gloss. See `polish/HANDOFF.md` and the comparison board.

Run in this order:

1. `python assets/drone-motion-v2-2026-09-26/build_rotor_review.py`
2. `python assets/drone-motion-v2-2026-09-26/build_motion_pack.py`
3. `python assets/drone-motion-v2-2026-09-26/build_work_loops.py`
4. `python assets/drone-motion-v2-2026-09-26/build_cardinal_work.py`
5. `python assets/drone-motion-v2-2026-09-26/build_job_sequences.py`
6. `python assets/drone-motion-v2-2026-09-26/pack_atlases.py`
   Then run `build_surface_polish.py` and `apply_surface_polish.py` from this
   same pack directory before building review boards. The latter packs the
   changed body atlases and switches the manifest atomically. Re-running it
   reads the preserved baseline, so polish never accumulates. A fresh unpolished
   manifest from steps 1–6 refreshes that baseline.
   Run `build_polish_review.py` afterward for the final masked comparison; the
   intermediate comparison from `build_surface_polish.py` precedes detail protection.
7. `python assets/drone-motion-v2-2026-09-26/build_direction_review.py`
8. `python assets/drone-motion-v2-2026-09-26/build_cardinal_review.py`
9. `python assets/drone-motion-v2-2026-09-26/build_job_review.py`
10. `python assets/drone-motion-v2-2026-09-26/validate_pack.py`
11. `python assets/drone-motion-v2-2026-09-26/validate_jobs.py`

Image generation is preserved in `sources/` and `polish/` with exact prompts. Rebuilds use
local sources only. `review/pack-validation.json` records geometry, atlas parity,
source hashes and actual light-brightness checks. The generic sprite validator
report is `review/manifest-validation.json` (earlier 20-clip revision only). Current
48-clip coverage is checked by `validate_pack.py`. Housing/hub invariance is checked
while generating propeller frames. Visual evidence is separate from these checks.
