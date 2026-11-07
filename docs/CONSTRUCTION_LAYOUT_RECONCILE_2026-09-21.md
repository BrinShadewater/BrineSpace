# Construction Drone Bay reconciliation

September 21, 2026. Broad objective remains active.

## Objective and constraints
Preserve the bought robotics/tool/loading groups and make fresh profiles agree.
No source art, owner reference rooms, library marks or gameplay rules changed.

## Installed change
Four saved/default keys now explicitly hide the legacy construction bench and
retain the panel platform at [72,84] for q0/q2 and [-156,84] for q1/q3.
The first candidate overlapped the forklift; visual review rejected it despite
passing routes. Revision 2 separates the platform and forklift in all rotations.
All other saved/default keys remain semantically unchanged. Single card refreshed.

Initial promotion copied sparse overrides and lost an inherited q2 panel size.
Native pixel comparison caught this (9,425 changed pixels). Corrected promotion
merges previous defaults with candidate overrides and writes that complete effective
layout to both destinations. Final four-view RGBA captures exactly match revision 2.
The q0 result was unchanged by this correction, so the already-baked card is current.

## Verification
Four views / 640 walking samples, zero failures; all views inspected. Live 52%/75%
station capture and crop reviewed using funded/free-building fixture, not ordinary
expedition acceptance. Final logs clean. Card inspected. Owner acceptance remains
open. Evidence/backups: output/construction-layout-reconcile-2026-09-21.
Changed: default-layouts.json, saved room_layouts.json, Construction card, docs/skill.
Current Windows/Mac packages predate these changes.

## Next action
Before this install, catalog-key comparison found 32 identities with saved fields
differing from defaults, including ten protected owner rooms. This is a review list,
not 32 proven visual defects. Construction is now reconciled. Snapshot inventory:
output/saved-default-inventory-2026-09-21/differences.json. Review Biodome's inherited
planting equipment next; do not bulk-copy sparse saved overrides. Keep Bill owner
motion feedback, full expedition and native Mac acceptance open.
