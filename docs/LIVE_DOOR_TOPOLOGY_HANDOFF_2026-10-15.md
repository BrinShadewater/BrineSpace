# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: live-room and door/light CPU

## Objective and acceptance

Owner requested less live-room drawing and door/light validation work toward
60 FPS without changing appearance. Install the verified structural-plan reuse
for its repeatable local CPU and normal-speed idle gain. Whole-workload pacing
and release acceptance remain separate.

## Accepted decisions and constraints

Only topology and door-style selection are retained. Door aperture, airlock pose,
crew depth, lights/flicker, flooding, warnings and animation clocks remain live.
Keep original drawing commands/order and preview/direct-draw fallbacks. Private
room-raster LOD stays private. Prior accepted water change is common to both lanes.
Native jobs serial; isolated APPDATA, copied owner layouts, fixed input-disabled
1920x1080 secondary window and real-save fingerprints. No export or commit requested.

## Current state

- `scripts/grid_canvas.gd`: one current structural plan serves door validation and
  ordinary-room side/omission preparation. Key includes ordered drawn structure,
  relevant occupied-neighbour structure with absence markers, layout revision,
  Store data identity and connection diagnostic mode. Deep snapshots detect
  in-place port edits. Dependency cells rebuild when drawn structure changes;
  unrelated offscreen rooms neither enlarge the per-frame scan nor invalidate it.
- Nursery reuse requires preparation in this actual grid draw, current frame/owner,
  canonical room identity and non-preview drawing. Held/unprepared/direct paths
  retain original preparation. Arrays passed to views are owned copies. The
  diagnostic `--reference-render-topology` flag retains the original implementation.
- `tests/test_structural_render_plan.gd` + UID and `tests/index.json`: permanent
  render-perf coverage. Existing Grid UID and unrelated edits preserved.

Evidence: `C:/bs-door-live-20261014/`; drivers: `output/door-live-20261014/`.
Final measured private PCK SHA256:
`026fa29bfb17f0e7bb4de7f1b5438acf34327616df408d0e939a4ad516836fe5`.
Reference PCK is the prior final water candidate:
`084ca0c0f8e0f2a1b706b3ace5d2f2eac8bd538dbfd300de35842170a071a965`.
Both contain the same private LOD baseline and accepted companion/water changes.
Installed Grid SHA256:
`27239e41740a7cca109bbf12458aaa1516449457cf37a6a514ce15a24f6bcf79`.
New methods and nursery replacement match the measured program; integration
excludes all private LOD differences. See `production-source.json`.

## Verification

Permanent plan test passes **7,294 checks across316 room/rotation variants**:
connections/actual large-room port neighbours, branch ownership, rotations,
placement/removal, missing/empty ports, in-place port edits, layout revision and
dictionary replacement without revision, uncached Store mode, drawing order,
dictionary replacement and unrelated offscreen additions.

Actual debug=false runtime passes120 live door/light key comparisons plus12
adjacent native frozen-image comparisons at fitted/.25/.5 zoom, both directions
and repeat controls; all channels exact and states equal. Representative image
reviewed. Final extra diagnostic run compares original door/light keys and complete
plans on **1,680 live frames** over all seven actions at1x/4x: zero mismatches.
Those extra-comparison timings are deliberately excluded from performance claims.

Installed normal-source maintained checks all pass: structural plan, connected
door rendering, placement previews and native live-surface retention. Logs clean,
no errors/warnings/leaks. Evidence:
`output/test-runs/20261015-002143-headless/` and
`output/test-runs/20261015-002219-native/`. Native/headless routing is unchanged.
Final source/test/UID/index review finds no actionable issue; whitespace checks
pass. All24 completed owner guards preserve2,948 files. No task-owned QA process remains.

### Performance result

Actual release-runtime overlay comparison: **6,720 measured frames**, seven actions
(idle/pan/zoom/lighting/placement/demolition/interface),1x/4x, both run orders.
All28 phase-end gameplay-state/camera pairs match. A0.5-second Windows process
snapshot guard detects no foreign Godot worker or duplicate game; it does not
measure every possible background load. Pack/source identities verify.

| Normal-speed idle | Reference then candidate | Candidate then reference |
|---|---:|---:|
| Door/light validation | 1.186 ->0.641 ms | 1.194 ->0.652 ms |
| Nursery preparation | 0.882 ->0.303 ms | 0.885 ->0.309 ms |
| Whole frame | 21.298 ->20.058 ms | 21.404 ->20.258 ms |
| FPS from mean frame time | 46.95 ->49.86 | 46.72 ->49.36 |

About1.1 ms is saved across the two separate preparation scopes. Live-room total
falls5.286->4.639 and5.327->4.703 ms; it includes nursery preparation and must not
be added to that subset. Render CPU stays essentially flat around5.3 ms and idle
draw calls around2369: this is CPU preparation reuse, not submission batching.
Texture peak is identical in every lane at2784.653 MiB. One plan/key and the
current dependency set are retained; no raster or texture allocation added.
CPU process RAM was not established by this experiment.

Whole-workload means remain mixed:24.001->24.803 ms (3.34% slower) and
24.009->22.880 ms (4.70% faster). P95 improves7/14 and11/14 phases. Worst frames
82.508->128.026 and83.120->81.395 ms; >50-ms samples14->28 and15->15. The128-ms
frame is placement, not a drone upload; its full cause remains unresolved. Later
first-candidate phases show broader CPU/render slowdown despite lower targeted
preparation work. No general pacing improvement or cause for that variation is
established. **All28 candidate60 FPS phase gates still fail.** See `analysis.json`.

Exploratory exclusions: a direct frozen-script class-name collision was corrected
before the expected missing-API RED. Store replacement coverage then found a real
stale-style case, fixed before final measurements. Three timing attempts were
rejected by the minimized-window guard (one retained only a valid reference).
User confirmed displays awake. A startup window-state probe subsequently remained
visible; final series completes with guards active. Earlier minimization's cause
is unknown. No excluded timings are combined with the final comparison.

## Next action

Requested prototype, normal integration and validation are complete. Keep admission
scoped to repeatable preparation/idle gains. Remaining live-room work is about
4.6–4.7 ms and render CPU about5.3 ms in this private baseline; investigate remaining
actual painting/submission before more cache layers. Resolve placement and other
frame spikes before claiming pacing readiness. Windows delivery remains unchanged;
actual PC/Mac, endurance, save/relaunch and60 FPS release acceptance remain open.
