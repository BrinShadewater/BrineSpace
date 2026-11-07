# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: room-phase prefetch investigation

## Objective and acceptance

Reduce remaining first large Continue latency without changing selected pixels, animation clocks, filtering, save state or default quality. Keep bounded workers/decoded memory and session release. Full original PC/Mac gameplay, memory, bug, endurance and certification scope remains active.

## Accepted decisions and constraints

Investigate missing versus repeated requests before changing scheduling. Trials are private in the existing physical frozen source, restored byte-exactly afterward. No normal runtime admission or export/upload. The observed test-station request list is diagnostic input, not a production room registry.

## Current state

Evidence under `output/drone-compiled-2026-10-07/`: `restore-order-images*`, `restore-order-sequence-images*`, `room-order-state-summary.json`, `room-phase-observed-paths.json`, `run-room-phase-prefetch-trial.py`, reference/fast and missing-guard reference/fast logs/results, plus loading summaries. Existing navigation release `5760e46d67c3376b` is unchanged.

## Verification

- Prefetch-state trace: 52 room-geometry PNG calls; 25 misses reference paths absent from the prior startup order, 9 misses revisit known paths no longer available, 18 hits. Twenty-one distinct paths are unknown. One 262-check trace and one 182-check sequence trace clean; owner files unchanged.
- Four-job phase prototype replays actual observed request order, including repeated paths; old outstanding jobs/results are joined/discarded before its bounded queue. Existing PNG decode/upload behavior and source-path identity retained. No permanent image cache.
- Unconditional original/fast native three-cycle pair: 262 checks each, no errors/leaks/warnings. All 12 complete crew snapshots and texture endpoints match. First Veld restore 1836.041→1568.919 ms; total first large Continue 7943.554→7804.849 ms. Later Continue 5853.528→6635.470 ms regresses; unconditional phase scheduling is rejected.
- Missing-path guard pair: 262 checks each, clean; all 12 crew snapshots/texture endpoints match. First Veld restore 1902.526→1518.452 ms; total first large Continue 8043.760→7709.097 ms. Later 5636.715→5820.095 ms remains mixed. Warm worker submissions 12,820 and unused results49 match exactly between lanes; first-restore unused76→36/submissions12,749→12,712. First total decoded-worker peak95,415,252 bytes and later110,421,636 bytes equal between lanes. This is whole-startup peak, not an independently instrumented phase peak or GPU memory. The trial's unused phase-peak field is not valid measurement evidence.
- Native ordered local pairs, OS cache uncontrolled; no packaged/60-FPS/Mac/hardware gate closure or claim that the previous548ms is fully removable. Source restoration and owner fingerprints verified: 2,936 files unchanged. All processes terminal.

## Next action

Replace the observed fixture list with actual selected-room source discovery. Consider bounded metadata collection from real room-view image requests, including runtime placement after startup, so a later Continue knows new room paths; metadata may retain paths, not images. Preserve complete trained orders, handle repeated/evicted requests and stale metadata, and prove first-load/warm behavior, pixels, peak/waste, pause ownership and packaged comparisons before admission. Complete independent edge fallback/layout admission and title-memory investigation, then remaining original release scope.
