# Marsh charging chamber

Updated: September 9, 2026 · BrineSpace · local source implementation

## Objective and accepted direction

Owner supersedes Marsh's cryo recovery: restore a powered-down derelict room; its machine pumps white fluid through tubes into Marsh, recharges him, and he wakes. Approved blond humanoid identity, temple plate and white suit retained.

## Current state

New loops place a dedicated single-occupant charging derelict at (19,21), unless Marsh is the selected starting architect. Human architects remain in the two cryo wards. The chamber uses the established recoverable room shell and north/south ports, with distinct charging pod art, discovery identity, inspector and selection guidance. Existing hull restoration costs 8 Metal / 18 seconds; after connection it consumes the shell's 1 Power. Recharge takes 12 powered simulation seconds, independent of food/oxygen. Full berths allow charging to finish but hold release. Pause, room suspension and power loss retain charge; Save/Continue preserves it. Successful release empties the pod and permanently unlocks Marsh once.

Architect schema 4 enforces the new occupant separation. Schemas 1–3 retain their existing occupants/routes rather than rewriting ongoing expeditions. A selected Marsh uses the charging cradle in the core's existing 10-second emergency start sequence.

Changed: `scripts/architects.gd`, `cryo_recovery.gd`, `wreck_field.gd`, `drone_fleet.gd`, `main.gd`, `grid_canvas.gd`, `architect_cryo_art.gd`, `architect_selection.gd`; new `marsh_charging_art.gd` with UID. Tests: Marsh unlock and architect recovery updated; new native charging playtest with UID. Art, source prompts, hashes, deterministic packaging and captures: `assets/marsh-charging-v1/`.

## Verification

- Final Marsh unlock suite passes: dedicated identity, paid restoration, no early unlock, power/food/oxygen distinction, outages, pause, suspension, partial disk restore, full-berth hold, one-time release, four-crew coexistence, selection and later-loop startup.
- Architect recovery and selection regressions pass, including legacy awake-save handling. Their intermediate headless runs reported shutdown resource warnings; final Marsh and native runs have no script/error entries.
- Native playtest passes: actual pod-region pixels change during powered pumping and freeze during an outage; four viewport widths (960/1280/1600/2560), four rotations, and awake Marsh beside empty cradle. Reviewed small window, rotating placement and empty state. Initial native fixture was corrected to freeze unrelated lighting fades and prevent tutorial dialogue from pausing it.
- Godot import passed; PNGs resolve to Git LFS. No export or commit.

## Art provenance and limits

Occupied and empty cradle sprites generated separately with shared 1024×1536 registration, packaged at 512×768 nearest. Empty source's painted checkerboard removed by edge-connected neutral extraction; its exterior silhouette masks the occupied source's halo. A generated background-cleanup attempt failed and is retained as rejected. Interior art is preserved. Runtime hose anchors follow source pixels and use saved charge time for fluid fill/pulses; live effects are separate from static art. Sources depict asleep and empty states; awakening is the transition to Marsh's active station actor, without a bespoke climbing-out animation. Existing Marsh secondary-action animation aliases remain as documented in the earlier integration handoff.

## Next action

Owner visual review in a new loop. Existing saved loops keep their original recovery layout. Export remains separate from source acceptance.
