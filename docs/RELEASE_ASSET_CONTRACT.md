# Runtime asset and release contract

Use this alongside the visual bible and subsystem production contracts. It records delivery requirements; dated handoffs record the particular build that passed.

## Load safely

Godot release exports remove assertions, including argument evaluation. Never put image decoding or other required work inside assert(). Use scripts/safe_image.gd for PNG consumers that require a drawable texture; preserve deliberate optional-resource skip paths and caller checks. Missing/corrupt art must produce a deduplicated diagnostic and a drawable placeholder, not a null-texture crash. A placeholder is failure evidence, never accepted artwork. Keep raw PNG loading and LFS source storage.

## Build the selected dependency graph

Run `powershell -ExecutionPolicy Bypass -File tools/export_release.ps1` from the checkout (override Godot, ProjectRoot and OutputPath when needed). It regenerates the Windows Game resource list, raw manifest and build identity before export; reject export errors even if an executable was emitted.

Track script/scene references, JSON-relative animation frames, dynamic directory prefixes and imported resources such as .tres controls. Never treat a bare res:// reference as permission to package the repository. Prune generated/build/cache directories before traversal. Reject LFS pointers. Keep source art and provenance even when they are excluded from the playable package.

When source changes concurrently, freeze scripts, manifests, configuration and their matching dependency closure together. Resolve selected assets against those frozen bindings. Record exclusions and build fingerprint. Use explicit text encodings; preserve legacy document bytes rather than silently transcoding them.

## Verify the delivered runtime

Use the actual release executable, not an editor engine loading the PCK. Exercise title, New Game, Continue, intentional dialogue pause, Resume and active frames. Keep free-building/failure overrides confined to dedicated fixtures. Check F8 diagnostics, build identity, separate unsaved live snapshot and unchanged player checkpoint. Editable source must not claim an old packaged identity.

Audit the PCK from outside the checkout against expected asset hashes so local files cannot mask omissions. Read invocation and scope in tests/release_new_game_smoke.gd and tools/audit_release_assets.gd before use. Preserve paired executable/PCK, build_info, rights notice and checksums; remove temporary test overrides from the deliverable. A byte audit does not prove native appearance, motion or owner acceptance.

## Optimize without changing the picture

Profile the active phase, actual room count, viewport and zoom on the same frozen input. Report frame time and remaining limits. Cache complete structural output with orientation/state keys and layout-revision invalidation; keep doors, actors, power and clocks live. Give culling an art-overhang margin. Compare cached/uncached and culled/unculled geometry plus close/wide native captures. Pixel parity protects existing appearance; it is not new aesthetic approval.

Current implementation evidence: [September 9 reliability and performance](RELIABILITY_PERFORMANCE_2026-09-09.md).
