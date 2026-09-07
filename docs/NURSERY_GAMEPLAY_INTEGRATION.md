# Nursery integration plan and evidence

## Accepted: one complete rotatable nursery

The single-room objective is complete in the current checkout. This does not
complete the separate broader room-expansion ledger or export the whole game.

| Requirement | Current evidence |
| --- | --- |
| Four rotations without sideways upright props | Four native embedded views and 12 station crops reviewed; positions/footprints rotate, height remains screen-up |
| Modular walls and fixed door openings | 1,540 geometry samples, four crossings, shared-edge owner and mismatch checks in `nursery-final-movement-01.log` |
| Various reusable art assets | Four furniture assemblies; 12 registered textures audited by `tools/audit_nursery_assets.py`; directional microscope, growth, reservoir, cartridges, floor and enamel |
| Character belongs in the room | 16 input-driven prop circuits, 2,192 collision-checked steps, 32 depth captures; 52 depth/route images match reviewed evidence; final whole-scene front/behind images separately reviewed |
| Functioning animation, offline and pause | 32 per-machine comparisons plus actual station motion/freeze checks across three viewport sizes |
| Playable unlocks and synergies | Native `nursery-flow-<width>-04` runs: normal costs/full cycles, discovery, prototype draw, four previews, paid operation and suspension; gameplay regressions cover terminal patterns |
| Station, preview, card and inspector | Actual scene captures at 1280, 1600 and 2560 widths; card equals canonical q0 render |
| Reusable package independent of checkout | `nursery-fixture-01.pck`, 27 explicit files; launched from empty `nursery-package-host-01` directory; `nursery-package-runtime-01.log` clean; all five native images exactly match source-scene outputs |
| Workflow and skill improved | Shared geometry/recipe, registered components, native evidence fixtures, read-only asset auditor, reproducible package smoke; installed/repo pipeline guidance includes directional registration and seam/crop lessons |

Accepted visual tradeoffs: upright growth/reservoir reuse is not a reconstruction
of rear surface wear; microscope contours have small guide-relative drift. These
do not prevent quarter-turn placement, readable upright art or movement. Older
whole-image rooms still differ in style; their full migration is separate work.

Package reproduction: run `tools/package_nursery_fixture.gd` with a new absolute
`--package=...pck`, then launch Godot with `--main-pack ...pck --script
res://tools/test_nursery_embedding.gd -- --capture-dir=...` from an empty directory.
The local pack explicitly retains raw PNG/JSON paths and the geometry helper;
it is not a signed executable, a full-game export preset or permission to publish.
The implementation uses Godot's [PCKPacker](https://docs.godotengine.org/en/4.5/classes/class_pckpacker.html).

Historical checkpoints below explain intermediate failures and superseded gates.

## Final audit checkpoint

The current four room crops at each of 1280, 1600 and 2560 widths have now been
visually inspected (`nursery-station-state-1280-03`, `1600-04`, `2560-03`).
The growth rack, analysis bench, reservoir and filter stay upright with clear
cross-aisles; the microscope and cabinet faces change with quarter-turns.
These cropped checks establish room readability, not a full HUD review.

`python tools/audit_nursery_assets.py` passes all 12 enabled registrations:
decoded native sizes, in-image display bounds, recorded clean hashes, required
component/directional coverage and the card's provenance hash. This read-only
audit is reusable when replacing a prop; it does not certify visual quality.

Upright growth/reservoir reuse is retained as an intentional 2D rendering
approximation. It meets the fixed-camera upright/readable requirement; it does
not claim reconstructed physical rear wear. Exact rear-surface reconstruction
would be a further art improvement, not missing directional microscope coverage.
The refreshed `output/nursery-final-movement-01.log` passes 1,540 geometry
samples, four input-driven crossings, 16 prop circuits / 2,192 movement steps,
eight walking-direction animation checks, 32 per-machine motion comparisons and
pause/offline checks. Of 54 depth/route images, 52 exactly match the previously
reviewed `room-acceptance-1600x900-01` set; the two whole-scene depth images differ
and have now been separately inspected: correct rack front/behind occlusion.
The reusable-room package is verified above; full-game release export is separate.

## Layered station/card integration checkpoint

The station now delegates nursery drawing into its own CanvasItem pass through
the reusable view; nursery textures never enter the old whole-image rotation
branch. Placed rooms and placement previews use the same component. Actual
powered-room state and visual time control its effects. The existing character
frame is inserted into the room's depth queue and excluded from the later global
human pass while its feet belong to a nursery cell.

Cards and inspector use `rooms/modular/nursery-card.png`, a 512px native offline
bake with recorded source/hash. The nursery card uses aspect-contain rather than
cropping its upper/lower machinery. PNG is covered by Git LFS; nothing was staged.

Native fixture `tests/playtest_nursery_art.gd` captures the actual station and
cards. `output/nursery-station-03/` passes its capture run; q0 was visually reviewed
after correcting legacy double-door overlays and the neighbor-floor overdraw of
shared walls. Two-stage modular floor then structure rendering preserves the seam.
Earlier q0/q3 station/card views were also reviewed but predate the floor fix.

