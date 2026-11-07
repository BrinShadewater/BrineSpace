# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Completion, dismantling, repair and ambient motion

## Objective and acceptance
Connect construction to underwater motion while preserving the painted overhead
style, restrained effects, physical material density and gameplay rules.

## Accepted decisions and constraints
Owner authorized all four proposed passes. Reuse selected original painted sources
and existing creature cycles; no new generation or source grading. Scrapping still
removes occupancy and refunds Metal immediately. Cosmetics freeze with visual time
and respect Reduced Motion and effects quality. Preserve concurrent owner work.

## Current state
`scripts/room_transition_art.gd` keeps up to 16 transient per-grid events, outside
saves. Successful construction emits a 3.2s hull-joint bubble/sediment effect above
the station. Scrap snapshots dismantle fittings, shell, deck and joists over 5.5s
below the station; reused/reserved cells permanently discard the old visual.
New loops clear events. Large-room footprints now use full bounds and destination
art without reading live airlock state; material strips repeat at fixed world
length instead of stretching their grain/bolts across two cells.

`scripts/flood_visuals.gd` renders localized painted repair sparks/vapor only while
the assigned worker is welding, stationary and alive; the authored dry weld keeps
its own torch. `scripts/ambient_fronds.gd` gently bends existing kelp, sea fans,
hydroids, red algae and sea lettuce while fixing the bottom root. Creature cadence
is smoothly varied; paired body/core frames stay synchronized and paths unchanged.

Integration touches `scripts/main.gd`, `room_scrap.gd`, `grid_canvas.gd`,
`room_construction_art.gd`, `construction_materials.gd`, `ocean_life.gd`, and the
seabed/sub-biome/red-algae/sea-lettuce consumers. No character selections or owner
layouts changed. New scripts/tests have paired UIDs.

## Verification
Logic and existing scrap, hull repair and fitting-route gates pass in
`output/room-motion-20260930-013900` (the initial large preview failure was corrected).
Completion/cancellation/payment/reset integration passes in `014541`.
Native ocean and motion gates pass in `014143` with all 2,786 owner files unchanged.
Final native gate in `015011` passes after fixed-density materials and stronger
checks: byte-identical paused frame, Reduced Motion across advancing clocks,
waiting repair suppression, reused-cell suppression, unchanged orders, all four
large-room types and actual station composition. Source loads report no failures.
Latest owner comparison changed logs; that profile gate failed. Earlier intervals
also observed logs/hallprobe.json changes of unknown attribution. All jobs set
scratch APPDATA/LOCALAPPDATA; no owner files were restored. Evidence is preserved
in each timestamped directory, not inferred from the artwork preview.

`tools/verify_room_motion.py` runs the scoped gates; narrower flags are documented
in its source. `tools/preview_room_motion.py` assembles 24 native frames with a
fixed GIF palette and no physical-pixel resizing. Preview:
`output/room-transitions-v1/room-and-ocean-motion-v1.gif`; native station and large
stages accompany it. Diff whitespace checks pass.

## Next action
Owner visual review. Playable-release acceptance remains separate; no export,
commit or push performed. For an uncontaminated profile comparison, use a quiet
interval with other game/probe activity closed.
