# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: large-room prop preparation keys

## Objective and acceptance

Continue the full PC/Mac performance plan. Avoid repeated deep comparison/copying of unchanged supporting prop lists while preserving authored edits, live effects, clock behavior, rendering order and resource lifetime.

## Accepted decisions and constraints

Normal change admitted for a consistent measured preparation reduction. Studio's cached runtime prop lists are read-only; layout edits go through Store and invalidate its revision. Identity also detects a replaced/cleared cache without a revision bump. No art, texture storage, quality setting, gameplay, owner layouts or engine changes.

## Current state

- `scripts/large_room_canvas.gd`: Props keeps the shared list identity beside a scalar key (room/rotation/revision/rect/operating). Drops the prop list from the deep snapshot and per-frame equality comparison. Existing preparation, wet fallback and live advancement unchanged.
- `rooms/large-rooms/studio_view.gd`: documents the existing shared read-only list contract.
- `tests/test_large_room_retention.gd`: existing paired UID/index retained; extends native coverage with dry/wet moved, resized, mirrored, hidden, deleted, restored and replaced-cache supporting props using scratch Store saves.
- Artifacts: `output/large-prop-key-2026-10-06/`. Private copies, normal controls, logs, paired comparison and retained station capture. No export/upload/commit.

## Verification

Private current-normal mixed40 pair preserves all six full crew/drone/door/light/power/zoom states, texture endpoints and prop prepare/advance/static/live draw counts. Preparation callbacks decrease645→476,645→460,634→472,661→467,660→473,652→480us across six phases: consistent saving0.162–0.194ms. Retained prop painting and renderer CPU remain essentially unchanged. Whole-frame p95 is mixed and remains38–53ms; no FPS gate or loading/memory gain claimed.

Private dry composition and corrected wet composition each149 checks/87 exact raster pairs clean. Installed normal test163 checks/94 exact pairs, zero failures/errors/leaks/warnings. Covers four rooms, rotations, nearest/linear filtering, modulation/materials, overlapping room order, clock advancement/static retention, flooding/offline state, layout edits, cache replacement, culling/hide/show/remove and container ownership release. Station screenshot retained and inspected. All2,936 owner files unchanged, all native handles terminal. Scoped whitespace clean; existing script UIDs preserved.

Initial edit extension queued its empty candidate reference host after wet prop configuration. That host's reference-only hide helper then hid all wet nodes. Original normal control reproduced seven failures; captures showed missing supporting props. Corrected test ordering to queue hosts before slot configuration, as the original fixture does. Both wet control/candidate pass; no normal wet rendering fix inferred. Failed fixture evidence retained. Initial performance copy also duplicated GridCanvas's global class name; exact failed candidate process stopped, temporary class declaration corrected, and only candidate rerun. Invalid results excluded.

The private benchmark and installed native composition establish this localized change; not three-run packaged performance, actual title/Continue endurance or Mac acceptance. No new runtime dependencies, so no new asset-selection change; refreshed package audit remains pending with other accepted source changes.

## Next action

Prioritize larger retained prop painting/room preparation and renderer submission costs, with matched workloads. Continue private crew/drone residency/full-room admission. Original normal frame/memory/loading gates, nine packaged reports, two-hour large soak, refreshed Windows release and actual Mac certification remain open.
