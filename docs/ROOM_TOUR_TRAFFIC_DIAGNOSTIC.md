# Controlled room tour and occupied destinations

## Biodome canopy package follow-up

`output/batch-two/biodome-canopy-package-v1` fails its ordinary controlled tour
after 17 completed legs at Battery Array `(25,20)`. Bill remains at
`(9614.9824,7872)` toward `(9792,7872)`; the recorded Veld position is
`(9635.5791,7878.2612)`. The final trace repeatedly reports waiting for passage,
a statically clear next segment, and traffic retries before route cancellation.
This identifies the observed failure state, not its complete underlying cause.

Runtime exits 1 with the exact-arrival assertion. No collision assertion is
reported. Source/card/component/profile loading succeeds. The same PCK's individual
Biodome fixtures pass at all three sizes; see `BIODOME_CANOPY_REPAIR.md` for hashes.
Controller SHA-256:
`1F1E3C1923AEB6CADCB8FF03DD99F11723BD7BF4BC87700F83E2A8FAB082350A`.
Retain `captures/controlled-tour-failure.json` and the failure screenshot for
reproduction. Do not infer that a later controller or a retry reproduces this run.
No movement, avoidance, retry limit or room collision was changed in this pass.

Follow-up now reproduces one mechanism with the recorded Bill/Veld positions:
the nearest safe graph entry is disconnected by padded peer exclusions, while a
farther safe entry has a route. The narrow join-selection repair and regression
evidence are in `BATTERY_TRAFFIC_JOIN_REPAIR.md`. The failed package remains
failed evidence; this snapshot does not reproduce its entire multi-crew history.

## Standalone follow-up: v19

The ordinary Windows debug tour passes outside the checkout: 30 arrivals/visited
rooms, 84 reciprocal transitions and 6,381 movement samples. All 36 full-frame
PNG captures independently measure 1600x900. This run required zero traffic
replans. Twenty source hashes/40 PNG decodes, six component assets and two
composition profiles pass, with no engine errors (raw-image warnings remain).
Evidence: `output/batch-two/windows-validation-v19/verification.json`.
PCK SHA256: `75B3D2082E25E88044E519F6AD8481F4777F01433A1B2A2F0E21A3AD58FE02F7`.

The same build's occupied-target attempt is retained as a failure in
`output/batch-two/tour-occupied-export-v19`. Before reaching the deliberately
occupied Holo target, it exhausts traffic retries near Crew Lounge `(25,19)`.
Bill ends at `(9774.816,7668.466)`, Veld at `(9788.690,7650.053)`, with waiting
for passage and an empty route. Seven legs completed. No collision or speed
assertion failed. This is persistent crew traffic in that run, not a successful
exported test of the Holo injection. Veld's independent random choices mean the
native success does not guarantee this same itinerary on every run.

The retry bound remains intact. Broader crew-traffic liveness needs separate
investigation; ordinary exported traversal is verified, adversarial exported
traffic recovery is not. No production movement or art was changed in v19's
verification pass. Historical pending-export text below refers to earlier work.

The v18 export failed exact arrival at Holographic Core `(25,21)`. It did not
record traffic state, so its precise cause cannot be proven retroactively.
A fresh ordinary native run (`tour-arrival-diagnostic-v1`) reached all 30 rooms,
84 transitions and 6,377 collision/speed samples without a room-art change.

## Reproduced failure mechanism

Main updates both Bill and Veld. Veld has independent randomized decisions;
the old itinerary assigned Bill an exact node without guaranteeing it stayed
unoccupied. Production Bill intentionally cancels travel after three seconds
of unresolved crew traffic. The tour treated that cancellation as a failed room.

`--tour-occupied-target` places Veld at Holo's target for a 60-second fixture
rest while keeping production avoidance enabled. Before the scheduler repair,
`output/batch-two/tour-occupied-target-v1` exits 1: Bill stops at
`(9790.786,8234.173)` short of target `(9792,8256)`, reports waiting for passage,
and clears his route after traffic_wait reaches 2.9 then resets. Source collision
and speed checks did not fail. This reproduces the mechanism, not the missing
v18 traffic trace.

## Fixture-only correction

