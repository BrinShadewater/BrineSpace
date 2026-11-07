# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: static monitor retention

## Objective and acceptance

Reduce measured animated-room rendering cost, preserving pixels, timing, transforms,
materials and screen/prop ordering. Overall PC/Mac release acceptance remains open.

## Accepted decisions and constraints

**Do not admit this prototype.** Ordered static/dynamic monitor child layers retain
static commands correctly, but measured total room callback cost increases. Normal
runtime, art, settings and test index unchanged. No export or release certification.

## Current state

Private source copies, generators, rejected fixture logs and results retained in
`output/retained-monitors-2026-10-06/`. Screens-only ordinary unflipped library slots
split each screen into adjacent static/live child nodes; complex/effect artwork
falls back. Registration, rectangle, colour, mirroring and transforms invalidate
retention. Children inherit the existing material. This preserves overlapping
screen command order but adds 250 nodes for 125 screens in this station.

## Verification

Final expanded native test: **671 checks / 462 exact raster pairs**, zero failures
or engine errors. Includes 179 current metadata registrations dry/flooded, overlapping
synthetic screens, clocks, operating state, Reduced Motion, filtering, inherited
tint/nonuniform transform, fallback cleanup and mutable screen invalidation.
Steady-visibility checks prove static commands remain retained while animated
commands redraw. Not full-room/Studio/packaged visual acceptance.

Rejected fixture attempts are retained: visibility toggling caused automatic
redraws, synthetic mirror metadata lacked `pieces`, and clocks differed after a
retention-only probe. Corrected the fixtures before accepting final image results.

The first copied station fixture still loaded an external earlier content renderer.
It did not measure this candidate; its results are invalid optimization evidence.
The same wiring error invalidates the previous point-array experiment's station
comparison. Its direct image/preparation tests remain valid. The earlier handoff
has been corrected; point-array station efficacy remains inconclusive.

Corrected `station-wired` copies explicitly preload their physical content source;
the runner asserts candidate monitor execution in every phase. Native 40-room
1080p idle/pan at 1/2/4x, 60 samples per phase, child `_draw` timing included:

| Phase | Baseline content ms | Candidate content ms |
|---|---:|---:|
| Idle 1x | 3.171 | 3.290 |
| Pan 1x | 3.058 | 3.216 |
| Idle 2x | 3.105 | 3.276 |
| Pan 2x | 3.213 | 3.380 |
| Idle 4x | 3.305 | 3.728 |
| Pan 4x | 3.237 | 3.412 |

115 eligible slots / 125 screens execute; static draws remain 125 across all six
phases, live draws grow 29686→64878. Renderer CPU is broadly similar (~10.05–10.60
ms); full-frame results mixed and still fail (candidate p95 36.526–46.832 ms).
One pair establishes no aggregate FPS benefit. Both use private compressed crew,
not normal or packaged release gameplay. All six actual crew/drone snapshots,
powered-room counts, zoom and texture counters match; final 3168.333 MiB unchanged.
All 2936 owner non-log files unchanged in successful and rejected isolated runs.
Processes terminal; no pending native run.

Godot's [4.7.2 CanvasItem implementation](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/scene/main/canvas_item.cpp)
builds arc points and submits a polyline. This supports investigating fixed geometry
reuse; it does not establish station performance benefit or pixel equality.

## Next action

Try slot-local fixed screen geometry preparation inside existing drawing layers,
without extra CanvasItems; preserve native arc math/output or keep the original arc
API. Verify candidate execution as well as explicit preload wiring in every future
physical benchmark. Repeat the point-array station comparison only with corrected
wiring if pursued. Larger renderer, memory/loading, lifecycle, original bugs,
endurance and packaged Windows/Mac gates remain open.
