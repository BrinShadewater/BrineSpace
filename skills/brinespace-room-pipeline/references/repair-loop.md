# Focused room repair loop

Use for an existing integrated room; retain the brief and accepted geometry.
The bible owns visual intent, this skill owns procedure, and room integration
records own revision-specific evidence. Do not paste the same history into all three.

## Decide and compare

- Name the defect and smallest affected surface: source-floor contamination,
  lost hardware construction, baked activity, registration or composition.
- Capture the current renderer before editing. For cutouts/materials use
  `tools/capture_registered_prop_edges.gd` on both backgrounds; keep the donor.
- Classify what must survive: bezel, unlit lens, platform, contact shadow or
  actual opening. Preserve accepted pixels/registration outside the target.
- Judge a candidate at diagnostic scale and gameplay/card scale. A narrow bezel
  can become subpixel at gameplay zoom; do not enlarge equipment to satisfy a
  detail test. Detail evidence does not establish gameplay readability.
- Reject changes that restore painted activity or flatten construction. Record
  a rejected candidate and reason separately from a passing technical test.
- Check hue as well as detail after suppressing emission. Xeno's textured RGB
  modulation retained construction but made violet lamps olive. Local lens
  reconstruction corrected the interiors while preserving surrounding housings.
  Compare unchanged props and outside-target pixels on matched native captures;
  colour samples alone cannot prove the complete repair boundary.
- A hue-filtered indicator audit can miss nearly white emission. Pair it with
  manually selected rendered off/on samples from visibly luminous fittings;
  do not interpret an empty colour-filter result as complete offline cleanup.
- Resolve each prop's actual texture before a source-pixel audit. Reused furniture
  can have coordinates from a separate atlas; sampling them from the room donor
  produces unrelated failures. Report source-specific coverage and exclusions.
- For foliage, trace leaf edges separately from pale planter rims and source-floor
  fringe; a global neutral-colour removal can erase valid construction. Pair
  excluded-background samples with retained leaf/rim samples. For ambiguous gaps,
  `tools/capture_source_detail.gd` accepts `--source`, `--rect=x,y,w,h`, integer
  `--zoom=1..16` and a new `--output=res://output/...png`; its nearest-neighbor
  diagnostic records source coordinates and hashes without editing the donor.
  Review open canopy notches separately from enclosed gaps; an outer contour
  repair does not remove background trapped between interior leaves. Polygon changes can
  also introduce tiny texture-sampling differences: report exact differences and
  their magnitude separately, rather than calling a visually unchanged region
  pixel-identical after applying a tolerance.

## Integrate and close the loop

For thin or articulated registered props, overlapping visual rectangles can
contain only empty space. Use `audit_room_composition.gd --polygon-overlaps`
on views with the source-space `life_point` contract to inspect their actual
cutout-piece intersections before moving furniture. This diagnostic does not
decode texture alpha or include dynamic overlays, shadows or collision; summed
piece areas can double-count overlapping pieces. Keep rendered review and crew
clearance separate. If refining a rectangle-based regression to cutout checks,
retain all prop pairs and prove it rejects a deliberately introduced contact;
do not exempt a lamp by name merely because its reach might be intentional.