The controlled itinerary may now replan to the same exact node only after the
explicit waiting-for-passage cancellation. At most 24 replans fit within the
unchanged 5,000-step leg budget. Geometry obstruction, missing graph routes and
failed physical arrival still fail. No production controller, room registration,
collision, crew separation, gameplay rules or saves were changed.

Native `tour-occupied-target-v2` passes all 30 arrivals, 84 transitions and
6,781 movement samples; Holo arrives after 13 traffic replans. Each successful
leg records its replan count. Failed legs now preserve the last 40 traffic/foot/
peer samples, endpoint, controller hash and a native failure frame.

The `--negative-tour-occupied-target` companion flag extends that fixture rest
to 600 seconds to test bounded failure. It must be combined with
`--tour-occupied-target`; this is diagnostic placement, not normal crew behavior.
Negative v2 exits 1 with the expected Holo physical-arrival assertion: the
destination remains occupied, and the fixture preserves its failure trace/frame
rather than accepting graph reachability. A fresh packaged tour remains pending;
the native scheduler fix does not retroactively pass v18.

The first negative attempt (`tour-occupied-target-negative-v1`) could not execute:
concurrent UI edits left Main with unresolved function references at load time.
The runner stopped only its own process after its timeout. Those logs are kept;
they are not evidence of bounded traffic failure. Once the functions were present,
the negative case was retried in a new directory without changing the UI work.

The separate crew-polish regression reports PASS with minimum separation 20.61
and checks crew checkpoint restoration; its log has no engine errors. The export
bridge's five consistency tests pass after regenerating from the source fixture.
Raw-image warnings remain in native logs.

Workflow lesson: a room-art traversal itinerary and autonomous crew destination
choice are different tests. Preserve traffic diagnostics and strict arrival
assertions rather than moving furniture or disabling avoidance to make a tour
pass. Original v18 remains failed evidence; no new room aesthetic rule follows
from this scheduler correction.

## V20 ordinary packaged tour

The fresh Xeno-card-v4 package loads all 20 selected sources, 40 raw PNGs,
six component assets and two composition profiles, but the ordinary tour exits
1 at Crew Lounge `(25,19)` after seven completed legs. No occupied-target flag
was used. The retained trace ends at step 921 with Bill waiting for passage,
an empty route and Veld still nearby. This reproduces the broader traffic stall
without adversarial placement; it is not a room-art loading failure or a passing
whole-station traversal. Keep the bounded arrival assertion unchanged.

Evidence: `output/batch-two/windows-validation-v20/runtime.log`, `runtime.err`
and its captures. Pack SHA256:
`A1399F00525F1A6BAD0B8D3FFF08807106AE65DFAD3D11D44201646824412A1F`.
Individual Xeno exported state checks against this pack are a separate scope.

## V21 ordinary tour follow-up

The Biodome-card-v4 package passes the ordinary controlled tour: 30 arrivals,
84 reciprocal transitions and 6,333 movement samples, with no traffic replans.
All 36 full-frame captures measure 1600x900. Asset loading checks also pass;
the runner reports no engine errors, while raw-image warnings remain.
Pack SHA256: `E15270102F1A4895F8F6CA15B1AAA14EDE64740E0B1AA5FE71AFB8B94F007987`.
Evidence: `output/batch-two/windows-validation-v21/verification.json` and captures.

Its recorded controller hash is
`4a627ee7af448bd57edd40d9c6d584fc720d738be175284055a4e2192e2b09bd`,
different from v20. This art-verification pass made no movement-controller edit
and did not isolate the effect of concurrent controller changes. The successful
run does not establish a traffic fix or invalidate retained v18/v20 failures.
Adversarial and repeated traffic-recovery coverage remain separate.

## V22 Research Lab obstruction

The Holo-card-v7 package loads 20 selected sources, 40 raw PNGs, 11 component
assets and five composition profiles, but its ordinary tour exits 1 at Research
Lab `(19,19)` after one completed leg. At step 504 the route is cancelled with
`route obstructed`, following waiting-for-passage samples and brief movement.
Bill's final foot is `(7461.1504,7702.0303)` versus target `(7488,7488)`; Veld is
nearby at `(7490.9121,7707.0117)`. Do not classify this as a proven traffic-only
stall: changed furnishing geometry and the actual blocked movement need review.

