# Mat repair batch — fresh package follow-up

`output/mat-repair-package-20260906-v1` is a failed traversal review, not an
accepted package. Originals and failed evidence remain preserved.

The selected manifests cover production-ten, whole-room, batch-two, Gravity Loom,
routing, and Construction. Dependency preflight passes 27 profiles. The generated
export bridge initially failed two of seven consistency checks because its station
source had changed; regeneration restored all seven without changing assertions.
Import, resolved dressing hosts and Windows debug export then completed.

The exported runtime, launched outside the checkout, passed 31 source hashes,
62 source/card PNG decodes, 51 additional component checks and 27 profile hashes.
All three crew were established through production recovery/thaw in the fixture.
These successes establish selected asset loading, not traversal acceptance.

Runtime exited 1: `Tour physically arrives at target: (18, 19)` failed on the
first Battery Array leg. The recorded tail has Bill stationary near
(7297.17,7858.32), another active crew member near (7283.19,7873.01), repeated
`waiting for passage`, and a planned-clear path. The final path is empty without
arrival. Controller SHA256 in the failure record:
`bccddbfc95004461c896c8b29539d58524ab546a96618f6e4d6c771ff233e40d`.

Next: distinguish fixture peer scheduling from a production traffic deadlock.
Do not disable crew, enlarge arrival tolerance, teleport the leg or count the
asset checks as successful multi-crew traversal. No verification.json was produced
by the fail-fast helper. Fresh package acceptance remains open.

## Reproduced traffic interaction

Native `output/mat-tour-traffic-trace-v2` repeats the first-leg failure at the
same Bill/Veld coordinates. The test now records all three crew immediately
before and after each movement update in the diagnostic tail. Production
`_update_test_walker` updates every present architect with active-peer avoidance;
this fixture does not freeze Veld.

Bill seeks (7168,7824), Veld seeks (7440,7840), and both remain stationary with
`waiting for passage`, cycling through route abandonment/replanning. Branforth
continues from approximately (8322.56,7872.45) to (8506.54,7874.07) over the same
tail. This isolates a local opposing-route traffic failure rather than a global
clock pause. Next test the exact local positions against registered geometry and
candidate yielding routes; neither arrival tolerances nor crew presence changed.
The native process reached its terminal failure marker and exited; no rerun is live.

## Local geometry probe

`tests/test_battery_passage_probe.gd` reconstructs the nearby Battery cells using
production room geometry and the recorded Bill/Veld positions. The corrected
`output/battery-passage-probe-v2` exits 0 without ERROR/SCRIPT ERROR lines:
Bill's foot is standable, 148 joins in his current cell and 93 in the next cell
are individually clear, but none produces a complete peer-avoiding detour.
The western destination cells have no direct clear join. This rejects the simple
hypothesis that searching additional nearby starting nodes alone will resolve it.

Production cross-cell graph links use door-center nodes; peer exclusion can
disconnect that gateway while leaving ample reachable space on Bill's side.
Next evaluate a local yielding movement that clears the gateway before retrying
the original destination. Do not bypass collision or reduce crew clearance.
This is a static four-cell probe, not a successful multi-crew movement test.
The v1 probe omitted current_scene and logged renderer errors despite exit 0;
that run is rejected, retained separately, and not acceptance evidence.

## Fixture-only yielding study

`output/battery-yield-study-v3` exits 0 with no ERROR/SCRIPT ERROR lines. It
enumerates reachable nodes within 96 world units of Veld, nearest first, and
finds (7248,7872): about 35.2 units back from her recorded position. That point
allows Bill's existing production detour search to find a complete route.

The fixture then moves Veld to that point using `move(0.1)` and moves Bill to
the original (7104,7488) destination. All 116 samples pass maximum displacement
4.601, registered segment clearance and minimum peer separation 19.99. Neither
actor teleports after setup. The original no-detour case remains in the same test.

This is staged sequential movement with a stationary peer during each stage,
not production arbitration, simultaneous traffic, Veld's resumed itinerary,
save/resume, or packaged acceptance. A production solution must select one
yielding actor, preserve/resume intent and prevent reciprocal yielding oscillation.
No production controller change has been made by this study.

