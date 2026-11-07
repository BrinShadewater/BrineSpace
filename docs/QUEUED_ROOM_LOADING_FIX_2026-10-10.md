# Project handoff — restored construction loading stall fixed

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Locate and fix the reproducible current-save pan4x/frame60 stall, preserving art,
simulation, owner data and selected quality. Previous goal turn was progress:
real-save repetitions established a reproducible CPU stall and corrected the fixture.
This turn installs a measured fix; the full performance/release objective remains active.

## Accepted decisions and constraints
Actual debug=false Windows RTX4070Ti/1080p, muted secondary display, isolated resolved
APPDATA and disabled physical viewport input. Frozen copy of the current10→11 save,
owner layouts copied read-only, owner fingerprints,20GiB storage floor, small overlays.
No private indexed-provider installation, art changes, global cache or package copies.

## Current state
Changed scripts/grid_canvas.gd (existing UID preserved): prewarm_station_views now
prepares placed rooms plus queued construction and active drone orders. It skips empty
IDs and already-prepared types using the existing session lookup. This runs during
Main's startup before startup_complete; only required room views load, and normal
construction/art/crew timing is unchanged. No new per-frame preparation or retained cache.

Temporary private callback instrumentation first isolated the stall to environment6
(exterior actors),~89.8ms. Finer instrumentation measured queued reactor construction
draw~90.9ms; harvest sites~0.10ms, survey probe~0.01ms. The saved order is a crew-built
reactor assigned to Branforth, absent from placed rooms/hand preparation. At~62% fitting,
construction first uses its room view. Preparing that view during loading removes the
stall in matched trials, establishing the first-use room preparation as the actionable
cause. Callback timers stayed in private overlays; normal diagnostics were not expanded.

Installed source text exactly equals the tested candidate. installation.json records
source SHA256 f7d6fa7a0eded093bac19f29cf31ce78227b2b65d8db4f2b150239a46881f3f9
and unchanged paired UID hash. No unrelated dirty worktree files were replaced.

## Verification
Three alternating normal/fix pairs on frozen current save,12 phases each, idle/pan/zoom/
lighting1x/2x/4x,90frames/phase,6,480 measured frames. All36 full gameplay snapshots
and phase camera pairs exact. No runtime/safe-image errors, guards pass.

| Metric | Normal | Pending-room loading fix |
|---|---:|---:|
| Mean ms |12.499|12.403|
| p95 ms |18.332|18.203|
| p99 ms |27.405|27.334|
| Maximum ms |105.184|61.377|
| >50 / >100 frames |6 / 3|4 / 0|
| Peak gameplay texture MiB |1940.831|1940.831|

All three pair means favor fix (~0.77% pooled). Pan4x maxima normal105.184/101.563/
101.125ms → fix28.614/28.864/28.451ms. Remaining zoom4x/frame27 crew spike repeats;
one additional candidate zoom/frame46 >50ms remains recorded. Do not call overall
performance gates passed or every gameplay stall fixed.

Instantiation-to-ready normal9,551.540–9,594.287ms, fix9,654.903–9,736.077ms.
Matched differences+60.616/+151.919/+166.528ms: moves required preparation into loading.
This timing excludes scene request/executable startup and does not certify cold/warm gates.
Reported texture peak covers gameplay samples, not complete startup peak/lifetime acceptance.

Separate native pixel pass freezes simulation while awaiting render, samples reactor
progress61.333%,62%,62.667%,63.333%,64% during the same pan/camera/game clocks.
All five169x169 RGBA pairs exact. Final pass hides the hand only in the isolated fixture
to expose the complete reactor region; captures inspected and contain3,210–4,258 distinct
colors, not empty acceptance. First pass matched but was partially occluded by hand.
Initial capture searched only drone orders and failed; corrected to include fleet.orders
(crew orders). Failed process terminal/config restored/owner unchanged before retry.
Pixel-pass timings are discarded due to screenshot reads; measured repeats contain none.
This is fitting-transition pixel coverage, not all rooms/rotations/effects or full-scene
motion acceptance. Selected-art pixels, frame/scale/order code were not changed.

Evidence roots under D:/bs-release-crew-cache-20261009/benchmark-input-isolation:
current-stall-callback-trace, current-stall-foreground-trace, queued-room-prewarm-trial,
queued-room-prewarm-pixels, queued-room-prewarm-pixels-v2. Trial comparison/identity/
installation/storage JSON, native reports/logs and visual captures retained.
Focused runners under output/renderdoc-tools-2026-10-08/run-current-*-trace.py,
run-queued-room-prewarm-trial.py, compare-queued-prewarm.py and pixel runners.

All jobs terminal/config restored; every owner guard2,938 files unchanged. Focused
source diff check clean. This-turn evidence+scratch97.13MiB, C126.93/D77.31GiB free;
small packs and bounded screenshots only. No cleanup workaround or full export batch.

## Next action
Trace _update_test_walker and construction completion at current-save zoom4x/frame27.
The crew timing wraps that whole call, including callbacks triggered by the builder;
do not assume navigation or animations are the cause. Correlate actual reactor completion,
room placement/UI/navigation work with bounded call timings, then fix the measured cost
and compare gameplay/art under matched workloads. Investigate remaining >50 frames.
All p95/p99 gates, target hardware, loading/endurance, private provider lifetime/art
acceptance, original bugs, latest PC/Mac freeze and actual M1/signing/notarization remain
open. No itch upload or published minimum-spec claim.
