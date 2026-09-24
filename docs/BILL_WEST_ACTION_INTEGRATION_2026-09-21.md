# Bill west action integration

Updated: September 21, 2026 · Project: BrineSpace

## Objective and acceptance
Repair west action identity and the kneel-to-work height mismatch. Installed for
playtesting; owner full-motion acceptance remains separate.

## Accepted decisions and constraints
Independent west sources, no east mirroring, no Higgsfield. No changes to owner
rooms, original source contracts, runtime movement or prototype economy.

## Current state
`tools/build_bill_west_actions.py` reads preserved raw sheets, prompts and registered
landmarks from `character/major-bill-v3/sources/west-actions-2026-09-21/`. Kneel uses
one scale and per-pose registration to the planted forward-boot toe (x106, bottom
band y218:224), with no clipped pixels. Work changes only the tool-arm polygon;
head/body/legs remain from settled kneel. Work endpoints match exactly and stand
reverses kneel. Equipment uses existing west helmet pixels and recorded head anchors.

## Verification
Maintained helper matches all 36 candidate frames exactly. Native candidate capture
records 198 frames per equipment state with zero failures/no logged errors. Agent
source/endpoint-board inspection confirms coherent identity, matching action height,
boot registration and helmet fit. Direction and helmet selection are forced; this
is rendering evidence, not autonomous-facing/donning or complete expedition acceptance.
Evidence: output/bill-west-candidate-native-2026-09-21.

Canonical rebuild and full validator pass: 2,214 frames, zero errors/border touches,
780 original frames/113 original manifests preserved. Exactly 36 west action PNGs
changed; all other generated assets, clearance and playback metadata are unchanged.
Backups, before hashes, diff and logs: output/bill-west-action-integration-2026-09-21.

Installed-loader confirmation completed: 198 frames per equipment state, zero
failures/no logged errors; equipped work frame inspected. All 36 installed PNGs
match reviewed candidate pixels. Evidence/GIF: output/bill-west-installed-native-2026-09-21.

## Next action
Review the repaired south/north/west
family in normal expeditions, including interactions and turns. East's authored
endpoints already match and remain selected. Current Windows/Mac builds predate
these action repairs; refresh at the next broader release milestone.
