# Project handoff

Updated: September 21, 2026 · BrineSpace · Support-room review and Radio restoration

## Objective and acceptance
Continue natural large/medium furnishing and runtime repairs. Coherent native-scale
work areas and preserved circulation are required; geometry alone is insufficient.
The broad animation, art, performance and release objective remains unfinished.

## Accepted decisions and constraints
Owner reference rooms and library marks remain untouched. No Higgsfield. No release,
commit or publication. Radio furnishing is a staged draft, not an accepted layout.

## Current state
Fixed `rooms/full-wall-v1/radio_lab_view.gd`: when the merged layout removes the
full-wall bank, retain the layout-applied standalone props instead of the q2 legacy
restoration, which discarded the calibration bench. Extended existing
`tests/test_removed_bank_restoration.gd` (existing UID retained) with Radio coverage.

Evidence and backups: `output/support-room-review-2026-09-21/`.
Candidate-r1 JSON removes overlapping transducers and loose console/chair and gives
the calibration bench a fixed placement. `radio-r1` is before the runtime fix;
`radio-r2` is the same JSON with the fix. No saved/default layout or card was changed.

## Verification
Initial three-room review: 12 native views, 1920 walking samples, zero route failures.
All twelve images reviewed. Radio q0 overlays transducers on receiver/rack; other
quarters inherit inconsistent calibration machinery. Salvage Workshop has an
oversized bright crate and scattered tools; Holographic Core is sparse with separated
stations. These observations are art-review findings, not new navigation failures.

Regression-before reproduced two missing Radio calibration benches (q2 across two
setup cycles). Regression-after: three rooms, four quarters, two setup cycles, zero
failures. Candidate after fix: four views, 640 samples, zero failures/overlaps; all
four images reviewed. Native funded/free-build fixture completed at 52/75 percent,
room crop and full 75-percent frame inspected. It is not balance acceptance.
Candidate remains visually too isolated/sparse at gameplay scale; not promoted.
Byte equality confirms owner save and defaults still match review backups.
No operating-effect or actual release check was performed for this patch. Existing
c09c builds predate this runtime fix and the recent three installed room changes.

## Next action
Build physically related workstations for Radio rather than four disconnected
corners; inspect source support surfaces before placing instruments. Then review
Salvage Workshop's handling/workbench/storage relationship and Holographic Core's
projection/analysis area. Keep current candidate as diagnostic evidence. Batch
accepted room changes and the runtime fix into the next release checkpoint.

## Subsequent r4 integration (supersedes staged-only state above)
Restored the existing low signal-routing panel as the principal instrument surface,
with bought reception desk and legacy calibration unit grouped below. Receiver/rack
and dish/controller remain separate functional areas. r3 visually overlapped the
raised wall because its registered visual bounds extend above its placement anchor;
r4 lowers the panel to [-174,-128], size1.45. Reception is [-174,42]; calibration
[-68,85], size0.85. Original r1 removals remain. No raster or registry edits.

Installed only four complete room-radio_lab keys in defaults and saved layouts;
all other keys independently compared equal to the original backups. Refreshed
assets/room-cards-v2/radio_lab.png. r4 and installed-default each pass four views,
640 walking samples, zero failures/overlaps; full RGBA is exact in all four pairs.
All four native images, live native crop and 75-percent full station, and completed
card bake were inspected. Live fixture completed both52/75-percent views.

This restores hierarchy and groups existing equipment without scatter. It remains
provisional: mixed art detail, further cohesion and owner visual acceptance remain
open. Signal-panel screen imagery is baked/static; no operating/pause acceptance
is claimed. Existing releases predate this integration. Next: Salvage Workshop and
Holographic Core, then focused operating-feedback improvements and batched release.
