# Second-batch Windows validation

## Anomaly indicator follow-up: v12

Current Anomaly card v8 passes all three actual viewport sizes via
`output/batch-two/anomaly-indicators-export-{1280,1600,2560}-v1/verification.json`:
1280x720, 1600x900 and 2560x1440, 53 dimension-checked full frames each (159 total).
All runs pass four rotations, three economy states, per-host motion/offline/pause,
containment, socket sampling and deliberate input isolation. Exit codes are zero;
ERROR/SCRIPT ERROR scans pass. Existing raw-image warnings remain.

V12 PCK SHA256:
`8740D205DBEB742BA5D8E4A808F355087325207C81ED313C6D4D5371A51C0463`.
Its controlled tour passes 30 visited/arrivals, 84 transitions and 6,367 samples.
Reviewed Anomaly native room crops: 1280 q0 and 2560 q3. These do not include
shared walls/doors and do not establish complete visual, autonomous-walker or
release acceptance. Other rooms' earlier v11 evidence remains scoped to v11.

## Current repaired-room coverage: v11

`output/batch-two/repaired-exact-export-{1280,1600,2560}-v1/verification.json`
records all twelve serial runs passing: Biodome card v3, Holographic Core card v6,
Xeno Lab card v3 and Anomaly Lab card v5 at actual 1280x720, 1600x900 and
2560x1440. Each resolution includes 61 full frames per Biodome/Holo and 53 per
Xeno/Anomaly: 684 independent PNG-header dimension checks in total. Each also
passes deliberate Escape/W/Space input isolation, the subject's four rotations,
economy cases and host motion/offline/pause assertions. Exit codes are zero and
logs contain no ERROR/SCRIPT ERROR entries. Raw-image loading warnings for wreck
assets remain; this is not a warning-free release build.

The shared v11 PCK hash is
`822D9E049399949D2E081315568F7E8A28BE145AF5D7089097BCAFD9EF330048`.
Its separate controlled-tour verification records 30 arrivals/visited rooms,
84 transitions and 6,367 movement samples. This is controlled traversal, not
autonomous destination-choice acceptance.

Native room crops reviewed in this follow-up: 1280 Holo q0 and Biodome q2;
1600 Xeno q1 and Anomaly q3. Machinery remains upright and readable at these
small scales. These crops exclude shared walls/doors and are not seam or full
48-rotation visual acceptance. Fine material/edge cleanup and owner review
remain open. This closes the corrected three-resolution gap for these four
revisions only, not every current room.

## Coverage correction: requested size is not actual size

Fixture sizing follow-up: merely assigning windowed mode still yielded 2560
frames for Biodome's requested 1280 run (`biodome-pipe-exact-1280-v5`, failed).
The harness now gives Preferences a fixture-local unsaved path before Main's
initialization and explicitly clears borderless mode. It neither reads nor
overwrites the player's settings. The subsequent 1280-v6 native run passes with
actual 1280x720 captures. Export runner now independently reads PNG IHDR dimensions
for every state-sidecar capture and compares both actual dimensions and metadata
with the requested viewport, recording the number checked. Old executables lacking
sidecars fail this new verification rather than being implicitly trusted.

PNG header inspection now confirms that all `xeno-material-export-1280/1600/2560-v1`
and `anomaly-material-export-1280/1600/2560-v1` full `life-q0-true-a.png` captures
are **2560x1440**, including the runs requesting smaller widths. Anomaly 2560-v2
also has that actual size. Earlier three-width claims below describe requested
arguments, not verified three-resolution coverage; they are superseded here.
Their state assertions remain recorded, but 1280/1600 coverage must be rerun
with authoritative captured dimensions. Smaller room-only crops do not prove
the full viewport dimensions. Do not edit historical verification JSON to hide it.

