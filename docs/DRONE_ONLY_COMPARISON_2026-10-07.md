# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: current-source drone-only comparison

## Objective and acceptance

Continue full PC/Mac performance readiness. Separate lossless drone storage from private crew storage, preserve normal flood code, and measure actual station states, upload pacing and memory before normal admission.

## Accepted decisions and constraints

Provider remains private. Normal runtime, art, owner data and frozen Windows candidate unchanged. Use current normal Main/Grid/crew/player code, with only drone exterior grouping, dock content/session and guarded zoom preparation adapted. No private flood reload or crew player injection. Previous goal turn was progress:1,516 exact native dock/room pairs, two private loader/cleanup fixes and current lifecycle evidence.

## Current state

`output/drone-only-2026-10-07/`: current-source adapter generation, private Main/Grid/scene, corrected benchmark, initial and complete-inventory matched results, summaries. Uses fixed sixteen-source provider from previous handoff. Existing normal large-room drawing fallback remains; this comparison does not optimize every possible owner-placed large-room dock.

Guarded `_prepare_zoom_art` chooses original Dock when palette mode is off and only creates an indexed session when enabled. Current crew and flood functions remain untouched. Exterior before/group/after ordering retains harvest, scrap/construction, dust/body and survey/admin order. Dock and exterior share one session. No normal admission, export or upload.

## Verification

Two native1920×1080 matched current-source pairs:60 idle/pan frames at1×/2×/4×, six phases each. All full crew/drone/zoom/power/door/light states equal. No missing art/errors/warnings/leaks or selected-source ordinary cache duplicates. Final station candidate capture inspected; all owner checks2,936 files unchanged and all handles terminal.

First pair: p954× idle55.861→44.196ms, pan52.153→44.533; frames>50ms8→4, max75.096→53.440ms. Earlier phases mixed38–40ms. Initial allocation inventories disabled; their equality check cannot prove unchanged allocations. Results preserved, no allocation claim based on this pair.

Second pair explicitly enables complete pool inventories and compares sorted resource records, excluding collection timing. Crew8,188records/1,610,154,592decoded bytes, rooms30records/182,419,284bytes exactly match control. No changed crew/room allocation explains the drone delta. p954× idle61.111→42.627ms, pan52.447→44.357; frames>50ms10→2, max69.488→55.056ms. Earlier phases remain mixed38–43ms. This is not the three-run release matrix or debug=false package certification.

Both pairs have identical texture deltas across six phase endpoints:−61.04/+31.04/+92.29/+92.29/−275.14/−258.62MiB. Thus final memory improves but intermediate residency worsens. Candidate ends4,131.23MiB raw engine texture counter, still above gate; no global mipmap correction applied. Final indexed cache277,317,632bytes plus ordinary242,221,988bytes. Indexed cache is all recent; ordinary cache includes145,309,712stale bytes. Current `trim_idle_storage` checks combined pressure but evicts only stale indexed entries, leaving this ordinary tail. Working-set overage is not permission to evict recently drawn resources.

Candidate cache totals15indexed uploads/67.791ms plus25ordinary/39.194ms in first pair. Counts/timings are prototype bookkeeping, not all driver allocations or a matched release upload total. Renderer calls and steady CPU/GPU timings broadly similar; persistent60FPS deficit remains. Ready time not controlled cold/warm and no loading-gate claim.

## Next action

Implement and test combined oldest-stale eviction across both caches, preserving the two-frame protection and live command ownership; use the current drone-only baseline, not old combined crew/drone timings. Measure whether it removes intermediate memory regressions without adding reuploads/stalls. Retain original image/fallback behavior, source-to-encoding build validation and larger lifecycle coverage before normal admission. Then refresh packaged comparison against build1a4d5f698ed2d862. Full benchmark matrix/issues/endurance/target hardware/Mac and steady-frame gates remain open.
