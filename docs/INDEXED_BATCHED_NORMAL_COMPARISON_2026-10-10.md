# Project handoff — combined private provider versus normal game

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Compare batched lossless indexed+bounded collection preparation against CURRENT ordinary
RGBA game, with representative framing. Previous turn established a private-provider
batch improvement, not a whole-game gain. This turn completes that required comparison
and tests one scoped overhead remedy. Full original release gates remain open.

## Accepted decisions and constraints
Native debug=false Windows/RTX4070Ti/1080p, muted secondary window. Scratch resolved
APPDATA, owner fingerprints and20GiB refusal floor. Corrected fitted camera, independent
actions, explicit zoom; no normal source/art/delivery installation or full package copies.

## Current state and verification
Three alternating pairs per saved12/expanded40; idle/pan/zoom/lighting1x/2x/4x,
90frames/phase,12,960measured frames. Reference=current accepted normal RGBA source;
candidate=batched twenty-source indexed+prewarm private provider.

| Map/lane | Mean ms | p95 ms | p99 ms | Max ms | >50/>100 | Peak MiB |
|---|---:|---:|---:|---:|---:|---:|
| Saved12 normal |12.741|19.557|23.044|27.196|0/0|1558.872|
| Saved12 candidate |13.029|19.051|22.983|30.886|0/0|1528.343|
| Expanded40 normal |25.870|43.246|54.378|81.126|57/0|3028.007|
| Expanded40 candidate |26.212|43.403|53.528|80.719|51/0|2629.355|

All six candidate pair means slower:2.27%saved12/1.32%large40. Memory saves30.529/
398.652MiB, but no overall mean win. Neither lane samples >100ms: prior legacy-camera
stall reduction does not reproduce in this corrected protocol. p95 fails both maps,
large p99 fails. Provider remains private; no optimization or release admission.

All72phase camera start/end snapshots exact; gameplay matches outside6cached Branforth
phase floats at1xzoom/lighting (two phases per large pair). Other playback fields exact.
Example3.18191861970263vs3.18191864698747,5.28841170125816vs5.288411728543:
about2.73e-8phase difference. Explicitly recorded, not normalized to claim raw equality;
this is no certification of all animation timing/pixels. Saved36full states exact.
Successful reports assert20selected sources/factory active, no selected original cache
duplicates or fallback draws, all rooms in view at phase start, input disabled/muted.

## Scoped overhead experiment
All twenty encoded source paths are mining-rover artwork, yet private room-content.paint
handled every room paint and wrapped construction/salvage docks too. New PRIVATE override
returns non-prop items to normal paint before registration lookups, and handles only
mining docks. Existing indexed groups release/hide on those other paths to avoid stale
commands on reused slots; normal rendering draws unconverted props. No game logic or
selected-pixel generator changes. Resources in indexed-targeted-dispatch-trial.

One pair/map, private batched provider before/after targeted dispatch,4,320frames:
- Saved12 mean13.035->12.835ms, p9518.691->19.815/p9922.388->23.136ms;
  peak1528.343MiB both.
- Large40 mean26.343->26.123ms, p9542.569->43.289/p9951.455->52.658ms;
  max86.744->71.053ms, peak2629.926->2629.355MiB.
All24full gameplay and camera pairs exact. Mean improves~0.20/0.22ms, tails regress;
single pair and no new dispatch pixel/lifecycle acceptance. Do not substitute these
private comparisons or cross-run normal averages for matched admission evidence.

All jobs terminal/config restored. Two owner guards2,938 unchanged.195.05MiB new
evidence+scratch/no full PCK copies; C126.90/D77.89GiB free. Evidence under
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/indexed-batched-vs-normal-maps
and indexed-targeted-dispatch-preliminary:comparison.json, per-run JSON/log/PNG and
storage-summary.json. Existing batched-provider108check/36pixel-pair evidence remains
scoped to its prior implementation, not this new routing behavior.

## Next action
Verify normal routed construction/salvage/non-prop images and reused-slot cleanup; measure
remaining palette-material/state churn before another renderer change. Then repeat current
NORMAL-vs-targeted candidate12/40 with this framing, three pairs. Preserve default effects,
linear/flood/unsupported fallback and scene lifetime; finish art/motion/loader/lifecycle
checks before installing anything. Broader frame pacing, loading, target hardware, endurance,
original bug register, latest PC/Mac frozen packages and nativeM1/signing/notarization remain.
