# iPad floor texture storage trial — 2026-10-20

Scope: nine offline ETC2 floor Images at original dimensions, only on supported iOS renderers. Source PNGs, room geometry, desktop loading and fallback behavior remain intact. Three of twelve pilot sources failed the conservative quality gate and remain PNGs (corridor floor, cargo anchor, service grating).

Derived assets and measured codec error are in `assets/tablet-floor-vram/manifest.json`. Each resource embeds its original path/hash. Export preflight rejects changed source or derived bytes; derived binary Images use Git LFS. The loader holds no Image/Texture cache and uses ResourceLoader CACHE_MODE_IGNORE; the existing drawing-session caches own uploads. Surface preparation jobs are consumed normally, including when their decoded PNG is superseded by derived storage.

Nine compressed payloads total 7,098,912 bytes versus 42,457,932 source-decoded RGB bytes (56,610,576 bytes RGBA capacity). These are storage capacities, **not measured device memory savings**. RGB error gate: MAE ≤2/255 and PSNR ≥38 dB; alpha MAE ≤0.5/255 and maximum error ≤8/255. A magnified image review and physical rendering check remain part of acceptance; numeric error alone does not guarantee visual equivalence.

Native regression: new trial fixture failed before implementation, then passed 31 checks for policy/fallback, every source hash, logical dimensions, actual decoded texture pixels, shared upload in both orders and final-owner release. Related shared-floor, opening-surface (12) and large-art lifetime (43) fixtures pass. Export manifest regression failed for binary Images, then all 11 manifest tests passed after `.res` selection was added without binary text parsing. Preflight fault injection rejects modified source and resource bytes. Scoped read-only review found no actionable issues.

The Mac renderer expands unsupported ETC2 to RGBA; forced native fixture results establish pixels/lifetime only. Physical iPad13,18 / A14 / 4 GB, iPadOS27.2: renderer reports ETC2 support; all nine resources served, 7,098,912 cumulative payload bytes per fresh process. Same paused56-room/four-crew checkpoint69, original preferences restored before each fresh comparison:

| Run | Process footprint MB | VM tag100 mapped resident MB | Setup ms |
|---|---:|---:|---:|
| Previous500/VM1 | 2271.776 | 850.805 | 10321 |
| f729 trial first | 2229.293 | 798.884 | 15967 |
| f729 PNG reference flag | 2327.335 | 850.919 | 16051 |
| f729 trial second fresh process | 2237.190 | 798.605 | 16105 |

The same-package off→on comparison lowers mapped driver pages by52.314MB and process footprint by90.145MB. Earlier installed-baseline comparison lowers process footprint42.484MB; allocator/cache variation prevents treating either process delta as a fixed saving. Driver pages may alias, are not a full GPU census and must not be added to footprint. VM walks are diagnostic and excluded from setup measurements. Zoomed rendering inspected: no obvious alignment, transparency or prop changes. Lossy fine-grain differences remain; this is validation acceptance, not a blanket approval for more artwork.

No total-loading improvement. UI/grid construction remains about8s with the trial both disabled and enabled; staged surfaces about1.6s. Repeat scene entry setup14.497s used the zoom saved by the preceding title transition and is **not** a matched RAM comparison. Title footprint918.917→928.698MB in the ordered old/new comparison; mapped driver pages189.121→188.989MB. No title-memory gain claimed. No new long soak, leak clearance or release clearance.

Actual touch card selection/return clears placement controls; serialized state confirms selected/hovered IDs empty, identical hand/rooms/resources and56 rooms. An initial UI checker incorrectly expected an empty inspector after return; the state comparison resolves selection independently of preview rendering. No game fix was made for that checker expectation. Actual owner cycle64/seven-room Save→Title→Continue→Save: complete serialized state equal and exact timer1.11834893097652s;4× reselected after the existing Continue1× reset. Final normal-policy launch restores all five original save/checkpoint files SHA-exact, station paused4× with menu closed and no selection. Final breadcrumbs: errors0, ETC2 supported/enabled, six compressed floors served. Owner setup5.385s is a separate seven-room workload. No new placement/rotation or long-soak clearance is inferred from the storage tests.

Installed candidate `brinespace-f729a310f8bdf68c`, source SHA `f729a310f8bdf68cf397acb9652dcb7fbc9a80355963568671fab0a98f2e4269`; PCK SHA `ff70c78c2c88e78970c26bf1409bbd9a15a509fdefb037cc418a377da7acd5d2`. Signed executable `4c65bce7df2e0120044b9bc936ffad831159324f19944acc5041ac1af91e3605`; native sampler SHA `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66` (on-demand VM tags v1). Source remains branch `codex/ipad-memory-placement-2026-10-17`, starting HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus prior accepted uncommitted work. No commit/push/merge or public release change this pass.

Actual-pack checks:31 floor trial,43 lifetime, shared-floor,26 session-art and18 session-material checks pass. Raster audit36191/zero issues, source audit439 selected+433 extras/zero issues; separate binary audit verifies all nine derived resource hashes. Strict signature and export/app PCK equality pass. Native tests protect the real Mac profile. Portable evidence is under `docs/ipad-memory-placement-evidence-2026-10-20/floor-vram-trial`.

Next: retain this bounded trial for validation; instrument UI/grid construction on the large checkpoint before attributing the loading pause. Expand any floor/wall/corridor storage trial only with separate RGB/alpha quality gating, real-device serving and matched memory evidence.

Local evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261020/floor-vram-trial`. Baseline: installed `brinespace-5004798d302747ec` plus on-demand VM sampler v1. First export omitted binary assets and is explicitly rejected; replacement export `brinespace-f729a310f8bdf68c` passed actual-pack audits and is installed. Frozen Mac/Windows releases and the prior validation/rollback packages are unchanged.
