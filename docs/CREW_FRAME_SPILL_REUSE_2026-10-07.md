# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: eliminate repeated same-frame animation spill uploads

## Objective and acceptance

Reduce proven redundant image decoding/upload work in the exact-pixel compressed-crew prototype while preserving retained canvas poses, complete interactive overflow, selected pixels/filtering/timing and save state. Full original PC/Mac release scope remains active. This is a private backend change, not normal source admission.

## Accepted decisions and constraints

Retain immutable orphan spill images only until the current rendered frame ends. Reacquiring an unchanged pose within that frame reuses its pixels; frame_post_draw erases only spills with no holders. Retained canvas commands continue holding their images. Final-owner exit still immediately clears all storage; Router close disconnects the new frame callback. No permanent asset cache or automatic quality change.

## Current state

Private candidate `output/crew-spill-reuse-2026-10-07/slots-candidate.gd` and `router-candidate.gd`. Slots removes eager orphan erase from clear_leases and adds finish_frame; Router connects/disconnects it at its existing start/close boundaries. Probe/benchmark use physically selected flood helper rather than runtime script reload. Temporary selected Slots/Router/flood files restored after each native process, UIDs untouched. Normal source/art remain unchanged.

Generators/runners under `output/compressed-crew-2026-10-06/`: `trace-spill-reuploads.py`, `validate-frame-spill-reuse.py`, `compare-frame-spill-reuse.py`. Original/candidate bytes, adapters, logs, reports and owner fingerprints retained. During first pair the generated Router used CRLF while byte restoration guard expected LF; corrected only newline representation after verifying text equality, and runner now writes exact bytes. Final restoration guard passed; no behavior change or invalidated measurements from this formatting correction.

## Verification

- Instrumented native40-room/15-phase trace:3,249 resolutions/2,532 uploads;1,936 spill allocations,1,910 discards,711 same-epoch reuploads/147,771,136bytes (~140.93MiB) repeated data;865 later-epoch reuploads,360 first uploads,217 hits,26 live spills. Bounded diagnostic table356 keys, no overflow; peak live spill payload3,664,128bytes. Trace changes counters only, not retention; no FPS acceptance from instrumented timings. Evidence `output/crew-spill-trace-2026-10-07/{report,summary,owner}.json`, native.log and traced source.
- Candidate native selected Veld validation14,482 checks/0failures:4,788 exact multi-pose raster pairs across three scales, integer/half-pixel origins, tint/alpha and clipped regions;33 exact overflow scene pairs. Complete source bytes/dimensions and consumer mutation isolation, retained pose across other-canvas redraws, overflow replacement/no history accumulation, last-owner GPU release.16 additional unchanged spill redraws skip upload and keep one leased spill. This does not replace full James/Marsh/Bill/flood/Studio consumer coverage.
- One uninstrumented matched native40-room busy pair,15 phases ×60 frames each, idle/pan/zoom/lighting/interface at1/2/4×: complete crew snapshots, action/speed/zoom/powered count/drone phase state equal in all15 phases. Zero missing routes/art/errors/warnings/leaked-instance reports. Uploads2,533→1,820 (713 fewer/~28.1%); end26spills,4slots and2,619.398MiB reported textures equal. Per-actor distinct presentations and selected immutable payload unchanged.
- Median across15 phase means32.613→32.880ms; p95/p99 mixed. No reliable FPS improvement established; frame gates remain failed. No repeated-pair or packaged/hardware/Mac claim. Source cleanup at frame end reduces redundant work but is not a further steady memory reduction.
- Owner2,936 non-log files unchanged for trace, validation and pair. Temporary source bytes restored; current processes terminal. Engine counters are not physical driver VRAM; no reset of acceptance budgets.

## Next action

Keep as preferred private spill candidate; no normal backend admission until broader retained-room, selected crew/flood/Studio consumers and large scene exit coverage. Repeat workload comparison only if pursuing an FPS claim or resolving regression concerns; present evidence proves deterministic avoided uploads and limited raster/behavior preservation, not60FPS. Prioritize measured compressed startup cost and larger steady rendering hotspots; do not spend further tuning on this smaller path without new evidence. Full original bug/UI/motion, two-hour native soak, target PC/M1, packaged performance/memory/loading and Mac signing/notarization certification remain open.