Fresh `anomaly-isolation-export-2560-v3` passes input injection and room checks
with an actual 2560x1440 frame. V10 PCK hash is
`C241ACA6FFEA17DF2D782CFC5FE1EFF6C24F76EBB84FDF6268640F0D2BC34BF8`.
V10 controlled traversal also passes 30 arrivals, 84 transitions, 6,367 samples.
Native input-isolated v7 has 53 unobstructed captures and no paired camera drift;
v8 passes deliberate Escape/W/Space injection. A menu negative still rejects a
real overlay; its v9 run also reports an actual/requested dimension mismatch.

`output/batch-two/windows-validation-v1/verification.json` records a successful
standalone Windows debug validation build run from a new external temporary
directory, not the checkout. Both executable and PCK hashes are recorded there.

Reproduce with the existing `tools/export_room_validation.ps1`, an explicit Godot
executable, a new output directory and
`-AdditionalManifest @('res://rooms/underwater/batch-two/export-manifest.json')`.
The manifest supplies all ten sources, hashes, live cards, views and base sockets.
`tools/audit_batch_two_integration.py` rejects stale source/card/view records in
this manifest; the seven Python audit tests pass, including stale export-card
rejection.

Runtime evidence:

- 20 selected source hashes and 40 raw PNG decodes pass (both batches).
- 30 rooms visited, including ten supporting trunk rooms; 297 connected
  transitions over 20,000 updates / 2,000 simulated walker seconds.
- Export/runtime exit checks and ERROR/SCRIPT ERROR scans pass.
- `captures/mixed-station-start.png` visually inspected: room interiors, cards
  and UI icons present. The lower-left overlay obscures part of two rooms; this
  20.4% zoom frame is not full close-up art acceptance. Other captures retained
  but not claimed individually reviewed.

The fixture deliberately exhausts its starting power allocation for some rooms;
Medical Center/Office are dark in the mixed view. Individual economy-state
fixtures remain the evidence for their functioning effects. No gameplay costs,
failure conditions, resource production or unlocks were changed for this check.

This is a validation executable, not the normal playable distribution or release
approval. Remaining fine art cleanup/owner review is a separate gate.

## Individual fixture bridge

The generated export scene now accepts `--room-fixture=<id>` for each of this
batch's ten identities, with the mixed station still the default. The generator
changes only inheritance/plumbing; three read-only Python tests check recorded
source hashes and exact preservation of all ten room assertion bodies plus the
shared subject helper. Sources remain authoritative, not generated copies.

`tools/check_exported_batch_two.ps1` runs every subject from a new external
directory, requiring clean logs, zero process exit, a subject-specific PASS and
four rotation captures. It records executable/PCK/log hashes and viewport scope.

`output/batch-two/exported-states-1600-v1/verification.json` records all ten
passing at 1600x900 using windows-validation-v2. All forty native room rotation
crops reviewed via `output/batch-two/exported-<id>-rotations-1600-v1.png`:
upright props, departmental floors and no visible wall overflow at this scale.
This is not doorway-seam, actor-depth or fine silhouette cleanup acceptance.

State coverage follows each original room fixture: Clone exercises six economy
cases; Bio five; Biodome, Holo and the two Medical rooms four; Cryo, Archive,
Xeno and Anomaly three. Per-host active/static expectations and paused comparisons
are preserved rather than requiring every furniture group to animate.

The expanded UID audit initially rejected the old generated room_base ID.
No source reference to that malformed ID was found; it was replaced with a
Godot-generated ID, not a guessed string. All 46 script/UID pairs then passed
canonical/unique checks (`output/batch-two-uids-export-v2.log`). V3 was rebuilt
after this metadata-only correction and its mixed-station export checks pass.

The exported selector also rejects an unknown fixture with exit code 1
(`output/batch-two/export-selector-negative-v1.err`). That intentional negative
test error is preserved separately from successful room runtime logs.

