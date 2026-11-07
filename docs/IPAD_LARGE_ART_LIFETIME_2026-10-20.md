# iPad large-room image lifetime and memory attribution — October 20, 2026

Validation 2 **brinespace-5004798d302747ec** is installed with the validation-only **on-demand-vm-tags-v1** native sampler. Large-room machinery/floor image lookups now release after the final registered gameplay or Studio owner exits. Native lifecycle accounting releases **40,934,676 bytes (39.038 MiB)** previously retained. Original artwork, metadata and gameplay remain unchanged. This is a scoped cleanup and diagnostic pass, not release clearance.

## Identity and preservation

Active checkout `/Users/Shared/BrineSpace-native-validation-20261017`, branch `codex/ipad-memory-placement-2026-10-17`, HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted work. Selected source fingerprint `5004798d302747ec58bbdbe00e49a09dd1b50d8a56019b3556b25a9ce3b731fb`.

PCK `cfde0442dfb85bf678bab15b2ed8736f5483c59c1846a0ab85ba43e735476de5`; installed signed executable `96d6837bdcbb6c4d34838e0ce776a2e85fe121ba588b0a728382cc9294819997`; QA native sampler `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66`. The native sampler was rebuilt independently of the unchanged candidate PCK, so source/PCK ID alone does not identify this wrapper. Strict signature and app/export PCK equality pass.

Full app/export and local evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261020/large-art-lifetime`. Full4ec previous candidate remains in `opening-surface-staging`; preserve7675/7bb donors and all recovery archives. Frozen published Mac and Windows packages were not rebuilt or modified.

## Change and verification

`session_art_cache.gd` previously removed only large-room aliases matching ordinary floor textures, leaving independently uploaded machinery in `common.gd.art_textures`. Final-owner cleanup now clears that entire lookup behind the existing owner/reference-mode guards. The real native regression initially produced18 expected failures; final43 checks pass, including actual Studio registration, both closure orders, surviving pixels, exact reentry pixels, reference-mode retention and subsequent cleanup. Related shared-floor, session-art26, session-material18 and large-room composition163 checks pass. Four targeted fixtures pass against the actual PCK. Asset audit:36,191 entries, zero missing/changed/unexpected; source audit:438 selected/433 extras, zero missing/changed/unknown. Owner Mac profile guards pass. Scoped code review found no actionable issues.

The existing validation-only native sampler now consumes an explicit request marker and atomically emits aggregate VM categories. It records no addresses, filenames, stacks or memory contents; the normal one-second sampler does no region walk without a request. Leaf/depth/cooperative time limits prevent an unbounded walk. A host regression failed for the missing snapshot, then two tests passed, including detection of a deliberately touched64MiB large allocation and no walk without opt-in. iPhoneOS arm64 compile and signing pass. These files are QA tooling, not automatically linked into frozen/public builds.

## Physical iPad results

A14/4GB iPad13,18, iPadOS27.2. Same disposable normal-rule56-room/four-crew checkpoint, paused at cycle69, profiling off. Last-ten-sample process-footprint medians:

| Phase | Previous4ec | Candidate5004798 |
|---|---:|---:|
| Large station | 2,267.508 MB | 2,324.353 MB |
| Title after save/return | 951.455 MB | 919.769 MB |
| Sampled first-load peak | 2,312.638 MB | 2,355.351 MB |

Title is31.687MB lower in this **one ordered comparison**. Active-station/peak memory did not improve. Large-station setup11.734s baseline versus15.984s candidate; candidate repeat14.637s. No faster loading is claimed, and different process/cache state limits causal attribution. Final owner seven-room setup4.974s is a separate smaller workload, not directly comparable to that table or a controlled historical gain. No new long soak or physical placement/rotation acceptance is claimed for this candidate.

External Game Memory profiling could not attach to the exact fresh PID even though devicectl and the helper confirmed it. Its all-process VM/Allocations fallback is unsupported. Those failures and a rejected incomplete-options attempt remain in local evidence. Do not treat those captures as successful attribution.

The self-only VM sampler completed on-device walks in87–203ms. The largest identified mapped category is **VM tag100, IOAccelerator/GPU driver** (SDK `mach/vm_statistics.h`):850.903MB resident at the56-room station,219.349MB at title,565.428MB in the owner's seven-room station. Corresponding process footprints in these separate diagnostic samples were2,325.319MB,919.703MB and1,770.524MB. **VM resident/dirty counts can alias and are not additive to charged footprint or a complete GPU allocation graph.** Exclude requested walks from timing comparisons.

A separate native Mac/tablet-policy census of named static ImageTexture lookups estimates RGBA capacities of83.95MiB painted shells,78.00MiB corridor wall sheets and71.98MiB floor materials. It deduplicates resource identities, reads no GPU pixels and covers only named caches; these capacities are not actual iPad resident bytes and group totals may share resources. It narrows a future texture trial without establishing its savings. The CPU crew bank's1.624GB decoded total is virtual; its compressed inventory is140.536MB, not proof of1.624GB resident animation memory.

## Owner restoration and next move

Actual iPad Save → title → Continue → Save passes complete gameplay-state parity and the exact1.11834893097652s timer at cycle64/seven rooms/4x. Only save timestamp/event history/path metadata differ in those UI-generated test copies. All five incoming original save/checkpoint files were restored and remain SHA-exact after the final launch and VM snapshot. Owner station is paused4x, menu closed. The healthy four-hour touch helper is retained; use local session-state metadata rather than stale PIDs.

Next, test one bounded iPad texture-delivery change against the largest floor/wall/corridor sources, retaining source PNGs/registrations and desktop behavior. Compare maximum-zoom quality, full-process memory and first/repeat load cost before broad adoption. Godot's [image import documentation](https://docs.godotengine.org/en/latest/tutorials/assets_pipeline/importing_images.html) distinguishes disk compression from VRAM compression and documents mobile ETC2 under Compatibility; high-quality ASTC import is not supported by that renderer. Runtime raw-PNG uploads do not gain from changing unrelated importer flags. Do not switch rendering backends or lower cache budgets without a measured candidate.

[Portable evidence](ipad-memory-placement-evidence-2026-10-20/large-art-lifetime/SUMMARY.json). Current QA workflow documents the opt-in sampler and metadata/footprint limitations.
