# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: real-station performance verification

## Objective and acceptance

Verify the accepted room shadow change on the reported station, alongside the
already measured deterministic 40-room extension. The full PC/Mac release plan
remains active; these scoped comparisons do not certify the release.

## Accepted decisions and constraints

Keep the accepted normal shadow implementation. No new production change in this
pass. Compare the same source inputs with the original shadow path selected by
the internal reference flag. Muted native tests on the secondary landscape display,
isolated profiles with copied owner layouts, unchanged real saves. Reuse the physical
QA executable/PCK; bounded small overlays and evidence, no new full package copies.

## Current state

New driver and analyzer under `output/renderdoc-tools-2026-10-08/`:
`run-room-shadow-reported12-performance.py` and
`analyze-real-station-shadow-verification.py`. The driver restores the runtime
configuration, benchmark fixture and existing loader in finally.

New evidence:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/room-shadow-reported12-performance/`.
`real-station-analysis.json` combines fresh reported-station results with the
existing `room-shadow-packet-normal-performance/` large-station evidence. The
40-room tests were not repeated unchanged. Source identity remains pinned to
`room-shadow-packet-normal-inputs/identity.json`.

## Verification

Fresh four actual debug=false Windows/1080p RTX4070Ti runs, 6,480 measured frames,
lighting, connected galley placement and demolition at 1x/2x/4x. Restores the
reported 12-room save and copied owner Studio layouts; active James, River and
Margot. Deterministic simulation fixtures use explicit test-only free-building
and failure flags, not normal gameplay settings. Both orders have nine identical
phase-end gameplay states each. No engine or missing-art errors; owner fingerprint
2,938 files unchanged. Job95645 terminal0; configuration and fixture restored.

| Map / order | Original mean | Improved mean | Reduction | Original / improved p95 |
| --- | --- | --- | --- | --- |
| Reported12 forward |16.280ms|15.976ms|1.86%|23.912 /22.959ms|
| Reported12 reverse |16.336ms|15.988ms|2.13%|23.921 /23.312ms|
| Expanded40 forward, prior evidence |31.279ms|30.764ms|1.65%|55.123 /53.385ms|
| Expanded40 reverse, prior evidence |31.234ms|30.444ms|2.53%|55.487 /52.126ms|

Reported12 p99 improves29.739->28.535ms and30.002->28.778ms. However, first1x
galley placement still takes215.665->212.840ms forward and215.867->209.290ms
reverse: one >100ms frame in every run. Floors, shells and wall submissions are
costly in that action frame; attribution is not a proven single cause. Improved
40-room runs retain six >100ms frames each; reverse p99 worsens73.511->75.489ms.
Both maps fail release p95/p99/stall gates. No minimum-target PC or Mac acceptance.
Phase texture counters are endpoint evidence, not within-frame peak certification.

Latest free space C124.37GiB /D81.56GiB. No full PCK copies or automated screenshot
batches produced. Existing frozen PC/Mac deliverables do not contain the later
normal source shadow update.

## Next action

Investigate the reproducible first connected-placement hitch separately from the
large-map visible drone upload bursts. Use the retained worst-frame layer excerpts
and prior rejected floor/wall/cache trials to avoid repeating unchanged variants.
Preserve pixels and complete interactive room presentation. Continue full frame
pacing, memory, bug/endurance, target-PC/Mac and packaging/signing gates. No itch upload.