The controller hash matches v21, but the package includes more component and
composition assets. Neither coincidence proves a cause. No controller, furniture,
collision or arrival assertion was changed in this Holo verification pass.
Evidence: `output/batch-two/windows-validation-v22/runtime.log`, `runtime.err`
and failure captures. Pack SHA256:
`3A51B01D450721425EBE25F12E727424FB71C550E67CA05CD2455D1F0B94DB8C`.
Individual Holo state checks remain separate from this failed station tour.

## Research approach: reproducible sampled-clearance disagreement

The native `research-route-diagnostic-v1` tour passes 30 arrivals, 84 transitions
and 6,355 movement samples. It does not reproduce v22's cancellation. Its fixture
now retains the pre-step foot, next waypoint and complete-segment clearance in
the failure tail, because the former trace discarded the waypoint on cancellation.

Focused probe v1 stopped before geometry review on a concurrent Storage Bay
composition/hash mismatch; no asset gate was weakened. The subsequent explicit
`--research-corner-probe` mode builds only the connected Battery Array/Research
pair and reports subject `research_corner_probe`, not full-station acceptance.

`research-corner-probe-v2` and `-v3` test v22's last safe foot
`(7461.150390625,7702.0302734375)` toward `(7488,7504)`. That waypoint is inferred
from the last movement direction, not recovered from the old log. Current
`segment_clear` reports the complete segment clear. Sampling at 0.1 units finds
23 blocked points beside the north doorway of the Battery Array in cell `(19,20)`.
The local blocking rectangle is `Rect2(-202,-210,176,36)`: its inner corner is
`(-26,-174)`. This is a wall-clearance boundary, not Research furniture.

V3 also executes one normal `move(0.1)` step without a peer: the NPC stays at the
same foot, clears the route and reports `route obstructed`. Thus the long-segment
sampling false negative is reproducible independently of crew avoidance. The
precise original v22 waypoint remains unknown; do not claim full historical replay.
Both focused probes exit zero because they are diagnostics, not passing safety
regressions. Their JSON records explicitly preserve `coarse_clear=true` and the
blocked samples. The full record is under `output/batch-two/research-corner-probe-v3`.

No renderer, furniture, wall width, collision margin or production controller was
changed. Next: add a failing clearance regression and make planned-segment and
movement collision agree at near-tangent corners; retain the actual room geometry.
The regenerated export bridge passes its five tests after diagnostic additions.

## Exact registered-blocker sweep

`bill_npc.gd` now adds an analytic segment/rectangle intersection check for
registered modular blockers. Blockers are clipped to their owning cell to match
`can_stand` at shared boundaries. Existing point checks remain for corridor,
legacy and topology constraints; this is not a claim of exact polygon sweeping
for those other geometries. No blocker dimensions, furniture or door art changed.

`tests/test_npc_segment_clearance.gd` uses the literal recorded wall corner in
four orientations. Before v1 fails the forward/reverse crossing and smoothing
assertions; after v1 passes, including clear doorway and stationary-point cases.
`research-corner-probe-v4` reports the formerly accepted segment as blocked.
The actual graph/smoother now chooses `(7488,7584)` then `(7488,7504)` and reaches
the target in 44 normal movement steps with every tested segment clear. The old
direct path remains blocked as intended. The waypoint remains an inferred v22
candidate; this does not recover the discarded original path.

Broader evidence is mixed and retained under `output/batch-two/segment-*`:
crew-polish and Dr. Veld v1 pass (minimum crew separation 20.04). Bill v1 reports
one movement-geometry assertion without old-step detail. Diagnostic Bill v2/v3/v4
pass, including 136 room/rotation checks each. Bill v5 fails its wandering and
complete-equipment-action coverage expectations, not movement clearance. These
varied needs-driven runs do not establish a fully clean crew regression pass.
The Bill fixture now records before/after feet and paths on movement failures.
Investigate remaining failures without weakening their assertions.

Both character skill copies now explain the sampled-corner failure and preserving
safe bends. Existing bible rules already require accurate paths and unchanged
shared geometry; no new aesthetic direction follows from this controller repair.
Fresh full-station and exported verification of this controller remain pending.

## Reproducible multi-crew regression scenarios

`test_bill_npc.gd` previously seeded only the station RNG. Veld and Branforth
randomized independent decision generators, so a repeat did not reproduce all
three actors' decisions. The fixture now recreates all three actors before the
first update, using `--crew-seed=N` for station/Bill and N+1/N+2 for their peers.
Default remains 2217. Production randomness, avoidance, costs and assertions
are unchanged; this is not a controller behavior fix.

