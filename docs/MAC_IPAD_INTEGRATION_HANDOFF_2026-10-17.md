# Mac/iPad integration handoff — 2026-10-17

Branch: `mac-ipad/integration-handoff-2026-10-17` (preservation branch; not merged).

## Starting point and preservation

Base Git commit: `67e7db969f7c5d952a3c80830369715d703199c5`.
Actual starting input was **not a clean checkout**: `BrineSpace-source-d3cfa1890bafefe7.zip`, 3,757,232,963 bytes, SHA256 `157b4ae797be415cce09b63cefeae02a4a798a7d9b04aa697b913cbde3f3de53`. Its runtime fingerprint is `d3cfa1890bafefe7e5b1a8c4e3f4f01f52e19d1e250701c27832d52b675e7514`. It includes accepted Windows working-tree/Save changes and documented test overlays. See original `SOURCE_PROVENANCE.json` and `MAC_TEST_KIT/Context/BUILD_AND_SOURCE.md`.

The first branch commit anchors that source-kit overlay onto the recorded base; the second preserves subsequent Mac/iPad work and this handoff. Files omitted by the kit remain from the repository; none are deleted. Kit line endings are preserved, so its anchoring commit includes substantial line-ending-only changes. Use `git diff --ignore-space-at-eol` for review. `docs/integration-evidence-2026-10-17/source-kit-anchor.json` records the anchor commit; `source-kit-delta.json` separates later edited/new code from kit content.

Working source preserved from `/Users/Shared/BrineSpace-iPad-QA-source`. Frozen original Mac packages, archives and release candidates were neither edited nor regenerated. Generated caches, SDKs, signed apps, provisioning/private keys, player saves and local output directories are excluded by repository rules. Raster/audio/movie additions use the existing `.gitattributes` Git LFS filters; no LFS history migration or original artwork replacement.

## Changes preserved

- Mac Escape deselects the active room during gameplay. Bare F7/F8 required a **machine macOS function-key preference**, not a portable game remap; Fn+F7/F8 already worked. Main-menu Escape behavior was clarified by the owner.
- iPad-only Compatibility renderer/export tooling, distinct QA bundle `com.shadewater.brinespace.ipadqa`, background save/pause and recovery from end-loop menus; iOS Quit is hidden/guarded.
- Pinch zoom/two-finger pan, two-finger tap rotation, visible room actions, drag blueprint back into hand to cancel; emulated mouse ordering/canceled touches guarded. Touch scrolling for archives/dialogue/settings and larger cards/HUD/menu controls; iPad settings omit PC options, Layout Studio disabled. Station centers after New/Continue. Intro Skip button; dialogue blocks room placement and restores selection after closing.
- iPad drone memory policy: one pending decode (including completed/unconsumed work), 64 MiB reusable cache instead of desktop 256 MiB; changing visibility drains jobs. Compact storage for 302 sheets/246 derived PNGs removes transparent frame padding with no rescaling, guarded by source/derived hashes and original fallback. Six reusable GPU frames per sheet plus explicit retained-canvas leases; worker policy captured on main thread. Desktop selection/cache policy retained. No intended game-rule/save-format or original art/audio changes.

## Validation and devices

MacBook Air Mac16,12, Apple M4/24 GB: native Mac launch/audio and owner Save/Resume/room/resource/crew checks; source and exact-export regression fixtures for touch dispatch, rotation, scrolling, layout, lifecycle, card dragging and menu recovery. Latest exact-PCK memory/worker/cache, compact rendering/hash/fallback/frame leases, 252 drone clips/144 phase checks and Save/Continue refinement passed. Full compact generator roundtrip/hash checks passed for all 302 records. Signed iOS Release compile, strict codesign, tested/signed PCK hash equality and asset audit (36,188 assets; zero missing/changed/remapped/unexpected) passed.

Physical iPad 10th generation (iPad13,18/A14/~4 GB), iPadOS 27.2: installed/launched iterative builds; owner confirmed audio after disabling Silent Mode, usable play, pinch/pan, larger cards/buttons and room rotation. Latest installed build **`brinespace-5f31e258a2e19ec5`**, runtime SHA256 `5f31e258a2e19ec5f4381d7aaaa8b16e569b0a8d1ece69f3206949ed9059c3ff`, installed/launched normally and debugger resumed. Latest memory pass awaits extended physical play/visual acceptance. No Windows testing of the merged work and no simulator acceptance claimed.

Isolated native Mac two-sheet loading benchmark: peak RSS 635,879,424 → 390,184,960 bytes (38.6% lower); **not total physical-iPad RAM**. Derived set aggregate decoded bytes 19.26 → 5.93 GB (69.2% lower; not simultaneously resident). Native full-scale/flood comparisons exact; fractional half-scale can choose adjacent nearest-neighbor source pixels. Packaging-time verification checks all 36,679 installed-build runtime paths against this integration copy: zero byte/hash mismatches. Prior tests are archived evidence, not newly rerun gameplay acceptance.

## Outstanding / Windows reconciliation

1. Windows has **additional uncommitted optimizations not present here**. Preserve them on their own branch before combining. Compare against the source-kit anchor, then reconcile overlapping runtime/renderer/cache/Save code deliberately; do not replace either tree wholesale. Revalidate Windows desktop policy and Mac/iPad native behavior after merging.
2. Prior iPad failure was debugger-caught `EXC_RESOURCE` memory high-water limit 2867 MB during worker PNG decoding. The apparent freeze was debugger suspension. Current optimization is installed; long-play/repeated room placement stability and measured whole-game physical footprint remain unproven. Active live texture leases may exceed reusable cache budgets.
3. Latest iPad layout and compact-animation visual acceptance pending. Half-scale sampling is not byte-identical. Known refinement fixture shutdown warning: 34 RefCounted objects from intro threaded preload. Desktop fixtures retain previously documented ObjectDB/resource exit warnings. Strict-guard invisible-cache fixture exited 2 and is **not claimed passing**.
4. Reconcile export presets/team/local SDK paths for the integration environment; never commit signing secrets or ship these QA artifacts as a public release. The local derived data adds about 403 MiB on disk.

Portable evidence: [integration-evidence-2026-10-17](integration-evidence-2026-10-17/), including latest RESULTS, exact-PCK logs, measurements, source provenance and packaging verification. Larger original local evidence/builds remain `/Users/Shared/BrineSpace-iPad-compact-evidence` and `/Users/Shared/BrineSpace-iPad-compact-delivery-build`; historical evolution is in `docs/CURRENT_STATUS.md`.
