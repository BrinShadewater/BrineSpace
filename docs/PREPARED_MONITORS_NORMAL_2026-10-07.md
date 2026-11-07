# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: prepared monitor geometry

## Objective and acceptance

Continue full PC/Mac performance readiness. Reduce the measured live monitor drawing cost without changing pixels, clocks, default quality, layering or filtering.

## Accepted decisions and constraints

Typed slot-owned geometry admitted; dictionary implementation rejected for negligible gain. Only the existing simple library path uses preparation. Mirrored layout transforms, custom/portable artwork, aquarium/drone registrations and non-station artwork keep their existing fallbacks. Dynamic waveforms, bars, radar sweeps and effects keep original clock arithmetic and draw commands. No frame thinning, textures, global caches or art changes.

## Current state

- New `scripts/prepared_library_screens.gd` and unique paired UID: typed invariant colour/width, screen boxes/category/inner geometry; original dynamic drawing arithmetic.
- `scripts/room_content_canvas.gd`: retained slots own prepared data and its item identity; changed-item submission clears it. Simple station drawing uses prepared monitors and the original registered effects. Existing painter clearing and counters preserved.
- `tests/test_library_live_context.gd`: confirms the prepared path executes and its data releases with the slot; existing UID/index retained.
- Evidence started October6: `output/prepared-screens-2026-10-06/`. Dictionary source preserved separately, typed/native/installed results and read-only manifest selection retained. Existing dirty source changes preserved; no export/commit/upload.

## Verification

Dictionary version:510 checks/406 exact screen/effect pairs across179 actual registrations and163 checks/94 exact full-room pairs pass cleanly, but actual-normal mixed40 painting changes are negligible/mixed. Rejected.

Typed version: same visual scopes pass. Actual-normal mixed40 matched six-phase pair preserves full crew/drone/door/light/power/zoom states, texture endpoints, simple paint counts and large prop preparation/advance/static/live counts. Large prop painting improves0.067–0.102ms; ordinary prop painting0.055–0.138ms across every phase. These are disjoint callback groups, total reduction0.122–0.238ms/frame. Renderer CPU remains broadly similar; draw commands remain unchanged. Whole-frame p95 mixed~37–54ms; no60FPS, loading or memory improvement claimed.

Installed source:512 checks/406 exact screen/effect pairs,179 registrations;163 checks/94 exact full-room pairs. Zero failures/errors/leaks/exit warnings. Covers clocks, reduced motion, operating state, inherited nearest/linear/flood behavior, copied IDs, layout-mirror fallbacks, actual registrations, overlapping rooms, dry/wet movement/resize/mirror/hide/delete/restore/cache replacement, culling and container release. Prepared geometry weak reference releases with slot. All2,936 owner files unchanged; all native handles terminal.

Read-only full release selection36,244files includes helper through RoomContent. Runtime UID exclusion is intentional; source pair preserved. Unique UID and scoped whitespace checked. No refreshed executable/PCK audit. Initial typed private member indentation parse failure corrected and excluded; prior dictionary experiment remains archived.

## Next action

Prioritize larger renderer submission and remaining room preparation costs; consider ordered static coloured polygon aggregation in cached large-room water only after exact native geometry/blend checks and measured gain. Continue private crew/drone residency and full-room admission. Normal frame/memory/loading gates, original nine packaged reports, endurance, refreshed Windows candidates and actual Mac certification remain open.
