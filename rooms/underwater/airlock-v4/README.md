# Airlock — underwater hull fittings and Engineering finish

## Current selected card — low cutaway

### Current export helper passes

`output/airlock-low-package-v4/verification.json` records a successful Windows
debug export and external runtime. Package SHA256:
`067E30966BDC3EC15AE590F31F399D1FEB9B993C1366F95588E2FF341110CCD4`.
The helper completed with exit 0 and verified its child processes and error logs.
Autonomous Bill visits all 17 rooms with 180 reciprocal door transitions over
20,000 simulation steps; all 17 rooms are graph-reachable and none unvisited.
Source/card/component/profile checks pass. External working directory:
`C:/Users/Alex/AppData/Local/Temp/brine-export-check-df81b2b3dfee49568102b301790e413f`.

This closes the default mixed-station export follow-up for this revision. It does
not imply a release build, owner aesthetic approval or exterior swimming. Full
three-actor Airlock pressure/equipment coverage remains recorded against v2;
single-crew controlled traversal against v3. Historical failures below retain
their original scope and are not current failures of v4.

Autonomous fixture repair: the default mixed-station branch now completes the
production core recovery prerequisite before asking Bill to move. It retains
unscheduled decisions and the all-rooms visitation assertion, rather than replacing
that check with the controlled tour. `output/airlock-autonomous-recovery-v1`
passes natively with observed child exit 0 and no ERROR/SCRIPT ERROR lines:
5,009 navigation nodes, 17 reachable/visited rooms and 180 connected transitions
over 2,000 simulated seconds. Normal gameplay is unchanged. Eight regenerated
export-bridge checks pass. This fixture correction still needs a fresh package;
v3 retains the failed default setup and passing controlled-tour evidence below.

### Mixed-station packaged traversal passed

Package v3 SHA256:
`CF68E221B09B4021CA75662EA68464D320DF4FD9F6C6B583D60B1DF3D5636FE2`.
Its default smoke run passed asset checks but failed visitation because the legacy
walker path did not perform architect recovery (1 room, zero transitions and an
empty crew graph). That failed helper record remains in `output/airlock-low-package-v3`.

The same immutable package ran with `--controlled-tour` and the Airlock manifest
from empty directory
`C:/Users/Alex/AppData/Local/Temp/brine-airlock-tour-aea23e70f7af4bf1bc72dd8bc00ca1e2`.
`output/airlock-station-packaged-tour-v1` completes with observed child exit 0,
no ERROR/SCRIPT ERROR lines, 17 arrivals/visited rooms, 45 reciprocal transitions
and 3,465 collision/speed samples. It uses production core recovery and movement,
with fixture-scheduled destinations. This is single-crew station traversal,
not three-crew crowd acceptance or exterior swimming. The full three-actor
Airlock pressure/equipment evidence below belongs to package v2.

### Dedicated standalone runtime passed

`output/airlock-low-package-v2/BRINE.pck` has SHA256
`E223895E7B9992191A448FA888DCEDBBEAA4066568AA2580BFA40243C74038E5`.
Its direct `--room-fixture=airlock` run from empty external directory
`C:/Users/Alex/AppData/Local/Temp/brine-airlock-low2-c285d70287c240ca9dcfb1a3be5ae6dc`
completed with observed child exit 0, AIRLOCK PASS, all three crew, four rotations,
1,039 movement samples and no ERROR/SCRIPT ERROR lines. Logs and native frames:
`output/airlock-low-packaged-runtime-v2`. No checkout path was passed to the exe.
This covers pressure phases, equipment transfer, interruption, pause, disk saves
and inspector sizes through the existing fixture, not exterior crew swimming.

The same package's generic station smoke remains failed: its assets passed
(11 selected sources, 22 source/card decodes, 31 components, 11 profiles), but
station placement lacked `canonical_ports_nesw`. Current source manifest now
records `[2]` from RoomDatabase's `layout_dead_south`, plus its one-cell footprint.
That metadata correction is not in v2; a new generic-smoke package is still needed.
Do not erase the failed helper run or call its verification complete.