Re-bake to a new card path, update current station/card/variant/export consumers,
and run affected native state/rotation checks. Include a negative control when
adding a new visual regression: it must reject the defect it claims to detect.
Keep precise PNG dimensions, renderer/source revisions, logs and reviewed frames.
For pause acceptance, explicitly advance the game's owning clock while paused,
then resume and require the affected host pixels to change. Two redraws at an
unchanged injected timestamp establish repeatability, not pause gating. Keep
direct operation flags separate from economy-driven operation and room darkness.
Include floor-only mats in containment checks after final host placement;
furniture bounds do not cover their host-relative offsets and sizes. Use
`audit_room_composition.gd --require-mats-contained` for rectangular profile mats,
and retain exterior margins in visual captures so overflow cannot fall off-frame.
This gate does not cover every route, decal, light or procedural floor detail.
For a catalog sweep, use `audit_room_dressing_hosts.gd --check-mat-bounds` to
resolve every live dressing helper, not only a property named `dressing`.
`capture_mat_bounds_review.gd --output=res://output/<new-directory>` captures
flagged rotations with exterior margin. A bounds failure is a review lead:
inspect its pixels before changing authored sizes or offsets; do not bulk-clamp.
When replacing a prop's drawing branch, check early returns against its existing
operating-effect contract. The fleet swap bypassed cradle cues while keeping the
host marked animated. Restore a physically appropriate cue or explicitly review
a changed state contract; do not animate unrelated vehicle tools to satisfy a test.
For owner-driven display states such as fleet deployment, set the authoritative
fixture state and exercise the normal binding. A direct view flag can be
overwritten on draw. Check occupied, empty and restored pixels separately from
operation/offline/pause; these controlled states do not prove mission progression.
After an atlas replaces a registered prop, measure the decoded runtime silhouette
at the actual draw transform; an old donor outline can still drive wall-clamping
and falsely certify containment. Keep visual envelopes, ground blockers and depth
anchors separate: alpha may include shadows and elevated parts. Do not replace
collision with an alpha bounding box or move the sort line to its last pixel
without a crew-overlap review. Include dynamic overlays in final bounds coverage.
For a rear-wall height study, move its cap and face as one assembly; adding only
a backdrop can leave a false ledge through the actor. Keep the trial separate
from production and review shared neighbours before adopting an exterior-looking
solution. A projection rise must not silently change floor or doorway geometry.
The owner subsequently rejected raised rear walls, including exterior-only ones:
retain the current low height everywhere. The height-study lessons here are
historical evidence, not instructions to resume that candidate.
Exercise the actual shared-edge owner: station composition can omit a room's
north/west edge in favour of its neighbour. Require a rendered difference between
candidate modes so modifying an omitted edge cannot pass as a visual comparison.
Check projected height under power loss as well as daylight: a cell-clipped
darkness pass may omit raised walls and actor heads. Tinting walls earlier in the
draw order does not shade actors drawn later; review the assembled silhouette
before promoting the candidate.
Depth regressions need actual overlapping pixels: compare native sorted output
with explicit correct and reversed draw orders. A standable pose behind a low
floor hatch may not overlap at all; record it as clearance, not depth evidence.
Label forced non-walkable overlap probes separately from reachable crew poses,
and keep the entire actor in the diagnostic canvas before visual acceptance.
When adding dressing to a base room renderer, inspect derived rooms that replace
its host registrations. They must clear or replace inherited profiles; otherwise
parent routes can point to removed machinery. Verify host references after each
room's final rebuild, allowing valid child-owned profiles rather than forbidding
dressing altogether. A dependency/hash audit alone cannot detect this mismatch.
Run `tools/audit_room_dressing_hosts.gd` for resolved native profile-host checks
before export; the export helper now gates on it after import. Its explicit
missing-host negative control must fail. This checks mats, supported objects and
route endpoint identities, not whether their pixels or paths look correct.
Reconcile coverage against the live RoomDatabase and station renderer dispatch,
not only batch manifests. Report procedural corridor exclusions explicitly.
An unmapped-room negative control must reject a silent fallback to another room's
renderer; intentional shared renderers require an explicit reviewed exception.

Use `--controlled-tour --composition-review` on the production station fixture for focused neighbour views at the normal initial zoom. The Windows helper accepts `-ControlledTour -CompositionReview` for the same exported views and records them in verification.json; its count/zoom/file checks establish capture availability, not visual quality. Inspect its recorded zoom and distinguish logical cell size from screenshot scaling. A fitted overview alone cannot establish tabletop readability. Review supporting bench scale beside both its main machine and a crew member; enlarging a bench until fine objects read can accidentally create a second focal machine. Check error logs even when the assertion summary says zero; capture methods can fail outside assertions. Before trusting a walker sweep, trace its position getter: changing legacy progress does not move an active production NPC. Use the controlled-tour fixture and verify actual displacement/arrival. Respect current crew-presence prerequisites when setting up that fixture; perform normal recovery setup instead of bypassing a presence gate. The focused `--crew-hab-tour` and `--med-bay-tour` modes check four rotated layouts and return to their starting room without teleporting movement legs. A single-entry room needs both entry and return evidence; an arrival-only itinerary may miss one direction.

Use a fresh exported build for package claims after a renderer/card change;
old package evidence still describes the old revision. Keep current-controller,
economy, renderer-only and owner-review scopes distinct.

When crew obscure a small machine display, keep the normal crew-bearing review
capture and measure machinery in a separate, explicitly labelled unoccluded pass.
Restore crew state before continuing; never hide crew in production or count the
measurement image as depth acceptance. Disable the actual effect in a negative
control to prove the revised measurement still rejects missing animation.
Record active and progression-present crew in capture metadata: preserving input
visibility can still mean no crew were present. Traversal fixtures must satisfy
the current recovery prerequisite through its production entry point, not clear
the progression state to trigger legacy behavior. Report single-crew traversal
separately from multi-crew traffic and actual overlapping-pixel depth review.
For post-recovery fixtures, count population against real berths rather than
assuming visible architects equal population; a prior economy step may produce
a clone. If setup adds a room, let production rebuild navigation before retaining
graph IDs or scheduling routes. Label pre-repaired wards as fixture preconditions,
not evidence that repair costs and exploration progression were exercised.
For near-machinery visit captures, select from registered prop footprints rather
than the combined navigation blocker list, which also contains walls. Record the
selected prop and fallback poses separately. Proximity alone is not pixel overlap.
When studying a setback to keep a working crew silhouette inside a low hull,
compare the whole activity group, not only isolated actor/prop ordering. Move
host-linked accessories coherently and audit adjacent furniture and usable sides.
Record access tradeoffs explicitly; a valid through-route does not prove that
every side of a berth or workbench remains usable.

When the owner requests ongoing pipeline improvement:

- Promote an observed reusable decision rule to the skill.
- Add visual intent to the bible only if it clarifies an established direction;
  new aesthetics remain proposals until accepted.
