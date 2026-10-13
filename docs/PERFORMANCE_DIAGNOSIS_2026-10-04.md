# Performance diagnosis and Windows candidate

Updated: October 4, 2026 · BrineSpace · PC/Mac readiness continuation

October 5 update: the visible, short-profile comparison is complete. See
[accepted packaged results](PERFORMANCE_PACKAGE_RESULTS_2026-10-05.md): twelve
clean runs, lighting p95 improved 19–20%, modest zoom changes, all candidate
performance/memory/loading gates still failing. The interrupted attempts below
remain historical evidence; the PC-availability question is resolved.

## Objective and acceptance

Explain slow zoom/lighting frames, refresh retained-image evidence, implement
measured improvements without changing selected artwork, and test a newly frozen
Windows release. The existing 60 FPS, loading, memory and stability gates remain.
An internal candidate is not approval to publish or a Mac certification.

## Accepted decisions and constraints

- Preserve animation pixels, frame identity, timing, effective filtering and owner
  layouts. No downscaling, frame reduction, lossy conversion or renderer upgrade.
- Run every native fixture in an isolated profile. Keep previous packages and
  failed diagnostic attempts as evidence. Do not upload or change visibility.
- Use one benchmark version for both package versions. Correcting a fixture is
  not a game optimization and does not retroactively certify older results.

## Findings and changes

**The benchmark caused extra redraws.** Advancing the game from `process_frame`
queued drawing before normal node processing, where the grid requested another
redraw. Godot's [SceneTree source](https://github.com/godotengine/godot/blob/master/scene/main/scene_tree.cpp)
shows the deferred-call flush between that signal and node processing. A native
regression reproduces two draws in each of four sampled signal-driven frames,
versus one draw with a normal Node driver, while preserving ten requested
simulation steps. The maintained harness now uses that node-processing phase
with a deterministic 1/60 step and records `simulation_driver`. Historical
signal-driver measurements remain labeled evidence for their original fixture.
This is still an automated workload, not normal-clock gameplay certification.

