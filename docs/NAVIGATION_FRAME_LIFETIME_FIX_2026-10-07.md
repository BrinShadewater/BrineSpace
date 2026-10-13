# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: remove navigation frame retention across scenes

## Objective and acceptance
Continue full PC/Mac readiness; investigate the36,840byte repeated texture rise without changing selected art/UI. Fix only proved ownership defect, verify pixels and release-runtime transitions. All other release gates remain open.

## Accepted decisions and constraints
Navigation processed frames belong to live UI callers. A lookup may reuse live results but must not own every discarded scene's copy. Keep default hull skin, panel/accessibility choices, source PNG loading, frame processing and filtering. Combined crew storage stays private; this small normal ownership fix does not admit that prototype or certify a delivery package.

## Root cause and change
Actual debug=false three-fresh-main attribution: `NavigationBadge.plain_frames` retained3/6/9 distinct48×48 processed textures; exited texture memory128.863051/128.898185/128.933318MiB. Each scene introduced three new source instance IDs, while the static dictionary strongly retained all processed results. Their increase exactly matches the previous36,840byte per-transition rise.

`scripts/navigation_badge.gd` now stores WeakRefs to processed results and removes expired lookup entries on use. Live callers still share the same processed resource; final caller release frees it. Image processing, base pixels/mipmaps and the tiny-source fallback remain unchanged. Unused weak metadata is pruned on subsequent calls; it does not keep GPU images resident.

Normal files changed: navigation_badge.gd; new tests/test_navigation_frame_lifetime.gd plus paired UID; tests/index.json UI group/native lane registration; tests/test_navigation_badges.gd fixture alignment. Preserve all unrelated earlier modifications in those files.

## Verification
Focused real native resource test: valid red run35checks/3 failures, exactly final-caller release for both mipmap cases and tiny source. Initial fixture parse-type error corrected before valid red evidence. After fix35checks/0failures/clean. Checks dimensions/mipmap state, source immutability, exact highlighted/unchanged rows, live-result identity, final-result/source lifetime and null input. Registered native lane verified by maintained runner listing.

Existing navigation test exposed historical fixture assumptions: bitmap-only StyleBoxTexture cast, fixed520px inspector after retired guide in small window, hardcoded scroll-grandparent. Temporary live probe showed actual custom shared ui_hull_style; current source uses a readable responsive inspector and fixed controls. Fixture now retains bitmap pixel assertions when applicable, checks actual shared hull skin otherwise, retired-guide/readable inspector behavior and reachable controls with optional scroll ancestor. Failed attempts/probe logs retained; owned errored engine processes stopped before reruns. Final native test exits0/clean, covers badge bindings, disabled/idle redraws, camera/window centering,1600×900 and960×540 layouts, diagnostics/journal actions and title capture. Both HUD captures reviewed; no full nine-report or motion acceptance. No game layout/design changes made to satisfy the fixture.

Actual release uses separately hashed tiny badge script overlay, loaded before Main/Badge; no script reload. Three fresh-main exits retain zero processed frame textures; exited texture memory128.827918MiB exactly equal allthree. Owner2936unchanged/QA adapter restored/process terminal.

Actual debug=false full candidate follow-up: same active40room9phase workload followed by ten paused43room/four-crew disk/staged restores (three real recovery wards, as prior accepted fixture). All restored room/crew dictionaries equal,0missing/router released each exit, clean logs. Every restored equivalent state exactly2067.386243MiB; warm exited states and final exit exactly234.533917MiB. First exit231.952271MiB precedes one-time warming, not an equivalent warm state. Previous per-transition rise is absent. Render-boundary peak2348.994739MiB(~2.294GiB),1468samples/probe4700us total/max18us. No within-frame/driver VRAM or two-hour endurance certification.

Matched previous/fixed40room crew/drone/doors/light/power/zoom/largeprops state has zero drift; texture endpoint unchanged. Frame-time result remains above60FPS gate; no FPS improvement claim for this small memory fix. Measurements and source/overlay/adapter/basePCK/EXE identities retained under `output/all-crew-storage-2026-10-07/{badge-retention,badge-overlay,badge-retention-fixed,navigation-tests-*,packaged-memory-lifetime-badge-fixed}/`. Final comparison.json retains scoped frame results. All owner checks2936unchanged; all processes terminal and QA adapter restored.

## Remaining work and next action
Normal source fix verified; retained full delivery PCK still predates it, diagnostic overlays are not a fully audited new candidate. Continue12room memory coverage and a bounded drone working-set experiment with measured upload reduction/peak/lifetime/pixel/state checks. Room redraw bursts also remain. Full frozen candidate/PCK audit, original nine bugs, normal title/Continue order/input/scale checks, two-hour resumed native soak, target PC and actual Mac/signing/notarization gates remain open.
