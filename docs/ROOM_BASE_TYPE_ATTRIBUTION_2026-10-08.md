# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: actual room-type base draw attribution

## Objective and acceptance
Continue full performance/bug/PC-Mac readiness scope. Target dominant ordinary rendering work using actual evidence; preserve default quality, dynamic water/beacons/doors and pixels. No publication. Diagnostic stage timings not FPS certificate.

## Accepted decisions and constraints
Per-type child _draw timings overlap live_rooms and total grid draw. Count includes startup/warmup, while stage means use3,000 measured frames. No blanket cache/redraw suppression. Existing idle cache hit evidence cannot substitute for active mission drawing. Normal sources unchanged.

## Current state
D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/room-base-preparation/ safely extracts actual canonical PCK large_room_canvas.gd into frozen-canvas.gd. room-base-attribution/ physical private runtime and canvas.gd override adds bounded per-type timing fields/base redraw counts to existing record_draw. Early owner pack includes canvas before compilation; every loaded large slot compiled SHA verified5fa3dde240e7a774e668f8c758a5ca21183b2f937b213db4b24abfc0cbc183f4. Existing navigation/source guards retained. No room geometry/painting change.

## Verification
Actual native debug=false1080p40rooms/four crew/3 natural missions,3,000idle1/2/4x frames. Full lifecycle, no route fallbacks, full graph recovery. Both renderer timers enabled/nonzero. Logs clean/no errors/warnings/leaks/missing art; owner fingerprints2,936same; adapters restored; all handles terminal. Analysis candidate.json/analysis.json plus identity-candidate/owner-candidate authoritative.

Three Moonbay bases combined mean6.752ms/frame, active in2,940of3,000frames, max12.671ms. Three Tidal bases mean0.791ms/max1.577ms. About89.5% of measured base draw CPU is Moonbay. Hydroponics/Storage bases no measured-stage redraws; cumulative lifetime2–3 each (startup/warmup included). Moonbase cumulative redraws3,119/2,869/3,120; Tidal3,182/3,182/3,180. Their prop setup/retained costs small by comparison: Moon0.132/0.106ms; Hydro0.145/0.338; Storage0.154/0.318; Tidal0.149/0.215. These are category aggregates, not per-room costs or exclusive whole-frame sums.

Source inspected actual private Moon used by base: draw order includes common shell/floor/shelf, bay/grating/water, sub, walls/corners/windows, doors/gate, beacons. _draw_water uses cached commands only at clock==0 and level==1; otherwise uncached moving geometry. Active mission cycle_clock continuously changes, so idle cached water evidence misses this workload. Earlier dynamic-water batching did not execute in idle workload and could carry CPU geometry-build overhead; do not assume that candidate is now a win. Moonbase submit snapshots all mission state and queues full draw when state changes. Static retention alone can save script regeneration but does not inherently remove retained GPU draw calls.

Instrumented means47.008/46.879/46.902ms,p9554.704/56.000/60.085,max143.225ms; no uninstrumented matched comparison, FPS gates still fail. Peak2,346.502MiB/uploads4,074/exit228.259MiB; unchanged fixture resources, no saving claim. Additional tag instrumentation bounded to room-type/label keys, no shader/effects/frame changes.

## Next action
Measure Moon component CPU and executed draw counts during active phases: moving water, common shell/floors, walls/corners/windows, doors and beacon. Optimize measured dominant geometry with exact native pixels across rotations/raised walls/filtering/phase clocks; preserve interleaved layering and movement. Need both script reduction and fewer GPU submissions, not just command retention. Separately keep drone upload preparation/wait as stall target. Combined navigation third/reversed timing, moved-prop/native motion/full combined checkpoint/title ownership and original nine reports/load/memory/endurance/target hardware/Windows-Mac packages/signing all remain open.
