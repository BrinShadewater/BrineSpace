# Project handoff — representative benchmark camera

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

Later correction: save actions below executed commands but did not establish checkpoint
writes. Fixture flags made RunSave reject writes; the action ignored failure. Actual
write/readback checks and corrected large-site seeding now pass in
[real-station verification](REAL_STATION_PERFORMANCE_2026-10-10.md). Earlier large
figures retain their original fixture scope and are superseded for current comparisons.

## Objective and acceptance
Ensure release workloads measure a visible station and independent camera actions,
including zoom and construction, before judging renderer candidates. This is benchmark
correctness, not a gameplay FPS optimization or release certification. Previous turn
progressed through current-renderer indexed+prewarm comparisons showing memory/stall
benefits but slower means; that candidate remains private.

## Accepted decisions and constraints
Native debug=false reused Windows runtime, RTX4070Ti/1080p, muted secondary display.
Resolved scratch APPDATA and owner fingerprints, 20GiB free-space refusal threshold.
No owner camera/layout/save changes, no full build copies or release upload.

## Current state
Changed tools/release_benchmark.gd only; existing UID preserved. Initialize fit AFTER
window size/container geometry settles. Fit full recorded room footprints. Restore a
fitted camera before each action, using current room bounds after layout changes.
Previously each phase inherited the preceding pan endpoint, drifting across speeds.
Geometry snapshots report start/end scroll, zoom, viewport, full/intersecting room counts
and per-phase minimum intersections. Require all rooms fully in view before workloads;
fail if measured coverage drops below half. Per-frame coverage collection is outside the
sample interval and reflects hull rectangles, not HUD/hand/toast occlusion.
Placement selects a valid fully visible site and fails instead of silently doing nothing.
Existing large-fixture construction keeps unrestricted find_space behavior. Explicit zoom
now included in verification. Game's ordinary fit/zoom/placement logic unchanged.

## Verification
Actual maintained release executable with current-source overlays, debug=false; two
native lane sets, 4,320 successful measured frames, 48 phases:
- Saved12 and expanded40: idle/pan/zoom/lighting at1x/2x/4x,90frames/phase.
  All12phase camera starts identical within each map, all rooms fully visible.
  Minimum intersections12/12 and40/40. Fitted startzoom0.1704545; zoom ends0.1448864
  at every speed. Current initial layout fit, unlike prior0.06148 legacy run.
- Fresh1 and expanded40: placement/demolition/interface/save at1x/2x/4x.
  Room count1->2->1 and40->41->40 at each speed, no blocked demolition reports.
  Every phase starts/ends with all current rooms fully visible, saving uses scratch profile.

Initial settle guard used camera_zoom_moving, which can stay true after target completion;
first trial failed after zoom. Corrected to actual target absence plus stable scroll and
finished pending layers. Initial fresh action trial exposed a newly placed room outside
original fixed fit; visible placement and current-bounds refit corrected it. Both failures
terminal with configuration restored and owner unchanged. No game-source workaround.

One-run current RGBA framing diagnostics (not compared to legacy differently scoped means):
saved12 mean12.711/p9519.481/p9923.709/max28.685ms, peak1558.872MiB;
expanded40 mean26.192/p9544.331/p9954.615/max75.226ms, peak3028.007MiB.
These include zoom and different scene coverage/phase preparation; NOT overall improvement
from earlier averages. Both p95 fail; large p99 fails. One run does not certify stall gates.
Final large capture inspected: station now centered and enlarged; hand/discovery toast
still covers part of it. Geometry validity is not full visual/motion/occlusion acceptance.

Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
benchmark-framing-verification-v2 and benchmark-framing-action-verification-v2;
camera-verification.json, action-verification.json, per-run JSON/log/PNG, identity/owner
and storage records. All jobs terminal/config restored; four owner guards2,938 unchanged.
Focused diff check clean.66.56MiB evidence+scratch/no full PCK copies, C126.91/D78.34GiB free.

## Next action
Instrument private current indexed+prewarm group's preparation, redundant cleanup and
slot draw costs, then compare against current RGBA using THIS verified framing and explicit
zoom. Do not reuse legacy-camera averages as an acceptance baseline. Confirm pixel/motion/
filtering/flood/fallback and lifecycle behavior before any provider admission. Additional
viewports/hardware, 3-run candidates, cold/warm loading, endurance, original bug coverage,
Windows/Mac package freeze and native M1/signing/notarization gates remain open.
