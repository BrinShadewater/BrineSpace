# Project handoff

Updated: October 8, 2026 - Project: BrineSpace - Task: moving-water runtime comparison

## Objective and acceptance

Continue the complete PC/Mac optimization and release-readiness plan. A selected
optimization must improve matched workloads while preserving selected animation
pixels/timing, simulation, saves and owner layouts. Full release gates remain open.

## Accepted decisions and constraints

Keep the moving-water batch private. It now has repeated evidence of a net frame
gain despite greater script preparation cost, but stationary/reduced-motion reuse,
third-run coverage and pan/zoom/lighting/lifecycle checks remain before integration.
No downscale, frame cuts, renderer upgrade or native dependency introduced.

## Current state

Two actual debug=false, 1080p, 40-room/four-crew/full-natural-mission pairs use
byte-identical navigation, canvas, Moon and stroke sources. Only the dynamic-water
flag differs within each pair; both retain scoped/fast/indexed navigation and
beacon batching. Candidate compiled branch and source hashes explicitly verified.
Reference-first then candidate-first order controls earlier draw-order concerns.
Profiling/trace/renderer counters enabled in both; these are diagnostic workloads,
not final release performance certification. Hardware is RTX 4070 Ti, not GTX1650/M1.

| Pair order | Speed | Mean ms: reference -> batch | p95 ms | p99 ms |
|---|---|---|---|---|
| reference first | 1x | 46.32 -> 41.30 | 53.28 -> 47.23 | 62.59 -> 59.16 |
| reference first | 2x | 48.68 -> 42.18 | 57.34 -> 51.55 | 73.32 -> 62.28 |
| reference first | 4x | 49.23 -> 42.86 | 63.83 -> 56.97 | 85.94 -> 72.16 |
| candidate first | 1x | 42.77 -> 38.11 | 47.28 -> 40.40 | 55.97 -> 51.69 |
| candidate first | 2x | 45.72 -> 39.22 | 52.80 -> 45.42 | 66.92 -> 55.84 |
| candidate first | 4x | 46.08 -> 40.28 | 58.87 -> 53.14 | 77.72 -> 70.77 |

Mean, p95 and p99 improve all six comparisons. Native draw calls fall from
~6,390-6,465 to ~4,943-4,954 (about 23%). First pair renderer CPU median15.27->11.55ms,
GPU12.97->9.17ms; reverse CPU14.26->10.87ms/GPU12.16->8.63ms. Timings overlap;
do not sum CPU and GPU savings. First grid script draw median21.42->21.72ms;
Moon base CPU increases roughly0.44-0.80ms/frame while renderer savings outweigh it.

Every compared phase's crew/drone/doors/lights/power/zoom/prop/mission/resource
endpoints match; final full mission histories match. All three missions launch,
return through pressure crossings and unload, recovering full station graphs;
zero bay fallbacks. Upload counts4074 in every run. Mean gain4.65-6.50ms/frame.
Candidate still averages38.1-42.9ms and has max135ms; 60FPS/stutter gates fail.
Worst frames do not uniformly improve, and no stutter closure is claimed.

Settled memory start1548.995/end1916.471/exit228.259MiB matches first pair. Its
reference peak2408.880 versus candidate2346.502MiB is not attributed to batching.
Reverse peak2346.502/exit228.259MiB equal. No texture-memory remedy or endurance
certificate is established by the stroke change.

Evidence under D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
water-topology-runtime/, water-topology-reverse/ and water-topology-repeated-comparison.json.
The private physical bootstrap copies mount the canonical PCK and override packs;
normal/public candidate files are unchanged. Changed checkout files: this handoff
and CURRENT_STATUS.md only.

## Verification

Full composition native QA proof:385checks/384 exact raster pairs across overlapping
Moon/Tidal/Hydro/Storage rooms,4rotations,raised/lowered walls,2filter modes,material
on/off,offline overlay,3water levels and2animation clocks,asymmetric transform/tint.
An initial fixture WeakRef inference parse error was fixed; failed log retained.

Extended sequence proof:529checks/528exactpairs, adding144 consecutive frame
comparisons with1/60clock steps across4rotations and flood/drain pressure states.
Existing6592stroke/index/scalar checks remain separate supporting evidence. This
is pixel parity at selected room states, not complete owner visual acceptance.

Actual runs clean/debug=false/focused; compiled Moon/stroke/navigation/canvas source
identity guards pass. All2,936 non-log owner files unchanged in both pairs and
visual proofs; all processes terminal and runtime adapters restored. Router releases.

## Next action

Preserve the original clock0/full-water command cache instead of rebuilding that
stationary case in the dynamic batch. Verify branch/settings behavior, then obtain
third matched evidence plus pan/zoom/lighting/doors and active pressure-cycle
workloads with full endpoint parity. Check cache invalidation and memory after
room removal/layout edits/scene exit before normal-source integration.
Keep full Windows/Mac certification,original nine reports,loading,endurance and
stutter/60FPS gates active; no public release is authorized by this milestone.