Capture-wait follow-up: the old direct package run was stopped after its
300-second bound. Its last capture remains motion-149; no package pass is claimed.
The source helper now requests redraw after settling and waits at most 120 scene
frames for frame_post_draw, reporting a test failure instead of an unbounded
render wait. `output/airlock-capture-wait-v1` completed natively with child exit 0,
1,039 samples and no ERROR/SCRIPT ERROR lines. This supports the revised capture
path, not a definitive diagnosis of every older stalled run.

The manifest now declares its selected card/view. The station fixture accepts
typed furniture or wall-fitting arrays with texture dictionaries, retaining
profile-hash checks. Eight regenerated bridge tests pass. These changes are not
inside the first package; a fresh export is required.

First package attempt: `output/airlock-low-package-v1/BRINE.pck` exported with
SHA256 `03C43B8B53C03C0C333A31641F3AB801B216F1741A3A7708196A8EE06A1F89E0`.
The helper's generic station runtime failed on the Airlock manifest's missing
`integration` field; its ROOM SCENE PASS marker does not override that script
error. No successful helper verification record is claimed.

A direct `--room-fixture=airlock` run of that same package was launched from the
new empty external directory
`C:/Users/Alex/AppData/Local/Temp/brine-airlock-low-645134f196a54b1b9bd389908c34123c`,
with no checkout path argument. Logs/captures are
`output/airlock-low-packaged-runtime-v1`. At the last observation child 76272
was live, Bill's release checkpoint had completed and no script errors were
reported; capture progress had stopped at `motion-149.png`. This is incomplete
runtime evidence, not a package pass. Poll that child before starting another run.

Export harness preparation: `tools/build_room_export_fixture.py` now includes
`--room-fixture=airlock` in its generated Node dispatcher. The Airlock fixture
accepts a fresh absolute `--capture-dir` for external package evidence. Eight
bridge tests pass, including exact Airlock assertion-body parity and dispatch.
`output/airlock-node-bridge-v1` exercises the generated scene headlessly with
Branforth: observed child exit 0, 151 samples and no ERROR/SCRIPT ERROR lines.
This verifies the adapter in the checkout, not standalone asset availability.

`card-low-cutaway-v1.png` is now selected by both room-card and station fallback
consumers and the manifest. It is the preserved native candidate from
`output/airlock-checkpoint-full-v1`, not a regenerated illustration. Its SHA256 is
`395AC16EB5F00B185E53C8FB8600C83A60FE3A668BD73C5B6FE64719687322AE`.
All four open exterior views and the candidate card have been inspected; the
raised hull strip is absent. This is agent visual review, not owner approval.
The old `card.png` remains unchanged as historical study art.

Both declared composition profiles and all component hashes pass their read-only
audits; the new PNG has the LFS filter. A fresh standalone package is still needed
to verify the selected card and low-cutaway renderer outside the checkout.

## Acceptance correction — low walls

The owner retained the current low height for every wall, including exposed north
edges. The room-specific raised assembly described below is therefore an unresolved
visual mismatch, not an approved exception. Preserve these source assets and prior
test results, but revise wall, hatch and fitting registration together and review
all rotations and shared edges before publishing a replacement card. The existing
settings regression does not cover the renderer's Airlock-specific bypass.

### Low-wall conversion baseline

`tests/test_airlock.gd` now saves review captures and `card-candidate.png` into a
fresh `--output=res://output/<new-directory>` directory. It no longer publishes
the production card as a side effect; native input is isolated during capture.
The first attempt (`output/airlock-low-wall-baseline-v1.log/.err`) stopped at
startup on the concurrently changed coroutine restore API. Current awaited calls
then completed `output/airlock-low-wall-baseline-v2`: terminal AIRLOCK PASS,
1,039 travel samples, 229 PNGs and no ERROR/SCRIPT ERROR lines. Raw image loading
warnings remain. The process is terminal; its exit code was not retained.

