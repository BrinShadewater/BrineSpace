# Project handoff

Updated: October 20, 2026 · BrineSpace · Windows candidate performance testing

## Objective and acceptance

Owner requested broader performance testing of `brinespace-ef1c732983837a49`.
The matrix, entry checks and sustained rerun are complete;
**broad frame-pacing acceptance is not met**.

## Accepted decisions and constraints

Exact unsigned candidate, isolated saves, physical QA copies, native release.
Owner closed previews; editor retained. No gameplay or art changes and no rebuild,
signing or publication. Synthetic stress fixtures are not balance evidence.

## Current state

Changed `tools/release_benchmark.gd` to use an existing recovered pilot with its
production actor class. This fixes stale mixed-fixture actor/roster assumptions;
the original failed attempts and focused reproduction remain recorded.
Added this handoff and updated CURRENT_STATUS.

[Full report](D:/bs-performance-20261020/REPORT.md) ·
[Machine-readable results](D:/bs-performance-20261020/results.json) ·
[Final receipt](D:/bs-performance-20261020/FINAL.json).

## Verification

Eight completed matrix cells at 900p/1080p; 41,040 measured frames including
8.66 minutes of sustained native mixed-station measurement.
Normal New/Continue loading measured with all UI/save checks passing.
Sustained p95 was 47.4 ms at worst, with a
220.7 ms maximum frame. Private-memory sampled medians grew
272.8 MiB; no leak-freedom claim.
Fresh station passes 24/24 and 23/24 phases; standard 40-room station passes 0/24
at both resolutions. See report for mixed, memory and loading values.
Focused corrected-fixture saves/readbacks pass at all three speeds.
All 2,971 owner file hashes, prior signed ZIP size/mtime and candidate binary identity
preserved. Benchmark screenshots/normal entry captures reviewed separately.
No hours-long endurance, other hardware or Apple acceptance.

## Next action

Target large-station frame cost and action hitches, then run matched comparisons.
Do not label this candidate as broadly performance-accepted.
