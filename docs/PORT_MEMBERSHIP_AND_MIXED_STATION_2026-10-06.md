# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: multi-cell connectivity/performance

## Objective and acceptance

Reduce repeated connection-query work and cover actual multi-cell room workloads.
Preserve port rules, rotation, owner metadata, gameplay and visual quality. Overall
release acceptance remains open.

## Accepted decisions and constraints

Normal `RoomFootprint.has_port` answers one membership query without constructing
the full world-port result list. `Main._ports_connect` uses it in its existing
footprint branches; single-cell fast path, branch-owner and internal-room checks
remain. No cache or geometry/pixel changes. Fallback may still allocate metadata;
do not describe the entire method as allocation-free.

## Current state

Changed `scripts/room_footprint.gd`, two query expressions in `scripts/main.gd`,
`tests/test_port_membership.gd`/paired unique UID and render-perf index.
Original `ports` enumeration remains unchanged as independent parity oracle.
Private evidence in `output/port-membership-2026-10-06/`.

New private 40-room `mixed` fixture includes **12 multi-cell rooms**, using all four
current types: Hydroponics Farm, Storage Depot, Moonbay and Tidal Power Plant.
Existing native single-cell station remains a separate workload. Future release
benchmark coverage must include this footprint distinction explicitly.

## Verification

Actual normal source **14772 checks pass**, including current catalog room/rotation
membership, rectangular/zero sizes, negative anchors, invalid/out-of-hull ports and
non-dictionary entries, metadata preservation. Normal Main script also preloaded
to validate the new call sites; zero parse/runtime errors. Unique UID/index checked.
Three alternating 5000-query large-room pairs: ~28.1–28.7 ms enumeration+membership
versus ~9.5 ms direct query (~66% lower focused CPU time).

The first 40-room fixture contained only single-cell rooms: candidate execution
guard correctly failed. Its completed run is **not optimization evidence** and
remains retained. No normal source was changed to make that fixture pass.

Mixed native 40-room matched comparison, 1080p idle/pan at 1/2/4x, 60 samples:
membership counter 37841→85279 proves candidate execution. Door/light preparation
baseline→candidate ms: 1.749→1.649, 1.745→1.647, 1.757→1.663,
1.776→1.664, 1.770→1.692, 1.796→1.657 (saving ~0.078–0.139 ms).
All six actual crew/drone snapshots, door entries/frames/depth/style, full lighting
keys, powered-room counts, zoom and texture counters equal. Final 3098.402 MiB
unchanged, still above the 3072 MiB large-scene budget. One pair does not establish
aggregate FPS gain. Both fixtures use private compressed crew, not normal release.

Successful logs clean; all 2936 owner non-log files unchanged in direct, native and
guard-failed isolated runs. All processes terminal.

## New material performance finding

Mixed baseline p95 **63.620–80.934 ms**, candidate **62.221–77.645 ms**; both far
above 16.7 ms. Baseline live-room preparation ~17.65–17.80 ms in idle/pan 1x,
versus ~4.24 ms in the earlier single-cell station. Reported global draw calls
~7553–7601 versus ~4836. Area/content mixes differ, so this is not a pure per-room
causal comparison; it exposes workload coverage and a substantial measured lead.

## Next action

Prioritize multi-cell live-room drawing, not further small connection optimizations.
`GridCanvas._draw_room` calls `LARGE_ROOM_VIEWS[room.id].draw` followed by
`LargeStudioView.draw_live` each pass (current source ~2518–2519). Attribute base
art, Studio dressing/effects and crew preparation separately, then retain static
work only where exact output/state invalidation can be proved. Preserve animated
water, doors, equipment, layering and complete bounds. Include mixed-footprint
stations in standard candidate performance gates. Memory/loading, original bug
closure, lifecycle/endurance and actual Windows/Mac release certification remain open.
