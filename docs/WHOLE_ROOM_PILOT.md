# Whole-room-first nursery pilot

Started 2026-09-05 after owner approved the research recommendation. Work remains
in the current checkout. Original source assets are retained; the current Nursery
and Life Support station/card consumers use the south-facing implementation below.

## Current owner direction: south-facing machinery

The owner subsequently requested that large props always face south regardless
of room rotation. This supersedes the directional-art requirement below: retain
the earlier side/rear images as experiments, not required production views.
Rotate door topology and prop centers, while keeping each prop's art, ground
footprint orientation and effects south-facing. A rotated collision box under
unrotated artwork is not acceptable. Four playable layout configurations are
still required; this changes the art rule, not the remaining room/integration scope.

`rooms/whole-room/nursery_south_facing.tscn` is the current isolated implementation.
Press R to cycle layouts. It reuses the approved master pixels for every facing
without regenerating or stretching machinery. `tests/playtest_south_facing.gd`
passes position, unchanged footprint, shell bounds, ground-anchor and rotated
socket checks for all four layouts (`south-facing.log`). All four native captures
under `output/whole-room-pilot-01/south-facing/` were inspected. Recognizable front
faces remain visible throughout; no side/rear candidates are used.

Remaining work for this new rule: tighter source silhouette edges and missing
plumbing, all-layout depth/movement/state checks, distinct Life Support seam
verification, station/cards integration and full regressions. Earlier q0/q2 depth
tests do not prove these new four-layout configurations. The connected Life
Support scene has been authored but not yet run; do not claim its seam passes.

### South-facing native verification follow-up

The expanded south-facing harness passes all four layouts with 16 front/behind
actor-region pixel comparisons, continuous accessible-side walking routes for
every prop, per-layout active/offline pixel comparisons, moving crew while offline,
and paused crew checks. Evidence: `south-facing-depth.log` and `south-facing/`.
This supersedes the earlier unverified-depth note for those exact checks; it does
not prove every viewport, mature station zoom, card or integration behavior.

The connected fixture now inherits the south-facing renderer. Native
`tests/playtest_connected_rooms.gd` passes with one nursery and one distinct
Life Support room: exactly one shared 96-unit opening, movement into Life Support
and back, and active/offline comparisons cropped specifically to Life Support.
The 1600x900 connected capture was inspected. Evidence: `connected-native.log`
and `connected-native/`. Both rooms remain isolated from normal runs and saves.

Life Support is an existing `layout_05_cross` identity; this art test does not
change its costs, production or unlock status. Its generated master, exact brief,
prompt and physical guide are under the pilot output directory. The native art
still omits some perimeter plumbing, and Life Support depth/routes beyond the
shared central aisle remain to be tested. Vertical seams and wider integration
are not implied by the passing horizontal pair.

### Vertical distinct-room seam

The connected fixture now toggles horizontal/vertical placement with V.
`connected-both-seams.log` passes both seam orientations: one shared edge,
96-unit opening, bidirectional walking, and Life Support-specific active/offline
pixel comparisons. The vertical native capture was inspected; the shared wall
is continuous outside its single central aperture and room interiors do not
erase it. This supersedes the earlier horizontal-only evidence limitation.

The next integration touchpoints have been located: `grid_canvas.gd` currently
uses `rooms/modular/nursery_view.gd` through `configure_embedded`/`render_into`,
with two-pass floor/foreground ordering and legacy-door suppression. `main.gd`
still maps the nursery card to the older modular card. The new south-facing
renderer is not yet connected to either consumer; preserve those existing
seam/depth behaviors when adapting it rather than swapping only the PNG path.

### Nursery station/card integration

The south-facing renderer now implements the existing embedded host interface.
Drawing commands target the host canvas, with separate floor/foreground passes,
omitted shared sides, host operating/pause time and external crew texture. The
standalone four-layout depth/state suite still passes after this adapter change
(`south-facing-adapter.log`). The new 512-square card is rendered by Godot from
the same approved source pixels and canonical shell (`tools/bake_whole_room_card.gd`,
`card-bake.log`), not a screenshot containing fixture UI.