The q0 start crop was inspected: the raised wall, windows and hatch are visibly
one rear assembly. This is before-change evidence, not low-wall acceptance.
The selected card remained byte-identical across the review (SHA256
`367FEC9C3DB7D1AFC91F75B62BE6281DA505FFCADC19C6A60D8384B9E0BAE46B`).
The candidate still renders the existing raised assembly. No replacement card
or revised hatch geometry has been published.

## Brief and source roles

### Low cutaway candidate — current station source

Exterior seam follow-up: `output/airlock-low-sill-v1` confirms the old solid hull
strip behind the open leaves is removed. `exterior_wall_segments()` splits only
the exterior-facing wall around the 72-unit aperture; a low metal sill spans the
wall depth. The q0 exterior capture was inspected. Four-rotation segment tests
check two remaining wall pieces, no intersection with the aperture and an
unchanged opposite edge. Navigation and pressure-cycle rules are unchanged.

Do not count this run as fully passed: the observed child exit was 1, with two
`Shelf helmet hides at grasp` errors from the current equipment-visibility checks.
The log still records 1,039 movement samples; no card was published. Resolve the
grasp failures and review the other open-edge captures before final acceptance.

Handoff diagnostic follow-up: `airlock-shelf-diagnostic-v1` completes headlessly
with observed child exit 0, AIRLOCK PASS and 1,039 samples. A native replay in
`airlock-shelf-diagnostic-native-v1` did not reproduce the grasp assertions before
its last capture, `branforth-q0-shelf-after-release.png`, but did not finish.
The live owned child (100164) was stopped after the 300-second bound. No terminal
PASS is claimed for that replay. The shared fixture gained post-release restore
checks during concurrent work; investigate this checkpoint with fixed-revision
evidence before declaring the original native failures resolved. Failure-only
diagnostics now identify actor, rotation, controller identity, timer and cells.

Current replay: `output/airlock-branforth-checkpoint-v1` passes natively with child
exit 0, 151 samples and no ERROR/SCRIPT ERROR lines. The fixture's `--actor=`
option validates the requested ID and labels focused coverage separately.
Checkpoint markers show write/restore completion rather than inferring a hang
from the last screenshot. Branforth's write and restore span 36 ms in that run.

`output/airlock-checkpoint-full-v1` then passes the full native sequence: child
exit 0, 1,039 samples, all three actors, Bill's four rotations and no ERROR/SCRIPT
ERROR lines. All three release checkpoints complete. Before/after hashes match
for the fixture (`25C6E686B33C7CFEC917DCACE976BCC09C38A9AF80A46D1009F56D872D6A067C`),
save module (`9DC4E352DD9B5E3E1149BF48DA8BEACDEDB3DB1C620FA0F26A9F959F4783B353`)
and shelf service (`E417FDA07479D6CEDFAB34D6D7D11872815FEEA11556EB2E44F0F240C5DD2A91`).
This is current-revision evidence, not a proven explanation of the earlier stall
or a hash freeze of every dependency. Retain the failed and terminated runs.
No production behavior was changed to obtain this pass. Card selection and
package verification remain pending.

`output/airlock-low-cutaway-v2` records the replacement code-owned low outer
hatch. The station no longer forces the Airlock raised-wall layer. The old
generated hatch and wall fittings remain preserved, unmodified source assets.
The chamber now reaches the exterior sill in all four rotations; v1 corrected
only the raised treatment but exposed the older shortened rotated chambers.
The q1 compressor moves above the extended chamber rather than overlapping it.
Outer leaves use the shared 72-unit aperture and the existing pressure pose;
the controller and wet-deck drains remain in the room.

Native v2 reports AIRLOCK PASS with 1,039 movement samples and no ERROR/SCRIPT
ERROR lines. The child is terminal; exit code was not retained. q1/q2/q3 start
captures were visually inspected, following q0 inspection in v1. These establish
the low silhouette and extended chamber placement, not full exterior crossing
or open-aperture acceptance. The existing hull infill behind the outer sill still
needs an explicit open-state seam review. No new card is selected or packaged:
`card-candidate.png` is evidence only and the production v4 card retains its
baseline hash. The prior raised-profile envelope audit is historical, not an
acceptance gate for this code-owned cutaway.

