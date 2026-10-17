# Placement navigation retention — October 15, 2026

The large rebuild is explained, but both tested ways of retaining more graph
objects are slower. Neither is admitted to normal runtime. The final prototype
keeps exact graphs/routes/images, but 4× placement frames worsen from
69.767/70.664 to 80.287/79.759 ms. Normal idle is essentially flat,
53.33→53.04 FPS. Installed navigation, crew behavior, art and exports are unchanged.

## Why a small placement rebuilds a large suffix

Navigation nodes receive dense IDs in occupied-cell and local-point order. The
existing optimization keeps the contiguous prefix with unchanged cell order,
layout revision and full room geometry keys. Connected sides are part of those
keys. A first mismatch ends retention so later point IDs and ordered connections
remain identical to a fresh build. See [prefix selection](../scripts/bill_npc.gd#L911)
and [suffix removal](../scripts/bill_npc.gd#L938).

The release trace identifies the actual 4× benchmark placement:

| Per companion | Before → after |
| --- | --- |
| Placement | Solar Array at `(24,17)` |
| Existing room affected | Life Support at `(23,17)` |
| Connected sides | `[2,3]` → `[1,2,3]` |
| Local nodes in that room | 307 → 310 |
| Total graph nodes | 14,382 → 14,673 |
| Existing nodes retained by the prefix | 8,580 |
| Existing suffix nodes removed/reconstructed | 5,802 |
| Existing cells with unchanged ordered local templates | 52 |
| Nodes belonging to those unchanged local templates | 14,075 |

The new doorway adds three local nodes before later rooms in the canonical
sequence. Their IDs therefore shift even though their room geometry is unchanged.
Merely ignoring the connected-side key or comparing point counts would be wrong:
the affected room's ordered points and links actually change.

River and Margot each own a mutable graph, and both synchronously rebuild when
their topology changes. Shared room templates save geometry generation, but do
not share mutable AStar objects. The main loop budgets one human crew rebuild per
frame; companions update afterward under their existing schedule. This task does
not change that schedule, route resets, water policy or decision clocks.

There is no special 4× graph invalidation rule. The benchmark's normal-speed phase
places first at `(23,23)`, adding an unconnected local template and retaining all
14,097 existing nodes. The later 4× phase uses the connected Life Support site.
Within-speed reference/trial comparisons are valid; the two actions do not isolate
the effect of simulation speed alone.

## What was tested

Both private Windows GDExtension variants reuse the same actor AStar object and
dense numeric slots. Slots receive their new canonical position/weight and enabled
state. Desired adjacency is derived in original room/local-link order. An edge
survives only when it belongs to both endpoints' common ordered neighbor prefixes.
Truncations propagate to a fixed point; missing edges are replayed in original
global order. The existing boundary pass then rebuilds seams.

V1 inspects the whole graph and includes retained canonical prefix seams in its
plan. V2 inspects only the rebuilt suffix. The original script keeps the proven
prefix, disconnects all nonretained seams, and submits suffix templates. Native
preflight validates the entire plan, dense ID order, mutable untyped outputs,
finite/representable data, indices, suffix reciprocity and absence of cross-prefix
edges before mutation. A rejection performs a full ordered script assembly.
Staged rebuilds, missing extensions and reference flags retain script paths.

V2 trusts the caller's existing unchanged-prefix geometry/lookup proof, just as the
installed prefix optimization does. It does not independently inspect prefix
positions/weights or adjacency. It preserves the APIs used by current routing;
identical global segment-set iteration for `get_closest_position_in_segment()` is
not claimed. There are no current game callers of that method.

The prototype uses Godot's existing point/weight/connection APIs; it has no access
to engine graph internals. See [AStar2D](https://docs.godotengine.org/en/4.7/classes/class_astar2d.html)
and the [pinned engine implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/core/math/a_star.cpp).

## Isolated CPU results

Twenty alternating-order paired rebuilds per case, with all raw samples retained.
The table uniformly omits the first pair and reports warmed nineteen-pair means.
Drawing and simulation are outside the timed calls. The first pair verifies exact
ordered graphs, maps, weights, disabled states and seam bookkeeping.

| Rebuild case | V1 reference → trial, ms | V2 reference → trial, ms |
| --- | ---: | ---: |
| Warm unchanged graph | 2.510 → 2.440 | 2.482 → 2.419 |
| Unconnected append | 3.426 → 3.320 | 3.091 → 2.962 |
| Middle rotation / large suffix | 13.406 → 22.597 | 13.244 → 16.644 |
| Connected append at `(24,17)` | 10.206 → 25.489 | 10.263 → 15.034 |

The native patch is bypassed for warm and unconnected append cases; their small
differences are not credited to retention. V2 removes much of V1's unnecessary
inspection, but remains ~46.5% slower for connected append.

The final live 4× patch reuses all 14,382 existing numeric point slots, moving
5,658 of their positions. Yet only **478 suffix edges** survive ordered retention:
17,881 are disconnected and 18,869 inserted. About 2.6% of old suffix edges
survive. Higher retained point-object counts therefore do not mean less total CPU
work. Adjacency inspection, planning and position/weight updates outweigh the
limited edge savings in these measurements. This interpretation is consistent
with the live crew-phase regression below; internal engine costs are not separately
stack-profiled by this trial.

## Full release comparison

Frozen 40-room / 52-occupied-cell large-station cohort, including four large rooms;
the same private distant-room LOD and one-spare setup as the preceding trials.
Actual release Godot 4.7.2 `ed1daf0bf`, Compatibility/OpenGL, RTX 4070 Ti,
1920×1080, debug=false. The private cohort is separate from acceptance of the
normal game and any public playable export.

Four serial visible processes, reference→V2→V2→reference. Each uses 180 warm
frames and 120 measured frames per idle/placement phase at 1× and 4×: 1,920 timed
frames. All eight state/camera endpoint/per-frame camera-path pairs match exactly.
Process/window guard: 241 samples, no foreign Godot processes or guard errors,
maximum sample gap 0.681 s. The owner's idle editor stays open. Reference and
trial load the same immutable V2 DLL; references record zero patch calls, trials
four each, including fixture preparation.

| Phase | Mean FPS, reference → V2 | Mean frame, ms | p95 frame, ms |
| --- | ---: | ---: | ---: |
| 1× idle | 53.33 → 53.04 | 18.752 → 18.852 | 20.617 → 20.903 |
| 1× placement | 50.54 → 52.08 | 19.788 → 19.203 | 24.386 → 22.431 |
| 4× idle | 46.21 → 46.39 | 21.640 → 21.555 | 37.006 → 37.618 |
| 4× placement | 43.56 → 42.90 | 22.957 → 23.308 | 36.438 → 40.392 |

FPS is 1000/pooled mean frame milliseconds. Compare within this series, not with
older reports' different reference timings. No phase passes the existing 60 FPS
mean/p95 gate: 0/8.

| Placement action | Frame, reference → V2, ms | Crew phase, reference → V2, ms |
| --- | ---: | ---: |
| 1×, forward | 46.007 → 46.670 | 8.186 → 8.401 |
| 1×, reverse | 46.114 → 44.439 | 7.947 → 7.827 |
| 4×, forward | 69.767 → 80.287 | 26.328 → 37.195 |
| 4×, reverse | 70.664 → 79.759 | 27.220 → 37.044 |

Normal action results are mixed and bypass native retention. Both 4× orders
regress by roughly 9–11 ms, consistent with the two slower companion rebuilds.
Action-frame sampled atlas upload time is zero.

Following sixty frames exclude the action itself:

| 4× following window | Mean, ms | p95, ms | Worst, ms | Frames >50 ms |
| --- | ---: | ---: | ---: | ---: |
| Forward | 23.509 → 24.341 | 36.438 → 40.764 | 57.998 → 62.321 | 1 → 1 |
| Reverse | 23.287 → 23.239 | 36.135 → 36.298 | 56.748 → 57.008 | 1 → 1 |

There is no dependable pacing benefit to justify installation.

## Validation and audit

Final V2 oracle: **13,424 checks, zero failures**, 290,960 ordered graph records,
2,508 routes and 126,528 sorted targets. Fresh references disable both packed
point/link optimizations and use original script loops. Coverage includes prefix
fractions, connected rooms and insertion orders, layouts, locks, Moonbay,
rotation/removal/reappend, staged/reference paths, forced rejection fallback,
successful/failed/partial search state and Josh wet/hysteretic/drained exclusions.
The extension-absent path passes 1,488 checks / 259,265 records / 2,328 routes.

Final native primitive suite: **1,474 assertions**, including ordered adjacency
closure, growth/shrink, disabled reset, fractional coordinates, aliased output
arrays, sparse IDs, invalid/overflow weights, cross-prefix/directed edges,
read-only/typed containers, late rejection atomicity and empty suffix/full plans.
An initial implementation compared float engine weights directly with double
packet weights and correctly failed its tests; converting comparisons to engine
precision fixed it before accepted timing. No failing run is counted as passing.

Twelve cross-process station RGBA pairs are exact across three zooms, lighting
on/off and repeats; twelve within-process repeat pairs are also exact. Five
first-placement frame pairs are exact from live draw through ready/active capture.
State, camera and visual sidecars match; the fitted station image was inspected.
The first short diagnostic did not reach the action and its shared JSONL had an
invalid line; it is excluded. Accepted trace uses separate closed actor files.

All **26 owner-folder guards** are clean. Final 2,948 non-log files equal both
task-initial and prior protected post-recovery fingerprints. Installed source,
paired UIDs and normal navigation test match the recorded pre-task hashes. Only
owner editor PID 46624 remains. The
[earlier profile incident](TEST_PROFILE_INCIDENT_2026-10-15.md) still applies; this
task does not erase the two legacy metadata differences from that incident.

## Artifacts and next direction

Raw evidence, DLLs and frozen packs: `C:/bs-nav-retention-20261015/`.
Helpers: `output/nav-retention-20261015/`. `final-audit.json` records source/binary
hashes, trace, checks and pair counts. Only the Bill overlay differs among 22
frozen scripts; loaded-source checks cover Main, its actual synergy constant, Bill
and the render/companion dependencies. The private stall-probe source is not
separately asserted as loaded.

Native sources use the prior exact engine API dump and godot-cpp pinned at
`1e7926375b62b445fa79db6851f7105b644831f2`, MSVC 14.44.35207, release/speed/single
precision. SDK license is copied beside the prototype. V1 source/DLL are archived
in `native-v1/`; its 356,864-byte DLL remains unchanged. V2 uses a separate
355,840-byte DLL, SHA256
`8234ad3cfe10610bc4d1f91be7be85daf256d3848ee78fa3bf3380f598594bf1`.
Ten release-run binary guards pass. No graph or plan persists in the native helper.
No normal-project extension, native packaging, Mac build, playable export, commit
or upload was added.

Keep the installed implementation. A further graph optimization needs a design
that avoids global ID renumbering while explicitly preserving route tie-breaking
and independent actor restrictions. Propose that design before restructuring
navigation. Repeating these mutation wrappers is not supported by the results.
