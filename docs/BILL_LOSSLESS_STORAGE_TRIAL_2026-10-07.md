# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: lossless Bill source storage prototype

## Objective and acceptance
Continue the full PC/Mac release/performance plan. Preserve selected art, filtering, complete historical Bill bindings, frame identity/alias graph, animation/save behavior. Memory saving alone does not certify FPS or release.

## Accepted decisions and constraints
Keep Bill prototype isolated, not normal admission. Preserve original BillCarryPlayer class chain and all four historical dictionaries. No archive deletion, art edits, filtering/downscale/frame-count changes or atlas budget increase. Current normal default is MASTER_BINDING; older minimal source-version fixture predates it and lacks inherited states.

## Current state
Private implementation/evidence `output/bill-cpu-storage-2026-10-07/`. Bill subclass overrides only begin_texture_batch using the existing bounded lossless worker. Loader copies exact current Grid._load_major_bill_animations selection function with one constructor substitution (function hash in selection.json). CPU bank adoption includes current/equipment and all carry_banks dictionaries, keeping original CanvasTexture objects and cross-bank aliases; Display scripts route existing native draw APIs. Support primitives copied from accepted frozen private crew candidate; no frozen inputs modified. Bank currently assumes Bill carry_banks and is NOT yet generic combined-provider integration.

Only normal change: tests/test_bill_carry_source_versions_v1.gd uses full normal Grid loading, asserts current reviewed East master default and exercises all SOURCE_BINDINGS. UID retained. Original subset fixture produced incomplete banks and cascading1688failures when expanded; logs retained. The earlier private full-loader test initially failed only its stale Current default assertion; corrected to current normal loader oracle. No normal Bill/rendering/source-selection code changed.

## Verification
Native source/metadata/identity parity28,977checks pass:5,672frame references/3,862distinct frame objects across selected and four historical banks. Entire decoded image bytes, dimensions, formats/mipmaps, per-frame metadata/filter and cross-bank object alias graph match.2,354unique compressed sources/543,183,616raw-equivalent bytes ->40,877,111compressed bytes (~518.02MiB ->38.98MiB); zero generated readbacks. Worker2354jobs/peak8/392pending-content aliases/zero leftovers or unused tasks. These sizes describe source storage, not total process RAM.

Expanded private source-version fixture2123checks pass across four bindings, gear, entry/stow, source-version restoration, future clock and invalid snapshot/bank rejection. Corrected normal production fixture independently2123checks pass/clean. Pixel rendering704nonempty exact pairs/707checks through actual private presenter: all four historical carry banks/body+helmet/source keys first+last frames, inherited nearest/linear, three native Texture2D draw APIs, transforms, tints and transposition.704resolutions/zero missing; presenter close clears active router. Not all live animation/motion/room effects or save/Continue certification.

Three native few-room startup pairs with alternating order: reported textures3107.527 ->2417.063MiB every pair, exact690.464MiB saving; all exits128.863MiB equal/router released/zero missing. One Bill GPU upload at sampled ready endpoint. Ready medians14995.457 ->14559.121ms (~436ms lower); OS caches uncontrolled, development scene loading included, not packaged cold/warm gate. Source format decoded bytes differ from engine texture accounting; do not equate the690MiB engine reduction with543MB source bytes. No frame-time/FPS claim. Same current master binding each lane. Snapshots retained, not yet exhaustively behavior-compared. Normal other crew stay on their existing GPU backend in these startup pairs, so this is not the combined frozen three-crew release.

All successful/failed test processes terminal; every owner fingerprint preserves2936non-log files. Art/layouts/archives/normal runtime unchanged; only normal test repaired. No package rebuilt or published.

## Next action
Integrate Bill into the existing private three-crew bank/router (conditional historical adoption, preserve original selection and existing singleton/lifetime). Measure combined startup and active12/40-room cases. Exercise actual Bill movement/equipment/cargo/entry/stow/save/quit/Continue and all retained source bindings; inspect water/depth/prop draw consumers and memory through scene transitions. Build/audit actual debug=false candidate when justified. Keep source parity/raster evidence scoped; original FPS, loading, peak/lifetime memory, bugs/UI/endurance/targetPC/Mac/signing gates remain open. Do not enlarge drone cache until combined memory headroom is measured and relevant upload behavior comparisons support it.
