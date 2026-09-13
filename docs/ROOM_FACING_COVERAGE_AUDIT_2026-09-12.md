# Room-facing coverage consistency audit

September 12, 2026. This audits the ledger, not visual acceptance or RoomDatabase completeness.

- 47 ledger identities and 188 directional entries inspected.
- 113 unique registered PNG sources: present, PNG signatures valid, registration hashes match.
- 12 ledger corrections: 10 capture-folder links now name their runtime.json; 2 stale generic north registration pointers removed where split-section registrations are authoritative.
- 40 directional entries have no registration recorded. This includes custom/architectural rooms and does not prove 40 missing art assets.
- 150 directional entries have no direct evidence link in this ledger. Some have historical review elsewhere; these are evidence-link gaps, not an automatic art rejection.

## Stage inventory

- existing-art-native-reviewed-retained: 11
- existing-live-corner-inventoried-facing-review-pending: 3
- integrated-native-reviewed: 27
- inventory-other-art-or-author-missing-view: 37
- native-reviewed-default-installed: 20
- native-reviewed-interior-installation: 1
- owner-accepted: 4
- registered-library-source-reviewed: 2
- requires-native-facing-and-fit-review: 83

## Reproduce

`python tools/audit_room_facing_coverage.py --out output/room-facing-audit-2026-09-12/after.json`

The tool only writes its requested report. Native source inspection, game-scale review, routes and state checks remain separate gates. Original findings and the exact corrections are saved beside the final report.

## Next action

Continue missing companions and remaining native direction reviews. Resolve evidence links from specific known handoffs as those rooms are revisited; do not infer completion from existing files or matching hashes.
