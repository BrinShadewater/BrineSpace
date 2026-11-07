# Construction/Biodome bank restoration repair

September 21, 2026. Broad room/animation/polish goal remains active.

## Objective and constraints
Follow the reproduced Salvage/Quarantine failure pattern through remaining room
wrappers. Preserve saved placements, default layouts, source art and library marks.
No Higgsfield, commit, publication or changes to the ten owner reference layouts.

## Installed changes
Construction Drone Bay and Biodome q3 restored deleted legacy furniture after the
layout store applied saved edits. Both wrappers now keep the layout-store result
when the full-wall bank is explicitly removed. Existing bank installations retain
their prior restoration behavior. No layout or card files changed in this pass.
The cards depict q0; the changed restoration path is q3.

Changed rooms/full-wall-v1/construction_drone_bay_view.gd and biodome_view.gd;
added tests/test_removed_bank_restoration.gd with paired UID and room-art/native
index entry. The test supplies explicit bank/furniture deletions and a bought prop,
then configures each of four rotations twice. Before repair: 12 failures, exit 1.
After repair: zero failures, exit 0, clean log.

## Native evidence
Current saved-layout snapshot: eight views / 1,280 walking samples, zero failures.
Inspected both q3 captures: Construction retains its bought robotics/tool-storage
area; Biodome retains the saved growing/life-support assemblies. Biodome still
has layered/inherited planting equipment at northwest requiring composition
judgment; this fix is not a complete furnishing-quality certificate.
Saved profile bytes were verified unchanged after the review. Evidence:
output/remaining-bank-restoration-2026-09-21.

## Remaining work
Review the remaining restoration wrappers against effective saved props, including
Medical Center/Office (which already respect explicit deletion in their restoration)
and Ore Refinery (which reapplies an asset-key layout after restoration). Those are
not proven affected by this test. Preserve the owner's Ore Refinery placement.
Continue Bill ordinary-motion acceptance, room composition and native Mac testing.
Current packaged Windows/Mac builds predate all four recent wrapper repairs.