Optional `--trace-path=res://output/...json` records all three actors' feet,
state, activity, goal, path and needs for 3,600 steps, plus the seed and controller
hash. It refuses an existing destination. The log includes a trajectory hash even
without a file. Before/after waypoint diagnostics remain on movement failures.

Six fresh runs pass: seeds 2217 twice, then 2218, 2219, 2220 and 2221. Evidence:
`output/batch-two/crew-seeded-2217-{a,b}.{json,log,err}` and
`crew-seeded-{2218,2219,2220,2221}-a.{json,log,err}`. The repeated 2217 trajectories
were compared as complete parsed arrays and are identical, not merely identical
PASS banners. Their trajectory SHA256 is
`73c00c31b3c602bda0ccbe20c7e3549ee4d304bc078afc4ed374e25eb40dee68`.
All use controller SHA256
`25a06732cc77336ca9f5162a8e232f406b7c34851e17208443053b2cd305ce1c`.

Each run retains the original movement, needs, work-action, pause and 136
room/rotation gates, without engine errors (raw-image warnings remain). Read-only
trace analysis found minimum pairwise foot separations of 20.0886, 19.9980,
20.0894, 20.1109 and 20.0118 units for seeds 2217–2221 respectively, within the
existing 0.01-unit crew-clearance tolerance. These are sampled recorded positions,
not a proof of every continuous inter-actor path or all possible schedules.

Older unseeded movement/action failures remain preserved; their exact random
states were not recorded and these passes do not retroactively reproduce them.
Both character skill copies now require seeding each generator in reproducible
fixtures and retaining multiple seeds. The bible's appearance and geometry rules
are unchanged. Fresh native full-station/export coverage remains pending.

## V23 preflight and waypoint-chord diagnostic

`windows-validation-v23` is rejected evidence: Cryo Chamber line 63 could not
infer `scale`'s type, cascading into scene/controller initialization failures.
It is not a traffic or art-state verdict. The current Cryo source already had
an explicit float annotation when inspected; this pass did not modify it.

`post-cryo-crew-v1` reached all 136 room/rotation checks but failed one movement
assertion at step 3542. `crew-bend-diagnostic-v1` repeats the same failure and
trajectory hash `19c1d07e4956285bd65de2dfecb36aa6b354f7c4e0feafb8c229cc722fac0170`.
It retains a full three-actor trace. The controller still has SHA256
`25a06732cc77336ca9f5162a8e232f406b7c34851e17208443053b2cd305ce1c`;
concurrent scene/furnishing changes mean this is not the earlier six-run snapshot.

The tick travels from `(7426.705,7922.705)` through consumed waypoint
`(7424,7920)` to `(7423.653,7919.307)`. Both individual legs pass clearance;
the endpoint chord fails. `move()` sweeps each leg before assigning its foot.
This supports a chord-measurement false positive for this specific recorded
failure, not proof that every older unseeded failure had the same cause.
The test now prints consumed-leg diagnostics; its failing assertion remains
unchanged pending independent coverage of an actual-traveled-path test oracle.
No production movement, geometry, room art or collision dimensions changed.

Both character integration references now distinguish traveled legs from an
endpoint chord and require matching revisions for seeded comparisons. Their
quick validators pass and reference hashes match. The visual bible is unchanged:
this is a verification lesson, not a new visual contract.

## V24 packaged station: arrivals completed, acceptance failed

`windows-validation-v24` PCK SHA256:
`19aac3fb19892699fd2dc0dd2435bf2c3fae2ee0cb6b8f4e80ac6f2fa160c39d`.
The trace records controller `25a06732...` above. Asset gates pass 20 selected
source hashes, 40 PNG decodes, 16 component hashes/decodes and nine composition
profiles. The controlled itinerary reaches all 30 arrivals with 84 reciprocal
transitions and 6,366 samples, but runtime exits 1 with one collision assertion.
Do not report this as a passing tour. Its checker also uses endpoint chords;
the exact failed tick still needs isolation before attributing it to the native
bend case. Arrival trace and frames remain under this package's `captures/`.