Primary department: Engineering. Secondary function: diving preparation and wet
transfer. Condition: maintained, with restrained handling wear. The pressure
chamber remains the focal structure, with a usable dry locker area around it.
The wall is pressure hull, and its glazing looks into the ocean outside.

Maintenance Bay supplied dark steel, amber accents and selective mechanical
detail; BRINE Core supplied readable pixel clusters and clean construction. Neither
reference supplied door geometry or required the airlock to adopt BRINE's pearl
cladding. Existing airlock locker, compressor, bench and hatch art remains in use.

`prompt.txt` records the exact imagegen prompt. `wall-source.png` is preserved
unmodified. The tool returned **1254 × 1254 RGB with a baked checkerboard**, despite
the request for transparent 1536-square output. Transparency and dimensions were
not accepted on faith. `build_assets.py` uses `tools/room_art_pipeline.py` to remove
only edge-connected light-neutral background from six explicitly reviewed regions,
then trims alpha without stretching. No enclosed-gap seeds were needed.
`registration.json` records source regions, trims, actual dimensions and alpha.

## Separate attachment classes

- Hull riser: rectangular ocean window, porthole, pressure controller, breathing-air
  manifold and two shielded lamps. `wall-profile.json` declares texture dependencies
  and independent screen-facing wall rectangles. The hatch bay stays clear.
- Chamber post: a supported copy of the pressure controller, located on the inner
  post. It does not add a floor blocker or a new interaction point.
- Wet deck: two flush drain cassettes, below the water overlay. These remain
  floor details; their source geometry does not become collision.
- Structural hull: existing code-owned boundaries receive steel cladding, recessed
  seams, raised edges and restrained ochre markings. The compressor's service line
  connects its real footprint to the chamber rather than floating on the floor.

The requested wide window emerged closer to square. This revision uses it at its
actual aspect ratio (about 46 × 36 world units), not stretched into a panoramic
window. A truly wide hull window would need another generated variant. Small
original microdetails naturally disappear at wall scale; source detail is not a
reason to enlarge fittings beyond the riser or crowd the hatch.

`fittings.gd` draws attachments over the airlock-only hull variant. During this
pass the shared raised-wall experiment was retired elsewhere in the workspace.
This room therefore owns its authored exposed-north hull independently of that
global study flag; the change does not restore the retired global setting or
modify other departments. Its rear wall remains suppressed with a north neighbor.
Windows show a static ocean view, not an interior aquarium.

## Current consumers and verification

Station: `airlock-v1/airlock_view.gd` plus the airlock branch in `north_wall.gd`.
Card: `airlock-v4/card.png`, a 512-square native Godot render. Older sources and
cards remain available for comparison. `manifest.json` records all current raster
and profile dependencies, including the retained floor-prop atlas.

`tools/audit_wall_fittings.py` checks real alpha, aspect-fit bounds, the 48-unit
riser envelope and hatch-bay clearance independently of floor navigation. Native
evidence is `output/airlock-v4`: all three crew, four rotations, ten pressure
phases and inspector widths 1280/1600/2560. Existing interlock, pause, power-loss,
save and locker-travel assertions still apply. No packaged export is claimed.

Final results: native airlock test PASS with 1,038 travel samples; low-wall
settings regression reports zero failures; run-save regression PASS. Six wall
attachments pass alpha/envelope checks, the hatch-overlap negative control is
rejected, and both composition profiles pass dependency hashes. Logs:
`output/test_airlock-hull-final.log`, `output/test_low_wall_settings-hull-final.log`,
`output/test_run_save-hull-final.log`, `output/airlock-v4-wall-audit.json`.
The [comparison sheet](review.html) retains native card canvases for current,
previous and two style references.

This revision demonstrates separate generated hull attachments in the actual
airlock; it does not establish that every room's existing wall art meets the new
direction. Lessons are recorded in the room pipeline and visual bible for future
work, without silently replacing the rest of the station.