`grid_canvas.gd` now loads the south-facing nursery renderer, and `main.gd` maps
its card to `rooms/whole-room/nursery-card-v1.png` (Git LFS covered). Native
`playtest_nursery_art.gd` passes in the real 1600x900 station/card consumers,
including four layouts, operation/offline comparisons and paused frames.
Station/card and mixed-legacy-room captures were inspected. The first run's route
assertions still used old proxy footprints, so the test was corrected to use
the actual embedded renderer's fixed-facing rectangles. Evidence for that rerun
is `station-south-footprints.log` and `station-south-footprints/`.

Life Support remains in the isolated connected fixture, not the normal station
or cards. Asset-edge cleanup and broader integration/regression coverage are
still open. No gameplay costs, failures, discovery timing or player saves were
changed by the nursery renderer/card replacement.

### Both identities in the actual station

Life Support now has a single-room south-facing embedded renderer and a matching
512-square Godot-baked card. Station floor/foreground ordering, shared-wall
ownership, legacy-door suppression and crew rendering now recognize both room
IDs. Old raster variants remain on disk; normal layered rendering uses the new
single master. Neither room's economy or discovery data was changed.

`tests/playtest_whole_room_station.gd` reuses the isolated-save nursery harness and
adds nursery/Life Support pair captures and Life Support-specific operating/offline
pixel comparisons in all four orientations. `station-both.log` passes; horizontal
and vertical real-game captures were inspected under `station-both/`. The test
also retains the nursery motion, pause and current-footprint route checks.
Life Support-specific prop depth/routes and broader viewport acceptance remain
separate work; a passing animation comparison does not prove those.

Before this second integration, all five regression suites passed: synergy manager,
discovery progression, gameplay polish, run balance and nursery gameplay. Logs
are `test_*-south.log`. The nursery gameplay smoke also passed after enabling
Life Support (`life-integration-smoke.log`). Full regressions should be rerun
after final cleanup. Both room integrations still need final visual acceptance.

## First gate: visual master

### Bench silhouette cleanup

Tightened the source-UV outline above the two rear specimen jars, removing the
obvious dark background blocks while retaining jar silhouettes. Native q0 was
inspected against the prior capture. The original raster, ground footprint,
scale and sort anchor are unchanged. `south-bench-mask.log` passes all four
layouts and the existing depth/routes/state suite. The shared base registration
also supplies this corrected outline to the embedded Nursery.

The card was rebaked as `nursery-card-v3.png` (`card-bench-mask.log`) and main's
mapping updated; previous versions remain preserved. V3 has the LFS filter.
This addresses the visible jar fringe, not every source-shadow edge or the
still-omitted long inter-machine hose.

### Reservoir local pipe restoration

The south-facing renderer now includes a narrow source-UV silhouette for the
approved reservoir's local return pipe. It translates with the tank and is drawn
before its body; no generated pixels or room-spanning hose were invented. The
long wall/inter-machine connections remain omitted pending layout-aware routing.
No collision rectangle changed; the side fitting is a visual attachment, and
these tests do not certify physical collision for its individual pipe segments.

`south-pipe.log` passes all four layouts, 16 depth pairs/routes and state/pause
checks. Native q0 and q2 were inspected. Minor source-floor fringe remains,
especially around the bench; extraction is not declared finished.
`nursery-card-v2.png` was baked through the same renderer (`card-pipe.log`) and
is the current main-game card mapping. V1 remains preserved. The card baker now
accepts an explicit new output path while retaining its no-overwrite guard;
the v2 PNG is covered by Git LFS. Actual-station rerun after this detail remains
pending; previous station runs predate the pipe addition.

### Visible shared-wall guard

The mature overview prompted a suspected missing-wall investigation. No production
wall change was made: `station-wall-pixels-fixed.log` passes direct native-pixel
checks on both solid halves of the distinct-room seam in all four orientations
at 1280x720, alongside route/state and mature-fit checks. The checks sample outside
the canonical aperture and require light hull pixels; collision assertions alone
cannot detect erased artwork. This is evidence for those pair samples, not an
exhaustive certification of every seam in a mature mixed station. The first
attempt's type-inference parse failure is retained in `station-wall-pixels.log`.

### Mature-station acceptance fixture

The actual-station harness now includes a 40-room (8x5) mixed legacy/layered
fixture, with all four rotations. This is deliberately a visual fixture, not
an affordable or connected run claim. It checks each cell's transformed bounds
against the station viewport after Fit Station and preserves a native capture.
`station-mature-1280.log` passes, including the previous route/state checks.

