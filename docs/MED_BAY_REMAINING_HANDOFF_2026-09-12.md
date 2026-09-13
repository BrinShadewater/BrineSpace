# Med Bay remaining views checkpoint

## September 12 blue treatment upholstery correction

The selected south/top-down treatment bank now uses muted medical blue upholstery
instead of orange. The versioned source and review record are under
`assets/med-bay-directional-v1/`; the current south registration selects it without
changing geometry. A generated edit was rejected because it changed the canvas
width and could not prove preservation outside the mattress. The deterministic
palette repair changed 188,410 pixels inside the upholstery ROI and zero outside.

Native Godot 4.6.1 captures in all four rotations were inspected at
`output/med-bay-blue-2026-09-12/native-verified`. The 176 furnished-orientation and
20 side-wall-variant checks pass at `output/test-runs/20260912-164920-headless`.
The existing north-view card contains no south upholstery, so it remains current.
Owner aesthetic acceptance and the broader side-view objection remain open.

## Objective and constraints
Continue all room art and missing directions. Preserve inward access, medical inventory, existing placements and live operating feedback. Owner has now said they dislike side views; the affected asset and reason are not yet confirmed. Do not call current side art accepted.

## Changed state
North and side idle-material candidates are installed through three medical-treatment registrations. Original registrations and exact prompts are preserved in assets/med-bay-directional-v1. North native view and new card visually reviewed; all three card bindings now use the new card. East native view inspected; west final visual review remains outstanding. South source is retained. Coverage explicitly leaves both side candidates pending owner review.

## Verification
output/med-bay-remaining-2026-09-12/comparison.json records unchanged north prop metadata, but west swaps med_console for med_bed_1. This is a regression under investigation. Layout test log passes 176 furnished orientations and 20 existing side-variant cases. State-checks.json records independent medical equipment temporal changes in all four rotations. Those crop differences are state evidence, not an aesthetic acceptance. Card parity check follows binding update.

## Remaining
Resolve the owner's side-view objection before choosing a replacement direction. Turbine was the latest explicitly named room; its captured side rotor reads as a narrow dark housing, a possible diagnosis rather than a confirmed owner complaint. Complete Med Bay west and powered visual review, provenance, and final geometry audit. Continue remaining catalog; no export or commit.

## West inventory correction
Removed the new west wall_contact flag. west-fit-check native review and mounting-checks.json prove all four original inventories, rectangles and independent bounds are preserved; south unchanged. New source/card hashes recorded in remaining-review.json. Earlier q3 state captures had the wrong inventory and must be refreshed. Side aesthetic feedback remains unresolved.

Corrected state follow-up: fresh off and two powered captures completed after removing west mount flag. corrected-state-checks.json confirms west console, bed and supply temporal effects; native powered west frame visually reviewed. Earlier state limitation is resolved. Side aesthetic feedback remains open.
