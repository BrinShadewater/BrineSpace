# Project handoff

Updated: October10,2026 · Project: BrineSpace · Task: owner-reported full drives

## Objective and acceptance
Identify sudden disk usage. Read-only metadata audit; no deletion authorized by
this diagnostic request or performed. Keep original performance/release objective.

## Accepted decisions and constraints
No new large builds while space is scarce. Preserve owner saves/layouts, selected
art, vendor art, Git/recovery archives, frozen source, current/rollback delivery
and useful diagnostic evidence. Cleanup requires concrete disposable-file review.

## Current state
C:930.49GiB total/3.70GiB free; D:930.98GiB total/5.40GiB free at initial check.
Metadata audit session9600 terminal0; D:463,254files/3access errors; Alex user tree
2,665,801files/1,213access errors. Reparse points skipped; duplicate hardlinks
checked,0bytes excluded. Logical file sizes, not an allocated-cluster measurement.
Recent3day fields use modification timestamps, not net growth or copy creation;
copy-preserved dates can understate recent creation. Windows/system folders outside
Alex's profile on C: were not comprehensively audited. No owner data writes.

| Folder | GiB |
|---|---:|
| C:/Users/Alex/Documents/Brine Space/output |315.659|
| C:/Users/Alex/Documents/Brine Space total |421.440|
| C:/Users/Alex/.codex |55.885|
| C:/Users/Alex/.codex/archived_sessions |24.699|
| C:/Users/Alex/.codex/sessions |11.484|
| C:/Users/Alex/AppData/Local/Temp |21.084|
| D:/bs-release-crew-cache-20261009 |89.548|
| D:/bs-release-20261009 |26.160|
| D:/BrineSpace-performance |11.492|
| D:/SteamLibrary |702.885|

Rows overlap; do not sum nested entries. The three independent D: BrineSpace
roots total127.200GiB. Steam has50.856GiB modified within3days (not net growth).
C:output has47.386GiB recently modified; temporary bs-* directory count1,335.
Big C:output groups:release-stall-trace41.975GiB,stall-attribution34.805GiB,
drone-compiled32.488GiB,drone-upload25.538GiB,combined-release-v36724.459GiB.
Game artcharacter47.914GiB/.git28.501GiB are outside generated output; not cleanup
targets. Git lost-found21.787GiB is recovery material, not disposable by this audit.

Scoped D:QA scan excluding source/windows/mac delivery folders finds24PCKfiles
over1GiB, totaling80.98GiB. These are candidates for redundant runtime-copy
cleanup, not approved deletion; preserve the currently reused QA runtime and
verify references/evidence requirements before disposal. Source inspection confirms
prepare_release_copy physically copies the complete external PCK for each QA
runtime. This explains repeated ~3.37GiB allocations. No subsequent GPU job live.

Evidence output/renderdoc-tools-2026-10-08/disk-usage-audit.json,
large-qa-pack-usage.json and audit-disk-usage.py. Full directory listing not needed.

## Next action
Review concrete redundant QA binaries/source snapshots for disposal with owner
authorization, retain compact reports/prototype inputs and accepted deliveries.
Prefer reclaiming duplicate packages before any game art or Git material. Introduce
bounded QA-runtime reuse and explicit retention so tests do not refill drives.
Resume graph-reuse performance work once enough space is available; no new
large snapshots/export copies until storage issue is handled.
