# Stable navigation IDs prototype — October 15, 2026

Stable cell IDs substantially reduce the connected-placement rebuild. In the
guarded release comparison, 4× placement action frames improve from
68.418/68.161 to **58.479/57.549 ms**, saving 9.9–10.6 ms (14.5–15.6%).
Steady FPS is mixed: normal idle 51.86→52.37, 4× idle 46.52→44.63.
This is a private Windows prototype; the installed game is unchanged. It does
not establish 60 FPS or justify integration without investigating the idle result.

## Design and preserved behavior

The [preceding investigation](NAV_RETENTION_PERFORMANCE_2026-10-15.md) identified
global dense node renumbering as the reason a three-node doorway change rebuilds
thousands of otherwise unchanged nodes. This prototype assigns each occupied cell
a reusable block of 1,024 IDs. Current room templates fit within 529 points.
Unchanged cells retain their IDs and ordinary AStar2D points; only cells whose
ordered center, offsets, weights or links change are reconstructed. Removed blocks
are recycled, and allocation is bounded by the peak simultaneous cell count.
IDs stay within signed 32-bit range for existing swim-state keys.

Each actor retains its own mutable AStar2D and helper. No graph is shared between
crew or companions. Cached local ID arrays are private and read-only; fresh caller
arrays receive their integer contents. Unchanged canonical coordinate-lookup
prefixes survive; a changed suffix is rewritten in original order. Equal packed
templates reuse their prior validation; changed templates receive complete
preflight validation before any graph or caller-output mutation.

All prior seam records are disconnected before dirty cells are removed. Current
seams are then replayed by the original script in its original cardinal/global
order, after local links. Room target arrays, coordinate keys and physical neighbor
order remain canonical even though their numeric node IDs are sparse.

The engine's ordinary AStar search still handles routes. Its heap compares total
cost and cost so far rather than numeric IDs; preserving physical neighbor order
matters for equal-cost discovery. See the
[pinned engine header](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/core/math/a_star.h)
and [implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/core/math/a_star.cpp).
Existing route/action resets, decision clocks, rebuild scheduling, water policy,
lock policy and Josh's post-rebuild water handling remain in place. Sparse graphs
use the existing dictionary-based detour reachability path; custom swim search is
unchanged. Full layout-revision changes reset the helper.

Staged rebuilds, unavailable native support, reference flags and rejected native
plans restore a complete canonical dense script graph. Preflight rejection is
atomic. The helper assumes sole structural ownership of its graph and lookup;
same-size external edits require an explicit reset.

This is physical routing equivalence, not universal numeric-ID API equivalence.
`get_closest_point()` resolves exact-distance ties using the lowest ID, which can
differ here. Normal actor routing has no caller of that API; the Room Scale Preview
tool does. This prototype is not integrated into that tool. Identical global
segment iteration for `get_closest_position_in_segment()` is also outside scope.

## Isolated rebuild results

Twenty paired alternating-order calls per case; the table uniformly omits the
first pair and reports warmed nineteen-pair means. Simulation and drawing are
outside the timed calls. The first pair checks exact ordered physical graph,
lookup, target and seam records against the original script implementation.

| Case | Reference → final V3, ms |
| --- | ---: |
| Warm unchanged graph | 2.536 → 2.961 |
| Unconnected append | 3.058 → 3.528 |
| Middle rotation / former large suffix | 13.140 → 3.406 |
| Connected append at `(24,17)` | 9.894 → 4.913 |

The middle-rotation fixture changes the old geometry key but leaves its actual
ordered local template identical. Stable IDs retain all 52 cells and 14,097 nodes
in that case. Connected append rebuilds two cells, removing 307 and adding 598
nodes, while retaining 51 cells / 13,790 nodes. Warm/simple cases cost an extra
0.4–0.5 ms per actor; this is a real tradeoff, not an across-the-board speedup.

V1 rewrote the entire lookup and regenerated every ID array: connected rebuild
10.044→6.194 ms, warm 2.583→5.006 ms. V2 cached ID arrays and preserved lookup
prefixes: connected 9.836→5.608, warm 2.619→3.969 ms. V3 additionally avoids
revalidating identical immutable template values and uses const packed-array
pointers for changed-data validation. All three versions have separate immutable
DLLs; only V3 receives the full live comparison below.

## Guarded release benchmark

Frozen 40-room / 52-occupied-cell large-station cohort, including four large rooms,
using the same private distant-room LOD and one-spare setup as preceding trials.
Actual release Godot 4.7.2 `ed1daf0bf`, Compatibility/OpenGL, RTX 4070 Ti,
1920×1080, debug=false. This frozen cohort is separate from normal runtime and
public playable-export acceptance.

Four serial visible processes: reference→V3→V3→reference. Each uses 180 warm
frames, then 120 measured frames per idle/placement phase at 1× and 4×:
**1,920 measured frames**. Eight state/camera endpoint/per-frame camera-path pairs
match exactly. The process/window guard records 241 samples, no foreign Godot
processes or guard errors, maximum sample gap 0.821 s. The owner's idle editor is
preserved. Both lanes load the same immutable V3 DLL; reference records zero helper
calls and each trial ten calls including fixture preparation.

| Phase | Mean FPS, reference → V3 | Mean frame, ms | p95 frame, ms |
| --- | ---: | ---: | ---: |
| 1× idle | 51.86 → 52.37 | 19.281 → 19.093 | 22.136 → 20.940 |
| 1× placement | 49.93 → 51.47 | 20.028 → 19.430 | 24.489 → 22.582 |
| 4× idle | 46.52 → 44.63 | 21.498 → 22.405 | 37.441 → 37.951 |
| 4× placement | 42.91 → 43.68 | 23.303 → 22.895 | 39.354 → 35.597 |

