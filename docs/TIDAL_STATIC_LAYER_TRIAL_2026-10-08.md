# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: function attribution and retained tidal layers

## Objective and acceptance

Continue the full PC/Mac performance/readiness plan. Preserve selected pixels, animation timing, layers, settings, owner layouts and saves. No publication or normal admission from a single private experiment.

## Current state

Recovered the completed debug function profile rather than rerunning it. Its clean-log assertion rejected 217 pre-workload GDScript source warnings; no runtime errors, leaked-instance messages or warnings occurred during the active workload. `analysis.json` contains 32 once-per-second last-frame snapshots, ranked separately by self and inclusive time. Debug/profiler output is intrusive and its >500ms stalls are not release-runtime measurements. Godot's script profiling is debug-only; inclusive/yielding functions can overlap and must not be summed.

Private `output/renderdoc-tools-2026-10-08/tidal-split.gd` separates unchanged original drawing statements into static floor/pipe/housing, live rotor/water, and static front enclosure. `tidal-retained.gd` retains the two static command lists, invalidating on room appearance, bounds, layout revision and Reduced Motion; chamber state and generic machine clock do not invalidate static parts. Live state remains redrawn in the original order. `tidal-large-canvas.gd` integrates this only into an identified private override PCK. Normal room scripts, art, layout data, original helper and retained full release remain unchanged.

## Verification

Native exact raster and retention: 288 checks, zero failures, clean log. 96 cases cover four rotations, nearest/linear filtering, 384/512 room sizes, raised/lowered walls, four authored port dictionaries with mixed opening amounts, alternating peripheral flooding, chamber water0/.4/1 and advancing rotor angle. Every case compares original immediate drawing against retained child layers twice, and verifies static commands survive rotor/clock advancement. This is not full lighting/material/Studio/save or Reduced Motion coverage.

Fixture failures retained: static `Script.call()` does not dispatch a static function, corrected to explicit calls; integer port fixture entries caused errors in both renderers and a misleading pixel pass, which the runner correctly rejected. Replaced with the actual port dictionary schema before acceptance. First release trial stopped deliberately after discovering the benchmark requires `hits`/`redraws` metadata on every submit-capable base; terminal runner restored its adapter. Counters added before building a new immutable identified PCK and restarting the corrected experiment.

Actual debug=false40-room/four-crew matched pair, idle/pan/zoom at1/2/4x, 180 frames each, default quality/cap0/VSync0/focused, detailed profiler and GPU queries off. Candidate executes retained bases in all three tidal plants: submit-capable bases9→12; total large-room canvases12. Every compared crew/drone/door/light/power-count/zoom field and all large-prop counters equal in all nine phases. Clean logs, no missing images, router released. Peak2348.739303MiB and settled exit228.259212MiB exactly equal; uploads4297 both.

Means improve in8/9 phases (0.086–2.110ms), but4x zoom worsens0.246ms. P95 improves5/9 and worsens4/9; old range34.138–59.787ms, candidate34.160–60.268ms. Maximum88.241→88.224ms. One ordered pair does not establish a robust performance gain; all phases still fail60FPS. This is a small output-preserving candidate, not the principal remedy. Candidate station capture reviewed; exact isolated room pixels provide stronger parity evidence than the whole-station still.

All tests use resolved scratch profiles; owner2936 files unchanged. Corrected release adapter restored byte-identically; all native/runner handles terminal. Full logs, profile/source identities, private PCK, raster result, station screenshots and per-phase comparison are under `output/renderdoc-tools-2026-10-08/{script-function-profile,tidal-retention-native-ports-corrected,tidal-release-trial-counters-corrected}`. Helpers and failed trial evidence retained.

## Next action

Keep this candidate private pending broader visual invalidation/settings and repeated matched measurements. Prioritize reducing substantial canvas command/submission work across environment and room layers; static retention alone leaves the renderer's thousands of draws intact. The profile also identifies repeated navigation topology construction (six calls in typical sampled frames); investigate its invalidation boundaries before caching it. Do not claim either lead solves the frame-time gap. Full combined integration, nine bug reports, loading, p95/p99/stutters, memory/endurance, target PC/M1, signing/notarization and final delivery gates remain open.

Primary profiling implementation: https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/core/debugger/local_debugger.cpp and https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/modules/gdscript/gdscript.cpp .