All ten individual fixtures also pass at 1280x720 in
`output/batch-two/exported-states-1280-v1/verification.json`, using V3.
All ten pass at 2560x1440 in `output/batch-two/exported-states-2560-v1/verification.json`,
also using V3. Thirty individual room/viewport runs have terminal success records,
with no ERROR/SCRIPT ERROR entries in their stdout/stderr. This supplements the
mixed-station raw-source verification from the same export builds.
At 2560x1440, q0 crops for Biodome, Bio Lab and Xeno have been visually inspected:
the larger frame preserves their equipment detail and floor treatment. Full-size
source cutout gaps and material/indicator cleanup still require their own review.

## Biodome contour revision

Windows-validation-v4 includes Biodome card v2 and its fern-edge regression.
Its mixed-station build/runtime checks pass. The repaired room additionally passes
all original rotation/economy/motion assertions at 1280, 1600 and 2560 widths in
`output/batch-two/biodome-edge-export-<width>-v1/verification.json`.
The selective runner uses `-RoomIds @('biodome')`; its default is still all ten.
Other rooms' individual coverage remains the earlier batch runs, not thirty new
runs. See BIODOME_INTEGRATION.md for the exact repair and remaining fringe debt.

## Clone Lab contour revision

Windows-validation-v5 includes Clone Lab card v2 and six source-point contour
regressions. Mixed-station export/runtime checks pass. The repaired room's
individual fixture passes at 1280, 1600 and 2560 widths in
`output/batch-two/clone-edge-export-<width>-v1/verification.json`, including all
four rotations and six economy cases. These three selective runs supplement,
not replace or inflate, the earlier full-batch coverage. The original PNG is
unchanged; PROP_EDGE_REVIEW.md records the visual repair and broader polish queue.

## Holographic Core material revision and current controller caveat

Windows-validation-v6 includes Holographic Core card v5. Its individual fixture
passes at 1280, 1600 and 2560 widths in
`output/batch-two/holo-material-export-<width>-v1/verification.json`. The separate
native material pilot detects retained bay detail and rejects the test-only flat
negative control; see HOLOGRAPHIC_INTEGRATION.md.

The V6 **combined station runtime check fails**: 23 of 30 rooms visited during
2,000 simulated seconds. All twenty source hashes and forty PNG decodes pass.
The shared checkout now uses `scripts/bill_npc.gd`, a needs-driven graph walker,
instead of the earlier neighbor-choice controller. Earlier successful visitation
counts do not establish coverage of this newer controller. The gate has not been
disabled or lowered, and gameplay navigation has not been changed by this pass.
The fixture now reports graph reachability and exact unvisited cells separately
to distinguish inaccessible geometry from finite-horizon destination choice.
Do not describe V6 as a fully passing combined validation build.

`output/batch-two/current-controller-diagnostic-v1/station-summary.json` records
the current native run: all 30 rooms are graph-reachable, but 19 were visited
with 124 transitions during the same 2,000 simulated seconds. It retains the
failed visitation assertion and lists all eleven unvisited cells. This is a
later shared-checkout snapshot than V6's 23-room result, not a rerun of its PCK.
Reachability does not prove actual autonomous visitation or continuous collision
correctness. Next fixture work should distinguish controlled all-room traversal
from needs-driven destination-choice coverage; do not change gameplay priorities
just to recover an old fixture's visit count.

## Separate current-controller traversal gate

V7 now passes the explicit controlled tour: 30 physical arrivals, 30 rooms visited,
84 connected transitions and 6,367 collision/speed samples. This supplements the
failed needs-driven visitation check; it does not silently replace it. See
CURRENT_CONTROLLER_TRAVERSAL.md for trace checks, negative control and limitations.

## Xeno material/card v3 export

`output/batch-two/windows-validation-v8/verification.json` passes a fresh Windows
debug export with Xeno card v3: twenty source hashes, forty raw PNG decodes,
thirty controlled physical arrivals, eighty-four transitions and 6,367 movement
samples. PCK SHA-256:
`DC0E06D21BCCA7606086E361D3DA33B0E840238A2554E204B49790FEBCC78176`.
This still does not establish autonomous destination-choice coverage.

