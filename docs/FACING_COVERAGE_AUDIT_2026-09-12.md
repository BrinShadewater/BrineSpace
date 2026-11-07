# Facing coverage reconciliation - September 12, 2026

Fresh RoomDatabase export contains 47 identities. The current facing ledger has exactly those 47, with no duplicate identities or absent compass-direction entries. This proves inventory coverage only; it does not establish art completion.

Added tools/audit_room_facing_coverage.py. It accepts a freshly exported catalog and reports identity/direction mismatches, declared stage counts and textual review candidates, including nested notes. Candidate flags are deliberately not defect counts: wording such as "not missing" or historical reverted drafts can be false positives. Unflagged entries are not automatically accepted. Owner feedback is carried into the report.

Evidence: output/facing-coverage-audit-2026-09-12/catalog.gd and catalog.json export actual RoomDatabase data; report.json comes from the maintained auditor. No visual tests or raster changes in this audit. Earlier room-level checks retain their recorded scope.

Concrete remaining work includes Airlock directional suit lockers and compatible helmet fitting, BRINE corner inactive display states, Salvage south live fit, and final owner camera review. Library-only companions such as Observation south and fixed-layout room alternatives need deliberate per-room acceptance; do not install all alternatives simultaneously merely to remove a library stage. The full objective remains active.

Use the audit again after catalog identities or coverage schema change. Do not rescan generated historical output trees or treat a stage histogram as a completion certificate.
