# Medical Bay layered integration

## Contour follow-up: card v5

Current individual export coverage: v16 passes this fixture at actual 1280x720,
1600x900 and 2560x1440, 69 dimension-checked full frames per size. See
`FOUNDATION_ROOM_EXPORT_FOLLOWUP.md` for working/offline, infill and review scope.
Earlier pending-export statements below describe their historical checkpoints.

Standalone follow-up: v13 verifies current source/card loading and controlled
arrival in a 24-room exported fixture at actual 1600x900. See
`ROOM_REPAIRS_STANDALONE_V13.md` for precise scope; this is not an individual
exported power-state suite or all-resolution acceptance.

Both bedside assemblies now exclude the source-floor wedge between the bed's
upper side and its monitor. The diagnostic console follows the rounded rear
shoulder instead of retaining a square background corner. Bed scale, complete
collision footprints, IV pieces, chair, source PNG and effect anchors are unchanged.
Chair-foot shadows and other ambiguous fine margins remain unmodified.

Reviewed native `output/batch-two/med-edge-before-v1/` console/bed captures,
`med-edge-notch-v1/med_bed_0-dark.png`, the console in `med-edge-contour-v2/`,
and card v5. Both card consumers and the whole-room export manifest select v5.
Originals are preserved and the new card has the LFS filter.

`output/batch-two/med-contour-state-v1.log` exits zero with no ERROR/SCRIPT ERROR
entries. Four rotations pass retained-hardware/excluded-floor regression points,
whole-assembly containment, per-host working/offline effects and neighbor-removal
infill; input isolation also passes. All full frames independently measure
1600x900. The fixture's legacy path-helper samples are not current autonomous
NPC-controller evidence. Raw-image warnings remain. Fresh standalone coverage,
other viewport sizes for this revision and owner approval are still pending.

The existing `med_bay` foundation now uses registered medical art in the station,
placement renderer, card and inspector. This is an art/operation pass, not a new
room ID or a changed unlock graph. Its costs, power consumption, south-only socket,
hidden care synergies and three-cycle stabilization rules remain unchanged.

## Art and registration

Source: `rooms/whole-room/med-bay-source-v1.png`, copied unchanged from the approved
batch candidate `output/room-batch-02/med-bay-v2.png`. Exact generation prompt and
brief are retained in `NEXT_ROOM_BATCH_BRIEFS.json`. No new generation was needed.
Native source is 1254 square. Original and prior card versions are preserved.

Two treatment assemblies use 90 world units across a 305-source-pixel registration,
roughly 17% smaller than the earlier 368/1032 room-source scale. Each bed, bedside
monitor and IV stand moves as one assembly. Bed silhouettes, monitor controls and
IV stands remain south-facing in every layout. Complete bounds, including the
separate IV silhouette, receive the shared inward containment adjustment.

Medical floor uses pale grey composite panels, 96-unit panel joints on the existing
48-unit module, quiet teal inlays and restrained grain. Equipment retains clean
white/teal materials. Two existing north fixtures use soft-white lenses and pools;
standing-lamp alternatives remain optional future room-specific work.

The room uses a fourth geometry-mask entry `[2]`, matching its single south socket.
It does not inherit Life Support's four-port topology despite reusing its registered
prop interface. Valid connections use shared department doors; medical currently
falls back to neutral grey. Unconnected sockets receive full wall infill.

## Function and progression

Bedside self-test traces, console telemetry and a cabinet status lens animate only
while functioning. These are equipment operation cues, not simulated patients or
new healing mechanics. Effects use the existing visual clock; pause freezes motion.
Shared power shading still distinguishes input shortage from lack of power.

Existing care patterns remain discoverable through functioning placement. Clinical
Airlock retains its Cryo Chamber reward, verified on the third functioning cycle.
No recipes are exposed by the art or added to pre-discovery UI.

## Verification

`tests/playtest_med_bay.gd`: four rotations, 808 actual entry samples in both
directions, complete assembly containment, non-overlapping ground footprints,
working/offline effect comparisons and removed-neighbor infill. Native station,
card and inspector consumers captured under `output/room-batch-02/med-review/`.
Final card: `rooms/whole-room/med-bay-card-v2.png` (512 square).

Synergy, discovery progression (including an explicit clinical-airlock test),
gameplay polish and run-balance regression suites pass. PNG paths retain LFS
attributes. No player save migration, commits or gameplay balance changes.

Art acceptance remains owner-reviewed. The diagnostic workstation/chair is one
registered assembly with conservative collision, not individually movable furniture.
Its narrow source-floor slivers around chair feet remain an extraction limitation.