Concurrent follow-up `output/battery-concurrent-yield-v5` passes: Bill reaches
the original tour destination and Veld reaches her recorded onward waypoint
(7440,7840), with both controllers advanced each tick and current peer positions.
All 163 movement samples preserve speed, geometry and separation. The fixture
schedules Veld's single yield and return waypoint; production arbitration is not
implemented, and Veld's full unknown maintenance itinerary is not verified.

Rejected v4 study: Bill's reconstructed path omitted intermediate doorway bends
because the failure trace only recorded the next waypoint. V5 obtains the entire
route from the production graph and smoother. Do not infer complete routes from
a next-waypoint diagnostic. The earlier sequential result remains separately scoped.

## Automatic dry-floor passage handling

`scripts/crew_passage.gd` is now called after the normal crew movement updates.
For two nearby, mutually waiting dry-floor crew, stable roster order selects one
yielding actor. It searches short, collision/peer-clear retreats and requires that
the hypothetical retreat opens a complete detour for the other actor. It restores
all hypothetical peer/path state before returning. The accepted retreat and return
point are prepended to the yielding actor's existing path; goal and remaining
route remain intact. Swimming and active locker service are excluded.

`output/battery-auto-yield-v6` passes the simultaneous recorded encounter in 169
samples using automatic arbitration, with unchanged speed/geometry/separation
checks. `output/auto-yield-negative-v1` disables only the coordinator and fails
both arrivals as expected. Existing `test_crew_polish.gd` passes (minimum separation
20.36) and `test_run_save.gd` passes in the corresponding `auto-yield-*-v1` logs;
both exit 0 with no ERROR/SCRIPT ERROR lines.

Remaining: explicit save/restore during the new retreat, native full-station
three-crew replay, varied encounters and a fresh exported tour. Existing save
tests alone do not establish mid-yield continuation or general crowd robustness.

## Native tour and mid-yield checkpoint follow-up

`output/mat-tour-auto-yield-v3` reaches its terminal PASS with 48 arrivals,
48 visited rooms, 135 reciprocal transitions and 10,430 collision/speed samples.
All three crew are present through the same recovery setup. No ERROR/SCRIPT ERROR
lines were recorded. This is the native checkout tour, not a fresh exported pack
or visual animation approval. The previously failing first Battery leg completes.

`output/battery-yield-save-v9` exits 0 with no engine errors. Two movement ticks
after automatic yield selection, it writes/reads an isolated real checkpoint,
clears the old paths, and restores through `run_save.gd`. The newly created crew
controllers match both pre-save snapshots exactly. Continue is paused, and the
fixture subsequently drives their movement to both destinations (169 samples).
This proves path/intent restoration, not UI-driven pause/resume animation.

V7/V8 were rejected fixture runs: they inspected old controller references after
Continue replaced the instances. V9 reacquires `game.bill_npc` and `game.veld_npc`.
Passage helper SHA256 for these checks:
`C8AD8752E016C304FBC0D466D8218E6EE4B8A5A552F394FB1CAF46138A57284A`.
Fresh export, broader encounter variation and native visual review remain open.

## Fresh exported traversal passes

`output/mat-repair-package-20260906-v2` now passes the complete export helper:
27 composition dependency profiles, floor hooks, native dressing hosts, refreshed
bridge (all seven consistency tests), import, debug export and external-directory
runtime. The current Battery v4 composition is included; this is not assumed
pixel-identical to the prior build.

The exported tour passes 48 arrivals/visited instances, 135 reciprocal transitions
and 10,434 collision/speed samples. All three crew are active and progression-present.
`verification.json` records PCK SHA256
`6135E61CB972078A460B70CE21FE0EBA5C11CDC952CCF2FDE07593CCC7526F24`
and executable SHA256
`8515CD8041A906BDF82A3C9926125E20F642A1062CB2A45A962F3A43DFFA41ED`.
The failed v1 package remains preserved. This establishes selected packaged asset
loading and controlled traversal, not autonomous choice, release acceptance,
multi-resolution state review or full-speed visual animation approval.