**Stall tracing narrows the work.** Optional `--trace` retains at most 4096 frame
records, separating action, simulation and render-signal boundaries. The first
1080-frame trace had complete boundaries, with recorded counter-collection p99
207 microseconds. Its slowest frame was 256 ms: about 141 ms before rendering,
16 ms between render signals and 76 ms afterward, plus 23 ms simulation. GPU
timings were approximately 10–13 ms in those slow frames. These are distinct
measurements: [render signals bracket viewport updates](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html#signals),
not GPU execution alone. A 24-callback process trace found no large callback
cost (about 2 ms maximum logged); a subsequent 31-script draw/notification trace
identified repeated surface work. The earlier near-one-second stalls were not
reproduced in these traces and remain unresolved, not declared fixed.

Temporary draw instrumentation initially failed because its wrapper included
StyleBox draw signatures and mishandled CRLF writes. Both failed runs are excluded.
Original bytes were restored, the wrapper narrowed and byte-preserving writes
used. The final trace restored all 31 scripts; the only subsequent difference
from its saved inputs is the intentional grid image-sharing change. No profiling
wrappers remain in runtime source.

**The engine texture counter overstates the controlled no-mipmap allocation.**
On the local Godot 4.7.2 Compatibility runtime, creating a 1024×1024 RGBA8 image
without mipmaps (4,194,304 decoded bytes) increases the texture counter by
5,592,404 bytes. With mipmaps, both decoded and reported allocation are 5,592,404.
Twenty CanvasTexture wrappers add zero to that counter; releasing everything
returns it to baseline. The upstream [GLES texture-storage implementation](https://github.com/godotengine/godot/blob/master/drivers/gles3/storage/texture_storage.cpp)
provides relevant allocation-accounting context, but the local experiment is the
evidence for this build. Do not divide an entire scene's counter by 4/3 and call
that certified GPU residency: other formats, render targets and driver allocation
are not covered by the probe. Preserve raw engine totals alongside inventories.

**Room images now share scene-owned storage.** The grid owns a separate weak-image
pool for dressing and corridor sources. Views receive it before loading. Repeated
immutable PNGs share GPU image objects; generated and composited art is untouched.
The pool and lookup tables disappear with their scene owners. The diagnostic flag
`--unshared-room-images` retains the earlier path. Native checks verify exact
pixels/dimensions, identical storage references, upload counts and resource release.
The 12-room scene's reported total falls from 3689.805 to 3621.842 MiB; the reachable
inventory removes 50.989 MiB of decoded duplicate storage. It does not meet the
existing memory gate.

The pre-sharing 12-room reachable inventory contains 9159 texture records and
2532.573 MiB of decoded image data; unique pixel groups sum to 2404.709 MiB.
8893 records match one or more of 13239 recorded PNG paths, with no source-read
errors. Unmatched generated/mirrored/unrecorded images remain explicit. Atlas
regions and viewport readbacks are not separate physical GPU allocations, and
the walker skips lazy getters: this is not an exhaustive driver allocation dump.
About 1365 MiB is byte-proven removable transparent padding in that inventory,
but changing storage geometry requires separate UV/filtering/identity validation;
no trimming was applied in this candidate.

## Current state

Runtime changes in this continuation: `scripts/grid_canvas.gd`,
`scripts/corridor_layout_view.gd`, `rooms/whole-room/room_dressing.gd` and
`rooms/underwater/corridor_surfaces.gd`. Diagnostic changes:
`tools/release_benchmark.gd`, `tools/run_release_benchmark.py`, paired
`tests/test_release_benchmark_driver.gd` and `tests/test_room_image_sharing.gd`,
their native test-index entries, and the release workflow documentation.

Frozen source: `output/release-stall-trace-2026-10-04/frozen-source/`.
Build: **brinespace-124c70736fbfb879**. Candidate: sibling `candidate/`.
55,687 files / 3,806,576,061 bytes physically copied, with zero source changes
during copying. Only five runtime files differ from the previous frozen baseline:
the four files above and `rooms/full-wall-v1/solar_array_view.gd`; the grid includes
the previously accepted retained wall slots. Selected art/animation inputs are
unchanged. Additional frozen differences are benchmark tooling only.

## Verification

- Room sharing: 22 native checks pass after correcting a null-default metadata
  lookup; the initial error log is retained and excluded from acceptance.
- Driver regression: ten steps, five scheduled node steps, four sampled redraw
  counts per mode, and no repeated consumed work; zero failures.
- Existing zoom regression: six room views, three transitions, zero failures.
- Python checks: nine manifest, two release-copy safety and two assert-safety tests pass.
- Native routing for both new tests verified; paired script UIDs preserved.
- Frozen Windows export succeeds. External empty-directory PCK audit checks
  35,779 assets: zero missing, changed or unexpected files.

Normal entry passes in the actual release template (`debug=false`): intro skip,
title, architect selection, dialogue Continue, active simulation, rendered rooms,
F8 pause/report ZIP/build identity and checkpoint preservation. The first attempt
used an outdated immediate-title assumption. `tests/release_new_game_smoke.gd`
now uses the intro's Space control and waits for observable title state; the second
attempt passes with zero engine/script errors. Its exit warning reports 34 leaked
ObjectDB instances; leak attribution and transition/endurance acceptance remain
open. The 1080p station screenshot was inspected for missing art, card/resource
alignment and general clipping; this is not all nine bug reports or motion review.
All 2,936 owner non-log files remain unchanged.

The additional 40-room reflective inventory was stopped after several minutes of
CPU work without an inventory result. Its partial benchmark is excluded from
acceptance; the separate concurrent export also prevents treating those timings
as clean measurements. The 12-room inventory is valid within its stated scope;
the large-scene source inventory remains incomplete. No runtime code was changed
to accommodate this diagnostic failure. Owner fingerprints were unchanged.

**At the October 4 handoff, no new matched package timing result was accepted.** The first two attempts
overlapped another native release-validation job and were stopped. A third failed
before launch because a retry-script replacement changed the baseline path; that
reference was corrected. The fourth recorded phases but its window was minimized
before final capture; the exact minimization point is unknown, so all its timing
results are excluded. Both packages are preserved. The comparison still needs
three clean, visible runs on each package; 1440p and the new candidate's 12-room
loading runs are not completed. A PC-availability question is pending with the
owner. No concurrent job was stopped or modified.

The maintained benchmark now rejects a minimized window during measured frames
and bounds render completion to five seconds instead of waiting indefinitely.
`tests/test_release_benchmark_render_guards.gd` verifies minimized rejection,
successful visible rendering and timeout (5005 ms); the driver regression still
passes all ten requested steps and expected redraw counts. Both native checks
have zero engine/script errors, and 2,936 owner non-log files are unchanged.
These harness changes are outside the frozen runtime dependency closure and do
not require a game rebuild. No speedup is inferred from an excluded run.

The candidate folder contains build identity, rights/font notices, instructions,
readiness limitations and checksums. Public-distribution notice completeness is
still a release gate. See the dated readiness register for broader open gates.

## Next action

The October 5 package comparison is now complete; use its measured pre-render
intervals to target the next optimization. Keep actual
GPU residency, broad workload/resolution coverage, one-second stall reproduction,
normal save/relaunch/upgrade, bug/visual coverage, endurance and target hardware
testing explicit. Replace the unbounded 40-room reflective inventory with a
bounded source/pool inventory before using it to choose further memory changes.
Mac gameplay/signing/notarization remain external requirements. The next memory
experiment is reversible, pixel-exact transparent-padding removal with UV,
filtering, layering and animation-frame identity checks; it is not yet accepted.