Native 1280x720 inspection shows the full station fits at 14% zoom. New clean
rooms remain visibly distinct from the much darker, denser legacy rooms; this
is an unresolved pack-coherence issue, not evidence of full art acceptance.
Fine machine details are too small to communicate identity reliably at this
overview scale. Shared construction across the remaining room rollout and
overview-level identity/status presentation remain necessary. This fixture
does not prove per-machine animation readability at 14% zoom.

### Life Support footprint correction and depth evidence

`life-depth-corrected.log` passes four layouts, 16 front/behind comparisons and
continuous prop routes, plus operating/offline/pause checks. The initial
`life-depth.log` remains as failure evidence: rough guide rectangles incorrectly
counted visible cabinet height as floor depth. Fan top planes span about 162
source pixels (54 world units at 108/326 scale); the console top spans about 170
pixels (64 world units at 104/274 scale). Registration now uses those floor depths,
keeping the south ground-contact edge and q0 artwork fixed. The original guide
is a composition study, not the authoritative final collider dimensions.

The actual-station pair harness now samples 101 real walker positions in each
orientation against both current renderer footprints. This supplements the
isolated per-prop depth tests; neither substitutes for the other. Source-mask
edge/plumbing refinement and the broader expansion ledger remain open.

`station-pair-current-1600.log` passes after the footprint correction: 404
distinct-pair path samples, 20 crossing captures, plus the inherited Nursery
motion/routes/pause checks and both cards. All four source/card PNG paths have
the Git LFS filter. No commit or staging was performed.

### Small-viewport operating feedback

The updated 1280x720 run (`station-pair-current-1280.log`) exposed a Life Support
q1 active-frame failure: the subpixel fan dots did not survive the vertical-pair
overview scale. The 2560 run passed, demonstrating why large captures alone were
insufficient. Replaced each orbiting dot with three restrained antialiased radial
fan marks contained within its housing, and antialiased the console traces.
These remain conditional on operation and use the existing machine clock.

Corrected runs `station-pair-fan-1280.log` and `station-pair-fan-2560.log` pass all
four layouts, distinct-pair crossing samples and active/offline comparisons.
The 1280 q1 capture was inspected at native size. This is two-room overview
coverage, not mature-station acceptance. Five gameplay suites also pass in
`test_*-current.log`, with no script/error entries; they ran before this visual-only
fan-mark change. Remaining work includes art-edge/plumbing refinement, mature
station readability, and the full asset expansion scope beyond these two rooms.

Reference: owner's `exec-865188c0-1a10-423f-b797-d3be7564f285.png`.
Preserve its rich machinery construction and high overhead cutaway treatment,
but use mostly clean enamel/glass and no baked-in character. The nursery's
database layout remains west/east/south, not the reference's single south door.

Two built-in image-generation edits are retained under
`output/whole-room-pilot-01/`. Full prompts and review states live in its manifest.
No PixelLab generation or external credit purchase was used in this pilot.

- v1: strong clean-surface candidate; rejected boundary because it invented a
  north entrance and side openings were visibly narrower than the south opening.
- v2: north wall repaired and south aperture widened, but side opening dimensions
  still do not match. Interior appearance remains substantially similar, not
  pixel-identical. This is the current visual-review candidate, NOT validated art.

The repeated dimensional failure ends prompt-only boundary repair. Do not launch
another equivalent doorway prompt. Preserve the interior and use the existing
authoritative shell/door renderer for final boundaries, with registered interior
masking and explicit doorway clearance checks. Do not merely crop wrong walls
away and claim validation.

## Acceptance and remaining work

1. Owner visual approval of clean whole-room master: approved in conversation
   ("I like this direction, it looks pretty good!"). This approves appearance,
   not generated boundary dimensions or missing directional views.
2. Register artwork to the pilot's 384-unit cell / 16-unit wall / 96-unit opening;
   validate the boundary mask and shared wall kit against the actual renderer.
3. Extract only depth-relevant silhouettes. Check reconstruction before adding
   crew; remove duplicated glass/shadow artifacts if extraction exposes them.
4. Add one localized reservoir effect and crew front/behind walking test in a
   dedicated fixture, not the player's save.
5. Test opposite view before commissioning remaining views. No four-view art is
   claimed; the existing modular approximation is not a substitute for this gate.
6. Validate horizontal and vertical room seams, offline/pause behavior, game zoom
   and card readability before integration.

