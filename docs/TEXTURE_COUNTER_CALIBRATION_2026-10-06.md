# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: texture ownership and counter calibration

## Objective and acceptance

Continue full PC/Mac release readiness. Explain the private collection trial's memory discrepancy before changing cache retention or judging memory gates. Separate known pixel payload, engine accounting and actual driver VRAM. No quality reduction, engine upgrade or global budget correction.

## Accepted decisions and constraints

The release gates remain open. Do not divide total game texture memory by4/3: imported/compressed textures, genuine mipmaps, render targets and untracked resources need their own accounting. Do not describe a counter interpretation as memory freed. No normal crew/drone provider admission this milestone.

## Current state

- New maintained `tools/texture_memory_calibration.gd` and unique paired UID. Refuses headless or mismatched isolated profile, allocates R8/RG8/RGBA8 at64×64,448×448,2688×8960 with/without mipmaps, records known image bytes and engine counter deltas, verifies release to baseline. Writes only `user://texture-memory-calibration.json`; classifies observed counter models without requiring the current discrepancy to persist in future engines.
- `scripts/performance_monitor.gd`: additive snapshot `texture_memory_scope` clarifies engine-reported allocations versus physical driver VRAM; existing numeric fields unchanged. No recurring calibration, readback or per-frame traversal.
- Private ownership audit and all evidence: `output/drone-normal-cache-2026-10-06/ownership/`. No normal cache/art/gameplay changes.

## Verification

Actual mixed40 twelve/sixteen provider diagnostic lanes preserve all six full crew/world states, no art errors or selected duplicates, clean native completion. At final endpoint simulation stops for eight rendered observations; full crew/fleet states remain equal to pre-settle, memory stays constant. Complete crew/room pool inventories identical in both branches (2,354 crew storage records/543,183,616bytes;30 room records/182,419,284bytes).

Drone-specific unique ImageTextures traced through both caches, live weak bank wrappers, canvas pins, command slots and retained palette uniforms. Control448.846MiB versus candidate495.646MiB. Noncached held palettes only0.131/0.175MiB: no large hidden drone command backlog in this boundary. Scope excludes engine-only RIDs and non-drone resources; inventories retain numeric/string metadata only, no GPU pixel readback. Stopped engine totals2,715.111/2,777.705MiB, so deferred rendering cleanup does not remove the difference.

Native allocation control: all18 cases show the engine counter equals complete mipmap-chain size even when supplied Image reports `has_mipmaps=false`/count0. Examples:64×64RGBA8 payload16,384bytes reports21,844;2688×8960RG8 payload48,168,960 reports64,225,216. Genuine mipmapped controls report the same full-chain bytes; every allocation returns exactly to baseline after release. No errors/warnings/leaks.

Actual Windows release executable with `debug=false`, older frozen build `brinespace-3429e7142ba143eb`, independently reproduces all18 cases and exact release-to-baseline. Guarded QA adapter temporarily replaced and restored byte-for-byte; not current packaged gameplay or release certification. Installed maintained tool passes18 cases with `gl_compatibility`/Godot4.7.2. All54 allocations across these scopes clean, all2,936 owner files unchanged. Performance monitor unit passes, JSON report serialization retained; scoped whitespace/UID uniqueness checked. All handles terminal. Initial ownership probe indentation parse failure preserved and corrected before valid lanes.

Applying full-chain accounting to the audited drone images predicts engine delta65,429,988bytes versus observed65,634,080bytes: remaining204,092bytes (~0.195MiB) outside this ownership scope. Actual decoded-image delta49,074,192bytes (~46.80MiB). This resolves nearly all of the previously unexplained gap; it does not prove every engine texture or driver allocation accounted.

Primary source corroboration, not exact local revision proof: Compatibility initializes `texture.mipmaps` as image mipmap count+1 and passes that integer into image size accounting; R8/RG8 map to their corresponding GL formats. Native/debug=false observations establish the local counter behavior. [Godot Compatibility texture storage](https://github.com/godotengine/godot/blob/master/drivers/gles3/storage/texture_storage.cpp).

## Next action

Return to measured remedies: shared provider residency and remaining dock/full-room/flip/type/fallback acceptance before normal admission, plus sustained preparation/rendering above16.7ms. Use raw counter and decoded inventories side by side; calibrate other runtimes separately. Full normal memory/loading/frame gates, original nine packaged reports, large endurance, refreshed exports and actual Windows/Mac certification remain open.