Regressions `output/integrated-test_nursery_gameplay-01.log`,
`integrated-test_discovery_progression-01.log`,
`integrated-test_polish_gameplay-01.log`, and `integrated-playtest_polish-01.log`
pass after initial renderer integration, before the final floor-order adjustment.

Latest native state checks pass at 1280x720, 1600x900 and 2560x1440 in
`output/nursery-station-state-<width>-03/`: eight motion comparisons, 404 actual
walker-path samples across four orientations, 28 walking captures and four paused
pairs per run. Earlier `-02` failures came from screenshot crops omitting viewport
stretch; those runs are not valid motion evidence. Corrected crops are saved too.

`output/nursery-station-state-1600-04/` repeats the checks after adding a floor
apron inside connected legacy doorway apertures. Horizontal and vertical Bio Lab
joins and a saved room crop were visually reviewed. Legacy/new art still differs
substantially in palette and density; this is seam compatibility, not pack-wide
style acceptance. Legacy rooms render before modular floors and structures.

Final-state nursery gameplay, discovery progression, gameplay polish and actual
scene playtest regressions pass with clean logs in `output/final-seam-*-02.log`.

`tests/playtest_nursery_progression.gd` now exercises a controlled foundation draft
with normal starting resources, paid foundations, full `_advance_cycle()` calls,
three-cycle discovery, a normal reroll to draw the earned prototype, four preview
rotations (including the blocked west-facing connection), an exact 7 Metal / 3
Biomass nursery purchase, real functioning economy, and inspector suspension/resume.
No resource grants, free-build flag, or disabled failure conditions are used.
Loaded meta is cleared and writes use a dedicated per-viewport fixture save.
The test briefly positions the native pointer for previews and restores it.

Clean native runs: `output/nursery-flow-1280-04.log`,
`output/nursery-flow-1600-04.log`, `output/nursery-flow-2560-04.log`, with matching
capture directories. Earlier progression `-01`/`-02` runs retain failed test
checks: a foundation directive reward affected net cost, and injected events did
not move the Window's queried pointer. No gameplay workaround was applied.
The 1280 blocked preview/stabilized discovery and 1600 valid preview/functioning
room were visually reviewed. Automated passes do not substitute for remaining
viewport/orientation visual reviews and the final room acceptance audit.
The fixture's two room placements are explicit art setup, not evidence of paying
for those screenshots. The paid click path has separate gameplay-test coverage.

This integrates only the approved Mycelium Nursery branch while preserving the
remaining expansion ledger. The existing room database remains authoritative for
gameplay; the modular recipe supplies art placement, not costs or unlock logic.

1. Add the approved locked one-cell Bio/uncommon definition: 7 Metal + 3 Biomass
   build cost; 1 Power + 1 Biomass consumed per functioning cycle; 3 Food produced;
   west/east/south tee; future-run biosphere/recovery decks after unlock.
2. Add its approved hidden unlock and two terminal synergies through the existing
   discovery manager. Preserve three consecutive cycles, reset on inactivity,
   one-time rewards, and current-run prototype injection.
3. Verify paid construction, functioning consumption/production, offline gating,
   rotated port matching, clean-save locking, deck eligibility and disclosure.
   Use dedicated fixture saves; run the existing discovery/gameplay regressions.
4. Integrate the reusable layered view into station and card consumers. Resolve
   shared seams once, supply actual operation/pause time, and integrate crew into
   depth ordering. Never pass this room through whole-bitmap station rotation.
5. Capture actual placement, rotation, functioning/offline, cards and discovery in
   the native game at supported viewports. Keep production acceptance open until
   those integrations and evidence exist. No gameplay balance claim from unit tests.

Implementation and results are recorded below as each step is verified.

## Gameplay data and behavior verified

Added the nursery definition, biosphere/recovery deck eligibility, its approved
Substrate Recovery unlock, and Culture Exchange / Restorative Culture terminal
patterns. The original foundation pool and all existing recipe IDs are unchanged.
No recipe partners or rewards were added to undiscovered card descriptions.

`tests/test_nursery_gameplay.gd` uses the actual grid-click purchase handler with
only UI refresh suppressed, not free building. It tests insufficient funds,
exact cost spending, functioning economy, input starvation, initial locking,
doctrine eligibility, hidden hints, real economy-driven discovery with an
interrupted streak, one prototype reward and idempotent terminal Research.
Both terminal pairs activate with matching doors in all four orientations and
stop when the nursery is rotated to present its sealed side. Test writes use
`user://brine_nursery_gameplay_fixture.json`, removed after the fixture; no player
player save is written by the fixture.

Clean exit-0 logs:

- `output/nursery-gameplay-02.log`
- `output/nursery-test_synergy_manager-01.log`
- `output/nursery-test_discovery_progression-01.log`
- `output/nursery-test_polish_gameplay-01.log`
- `output/nursery-test_run_balance-01.log`
- `output/nursery-scene-regression-01.log`

The last is the existing real-scene headless regression, not native screenshot
evidence of the new nursery. The former generic-art fallback has since been
replaced by the layered component and card bake described above. Native acceptance
remains open for the listed checks. Broader balance sweeps and the other two
expansion branches remain separate unfinished work.
