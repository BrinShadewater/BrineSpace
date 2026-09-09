# Combined polish and release handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: final polish, GitHub update and playable Windows build

## Objective and acceptance
Integrate the completed local artwork, companions and reliability work, address concrete polish/reliability issues, push the source to GitHub and deliver a tested Windows release.

## Accepted decisions and constraints
Preserve paid construction, failure conditions, hidden discovery, authored layouts and open-ended expeditions. No balance changes, source-art deletion or monolith refactor. The owner authorized committing and pushing the combined completed work.

## Current state
- Includes the closed September 9 art, portrait, room, companion-water, animation and reliability sessions together.
- `scripts/crew_sprite_player.gd` now preserves missing/corrupt frame slots using diagnostic placeholders, keeping subsequent durations, facing and depth metadata aligned. Authored clip duration totals are calculated once during loading; generated clips retain their existing fallback.
- `scripts/title_cover.gd` and `scripts/navigation_badge.gd` use the safe raw-PNG loader. Missing title art returns a drawable fallback before silhouette geometry uses image dimensions.
- `tests/test_sprite_loading.gd` and its UID cover failure reporting, preserved timing/pixels/metadata, generated durations and reload invalidation.
- GitHub source checkpoint: `41a0efdccc167729a4663eaf59ad0774ef8067c7`, pushed to `main` with 1,758 LFS objects (322 MB). CI now imports before script checks and fetches the preloaded OGG music/ambience and polished WAV effects only; the previous pipeline failed to resolve unimported audio/SVG resources.

## Verification
- Release assertion guard and manifest unit tests: four tests pass. Character registry: nine packs, 355 clips, 1,488 frame references, eight portraits, zero errors.
- Gameplay polish, Save/Continue, companion animation expansion, water routing, repair assistance, sprite loading, native sprite polish, reliability diagnostics and native rendering parity pass. Navigation fixture passes at two HUD sizes; station and title captures reviewed.
- Native rendering parity reports zero failures for close/wide cache and culling comparisons. This is correctness evidence; no new whole-station FPS claim. Large fitted stations and long-expedition pacing remain follow-ups.
- The sprite visual fixture was initially launched headlessly, then stopped and run successfully with native rendering. Only the native run establishes its visual check.
- Staged source preserves existing files; raster index blobs remain Git LFS pointers.
- Paid-opening fixture: both controlled one/two-generator stations constructed and survived 300 simulated seconds with costs/failures enabled. One generator spent 274.2 seconds waiting for charging power; two spent zero. No balance adjustment. The headless fixture emitted `2 resources still in use at exit`; gameplay passed, shutdown cleanliness is not established by that run.
- Maintained export: zero errors. Isolated PCK audit: 10,978 raw assets checked, zero missing/changed. Actual Windows release New Game/dialogue continuation/Resume/240 frames/F8/live diagnostic snapshot: zero failures, `debug=false`, no runtime errors or image fallbacks. Native 1600x900 release game/report captures reviewed. Temporary override removed.
- Build `brinespace-445a66b8fe2d337e`, source fingerprint `445a66b8fe2d337eda91a11fb307c2dc3917ecf693ce9701764d2ba54adb3c57`. Runtime source is commit `41a0efdc`; metadata truthfully records documentation edits present at export. Later handoff/CI changes do not change runtime files.
- EXE SHA-256: `6a0266cb7571aa4d437a32094acd353f020c77dcf7ff5a3305ae45d0609e5c20`. PCK SHA-256: `8556107daeaf6e3099ac57ae7a710e1e58f984604414ff6989598d0b2b063214` (5,283,286,532 bytes).
- Evidence: `output/final-polish/`; actual release captures in isolated Godot user data `BrineSpacePolishReleaseFixture20260909`. Source/native tests and release smoke have distinct scopes; no full expedition or all-hardware acceptance is claimed.
- [GitHub CI run 34416831756](https://github.com/BrinShadewater/BrineSpace/actions/runs/34416831756) passed on `2ba79d6b9afec2f4adc6874ec5df67b92998b498`: release guards, selective audio fetch, resource import and every tracked GDScript. The final documentation-only acceptance commit skips redundant CI; runtime and workflow files are unchanged from this verified revision.

## Next action
Playable deliverable: `builds/BrineSpace-2026-09-09-polished/BrineSpace.exe`, with PCK, build_info, README, rights notice and SHA256SUMS. Prior builds preserved. Requested source push, release build and validation are complete. Review normal expedition pacing and dense-station performance next; no further rebuild is required for documentation-only closeout.
