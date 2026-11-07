# iPad retired equipment demand loading — October19,2026

Status: installed as Validation 2. Seventeen actual-pack fixtures, actual touch and Save/Continue pass. The planned 20-minute soak ended after 10.14 active minutes through normal crew loss. Not release-cleared.

## Identity and scope

Active checkout `/Users/Shared/BrineSpace-native-validation-20261017`, branch `codex/ipad-memory-placement-2026-10-17`, HEAD81b2f9a4a36eb0e3162d86ccfb4e9ef735836122 plus accepted dirty work. No commit/push or public delivery. Frozen Mac/Windows releases unchanged. Current candidate **brinespace-da3bbf15d037ac91**, bundle `com.shadewater.brinespace.nativeoptimization20261017`.

- Source SHA-256: `da3bbf15d037ac91681436b71b27406513e76b545b2e2d4f0364ba4bbdc5db68`.
- PCK SHA-256: `f54dfb2b660c5654867c53b06aa05d3d587dfd2902054e8a83ba32d9f9b03066`.
- Signed executable SHA-256: `655148993d074ed93f686f2f653ddfe6d2b7bf668eb41a42152fcf42101d97cc`.
- Immediate complete tested rollback6c362d6f692b2d6f remains in `station-first-frame`; complete7bb44e16b7f164d3 remains in `texture-residency-pass` as a recovery donor. Keep both.

## Attribution and change

The prior first-draw PNG census and source review showed Storage Bay, Mining Drone Bay and Solar Array decoding and uploading retired equipment sheets after their parent setup, bypassing the existing tablet-only lazy source policy. Three call sites now use inherited `set_life_texture_source` instead of immediately creating ImageTextures. The established getter preserves exact source pixels and dimensions on fallback demand; desktop/editor remain eager. No artwork, geometry, simulation, navigation, renderer or worker policy changed.

The export manifest has exactly the same paths as6c; only those three production scripts changed. New native fixture `test_tablet_equipment_sources.gd` and paired UID are registered in tablet-memory/native lanes.

## Verification

Native regression failed on3intended eager-upload assertions, then passed. It checks desktop/editor behavior, geometry, all4rotation fallback pixels, lazy source pixels/bounds and upload reuse. The initial mining comparison needed a second explicit redraw to compare settled rendering; the corrected baseline still failed only those3storage assertions before production edits. Related legacy-room suite passes. Scoped independent static review found no actionable findings; runtime evidence is separate.

Frozen native owner station pixels are exact (`98066f5377f1d16c3d500ebc945c0aa66806cf53399f8a1a16416ba96d41699d`). Native texture counter740.478→722.488MiB, **17.990MiB lower**. This is texture accounting, not proven total iPad RAM savings or first-redraw latency clearance.

Seventeen actual-PCK fixtures, full asset/source audits and strict signing passed. All4temporary export configurations restored byte-exact. New package installed with all5incoming save files SHA-exact before/after installation. Incoming primary checksum differs from prior6c final snapshot, but full native `state` and exact timer are identical: cycle64/seven rooms,4×, timer1.11834893097652, water0; latest incoming files are protected rather than replaced by older metadata.

Normal physical iPad13,18/A14/4GB/iPadOS27.2 observations: setup3968ms, repeat3220ms; first redraw2264.393ms with1,750,916us grid draw still remains. Physical station peak texture counter752.763→734.773MiB: the same17.990MiB reduction as native.122nominal1Hz normal-process samples peaked1,782,549,760bytes. Prior prepared crew disk cache and prior synthetic activity retained; one ordered observation, not a controlled whole-load or sustained whole-process improvement. The manual report logged0errors.

One clean packaged synthetic pass completed9phases/5,400frames (234.179sampled-frame seconds), idle/zoom/placement at1/2/4x. Every phase retained all40–42current rooms in view. Sampled process peak1,976,667,536bytes/end1,916,636,536; maximum measured frame483.015ms. No missing-art failures; no blanket logged-error claim for this first pass, which did not retain an error-counter snapshot. It is a method-driven free-build/failure-bypass fixture, not actual touch or normal simulation acceptance. A second pass was intentionally interrupted when renewed Apple authorization put the app in the background; exclude it from timing/memory acceptance. Its finally handler restored all5incoming files exactly and removed the QA marker. The loop coordinator was stopped after that cleanup; it did not finish its earlier900second repeated-render target.

