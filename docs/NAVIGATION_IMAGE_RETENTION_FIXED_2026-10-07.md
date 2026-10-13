# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: navigation image retention

## Objective and acceptance

Release unused room GPU images after scene exit while preserving useful navigation topology, collisions, activity approaches, rendering quality and save state. Full original PC/Mac performance/release gates remain active.

## Accepted decisions and constraints

Do not clear the whole navigation cache or materialize lazy images for diagnostics. Release only the drawing-only `library_texture` field after the final gameplay/Studio owner exits. Preserve owner layouts, selected art, timing, normal gameplay decisions and paired UIDs. No upload authorized.

## Current state

Normal `scripts/session_art_cache.gd` now removes cached navigation prop image references after the existing final-owner gate. Cache keys, points, links, blockers and remaining prop metadata stay resident. `tests/test_session_art_cache.gd` adds overlap, release, topology/metadata and reload coverage; tests/index.json describes it. Existing UIDs retained. Native and actual-package evidence retained under `output/drone-compiled-2026-10-07/navigation-retention*` and `navigation-images-wired*`. Retained5760e46d package predates the source cleanup.

## Verification

- Actual debug=false three-cycle read-only inventory:263 checks clean. Cached navigation data holds8 GPU images at first title and52 after large restore. Base RGBA8 size estimate19.789→51.091MiB; estimate is not exact format/mipmap accounting or physical VRAM. Inventory reads stored ImageTexture/ArtSource.loaded fields only, deduplicates RIDs, no readbacks/lazy getter calls; no truncation.
- Actual package controlled title purge:668 checks, zero errors/leaks/warnings. Removing11 image fields at first title reduces reported textures284,542,643→263,176,429bytes; removing110 fields at large title303,870,117→266,430,247bytes (~35.7MiB at that boundary). Third purge removes0 fields. All12 recorded full navigation graphs and complete crew snapshots match untouched control. Collision rectangles and activity approaches match before/after removal. After subsequent Continue, reported textures58,806,084bytes (~56.1MiB) below control; save/fleet checks pass. This is a measured component remedy, not whole-game budget closure.
- Installed normal native ownership regression:22 checks, no errors/warnings. Surviving owner and reloaded pixels exact; final owner releases images/worker queues; navigation metadata, blockers, points and links remain; new drawing images do not refill old nav snapshots.
- Real source-wired native three-cycle title/save/Continue:262 checks clean, title textures250.985/254.088/254.623MiB, no old owner/library images. This confirms the exit hook, not new packaged certification. Remaining title growth is not explained or closed by this component fix.
- Owner's2,936 non-log files unchanged in every run; QA adapter restored byte-exactly and frozen diagnostic sources restored. All processes terminal.

## Next action

Refresh/audit an actual release candidate containing cleanup and verify longer large-station transitions, including remaining small title growth. Consider enforcing texture-free navigation snapshots at creation only after wider metadata/activity coverage; current accepted exit cleanup is sufficient to avoid cross-session duplicate ownership. Complete navigation-edge fallback/layout admission and combined compressed-provider memory/rendering work, plus original loading/FPS, bug/UI/motion, two-hour soak, target hardware and native Mac release gates. No public release readiness claim.