Technical integration of the previous modular nursery remains historical evidence,
not current owner approval of its artwork. Never promote this pilot automatically
based on geometry or image-file checks alone.

## Whole-image native fixture: first orientation

Implemented `rooms/whole-room/nursery_whole.tscn` and its paired script/UID.
The copied `nursery-master.png` is byte-identical to the approved v2 output
(SHA256 `002C922CC19695B133626827F1EF89ACCCE5E9A82C0C8450803F58D29DE5BA66`).
Raster path is covered by Git LFS. No existing game asset was replaced.

The renderer samples the original interior at a uniform scale, with a small quiet
floor rim. Four source-UV silhouette polygons redraw original pixels for character
occlusion; no generative extraction or independent machinery reconstruction was
needed for this fixed, opaque scene. Ground footprints and sorting anchors are
registered separately. It uses the existing directional test character, not a new
astronaut asset.

Code-owned walls use the shared 96-world-unit aperture and original wall material
strips. Corners and jamb caps are registered independently of the generated doors.
Reservoir bubbles stay inside the glass; an operating indicator is local. Offline
stops the machinery effect and clock, not the crew; pause freezes both clocks.

`tests/playtest_whole_room.gd` passes natively with Godot 4.6.1 at 1600x900:

- exactly one shared edge and 96-unit aperture for horizontal/vertical fixtures;
- simulated movement crosses each connected doorway; solid north blocks movement;
- active/offline native pixel comparisons and separate crew/pause assertions;
- four front/behind native pixel comparisons prove character occlusion;
- continuous accessible-side movement routes keep collision clearance.

Two machines are intentionally too close to the right wall for a full circuit.
Tests exercise their accessible left/front/behind routes; collision was not shrunk
to let the actor squeeze through. Native captures/log are under
`output/whole-room-pilot-01/native/` and `native-run.log`.

Run the fixture with Godot and `res://rooms/whole-room/nursery_whole.tscn`.
Controls: WASD/arrows walk, O operating/offline, Space pause, C seam fixtures,
G collision footprints. This scene never accesses player saves.

## Full-goal work still required

### Opposite-view experiment (2026-09-05)

`tools/bake_whole_room_proxy.gd` builds one coarse physical layout and renders
four fixed-camera guides. Its native run passed 16 camera-projection assertions;
this proves the guide transforms, not generated-art fidelity. Guides and log are
under `output/whole-room-pilot-01/proxy-01/` and `proxy.log`.

The first q2 paintover is retained as `nursery-opposite-v1.png`, alongside its exact
prompt and separate `opposite-view-review.json`. Built-in image generation used
the q2 guide for layout and the approved master for materials/identity. No existing
room art was overwritten and no external paid generator was used.

Visual review finds a useful rack service back, upright tank with opposite-side
plumbing, and consistent clean materials. It does NOT pass directional acceptance:
the microscope remains frontal, one specimen container is missing, equipment
footprints drift, and floor grates were placed in front of the machines instead
of rotating with their physical floor positions. The proxy itself needs explicit
floor landmarks and a stronger microscope rear silhouette before the next pass.
The candidate remains outside runtime registration; q1/q3 are not commissioned
from it. No four-view completion is claimed.

The follow-up proxy revision adds the missing fourth specimen container, a wider
microscope rear support/service patch and four source-registered floor grates.
`proxy-02/` preserves its four new guides; `proxy-02.log` again passes all 16
projection checks. In q2 the grates now occupy the north side of their equipment
footprints, with appropriate equipment occlusion, rather than moving to maintain
the original illustration's composition. This revised guide has not yet been
painted or accepted as final art.

### Experimental q2 native registration

The proxy-02 whole-room paintover (`nursery-opposite-v2.png`) improved the microscope
but invented a south opening and front drawers on the rear bench. It is rejected.
A localized edit of v1 instead repaired the microscope and restored the fourth
container (`nursery-opposite-local-v3.png`). It still changed the bench width;
localized prompts do not guarantee protected pixels. Exact prompts, hashes and
findings are in `opposite-followup-review.json`.

The isolated `rooms/whole-room/nursery_opposite.tscn` now tests v3 machinery with
source-UV silhouettes. No bitmap is quarter-turned. Each assembly uses a uniform
scale and registered bottom-center pivot against the ORIGINAL q0 physical
footprint rotated 180 degrees. Code-owned walls and registered floor grates do
not inherit the generated scene's misplaced structures. Original pixels supply
the floor material. The q0 renderer gained only two drawing hooks for this study.