The error log additionally records a JSON parse/nil-dictionary error from
`room_dressing.gd:10` while `underwater_life_support_view.gd:20` initializes.
The nine passing profile checks therefore do not establish complete furnishing
dependency coverage. Investigate the Life Support profile/package registration
separately; no fallback or error suppression was introduced. Native/exported
visual approval remains separate from these technical results.

## Life Support package isolation investigation

The first mounted-PCK probes (`life-profile-pack-v24`, `life-renderer-pack-v24`)
ran with the checkout as the project and reported a valid profile. Those are
**not package-presence evidence**: mounting falls back to local files.
`life-profile-isolated-v24` instead uses an empty temporary project directory
and reports `exists=false`, zero bytes and JSON parse failure for
`res://rooms/whole-room/life-support-composition-v1.json`. This establishes a
missing v24 packaged dependency, despite its presence in the current checkout.

The read-only `tools/inspect_pack_profile.gd` now refuses a project directory
containing `project.godot` before mounting. `profile-isolation-negative-v1`
exits 2 with that guard, preventing the observed false positive. Both room
pipeline production references include this lesson and pass quick validation.

A fresh headless editor import (`pre-export-import-v25`) exits 0 without engine
errors. Export v25 then hits the existing 60-second export timeout while storing
files at 54%; its child is stopped and evidence retained. It never reaches a
runtime test. The helper now accepts a separate bounded `ExportTimeoutSeconds`
(default unchanged at 60) without changing runtime timeout or acceptance gates.
This does not yet prove the stale-scan hypothesis; verify the next package from
an empty directory. Logs also show QA images being included by the broad PNG
filter; dependency-aware packaging reduction is separate pending work.

V26 completes export after that refresh. PCK SHA256
`7f67d9479aec0f30710ce26620ac931a02b0e9ddbe99be6f0bc86d8bcc906a25`.
`life-profile-isolated-v26` exits 0 in an empty project: 6,908 bytes, valid JSON,
SHA256 `29db1666722602439e3df15abc623310faf040e1297ce6cf7062b17b2c7acb87`.
The runtime log no longer contains the Life Support JSON/nil error. The helper
now explicitly performs the same checked headless editor import after fixture
generation and before export; default export timeout stays 60, while this run
used 180. That sequence was exercised manually for v26; the newly integrated
helper sequence still needs its next end-to-end run. PowerShell parsing and
all five export-bridge unit tests pass.

V26 remains failed traversal evidence: all 30 destinations are reached over 84
reciprocal transitions and 6,400 samples, but one collision assertion remains.
The current fixture records its tick: before `(7438.6055,7824.3804)`, next
waypoint `(7440,7824)`, after `(7440.5483,7820.8936)`, Battery Array `(19,20)`,
target Research Lab `(19,19)`, step 189, planned segment clear. Preserve this
sample for the traveled-leg investigation; the JSON fix does not clear that gate.

## Actual-traveled-leg observer

`tests/traced_bill_npc.gd` is a fixture-only subclass of the current controller.
It delegates update, movement and clearance to production code, observing foot
changes between movement checks and at return. It records actual assigned feet,
not attempted pathfinding queries or a reconstructed guess from the final path.
Both the Bill fixture and controlled tour now sweep those legs and additionally
bound their summed distance; net displacement, independent renderer-foot checks
(Bill fixture), speed limits and reciprocal-door checks remain.

`test_npc_movement_trace.gd` uses a literal rectangular obstacle and a two-leg
bend with a blocked endpoint chord. The initial endpoint-only observer fails
three assertions (`movement-observer-red-v1`); the completed observer passes
(`movement-observer-green-v1`, exit 0, clean log). It also rejects a recorded
direct corner cut and verifies that a rejected attempted move records no travel.
No production controller or room geometry was edited by this observer pass.

`crew-observer-2217-v1` passes the existing 136 room/rotation checks and 3,600-step
crew scenario with no engine errors. Its complete parsed trajectory is exactly
equal to `crew-bend-diagnostic-v1`, hash
`19c1d07e4956285bd65de2dfecb36aa6b354f7c4e0feafb8c229cc722fac0170`.
Thus this measured failure is corrected without changing the traveled route.
Current controller hash during this pass is
`ffe25488002785a2be38f531d340f5b17ef5aa623827c8d771c1f730212b3f8d`;
other ongoing controller changes predate this observer pass.