The helper was then authorized successfully; retain healthy2hour helper22142. Normal loading/Continue was tested through actual UI. Following evidence is the planned normal-rule 20-minute, 40-room disposable soak, not the excluded repeated-render target:

The normal-rule fixture reached cycle193 from65 before its only crew member died. Actual Expedition Report screenshot confirms ordinary gameplay termination, not an app crash; errors0. The planned20active-minute target was **not completed**: endpoint-counted active time608.555s (10.14min), wall675.917s,648nominal1Hz memory samples. Peak2,148,961,872bytes/end2,126,270,008; first/last60second medians2,036,559,332→2,115,505,720bytes (+78,946,388;58samples each).39sampled active latest-frame buckets: median20.323FPS/minimum1.354FPS, maximum frame2116.460ms. These are sparse bucket observations, not a full-run FPS distribution. Memory growth and long frames remain open; no leak clearance or sustained RAM improvement is established.

Normal gameover removed the disposable primary/backup saves. Other fixture files and the final session were captured; no terminal full-state Save exists. An attempted native inspection of that missing save was stopped and excluded. The last active bucket retained40rooms; the Expedition Report showed0crew. No replenishment, revival or failure bypass was used to extend this test. Owner originals remained protected off-device throughout.

Actual UI checks passed: card return removed placement selection, pinch changed saved zoom, rotation saved as1, Codex drag exposed new entries, and background/activate returned paused. Saved rooms/resources/hand/cycle/crew/speed and exact timer remained equal. Two-finger pan/tap are not supported by this helper and were not retested.

Controlled Save → title → Continue → Save passed complete state dictionary and exact timer equality (cycle64,7rooms, speedindex2, timer1.11834893097652); only path/event history/save timestamp differed. All five incoming originals were then restored and verified SHA-exact **after final launch**. Owner station is paused4×, menu closed, actual PID36082. Healthy helper22142 retained.

## Rejected evidence and workspace retention

The first export ran out of space; its903MB truncated pack was hashed/recorded then removed. Logs retained in `failed-space-export`; all4source configuration files restored byte-exact after the error before the successful retry. The first rendering run was rejected: the intentionally stopped app's generated recovery dialog paused the input-disabled workload, which failed its settle deadline. Original5files unchanged; marker removed; owner restored. That attempt remains in `rejected-render-recovery-dialogue`. The harness now preserves and clears only the generated session lock immediately after verifying and intentionally stopping the exact validation process. Unexpected stopped/crashed processes do not pass that guard. Game recovery behavior is unchanged.

Superseded e8af/title/card-staging/diagnostic-wrapper packs were recovery-archived with complete reconstruction hashes verified; named7bb donor stays complete. Those removals reduced logical size but initially freed little physical space.57inactive generated scratch crew caches were removed (2,611,440,808logical bytes), sibling profile files hash-verified unchanged.5,269byte-identical report copies were consolidated into hard links (11,177,670,128logical duplicate bytes); every report path and unique content retained. Source, saves, frozen/current/rollback binaries and unique evidence remain safe. Recovery instructions are beside each archived package and in `/Users/Shared/BrineSpace-workspace-cleanup-20261019-consolidation`.

## Limits and next work

The prior6c normal owner load still measured3.984ssetup /2.382sfirst redraw. That unresolved pause remains a target; this change removes a narrower source of unnecessary uploads. Follow remaining floor/shell/environment decoding and draw preparation. Synthetic method-driven workloads with free building/failure bypass cannot certify normal failure behavior, organic multi-crew play, actual touch or leak clearance. No release clearance is implied by texture counters, source checks or signing.

Full evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261019/legacy-equipment-demand`.
