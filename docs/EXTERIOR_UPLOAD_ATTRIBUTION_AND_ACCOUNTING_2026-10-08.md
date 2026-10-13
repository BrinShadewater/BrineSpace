# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: identify exterior stall and correct private sampler attribution

## Objective and acceptance

Continue full PC/Mac readiness with exact selected visuals, bounded session storage, owner data isolation and matched runtime evidence. Previous turn made progress through settled visual and three-pair zoom tests. No publication, normal runtime/art change, quality change or engine upgrade in this pass.

## Accepted decisions and constraints

Keep the zoom candidate private; its mixed performance does not close FPS gates. Do not repeat rejected frame cropping, sampling remapping or global512MiB drone-cache trials without a materially different measured remedy. Do not reinterpret texture budgets using a blanket correction factor. Keep historical reports intact and document changed interpretations explicitly.

## Current state

Private `exterior-stage-grid.gd` splits harvest, transitions/construction, per-drone anchors/position/sample/dust/work-heading/draw, and survey timing. Bounded1024 slow events (threshold1ms), current-frame category sums; no changes to drawing math/order/state. First actual40room9phase probe301events/37slow drone-drawing frames. Typical medians: harvest132.5us, anchors12us, position31us, sample31us, dust87us, heading3us, draw120us, survey10us. At idle4x146, exterior30.353ms, drone draws29.997ms; two mining drones draw15.307/14.690ms. The cost is in drawing/upload, not measured anchors/navigation/dust/sample preparation.

**Correction:** private `capture-adapter.gd` still queried `frame_upload_diagnostics()` at the sampler's next process frame. The maintained `tools/release_benchmark.gd` already corrected this on October7; the private master had not inherited it. Thus earlier private "zero upload" observations at idle4x146 do not exclude coincident uploads. Retained latest-upload bucket1407 matches completed driver frame; sampler1408 incorrectly returned zero. The master now records `FrameDriver.process_frame_index`, exposes additive `sampled_process_frame`, and queries that explicit index. Backup and before/after hashes retained. Existing raw reports and ordinary QA adapter remain unchanged.

Aligned second actual probe confirms all1620 driver indices and upload-bucket frames agree, driver index=sampler-1 throughout. At idle4x146: frame61.751ms, exterior29.197ms, draws28.858ms. Two uploads229.6875MiB raw: mine-west-effects2688×13440/138MiB/API10.586ms and collect-south2688×8960/91.875MiB/API11.687ms. First probe same pairAPI23.514ms; aligned22.273ms. These are synchronous graphics API wall intervals, not GPU completion. They account for most measured drone-draw work at this point; do not claim full cause of every earlier>100ms stall.

Aligned workload190 sampled upload frames/9065.195MiB cumulative raw payload/927.070ms API calls; repeated paths include tiny transparent placeholders and dock parts, so count alone is not cost ranking.295 slow-stage events, complete below bound. Existing broad atlas-burst evidence from October7 is confirmed with precise current drone/callee attribution rather than a new discovery of atlas uploads generally.

## Accounting research and verification

Official4.7.2 Compatibility initializer passes a positive mip-level count into `Image::get_image_data_size`'s Boolean mipmap argument when registering allocation bookkeeping; actual texture upload uses image mipmap presence and overwrites local texture size. This suggests an accounting discrepancy for non-mipmapped images, not automatically generated extra image levels. See [texture initializer/upload source](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/storage/texture_storage.cpp) and [Image size signature](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/core/io/image.h).

Native tiny controlled allocations6observations/0failures: RGBA8 without mipmaps4×4 source/readback64bytes but counter+84;16×16 source/readback1024 but counter+1364;48×48 source/readback9216 but counter+12280. Readbacks have no mipmaps. Mipmapped controls report84/1364/12280 matching their source/readback. This supports overcounted bookkeeping in this tested GLES3 runtime; physical driver VRAM remains unmeasured. Do not divide whole-scene counters by4/3, loosen gates, infer M1 results, or claim a memory optimization from a reporting correction. Existing normal monitor scope already warns to calibrate and avoid a global correction, so no normal change needed.

First accounting fixture attempted C++-only `texture_debug_usage`, which is not script-exposed; compile failure/log preserved. Corrected six-case probe uses source/readback metadata and counter deltas. Small diagnostic readbacks are outside gameplay/performance samples.

Both actual probes and corrected native accounting are terminal/clean in accepted runs. Owner2936files unchanged, physical adapter restored byte-identically. GPUqueryfalse/focused/released router, same2348.739303MiB peak/228.259212MiB exit/4297crew uploads in both actual runs. New data are diagnostic, not candidate FPS acceptance. Disk~36MiB free; no full export. Evidence under `output/renderdoc-tools-2026-10-08/{exterior-stage-probe,exterior-stage-aligned,texture-accounting-native,texture-accounting-native-readback}`; private master backup/hashes and analysis/generators alongside. No art, archive or selected input deletion.

## Next action

Rank repeated upload payload/API cost by path and first-use versus reload. Test a bounded session-owned retention policy for costly repeatedly used sheets (rather than globally enlarging the cache), with an explicit texture budget/lifetime guard. Preserve the original ImageTexture, full PNG dimensions/UVs/filtering/material/layer order; prove actual reuse,12/40room memory, exact pixels and settled scene exits before admission. If it cannot meet both memory and pacing gates, keep the failure explicit and choose a materially different exact-storage remedy. Whole-frame baseline geometry/preparation and every original bug/endurance/platform/package gate remain open.
