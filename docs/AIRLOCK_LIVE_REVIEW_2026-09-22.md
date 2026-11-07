# Airlock live handoff review

Updated September 22, 2026. Broad animation and polish goal remains active.

## Objective and constraints
Verify the installed R2 airlock through live Bill locker actions and chamber cycles.
Preserve owner rooms, layout marks and selected runtime art; no generation or publication.

## Current state
Changed tests/test_airlock.gd to require the retained functional chamber, hatch and
locker plus the five selected bought props, replacing stale legacy furnishing
expectations. Current default layouts explicitly hide the legacy props that failed.
Continuous capture filenames now include actor and quarter, preventing overwrites.
Updated character-pipeline acceptance guidance and synced its installed copy.

## Verification and findings
Evidence: output/airlock-live-review-2026-09-22, with native logs beside that folder.
Initial headless run failed only stale furnishing checks; its log is preserved.
Corrected native Bill run passes four rotations, 743 travel samples, equipment
pickup/return, all ten interlock phases, power interruption, pause, disk restore
and inspector controls. Exit 0; no engine/script errors in final log.
Continuous run passes all four rotations, eight complete action traces and 360
captured samples at 0.05-second simulation steps. Exit 0. Contact sheets inspected.
These are controlled service/cycle fixtures, not an autonomous expedition or actual
packaged-runtime test. Other humans were not exercised in this pass.

Visual review exposes a remaining identity mismatch: removal shows a warmer
face/suit than equip and the selected standing endpoint. Fixed feet and correct
handoff timing do not close that visual defect. The contact sheet preserves the
comparison; no replacement art or timing change has been made yet.

## Next action
Inspect Bill's canonical equip/remove sources and rebuild provenance, isolate the
face/suit mismatch, repair only the inconsistent pixel layers, and repeat the
affected native joins. Keep packaged and other-crew acceptance separate.
