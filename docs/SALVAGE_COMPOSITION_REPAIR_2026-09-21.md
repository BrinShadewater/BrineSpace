# Salvage rotation repair and composition candidate

September 21, 2026. Broad room/animation/polish goal remains active.

## Objective and constraints
Group processing machinery with tools and cargo logically. Preserve owner layouts,
marks and source artwork. No Higgsfield, publication or commit.

## Installed repair
The fourth rotation restored legacy hatch, winch and ROV after the layout store had
removed them. It also discarded the sorter while retaining bought furniture. When
the saved layout removes the full-wall bank, the wrapper now keeps the layout store's
result and skips legacy restoration. Existing bank installations retain their path.
Changed rooms/full-wall-v1/salvage_drone_bay_view.gd; added
 tests/test_salvage_layout_deletions.gd with paired UID and native room-art index entry.

## Verification
Native regression runs four rotations twice, checking all four deleted IDs stay
absent and both the sorter and bought tool storage remain exactly once. Baseline:
eight failures, exit 1. Fixed: zero failures, exit 0, clean engine log. Guarded
baseline comparison restored the exact repaired source afterward.

## Composition revision 3, subsequently installed
Revision 3 puts tool storage beside the sorter in a southwest processing area,
keeps the desk northwest and cargo rack/crate northeast, with the parts bin east.
The small loose case is hidden. Sorter placement is explicit in all rotations.
Revision 1 blocked side approaches; revision 2 passed but kept the equipment too
separate. Revision 3 passes four native views / 640 walking samples; every view
was inspected. Source pixels and library marks are untouched. The owner profile
still matches its pre-review backup byte for byte. Defaults and cards unchanged.
Candidate/evidence: output/salvage-composition-2026-09-21, candidate-r3.json and native-r3.

## Installation and live review
Revision 3 was reviewed in a native station fixture at 52% and 75% zoom. The
fixture uses free construction, funded resources and disabled failures, so it
establishes framing/rendering rather than normal expedition balance or actor work.
The sorter has no dedicated CrewRoomActivity station binding; its existing visual
feedback follows prop registration. Four native on/off/held-clock comparisons
confirm feedback changes stay inside the relocated sorter. No crew service binding
was changed or autonomous work acceptance claimed.

Guarded installation changed exactly four Salvage keys in the saved profile and
fresh defaults. Other keys are semantically unchanged, including all ten named
owner reference rooms. Backups remain beside candidate evidence. Four installed
default renders match the candidate's complete RGBA arrays exactly; navigation
passes 640 samples with zero failures. The single Salvage card was rebaked and
inspected. Live, operation, card and installed-default logs have no engine errors.
Changed: default-layouts.json, saved room_layouts.json, Salvage card, renderer repair,
regression test/UID/index and current documentation/pipeline lesson.

## Next action
Gather owner composition feedback and continue the saved/default Quarantine review.
Keep ordinary expedition/Bill motion and native Mac acceptance open. Existing
Windows/Mac packages predate this runtime repair, furnishing and card update.
