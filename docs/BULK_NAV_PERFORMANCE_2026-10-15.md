# Bulk navigation construction — October 15, 2026

Both native prototypes remain private. The final whole-suffix batch saves about
0.95 ms / 7.1% on an isolated large suffix rebuild, but does not improve the full
game comparison. Normal idle measures 51.35→48.24 FPS; 4× placement action frames
measure 68.306/70.146→71.624/72.386 ms, with worse following-window pacing.
Installed runtime source remains selected and unchanged by this task.

## Scope and implementation

The requested constraint was unchanged appearance and crew behavior. Two Windows
GDExtension variants move ordered AStar2D mutations into C++ while retaining each
actor's existing graph, point IDs, weights, disabled flags, room-ID arrays, lookup
maps, connection order, boundary seams and synchronous rebuild schedule.

- V1 batches prefix reset, room point additions and room-local links separately.
- V2 prepares cold templates in the existing room order, then submits the entire
  rebuilt suffix in one call. The native call validates all packets before mutation
  and appends each room's points then links in the original order. Boundary seams
  still use the existing code afterward.

Only the private Bill overlay differs from the frozen reference's 22 script
files. Missing native support, explicit reference modes and staged rebuilds retain
the script path. Rejected V2 packets fall back to the original ordered helpers;
the helper is active only during the synchronous rebuild. There is no graph
sharing, threading, route scheduling change, replacement graph or renderer change.

