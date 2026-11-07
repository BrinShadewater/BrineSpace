# Medical support composition

Updated September21,2026. Brine Space. Broad goal remains active.

## Objective and acceptance
Give unprotected Med Center and Med Office coherent large/medium functional groups,
remove duplicate/scattered furnishing, preserve circulation and all owner layouts.
Med Bay is a different room and was not changed. Owner visual acceptance remains open.

## Decisions and implementation
Med Center groups bought bed/IV and scanner with the existing diagnostic console,
medicine storage and handwashing. Removed duplicate legacy imaging, tiny loose
vitals/cabinet props and the redundant stool (console already includes a seat).
Med Office restores the supported consultation table/two seats, pairs bought records
monitors with their operator chair and filing cabinets, and places a palm beside
consultation. Removed examination light over the desk, loose laptop/extra seat,
old overlapping desk/records and medicine cabinets from the records function.
No new raster generation, Higgsfield, source-atlas or registry/mark edits.

The Med Center q3 bank wrapper discarded explicitly placed medical_station when
restoring its old retained set. rooms/full-wall-v1/med_center_view.gd now keeps the
complete layout result when its full-wall bank is explicitly removed. Existing
UID preserved. tests/test_removed_bank_restoration.gd adds presence/position coverage.

Exactly8complete keys per defaults and player Studio store were promoted using
backup guards. Every other key is semantically unchanged, including Research Lab,
Mycelium Nursery, Med Bay, Pressure Control, Crew Lounge, Mining Drone Bay, Ore
Refinery, Cryo Chamber, Listening Post and Xeno Lab. Only med_center/med_office cards
changed; other card hashes remain identical.

## Verification
Evidence/backups/drafts: output/medical-composition-2026-09-21/.
- Before:8native views/1280walking samples pass routes, but agent review found
  duplicated equipment and unsupported/overlapping examination light/desk.
- r1 exposed missing Med Center console in q3; the new repeated-setup test
  reproduced2failures before the wrapper fix,0after across5rooms/four views/two setups.
- Final r2:8views/1280walking samples,0failures and0reported visual overlaps.
  All8images inspected. Repeated door-quarter captures do not establish separately
  authored directional furniture art; bought sources retain their authored view.
- Funded/free-build live fixture: both room centers visible at52/75percent zoom;
  complete individually focused52percent crops inspected.75percent overview clips
  the far right edge of Med Office; do not count it as complete-room framing.
- Installed defaults:8views/1280samples pass and every RGBA image exactly matches
  the corresponding candidate. Two cards baked from current saved/default designs,
  inspected; hash comparison confirms only those2cards changed.
- No new operating effect, autonomous medical activity, balance or export acceptance
  claimed. Diagnostic console's existing operating renderer remains; other bought
  source screens retain their existing behavior.

## Next action
Continue focused animation/performance and remaining visual polish. Owner review is
still needed; mixed detail and density are not globally resolved. Existing release
build2601720e53d908cc predates these room/card/wrapper changes plus recent south Bill,
departure and release-manifest work. Batch them into the next verified release.
