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

## Verification
- Release assertion guard and manifest unit tests: four tests pass. Character registry: nine packs, 355 clips, 1,488 frame references, eight portraits, zero errors.
- Gameplay polish, Save/Continue, companion animation expansion, water routing, repair assistance, sprite loading, native sprite polish, reliability diagnostics and native rendering parity pass. Navigation fixture passes at two HUD sizes; station and title captures reviewed.
- Native rendering parity reports zero failures for close/wide cache and culling comparisons. This is correctness evidence; no new whole-station FPS claim. Large fitted stations and long-expedition pacing remain follow-ups.
- The sprite visual fixture was initially launched headlessly, then stopped and run successfully with native rendering. Only the native run establishes its visual check.
- Staged source preserves existing files; raster index blobs remain Git LFS pointers.

## Next action
Create the combined Windows release using the maintained exporter, audit the PCK from an empty directory, exercise actual release New Game/Resume/F8, review captures, record package identity and push the final handoff.