`output/batch-two/xeno-material-export-<width>-v1/verification.json` records
individual Xeno fixture passes at 1280, 1600 and 2560 widths, all from that build
and external working directories. The runners require clean engine-error logs,
zero exit status and all four rotation captures. Eleven asset/bridge unit tests
also pass. Only the 1600 `xeno_lab/room-q0.png` was visually inspected in this
export follow-up: the four machines, active marks and shared hull appear. Other
captured rotations/states are automated evidence, not new visual approvals.

Exact aperture contour refinement and owner aesthetic approval remain separate.

## Anomaly card v5 and slanted apertures

Windows-validation-v9 passes the controlled station fixture: 30 physical arrivals,
84 transitions, 6,367 movement samples, twenty source hashes and forty PNG decodes.
PCK SHA-256: `4AC1D1A4BF3327A724823BB490BCE1F76821E6468CB6ABDDBE6FF5CD882F7405`.
Eleven asset/bridge unit tests pass. This is not autonomous destination coverage.

Individual `anomaly-material-export-1280-v1` and `-1600-v1` fixtures pass.
All four `room-q0..q3.png` images from the 1600 run were inspected: machinery stays
upright as centers rotate, shared walls and lamps remain present, and operating
marks stay on their hosts at that scale. This is not a fine-aperture pixel audit.

The concurrent 2560-v1 run failed 21 motion/pause assertions and exited 1. Preserve
its logs; the build is not certified at all three widths by the lower-size passes.
A same-binary, isolated retry is recorded separately as 2560-v2. Do not infer the
cause from concurrency alone or weaken assertions to obtain a passing result.

The isolated 2560-v2 retry passed with unchanged PCK and assertions. Three widths
now have passing records, but the prior intermittent failure remains unexplained.
Prefer serial timing-sensitive graphical runs pending capture-stability diagnosis;
this single retry does not prove concurrency was the cause.

### Capture contamination diagnosis

Direct inspection of failed 2560-v1 `life-q1-pause-a.png` and `-b.png` shows
the game menu open in A and closed in B. The full-frame difference spans the
viewport. This establishes overlay contamination for that pair, not who opened
the menu or the cause of every failed comparison. It is not evidence of broken
room pause animation.

The native fixture now rejects menu-obstructed captures explicitly, preserves
the screenshot, and writes per-frame `.state.json` (menu, pause, visual time,
viewport, camera scroll and zoom). `anomaly-capture-negative-v6` deliberately
opens the real menu for station-q0 and exits 1 with the new precise error; its
sidecar records menu_open=true. Four export-bridge tests pass after regeneration.

`anomaly-capture-state-v6` still fails four host comparisons without menu flags.
Its q1 power-starved pair changes across a broad screen region despite a paused
state. Source inspection shows camera pan polls global held keys even while
paused. External input is a plausible contributor, not proven from those older
sidecars (camera fields were added afterward). Do not label capture stability
fixed. Isolating fixture input/camera updates is the next diagnostic task; leave
normal gameplay controls and production pause semantics unchanged.

### Scripted art-fixture input isolation

The base art fixture now disables its instantiated Main node's automatic process
and unhandled-input callbacks after pausing, and disables viewport GUI input.
Child rendering/light processes remain intact; fixtures explicitly advance
economy, visual time and controlled walker updates. This is not an interactive
controls or automatic simulation-clock test. Production game scripts are unchanged.

Native `anomaly-input-isolated-v7` at 2560 passes all existing room assertions
with clean engine logs. Its 53 state sidecars contain no open menus and no paired
scroll/zoom drift. Earlier failures remain preserved. This is evidence for the
isolated fixture, not proof that every historical failure had the same cause.

`anomaly-input-injection-v8` additionally passes at 2560 while injecting/releasing
Escape, W and Space through Godot input. Camera, pause and menu remain unchanged;
all room assertions pass with clean logs. The exported individual-room runner
now accepts `-ExerciseInputIsolation`, requires its marker and records whether
it ran. This verifies deliberate fixture isolation, not production input behavior.