- Keep coordinates, hashes and failed-run details in the room record.
- Update project and installed skill copies with narrow matching patches,
  preserving concurrent changes, then validate both and check edited-file parity.
- Prefer a focused amendment over duplicating an existing lesson.

A full-room crew diagnostic must render the floor pass as well as sorted props, so pads and service leads remain visible. Keep floor-free isolated depth comparisons separate. Check working-side standing space after grouping furniture; nonintersecting prop footprints alone do not establish crew access. For articulated lamps, distinguish deliberate reach above the work surface from overlap with unrelated equipment in rotated views.

For single-entry rooms, compose against the actual sealed walls rather than retaining a four-way empty cross from the source atlas. For straight and tee rooms, apply the same topology rule to effect-envelope checks: test the actual connected aisle in canonical coordinates, not an obsolete four-quadrant art assumption. Pair equipment by workflow and preserve working-face access. A long exposed service line should have a physical reason; prefer a short local connection where that better describes the activity.


A service group needs a usable working surface: tools and inspection parts should rest on a bench or cart beside the machine they service. Recessed drains can identify wet-service space without adding floor obstacles. Check the group in all orientations: upright sprite silhouettes do not rotate with floor coordinates, so a safe canonical bench can overlap its machine after a quarter-turn. Author a local alternative position when needed and recheck crew access.


At station scale, rugs and mats must belong to visible furniture or a specific service task. A generic central rug floating in circulation space adds decoration but does not make an inhabited room. Review floor-theme dressing together with room-specific mats to catch duplicate or detached textiles.


Run tools/audit_room_floor_hooks.py when adding floor details or overriding draw_room_floor. It resolves inherited methods and explicit super delegation, and rejects profiles with mats/routes/decals whose helper has no reachable floor call or duplicate calls through parent delegation. This is a static integration check; recovery conditions, host validity and rendered visibility still require native review.


When a room replaces registered source sprites with fleet or other procedural asset draws, derive visual bounds from the actual draw rectangles and composite pieces. Placeholder registration outlines can understate both width and height. Construction Bay required separate bounds for its cradle/drone, hatch, wider bench and tall stock rack before grouping furniture. Recheck placement after correcting bounds because wall containment may move the furniture.


For shallow corridor fittings, validate every rectangular segment against the actual hull including chamfers, not only its enclosing rectangle. Keep floor and wall-band placement separate from crew collision. Headless geometry fixtures should report the offending geometry and quit nonzero on failure; an assertion that leaves SceneTree running obscures the result. Verify a deliberate invalid fitting exits before relying on the fixture.


Repeat native room reviews into a fresh output directory and keep card publication explicit. BRINE test_brine_room_v2.gd supports --review-only --output=res://output/<new-review>: it renders its comparison card into evidence rather than overwriting the selected production card. Record the tested source hashes when concurrent renderer work can change the reviewed state.

### Retained furniture belongs to the current occupant
A same-cell room replacement can keep a visible retained canvas even when routes and collisions pass. When the new room does not submit retained contents (including narrow corridors), release the old occupant's canvas. Verify a furnished-room-to-corridor replacement sequence in native rendering and inspect the normal-scale capture. The 37-room v2 package predates this source fix; new-room-composition-routes-v2 covers the corrected replacement.

Composition dependency hashes now gate export before it starts. The catalog37-preflight-reject-v1 negative control rejected a stale profile hash; a later successful export is separate evidence, not grounds to erase the rejection.

### Composition changes need a visual verdict
Moving a bank diagonally can break mirrored symmetry without resolving a four-quadrant composition. Record that remaining visual limitation even when every route and furniture front passes. Connect accessories to physical work surfaces and services, then judge their relationship at station scale. Do not promote a technically verified regrouping to completed organic furnishing.

### Verify an entire activity group after moving its anchor
Moving a scanner changes the neighbouring work area even when only one footprint changes. Enumerate current furniture from the selected profile and include every item in depth review; do not reuse a remembered six-item list after a cooler or shelf was added. Keep open entrance approaches intentional, and use short instrument connections to explain relationships without carpeting the floor in detail. Research services depth v2 includes all seven current props.

### Review current sockets and preserve texture ownership
Use --review-rooms=id,id with tests/playtest_production_ten_station.gd to derive canonical doors from current RoomDatabase layouts, then exercise all four rotations. Unknown room/layout/door names fail explicitly; catalog-review-negative-v2 exits 1 for the requested unknown ID. The v1 negative attempt failed during startup while main.gd was temporarily invalid UTF-8; it is not rejection evidence. Current source had been corrected before any byte repair was written here.
The three rare room views previously discarded their Dressing helper while retaining its registered props, causing wrong-atlas image fragments. Preserve the helper when retaining those props. rare-room-catalog-routes-v3 passes all three rooms in four rotations and q0 captures were inspected. This restores texture ownership only: generic positions and inherited service routing still need authored room-specific layouts. Earlier v1 captures also contained an inspector layout-API error; the current worktree had already corrected that call before v2.
