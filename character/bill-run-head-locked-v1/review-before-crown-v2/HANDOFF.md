# Project handoff

Updated: October 1, 2026 · Brine Space · Bill cardinal run master-head consistency

## Objective and acceptance
Continue full Bill master/material/anatomy/perspective/motion consistency. This layer fixes running head identity and size drift; full goal and owner visual acceptance remain open.

## Accepted decisions and constraints
Keep accepted masters, matte finish, native256 plane/p128,224/H148, independent authored gait/body,540ms clock and .168cell directional stride. Native head reuse is a bounded deterministic consistency fit, not new hand-authored anatomy. Helmet source frames unchanged. Normal Bill NPC still walks; no new run route.

## Current state
24 bare frames and four exact native master components in this folder. Paired manifests selected through scripts/grid_canvas.gd and character/ACTIVE_ASSETS.json. Four existing directional tests updated to current manifest/state IDs. New paired all-direction fixture tests/test_bill_run_head_locked_selected.gd with paired UID; scratch runner tools/run_bill_run_head_locked_selected_validation.py. Original run sources remain untouched. build_candidate.py delegates to build.py; obsolete prototype archived. New inventory bill-selected-source-audit-2026-10-01-locomotion-v4 and current locomotion comparison rebuilt. Diagnostic original head board retained in bill-run-head-master-audit-v1.

## Verification
137 package checks pass; master component pixels exact, protected body exact, original source hashes unchanged, gear references/clock exact, all24 connected at alpha160. Normal-loader native289 checks/0 failures/engine0/12.52s with fresh four148/82 boards, all reviewed. Strict real-profile fingerprint guard false: last_session.json changed among2931 non-log files; attribution unproven. No owner restore, unrelated rerun, actual NPC run or Continue proof. Native evidence in output/bill-run-head-locked-selected-native-v1; snapshots/hashes in runtime-evidence.json.

## Next action
Review moving idle/walk/run joins in all directions and finer head/collar/shoulder/counter-swing/material cadence; then other selected families against masters and previously unproven physical/service/Continue contexts. Current source review is bill-locomotion-consistency-audit-v2/join-review.html. Source-key counts212bare/194helmet do not establish completion. No export/commit/push in this milestone.
