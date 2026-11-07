# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: identify61MiB exception and zoom stall

## Objective and acceptance

Identify retained images behind the repeatability exception and discriminate uploads from CPU redraw work before changing cache policy. Preserve renderer pixels, simulation, cached interactive commands and owner saves. Entire original PC/Mac release scope remains active.

## Accepted decisions and constraints

Read existing ImageTexture metadata, lookup accounting, stored canvas pins and viewport sizes only. Do not force lazy image loading, read GPU pixels or evict during inventory collection. Engine texture accounting is a gate counter, not driver VRAM; no blanket4/3 correction. Controlled allocation/removal probes are separate from unchanged-inventory runs.

## Current state

Driver `output/compressed-crew-2026-10-06/trace-large-texture-retention.py` copies current private benchmark and adds bounded phase metadata plus existing frame trace. Evidence under `output/large-local-retention-2026-10-07/texture-trace/`: candidate/control reports/logs, attribution.json, benchmark and owner. Scope covers ordinary drone lookup/pin images and SubViewport size/update mode; not all fonts/UI/room/crew GPU resources. Tree walk capped12,000 nodes; rows only retain scalar metadata/owner names, no image references. Collection occurs after each phase's measured samples (~0.986–1.135ms).

Later gameplay removal probe and isolated allocation probe under trial `stale-release-probe/`; drivers `probe-stale-drone-release.py`, `probe-stale-allocation.py`. Normal source/art remain unchanged. All processes terminal.

## Verification

- Fresh native40-room/1080p candidate-first traced pair, idle/pan/zoom1/2/4×,60frames/phase: all9 full recorded crew snapshots/drone dictionaries/door/light/zoom/power/phase states equal, no missing art/errors/warnings/leaked instances. Inventories untruncated. No duplicate pinned images by source path found in either sampled inventory.
- Exception reproduces **exactly** at zoom2×: candidate+64,225,188reported bytes; other8 endpoints equal. Cache difference consists only of unused `res://assets/mining-rover-v1-2026-09-26/tyres-v2/atlases/steer-right-west.png` (2688×4480,RGBA8,48,168,960decoded bytes) and `res://assets/mining-rover-v1-2026-09-26/atlases/steer-right-west-effects.png` (optimized invisible1×1,4bytes). Both age18 frames. Candidate cached decoded771,277,716 vs control723,108,752bytes; candidate stale48,168,964 vs control0. Current canvas-pin image descriptors/lookup association and viewport dimensions equal. These extra lookup entries are not current recorded pins; no missing drawing ownership inferred elsewhere.
- Full mip-chain integer accounting for that2688×4480 allocation is64,225,184bytes, plus placeholder4 equals observed delta. Image metadata has no mipmaps; this numerical correspondence alone is not actual VRAM or mip allocation evidence. **Independent isolated real-source probe** confirms reported allocation64,225,188 and reported release64,225,188 after removing lookup owners, weak image refs expire and exact baseline returns. This corroborates source attribution without adjusting gate counters.
- In-game diagnostic unused-entry removal at the same later phase does **not** encounter the entries in that run: removed0, released0; complete crew/drone state remains equal. Preserve this result; it is not a successful production eviction remedy. Its timing/history differs, showing exception is conditional. Isolated allocation probe proves component ownership, not full-game pixel/eviction-policy correctness.
- Control zoom4× frame12 **104.037ms** repeats earlier104.846ms at same action/sample. New trace:4.542ms step,87.213ms before-render,12.139ms render-signal interval,.113ms after-render; measured render CPU11.86/GPU9.234ms are separate scopes. Latest drone upload frame662 vs sample674; no coincident drone upload. Earlier detailed row reports~69.949ms aggregate draw callbacks/269callbacks (not269 full grid rebuilds), with floor/wall/terrain/live-room work. Scopes overlap; do not sum them or infer an exclusive engine/driver cause. Candidate traced run has0frames>100ms; one lane does not certify absence of stalls. All>50ms traces retained for further classification.
- All runs preserve2,936 owner non-log fingerprints; isolated user path checked. No normal source/provider/large-base admission, exports, FPS certification or changed user settings.

## Next action

Prototype pruning over-budget lookups that have become stale after rendering, retaining images needed by current/retained canvases. Measure later upload/decode churn and prevent duplicate storage on reacquiring an image still held elsewhere; do not replace cache cleanup with destructive image mutation. Validate pixel/ownership/reload behavior and equivalent phase sets before normal admission. Stop treating this exact exception as an unknown large-room image allocation, but keep broader memory/FPS gates open. Independently target the larger pre-render zoom floor/wall/room/terrain redraw burst with matched callback attribution and complete interactive visual retention. Full original bugs/UI/motion/endurance, target PC/M1 and Mac signing/notarization certification remain open.