V27 exercises the integrated pre-export import and correctly stops before
export: `salvage_drone_bay_view.gd:66` references undeclared `drone_deployed`,
cascading into Main compilation. This is retained failed import evidence, not
a traversal verdict. The new observer's full packaged-tour result remains
pending. The five regenerated export-bridge consistency tests pass.

V28 runs after the concurrent Salvage declaration appears. Import and export
complete; PCK SHA256
`851771af5b5f4f88ee4598239be992a58a65b70731cb944d2a7f668a07f7db4d`.
The controlled movement fixture passes all 30 arrivals, 84 reciprocal transitions
and 6,359 sampled ticks with zero assertions using the traveled-leg observer.
This closes the packaged movement-measurement check, not global traffic or art
acceptance. Runtime exits zero, but the export helper correctly rejects the
package for logged image-buffer/assertion/null-texture errors originating in
`scripts/drone_art.gd:14`, called by Mining Drone Bay. Investigate the new atlas
dependency in isolation next; the live renderer now references
`assets/drones/fleet-v1/atlas-matte-v1.png`, which is not proof of its packed path
or availability. No error filters or acceptance gates were relaxed.

## V28 drone atlas dependency diagnosed

`drone-source-isolated-v28` confirms the packaged renderer's exact SOURCE is
`res://assets/drones/fleet-v1/atlas-matte-v1.png`. The new PNG branch of the
read-only package probe reports `exists=false`, zero bytes and exit 1 in
`drone-png-isolated-v28`. A positive control (`life-png-isolated-v28`) loads
the 1254-square Life Support image from the same PCK with matching hash and exit
0. Neither run can fall back to the checkout. The failure is missing packaged
bytes, not an inferred palette, chroma-key or room-geometry defect.

Both drone-bay component asset lists now register the shared atlas at SHA256
`01825580fbe892cd290ed3b9583304ba27a7cc86da17937cc7ba1c5bdea03b40`.
Current source PNG verifies at 1536x1024 and both manifest hashes match. The
existing packaged component gates will check it before traversal on the next
build. Older room-art state evidence does not cover the substituted drone props;
new visual/state/card coverage remains pending. No atlas pixels were edited.

Both room production-skill references now cover isolated PNG diagnosis and
shared runtime atlas registration. Five export-bridge consistency tests pass.
Another full export was deferred with about 5 GB of disk space remaining;
retained evidence was not deleted. This is not a claim that the v28 package has
been repaired in place or that a fresh package has passed.

## V30 closes the raw-atlas packaging failure

Disk recheck before this pass reported about 278 GB free; no files were deleted
by this pass. The current composition audit passes 14 profiles across production,
whole-room and batch-two manifests. V29 then fails the newly added drone atlas
component gates before traversal. Its export log contains the atlas `.ctex` and
`.png.import`, but not the original PNG. This rules out a scan-only explanation:
`addons/brine_raw_export/plugin.gd` explicitly enumerated runtime raw-image roots
and omitted `assets/drones`.

The exporter now adds that directory alongside the existing roots. No runtime
loading, image pixels or collision geometry changed. V30 import, export and
external-directory runtime all pass, with no ERROR/SCRIPT ERROR entries. The
fixture verifies 20 selected source hashes, 40 source/card PNG decodes, 18
component checks, nine profile checks, 30 arrivals, 84 reciprocal transitions
and 6,345 movement ticks with zero assertions. Raw-image warnings remain.

PCK SHA256 `b7cf2ac0871d6fd289e890dbe2116a2e71e82a93c36ca9f3f0728c46d67cde8f`;
the checked helper writes `windows-validation-v30/verification.json`.
`drone-png-isolated-v30` independently loads the raw atlas from an empty project:
2,007,495 bytes, 1536x1024, SHA256
`01825580fbe892cd290ed3b9583304ba27a7cc86da17937cc7ba1c5bdea03b40`, exit 0.
The earlier failed packages remain failed, preserved evidence.

Both room-production skill references now require checking raw-export roots for
new image directories, distinguishing imported textures from FileAccess bytes.
The export-bridge's five tests pass. This closes packaged dependency and scheduled
traversal checks for this snapshot, not new drone-prop visual/state/card approval,
all-room aesthetic acceptance or autonomous traffic under every schedule.