`tests/playtest_whole_room_opposite.gd` passes ground-center/size/pivot checks,
north-open/south-solid checks, active/offline image comparisons and paused crew
clock checks. Its initial parse error is preserved in `native-opposite.log`;
the corrected passing run is `native-opposite-fixed.log`. The original full q0
native suite still passes (`native-regression.log`). No player saves are accessed.

Native q2 captures were inspected: the machinery remains detailed and upright,
and the tank can extend above the north wall without clipping. This is NOT art
acceptance: plumbing outside the current main silhouettes is missing, the floor
needs panel seams, and full q2 continuous routes/depth/viewport coverage remains
unverified. These are the next corrections before accepting the opposite view.
The candidate is not enabled in the actual station or cards.

### Q2 detail and depth follow-up

Restored source-pixel plumbing silhouettes for the tank, rack and filter; added
quiet code-owned panel seams beneath the crew and machinery. No source raster
was modified. The narrow pipe masks retain minor source-floor fringes and are
not claimed as production-perfect extraction.

Expanded `tests/playtest_whole_room_opposite.gd` now compares actor-region pixels
with/without the crew for all four front/behind pairs and walks continuous routes
around an accessible side of every machine without shrinking its collision box.
`native-opposite-depth.log` reports zero failures, including existing anchor and
state checks. Native captures at 1280x720, 1600x900 and 2560x1440 were inspected:
equipment stays upright, tank overhang remains visible and the restored pipes
stay inside the room boundary. Files are in `native-opposite/`.

This advances the opposite-view technical gate, but owner art approval, q1/q3,
the distinct neighbor, card/station integration and their acceptance remain open.

### Side-view candidates

Guide review caught a clipped reservoir in q1. The proxy now uses one larger
500-unit orthographic canvas for every direction, preserving a shared center
and scale rather than independently fitting views. `proxy-03.log` passes all
16 projection checks; q1 was visually inspected before generation.

Generated q1 and q3 independently from their physical guide plus the ORIGINAL
approved master, not a chain of unapproved style references. Candidates, exact
prompts and findings are in `side-view-review.json`. Q1 has useful narrow side
profiles but omits its north door. Q3 v1 incorrectly laid filter cylinders on
their sides. A localized v2 edit made them upright but left only three specimen
containers and lengthened the cabinet. These remain outside runtime registration.

The side rack also needs explicit continuity review: a convincing side silhouette
does not prove that its three growth trays remain at the same physical heights.
No complete four-view room is claimed from these files alone.

- Opposite-view artwork with stable equipment identity; then the other two views.
- Direction-specific masks, collisions, effects and native inspection across views.
- A distinct second room's art, not just duplicated nursery seam fixtures.
- Broader viewport/game-zoom/card checks and final game integration/regressions.

The current horizontal fixture duplicates this nursery; the vertical fixture uses
the same interior with an NS shell. They prove seam mechanics, not a second room
identity or a completed four-rotation art pipeline. The active goal remains open.
# Locked doorway scale and full-assembly containment — 2026-09-05

Owner approved 48-unit floor tiles and 72-unit clear door openings (1.5 tiles).
Shared geometry and the four layered room floors now use that contract. After
rotation, complete visible assemblies are translated minimally inward to a
360-unit safe interior (four units inside the inner walls). Artwork and collision
move together; south-facing orientation and dimensions remain unchanged. Nursery
bounds include its attached reservoir pipe and floor grates. No crop or shrink
is used to disguise overhangs. The visual bible records the rule.

Native evidence: nursery-wall-fit.log, life-wall-fit.log, hydro-wall-fit.log,
reactor-wall-fit.log under output/whole-room-pilot-01 each pass four layouts,
visible containment, depth/routes, operating state and pause. station-wall-fit.log
passes connected Nursery/Life Support paths and the mature-station fixture.
nursery-four-rotation-locked-fit.png uses the production renderer, with 72-unit
apertures and containment assertions, not a preview-only geometry override.
Cards refreshed to Nursery v4 and Life Support/Hydroponics/Reactor v2; originals
retained, new PNG paths use Git LFS. Legacy room bitmap migration, departmental
finish alignment, sealed card sockets and animated door leaves remain separate.
