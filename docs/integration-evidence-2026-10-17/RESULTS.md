# iPad compact animation storage — October17,2026

Build brinespace-5f31e258a2e19ec5. Follow-up to confirmed physical-iPad2867MB memory-limit exception during PNG decoding.

## Implementation

Generate302 compact drone hull/effect/cargo sheet records (246 unique derived PNGs) from current runtime manifests. Remove only per-frame transparent padding with a1pixel border, no image rescaling; generator checks retained RGBA pixels exactly and verifies alpha outside retained area is zero. Original files remain intact and both original/derived hashes guard fallback. iPad-only selection reuses cropped frame renderer and limits GPU frame cache to6frames per sheet; retained draw commands keep leased frames valid. Source dimensions remain virtual-original dimensions. Previous single-pending-decode and64MiB reusable-cache policies retained. Recent/live leases can exceed cache budget. Desktop selection/cache behavior retained. Added ~403MiB derived storage on disk in exchange for lower runtime allocations.

Worker policy is captured on the main thread and passed to background decoding; workers do not access SceneTree nodes. An earlier compact-build benchmark exposed this bug and is superseded. Do not install /Users/Shared/BrineSpace-iPad-compact-build. The later compact-final-build was installed as an intermediate but not launched for handoff; a retained-frame lease issue was found and corrected in this delivery build. Both intermediate folders are superseded.

## Measurements and validation

Full generator --check:302records, all visible pixel roundtrips valid; original aggregate decoded19,257,622,528B→compact5,931,156,048B,69.2% reduction across that asset set (not all resident simultaneously and not total app RAM). Example mining hull144,506,880B→46,085,760B; effect144,506,880B→413,280B. Six small GPU frames are retained per used sheet.

Final exact-PCK isolated two-sheet native Mac benchmark, sequential identical inputs: peak process resident635,879,424B→390,184,960B (~38.6% lower). Cache payload289,013,760B→48,049,008B after drawing20frames. This is a focused loading workload, not a physical-iPad whole-game measurement. Initial broad synthetic-cache benchmark peak was dominated by its other allocations and did not establish a saving. Initial worker-error benchmark is invalid and superseded by clean thread-safe pair. Device Activity Monitor capture could not attach toPID3000; no physical footprint claim.

Native hull/effect/construction cases pass: full-scale first/mid/last-frame comparisons and flood shader exact; scale0.1/0.3/0.73 exact, scale0.5 differs only at nearest-neighbor half-source-pixel choices (7383hull/11effect/3646construction changed pixels in representative captures), zero unexplained pixels against nine exact/half-pixel source references. Half-scale hull comparison inspected; geometry/placement retained, fine sampling details differ. Do not claim byte-identical fractional rendering. Physical iPad appearance acceptance pending.

Final exact-PCK native memory/worker/pending-job/cache regression, compact hull render/hash rejection/desktop guard,252clip/144directional-phase drone checks, and lifecycle refinement (Save/Continue, station centering, real touch dialogue Close, title/menu recovery) pass0failures. Refinement retains previously isolated34RefCounted shutdown warning from intro threaded preload. Full derived assets/hash audit passes; independent review found no important issues after worker fix and scaled checks.

Signed Release compilation and strict codesign verification pass; signed-app PCK hash matches tested export. Asset audit36,188checked with0missing/changed/remapped/unexpected. Runtime manifest36,432→36,679paths,247added (catalog+246derivedPNG), none removed; only drone_animation.gd/drone_cargo_storage.gd existing runtime hashes changed. Original art/audio/save/game-rule files unchanged.

## Device delivery

Existing checkpoint copied read-only before stoppingPID3000 for update. Installed/launched final delivery normally on physical iPad; PID3045 present afterward. LLDB attached and resumed (PTY25128) for owner test. Physical longer-play memory stability and visual acceptance remain pending; no claim that overall memory-limit termination is eliminated.

Evidence: this directory and /Users/Shared/BrineSpace-iPad-compact-evidence.