## Resolution checks — Reactor remains open

Combined `output/mat-state-export-1280-v1` passed Anomaly, then Reactor exited 1
with six legacy perimeter clearance assertions (q1 east-entry samples 23–26;
q2 south-entry samples 13–14). The helper stopped before larger resolutions.
This failure does not invalidate the separate passing controlled station tour,
but prevents acceptance of the older Reactor fixture.

`playtest_whole_room_station.gd` constructs these checks by changing
`test_walker_progress` and reading the legacy position getter, not by advancing
the production NPC. Compare that route and its visual-foot offset with current
registered geometry before modifying either the art or assertions. Preserve the
failing log; successful production traversal does not make this failure disappear.

Anomaly-only `output/anomaly-mat-export-1280-v2` and `1600-v2` both pass on the
same v2 PCK: 53 dimension-checked full frames each, with input-isolation exercises.
The 1600 q3 room crop was inspected; cart/lamp separation remains visible.
These are 106 verified full-frame records, not three-size acceptance.

`output/anomaly-mat-export-2560-v2` failed 68 assertions. The first failures are
injected-key menu/pause isolation; subsequent captures report the game menu
obscuring the room, followed by invalid motion comparisons. Treat those pixels
as contaminated, not proof of broken Anomaly machinery. No verification.json
was written for that size. Diagnose fixture input isolation before repeating;
do not close the menu after contamination and count the old frames as valid.

Input-isolation follow-up: the shared art harness previously waited for window
setup/render frames before disabling Main input. It now disables process polling,
input, unhandled input/key input and GUI input immediately after adding the scene,
before those awaits. The injected-key check additionally asserts an unobstructed
paused baseline and disabled input gates. Production input behavior is unchanged.
This closes an observed initialization gap; the old log alone cannot establish
which physical or injected event originally opened its menu.

`output/anomaly-input-2560-v3` then passes the native 2560x1440 Anomaly fixture,
including Escape/W/Space injection, all rotation/state assertions and 404 socket
samples, child exit 0 with no ERROR/SCRIPT ERROR lines. This is fresh checkout
evidence, not a repair to the already-exported v2 PCK. Regenerate/rebuild the
export bridge before claiming the new isolation behavior in a package.

Reactor legacy diagnosis: current registered bounds place its service cylinder
at q1 Rect2(55,-84,24,8), q2 Rect2(58,109,24,8). The six reported legacy-foot
samples intersect those rectangles expanded by the legacy 7-unit radius. The
fixed perimeter waypoint route does not account for that accessory. No furniture
was moved to accommodate the proxy route.

Dedicated production comparison `output/reactor-current-route-v5` also has an
open failure, separately from the proxy: q0/q2/q3 tours complete six arrivals
each (642/692/693 samples), but q1 abandons its second leg as `route obstructed`.
The record is `reactor-q1/controlled-tour-failure.json`: foot
(7862.20654296875,7634.875), next (7856,7728), planned_clear=false, destination
Battery (19,20). Thus do not dismiss all outstanding route work as legacy-only.
This newer dedicated layout is different from the passing 48-instance package
tour. Next inspect the failing actual segment and its room/doorway blockers.

Exact segment reproduction `output/reactor-segment-v2` confirms the whole planned
line (7872,7488) → (7856,7728) was accepted, but incremental movement stopped at
the recorded foot. The remainder intersects a Battery blocker at world
Rect2(7728,7554,134,84). The intended line grazes its (7862,7638) corner;
incremental float drift crosses inside. This is not a Reactor furniture defect.

The authored-blocker planning sweep now reserves 0.05 world units beyond its
existing bounds (then clips to cell ownership). Collision is not reduced; walls,
doors and furniture remain unchanged. `output/reactor-segment-margin-v3` rejects
the tangent and reaches the original target through the production graph/smoother,
exit 0 with no engine errors. The first probe v1 had a type-inference parse error
and is not evidence. Full rotation/crew regressions and fresh packaging must be
repeated before accepting this planning change broadly.

