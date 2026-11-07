# Project handoff

Updated: October 9, 2026 - Project: BrineSpace - Task: water-worker visibility and reverse check

## Objective and acceptance

Continue full PC/Mac optimization/release readiness. Worker preparation must retain
current-frame pixels/timing,release resources during hiding/removal and demonstrate
matched net pacing improvement. Keep prototype private;release gates remain open.

## Accepted decisions and constraints

Two numeric jobs maximum,no SceneTree/GPU/image/simulation work on threads.
Exclusive buffer/topology ownership until joined,current input-key match and sync
fallback,stationary cache preserved. No normal source change this turn.

## Current state

Native visibility/settings test reproduced2failures/598checks:pending work remained
when an ancestor hid the room,and hidden submit scheduled new work. Private base
now joins/discards on NOTIFICATION_VISIBILITY_CHANGED when invisible in tree and
checks visibility before scheduling. Green598/0,including return-current-image and
4reduced-motion transitions,prior288sequential raster pairs/material/filter matrix,
latest-input invalidation and immediate-exit joins. Intentional red artifacts kept.

Visibility-safe actual debug=false1080p40room/fourcrew/full-mission reverse pair:
worker-first then reference,3000idle frames each1/2/4x. Correct saved-byte canvas
hash is used in both runs,no validator repair this pair.

| Speed | Mean ms direct -> workers | p95 ms | p99 ms |
|---|---|---|---|
| 1x | 40.800 -> 38.638 | 46.631 -> 45.248 | 58.082 -> 58.262 |
| 2x | 41.977 -> 39.308 | 50.006 -> 47.465 | 60.572 -> 65.886 |
| 4x | 43.203 -> 40.322 | 57.593 -> 54.328 | 78.872 -> 73.025 |

Mean/p95 improve3/3 but p99 worsens2/3;worst frames worsen all3. Candidate max143.828ms
versus141.189ms. Earlier first-order prototype pair gain5.66-5.89ms is not a guarantee;
current reverse gain2.16-2.88ms. Different visibility-safe revision is identified,
not silently treated as byte-identical across both historical pairs.

All compared endpoints/final mission histories equal.6238starts==joins,peak2/active0,
all3missions return/unload/fullgraphs recover. End memory1916.471/exit228.259MiB match;
workerpeak2408.880 vsreference2346.502MiB repeats prior+62.377MiB difference. No
memory/no-growth claim. Worker cumulative wait37.666ms includes warmup;per-frame
wait data missing,so cannot attribute tail regression to waits from that aggregate.

Worst2x candidate frame600115.103ms:step1.389ms,scriptdraw96.385ms,321.563MiB current
frame drone uploads. Reference sameframe105.700ms/draw86.424ms/same upload bytes.
Other high tail frames align with large uploads;one reference frame75 has42.101ms
simulation work/zero current uploads. These are attribution leads,not proven worker
causality or GPU-stall diagnosis. Full tail excerpts retained in evidence JSON.

Evidence:D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/
water-worker-render/(hidden-red/current native artifacts),water-worker-visibility-reverse/
(comparison.json,tail-excerpts.json,source identities and actual logs). Normal source
unchanged;checkout changes this handoff and CURRENT_STATUS.md only.

## Verification

Native red598/2fail -> green598/0,actual reverse clean/debug=false/focused/source and
branch proofs pass. Actual profiles isolate/copy owner layouts;all2936non-log owner
files unchanged,all processes terminal,adapters restored/router releases. No identical
third-run/full interaction/endurance/Mac or complete prop/owner visual acceptance.

## Next action

Keep workers private. Add per-frame worker start/join/wait and transfer-byte/count
attribution with bounded overhead;compare worst frames to upload/retention events
and diagnose repeated texture peak increase. Validate unchanged-room pause and
actual layout/prop transitions. Accept scheduling only if matched pacing/retention
results justify it;better means alone do not close stutters. Continue independent
upload/navigation and full release requirements. No upload/public package change.