The native helper owns no actor, graph or persistent packet data. It still calls
Godot's bound AStar2D operations for individual mutations. These trials therefore
measure a native orchestration approach, not an engine-internal bulk API.
Godot documents the underlying point, connection and disabled-state methods in
[AStar2D](https://docs.godotengine.org/en/4.7/classes/class_astar2d.html).

V2's input contract uses the ordinary mutable lookup dictionaries and fresh
untyped room-ID arrays created by the game. Sparse IDs, invalid packets, shared
output arrays, bad indices, non-finite values and overflow are checked before
mutation. Read-only or incompatible typed output containers are outside that
private contract; universal validation of arbitrary Godot containers is not claimed.

The template/clearance audit found no current production override that observes a
partially built graph. Companion water exclusions apply after construction; the
actual wet/dry companion path was tested. A future graph-reading clearance
override would require rechecking V2's delayed mutation contract.

## Frozen benchmark method

Evidence is in `C:/bs-bulk-nav-20261015/`; reproducible helper sources are in
`output/bulk-nav-20261015/`. This is the same private 40-room / 52-occupied-cell
large-station cohort, including four large rooms, used by the preceding crew
trial. Private distant-room LOD and one-spare capture setup remain in this frozen
QA cohort; these numbers do not certify the current public export.

Actual release runtime: Godot 4.7.2 `ed1daf0bf`, Compatibility/OpenGL,
RTX 4070 Ti, 1920×1080, debug=false. Each variant has a separate four-process
reference→candidate→candidate→reference series. Each process uses 180 warm frames
then 120 measured frames per idle/placement phase at 1× and 4×. Total: 3,840 timed
frames and sixteen exact state/camera endpoint/per-frame camera-path pairs.
Reference and candidate in each series load the same immutable native DLL; the
reference records zero native calls. V2 candidate counters confirm ten room-batch
calls per process, in addition to 276 point batches, 276 link batches and six resets.

The visible-window/process guard records 253 samples for V1 and 252 for V2, with
zero foreign Godot processes, duplicate game runs or guard errors. Maximum sample
gaps are 0.998 s and 0.638 s. The owner's idle editor remains open, as in the prior
comparison. Loaded-source checks cover Main, its actual synergy constant, Bill and
the render/companion dependencies; all 22 overlay files are frozen and hashed.
The stall-probe source is not separately asserted as loaded. V2 DLL hashes are
guarded before/after all nine release microbenchmark/timing/image runs.

FPS below is 1000 divided by pooled mean frame milliseconds. Compare each variant
with its own reference; the separate series have different reference timings.

## Isolated graph rebuild CPU

Each case has twenty paired calls in alternating order. The warmed result omits
the first pair uniformly; all twenty raw pairs are retained. Simulation/drawing
are outside the timed graph rebuild. Each case first verifies exact graph,
lookup, ID-array, weight, disabled-state, connection-order and seam results.

| Case | V1 reference → trial, ms | V2 reference → trial, ms |
| --- | ---: | ---: |
| Warm unchanged graph | 2.600 → 2.633 | 2.447 → 2.478 |
| Append room | 3.356 → 3.414 | 3.055 → 3.026 |
| Middle rotation / large suffix | 13.919 → 12.999 | 13.319 → 12.367 |

V2 middle-rotation all-twenty means are 13.475→12.439 ms. Both variants save
roughly one millisecond for that large suffix; neither establishes a useful warm
or append gain. Most measured rebuild time survives this approach. The trial
does not separately attribute the remaining time to native mutation, allocation,
script geometry or other preparation.

## Full game FPS and placement

| Normal-speed idle | V1 reference → trial | V2 reference → trial |
| --- | ---: | ---: |
| Mean frame, ms | 20.539 → 19.247 | 19.472 → 20.730 |
| Average FPS | 48.69 → 51.96 | 51.35 → 48.24 |
| p95 frame, ms | 26.831 → 21.233 | 21.123 → 26.346 |

V1's apparent idle gain has no corresponding isolated warm-rebuild improvement;
its two reference order means also drift from 21.384 to 19.693 ms. It is not
accepted as a dependable steady-state gain. V2 idle worsens in both orders
(19.616→21.400 and 19.329→20.060 ms).

| Action frame | V1 reference → trial, ms | V2 reference → trial, ms |
| --- | ---: | ---: |
| 1×, forward order | 48.520 → 46.675 | 48.562 → 45.787 |
| 1×, reverse order | 45.568 → 46.978 | 45.101 → 48.169 |
| 4×, forward order | 69.749 → 69.697 | 68.306 → 71.624 |
| 4×, reverse order | 73.480 → 67.584 | 70.146 → 72.386 |

At 4× V1's crew phase falls 26.656→25.757 and 26.492→25.016 ms, while following
sixty-frame means and p95 worsen in both orders. V2's crew phase is effectively
flat/worse, 25.887→26.040 and 26.227→26.669 ms. Action-frame sampled atlas upload
time is zero throughout these comparisons.

The following table excludes the placement action itself and measures the next
sixty frames, so it reveals work or stalls displaced beyond the action frame.

| Following 60 frames at 4× | Mean, ms | p95, ms | Worst, ms | Frames >50 ms |
| --- | ---: | ---: | ---: | ---: |
| V1, forward | 24.410 → 24.469 | 39.907 → 40.258 | 60.431 → 60.209 | 2 → 1 |
| V1, reverse | 23.900 → 24.252 | 35.766 → 39.383 | 58.969 → 57.097 | 1 → 1 |
| V2, forward | 23.525 → 27.082 | 37.075 → 41.475 | 57.999 → 78.402 | 1 → 2 |
| V2, reverse | 23.518 → 26.042 | 38.255 → 45.610 | 57.397 → 58.666 | 1 → 3 |

V2's 78.402 ms is a later frame, not its 71.624 ms placement action. Normal-speed
placement remains mixed by execution order. Neither series passes any of the
eight existing 60 FPS phase gates: 0/16 in total. The measurements support keeping
both variants private; they do not establish the cause of the full-game regression
or predict a permanent regression on every machine.

## Correctness and appearance

- Final V2 navigation oracle: 9,425 checks, zero failures; 269,812 ordered graph
  records, 2,352 routes and 126,528 sorted targets. Reference graphs explicitly
  disable both packed point/link optimizations and run the original script loops.
  Coverage includes prefix fractions, connected large rooms, layouts, lock policy,
  Moonbay, staged/reference flags, rejection fallback and cleared native context.
  Actual Companion Josh is compared at water depths 0.6, 0.48 and 0, including dry
  reset. The same graph object and actual room-ID array aliases are preserved.
- Extension-absent script fallback: 1,488 checks, zero failures; 259,265 graph
  records and 2,328 routes. Native primitive suites pass 346 + 226 assertions,
  including a bad final packet leaving earlier packets and graph state untouched.
- Twelve cross-process station RGBA pairs are exact across three zooms, lighting
  on/off and two repeats. Twelve within-process repeat pairs are also exact.
  Five first-placement frame pairs are exact, from the initial live draw through
  active/ready capture frames. State, camera and visual sidecars match. A fitted
  station image was visually inspected.

Earlier V1 checks also pass (1,498 navigation checks and 346 primitive checks).
One intermediate V2 harness used `.any` on PackedInt64Array and aborted with a
script error; its exit code was zero but the maintained wrapper rejected the log.
It is not a passing test. Converting that test input to Array corrected the
harness; the final V2 run has no script errors or leak messages. The subsequent
microbenchmark was independently valid and the corrected oracle passed afterward.

## Native build and delivery boundary

Windows x64, MSVC Build Tools 14.44.35207, release/speed/single precision, exact
4.7.2 extension API dump. The pinned
[godot-cpp source](https://github.com/godotengine/godot-cpp/tree/1e7926375b62b445fa79db6851f7105b644831f2)
is `1e7926375b62b445fa79db6851f7105b644831f2`. The minimal
[build profile](https://github.com/godotengine/godot-cpp/blob/1e7926375b62b445fa79db6851f7105b644831f2/build_profile.py)
enables AStar2D, RefCounted and OS. SCons 4.11.1 is installed only in the private
evidence directory. SDK license is copied beside the prototype sources.

V1 DLL is 337,920 bytes, SHA256
`7db299b017171056e3f6e1109d49948a120da5a277895174815bd279b255691d`.
V2 DLL is 346,112 bytes, SHA256
`551a4eb3fe27982fedb7b2ad945bfbfba7f07ca8d8ae1e1650b61464624f2933`.
V1 source and binary are archived in `native-v1/`; V2 never overwrote the V1 DLL.
V2's inspected dependency list contains KERNEL32.dll. An initial SDK build needed
OS enabled for godot-cpp's print helper; the corrected builds succeeded.

Both external `.gdextension` descriptors are explicitly loaded by fixtures before
game creation; nothing is installed or auto-loaded in the normal project. No Mac
binary, release manifest integration or playable export was produced. The maintained
release manifest does not yet include this native packaging route. Shipping would
require explicit platform packaging and release validation, including the
[GDExtension descriptor/export configuration](https://docs.godotengine.org/en/4.7/engine_details/engine_api/gdextension/gdextension_file.html).

## Profile and source audit

All 28 operation guards have zero owner-folder changes. Final 2,948-file non-log
fingerprint equals both this task's initial fingerprint and the prior protected
post-recovery baseline. Installed Bill/Synergy source and paired UIDs match their
accepted hashes. Only the owner's idle editor PID 46624 remains; task game
processes have exited. `final-audit.json` records identities, hashes, checks and
pair counts. Full run logs remain in the evidence directory.

This preserves, rather than erases, the earlier
[profile incident caveat](TEST_PROFILE_INCIDENT_2026-10-15.md): a previous unisolated
test changed an introduction counter (restored from backup) and two legacy test
metadata files. No new profile changes occurred during this bulk-navigation task.

## Next useful investigation

Keep the installed implementation. Inspect why placement requires large suffix
rebuilds for both companion graphs and separate their script preparation from
native graph mutation. A further retention prototype should preserve exact IDs,
ordered links, routes and lock/water policy before any full-game benchmark.
The current native wrapper is not a demonstrated route to 60 FPS.