Margin follow-up: `output/reactor-margin-tour-v6` now passes all four rotations
and returns: six arrivals/eight reciprocal transitions per layout, with
643/693/693/694 movement samples. No ERROR/SCRIPT ERROR lines; terminal fixture
PASS confirmed and process no longer live. `margin-segment-v1` passes rotated,
reverse, doorway, stationary and smoothing regressions; `margin-crew-v1` passes
crew interaction at minimum separation 20.36; `margin-yield-save-v1` passes the
automatic yield plus mid-retreat disk restoration. All three exit 0 cleanly.

The character pipeline's project and installed Godot-integration references now
include the verified tangent-replay and post-Continue controller-rebinding lessons.
Both validate and match SHA256
`C45492401A7E570A559260B50B6DCE77B0F4644BB00B2F31F40A8EA5D593C67D`.
This is a focused evidence-backed guidance amendment, not an independent skill
behavior benchmark. No new visual direction was added to the bible. Fresh package
coverage for the margin and early-input isolation changes remains pending.

## Package v3 — split results

`output/mat-repair-package-20260906-v3` includes the planning margin and early
input isolation. Dependency/host/export checks and seven bridge consistency tests
pass, but the full tour hits its 180-second runtime limit after 25 arrival captures.
The helper stops its owned runtime; there is no terminal tour pass and no package
verification.json. No ERROR/SCRIPT ERROR lines were present before timeout. Do
not transfer v2's complete-tour acceptance to v3. Determine whether the remaining
leg stalls or simply exceeds the bound before changing the timeout.

Independent exported Anomaly review on this exact v3 PCK passes at 2560x1440 in
`output/anomaly-export-2560-isolated-v4`: exit 0, input-isolation exercise, 53
dimension-checked full frames and subject-specific state/rotation assertions.
PCK SHA256: `B419D77B247AB252613DEED766C0FAF9EAD4F5817A5745E8F529319DB3CF592E`.
This resolves the high-resolution fixture contamination for the tested package,
but does not establish a completed v3 station tour or all three sizes on one PCK.

Same-PCK traced replay `output/mat-package-v3-traced-replay` finishes at about
49 seconds: 48 arrivals, 135 transitions, 10,447 samples, terminal PASS and no
engine errors. The process exited and the PCK hash remains B419D77B…CF592E.
Do not conclude the earlier timeout was solely performance: Veld and Branforth
randomize independent decision generators, while the older fixture seeded only
the station RNG. These runs did not have identical traffic histories.

The native tour fixture now assigns and records all three crew seeds before
recovery/movement. Default review seeds are 77321/77322/77323; `--crew-seed=`
changes the base for varied tests, not normal gameplay. Next repeat one seed
against identical source revisions, compare trajectories, then run varied seeds
without discarding failures. This new fixture requires regenerated package code.

Seeded native checks: `output/seeded-tour-repeat-a-v1` and `repeat-b-v1` both
pass seeds 77321/77322/77323 with 48 arrivals, 135 transitions and 10,443 samples.
Their `controlled-tour-trace.json` files match byte-for-byte, SHA256
`B52070EBEB4D7B0378196A9F824C3EEF9D22F64D838C37CA54B0E6397517C01B`.
This trace records Bill's itinerary/positions, not every peer's full trajectory.
`output/seeded-tour-variant-v1` passes seeds 88432/88433/88434 with the same
arrival/transition counts and 10,429 samples. All three child exits are 0 with
no ERROR/SCRIPT ERROR lines.

Reproducibility limitation: aggregate script/room/test GD+JSON inventory changed
during these shared-checkout runs (500 files / 43ab6e7d…e25a7b to 502 files /
f5f91e8e…e4e808). Identical observed repeated traces are established, but this is
not a frozen-source benchmark or broad randomized-traffic reliability estimate.
Retain the earlier unseeded timeout. Use an immutable package for the next seeded
comparison and include peer trajectories if claiming whole-crew determinism.