FPS is 1000/pooled mean frame milliseconds. Normal idle improves in the forward
order and slightly worsens in reverse; 4× idle mean worsens in both orders.
The all-phase mean improves in forward and worsens in reverse. Do not credit
these mixed results as a dependable steady FPS gain. No candidate phase passes
the existing mean-and-p95 16.667 ms gate: **0/8**.

| Placement action | Frame, reference → V3, ms | Crew phase, reference → V3, ms |
| --- | ---: | ---: |
| 1×, forward | 46.925 → 47.019 | 7.942 → 9.572 |
| 1×, reverse | 45.895 → 45.925 | 9.004 → 9.285 |
| 4×, forward | 68.418 → 58.479 | 26.318 → 15.410 |
| 4×, reverse | 68.161 → 57.549 | 26.373 → 15.060 |

The normal action adds an unconnected Solar room at `(23,23)`. The later 4× action
adds Solar at `(24,17)`, opening another side of Life Support at `(23,17)` and
adding three nodes to its local template. There is no special 4× invalidation
rule; compare reference and trial within each speed. The final native call retains
52 cells / **14,075 existing nodes**, reconstructing only two cells: 307 old nodes
removed, 598 new nodes added, graph ending at 14,673 points. The old dense prefix
path retains 8,580 nodes and reconstructs 5,802 old suffix nodes for this action.
Action-frame sampled atlas upload time is zero in both lanes.

Following sixty frames exclude the action itself:

| 4× window | Mean, ms | p95, ms | Worst, ms | Frames >50 ms |
| --- | ---: | ---: | ---: | ---: |
| Forward | 23.526 → 23.033 | 39.354 → 35.597 | 57.340 → 55.999 | 1 → 1 |
| Reverse | 23.426 → 23.214 | 36.310 → 34.800 | 58.339 → 57.729 | 3 → 1 |

The placement savings are not simply moved into the next sixty frames. Other
large spikes remain: worst 4× idle frame 70.630→74.365 ms. Mean crew work during
4× idle changes only ~0.797→0.824 ms, so this capture does not establish the cause
of the larger whole-frame idle difference. Sparse detour cost remains worth
isolating, but blaming it for that regression would be speculation.

## Validation, scope and artifacts

Final native suite: **3,157 assertions, zero failures**. It covers stable IDs,
ordered edges/routes, stale search/disabled state, key-only changes, lookup
replacement and prefix retention, immutable cached ID isolation, block recycling,
reset ownership, invalid/overflow data, duplicate/aliased/typed/read-only outputs
and late rejection atomicity. Initial expected-failure runs establish the missing
primitive and warm-cache regression checks before their implementations.

Final integrated oracle: **2,530 checks**, 317,303 ordered physical graph records,
2,872 routes and 126,528 sorted targets, zero failures. Fresh references disable
both packed point/link optimizations. Coverage includes rotations, insertion and
removal, layouts, locks, Moonbay, exact target/neighbor/seam order, stable IDs,
forced rejection, staged/reference fallbacks, successful/failed/partial engine
searches, dry and flooded routes in all facings, smoothed routes, traffic padding,
sparse/dense detour discovery, fire exclusions and Josh/River/Margot water states.
Extension-absent fallback passes **2,216 checks**, 259,265 records and 2,328 routes.

Twelve station image pairs are pixel-exact across three zooms, lighting on/off
and repeats. Twelve within-process repeat pairs and five first-placement frame
pairs are also exact. First placement matches from its initial live draw through
ready/active capture; state, camera and visual sidecars match. The fitted station
image was inspected. Headless checks alone are not counted as visual acceptance.

All **24 owner-folder guards** pass. Final 2,948 non-log files equal the task's
initial and prior protected post-recovery fingerprints. Installed sources, paired
UIDs and normal navigation test match the recorded pre-task hashes. Only the
owner's idle editor PID 46624 remains. The
[earlier profile incident](TEST_PROFILE_INCIDENT_2026-10-15.md) and its two legacy
metadata differences are still documented; this task makes no further changes.

Raw evidence and native source: `C:/bs-stable-nav-20261015/`.
Helpers: `output/stable-nav-20261015/`. The reference and three trial packs freeze
22 selected scripts; only Bill differs. Loaded-source checks cover Main, its actual
synergy constant, Bill and render/companion dependencies. The private stall probe
is not separately asserted as loaded. No normal source, paired UID, navigation
test, art, renderer setting, playable export, commit or upload is changed.

Native build uses the exact Godot API dump and godot-cpp pinned at
`1e7926375b62b445fa79db6851f7105b644831f2`, MSVC 14.44.35207,
release/speed/single precision. V1/V2 source and binary identities are archived;
V3 uses `native/bin/brine_stable_v3.dll` and API revision 3. SDK license is copied
beside the source. No Mac binary or release-manifest integration exists. ID caches
and metadata add per-actor memory; block recycling is tested, but this trial does
not quantify process memory or a long-session high-water mark.

`final-audit.json` records hashes, checks and counts; eleven release binary guards
pass. V3 DLL: 350,208 bytes, SHA256
`ccc5debfd91df60c9940ac217e1859841363c265ccd343f9c1c19643f783a23d`.

Next: investigate the mixed idle result and sparse reachability cost, then validate
platform packaging before considering integration. Keep the stable-ID design and
its ordered physical-graph oracle; do not replace numeric tie-sensitive tool APIs
without their own acceptance.
