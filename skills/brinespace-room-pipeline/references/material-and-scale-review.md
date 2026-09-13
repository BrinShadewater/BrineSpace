> Current owner decision: [top-down and inward-facing contract](top-down-owner-contract.md) supersedes conflicting historical camera guidance below. Read it before production or handoff.

# Material and scale review

Derelict lighting contract: found rooms are unlit, including companion rooms
drawn through the preview path. Repair removes visual decay independently of power;
electric lighting then follows allocation and the interior switch. Review three
separate states: unrepaired/off, repaired/off, repaired/on. Keep enough ambient
visibility to read the rescue subject. Shared recovery views must be configured
for the current room before a later wall pass reads their mutable geometry.

Owner correction to derelicts: debris around pristine interiors is insufficient.
Condition must reach the floor finish, wall cladding and equipment casings.
Keep material wear attached to the source through pan/zoom and preserve alpha,
dark recesses and readable occupants. Verify both actual worn pixels and exact
restored-art parity; a debris manifest alone cannot establish surface weathering.

Derelict condition lesson (September 12): broad flat procedural polygons read as
markers against painted room art. The adopted condition layer uses a true-alpha
painted sediment/debris source beneath furniture, with the central crossing left
transparent. Review found and restored views separately; shared room-view selection
can mutate recovery geometry, so inspection probes must not call setup getters
merely to read metadata. See `docs/DERELICT_CONDITION_2026-09-12.md` in the project.

Owner direction: props must stay modest and matte. Darkening a shiny source is
not a material correction. Cleanliness, departmental color and gloss are separate.
Read this workflow for every asset; consult the [casebook](material-scale-casebook.md)
only for relevant failures and evidence. Its dated statements are historical;
current owner decisions, current code and exact reviewed revisions govern.

## Establish the brief

1. Inspect a stable furnished room and relevant material reference. Record paths,
   hashes and separate roles: camera, geometry, subject and finish. Do not make
   the latest candidate the only style master or copy old glossy highlights.
   The owner-selected repainted Tidal room governs the current matching pass;
   read `docs/ROOM_REFERENCE_DIRECTION_2026-09-08.md` for supplied interior roles.
   Use their functional bays and tactile materials, not ceiling/camera/glow density.
2. Record department, condition, camera, facing, intended visible world dimensions
   and ground footprint. Wall length comes from adjacent small task areas. Vary
   bay widths and supported equipment; preserve usable working space.
3. Classify floor equipment, fitted cabinet or hull attachment. Measure the actual
   host and door exclusions. Use current owner-directed geometry; do not enlarge
   it merely to fit an accessory. Distinguish wall-strip depth from projected
   riser-face height: September 8 code retains a16-unit strip but raises the face
   to60 units (`rooms/whole-room/riser_geometry.gd`). A schematic strip fit does
   not prove face mounting, orientation, depth ordering or access. Recheck recorded
   renderer hashes before carrying earlier mounting evidence into a changed room.
4. Specify quiet powder coat, composite, rubber, cloth, uncoated paper or wood:
   broad pixel clusters and sparse midtone edges. Exclude chrome, white rim lines,
   metallic sparkle, glossy gradients, wet sheen, bloom and dense scratch noise.
   Pale ceramics and gauge faces may remain pale. Keep live emission separate.
5. Name functional bays in spatial order. Record actual depicted open/closed or
   loaded/empty state separately from `runtime_behavior`. Incidental variants
   must be described honestly; repair explicit owner or gameplay-state mismatches.

## Review and repair

- **Materials:** inspect each component, especially cylinders, glass, tools,
  handles, wood edge lines, ceramic rims and mineral sparkle. A dark histogram
  or matte cabinet does not establish that its accessories pass. Check exterior
  halo separately. Do not replace shine with grime or global desaturation.
- **Camera and direction:** verify top-plane proportions and every inward-facing
  handle, spout, opening and control. A tall strip can be a stacked front elevation.
  Do not rotate a front sprite into a side view. If construction changes to achieve
  the view, identify it as a companion design, not an exact reconstruction.
- **Native scale:** inspect nearest-filtered art beside established furniture and
  crew at equal world scale. Let fine texture simplify. Never enlarge props to
  expose detail. Preserve working surfaces; include projecting handles, wheels,
  footrests and operator approaches in later placement checks.
- **Alpha:** inspect image mode and dimensions after every edit. True-alpha input
  can become opaque checkerboard. Choose neutral thresholds from source pixels,
  never another asset's settings. Inspect corners, long rails and enclosed gaps
  on light/dark grounds. A loop over a solid tray is not a through-hole. Pair an
  aperture alpha probe with a retained-interior probe where applicable.
- **Edge repair:** isolated background spikes can survive corner checks. Preserve
  earlier registrations; any bounded source-space exclusion must be reviewed
  against real fixtures. Repair source defects through imagegen when needed.
- **Integration:** only actual placement verifies wall contact, mounting plane,
  footprint, doors, chamber access, circulation and depth in supported orientations.
  Standalone, group and schematic captures do not prove occupied crew clearance.

Use imagegen for material/proportion repairs with stable references. Preserve raw
sources, exact prompts and rejected reasons. Re-register changed dimensions and
verify source/export hashes. Do not claim a construction substitution was a
material-only edit or pixel lock. For atlas repainting, inspect structural wall
UV samples and auxiliary props as well as the new bank; retain source dimensions,
UVs and authoritative hull geometry, then review hull, returns and foundations.

## Record and compare

Use `templates/material-scale-review.json`; unknown fields stay null and owner
acceptance remains separate from agent findings. Initialize after export:

```powershell
python tools/init_material_scale_review.py --registration assets/example/registration.json --export assets/example/asset.png --prompt assets/example/source.prompt.txt --asset-id example --width 328 --output assets/example/material-scale-review.json
```

Use `--height` for vertical banks and repeat `--reference PATH ROLE` as needed.
Dimensions derive from registered content, not transparent margins. Initialization
checks hashes/dimensions/alpha, refuses overwrite and never grants visual acceptance.
Fill department, facing, condition, exclusions and actual findings afterward.
Focused validation: `python -m unittest discover -s tests -p test_init_material_scale_review.py`.

For reviewed openings and retained interiors, save named pixel probes with native
canvas coordinates, expected `transparent`/`opaque`, measured alpha and export hash.
Run `python tools/check_asset_alpha_probes.py assets/example/alpha-probes.json`.
The textile basket record is a schema example. This read-only check rejects stale
hashes, invalid coordinates, missing alpha and changed point values; it checks only
selected pixels, never the entire silhouette. Re-select probes through visual review
after geometry changes rather than just updating hashes. Focused tests:
`python -m unittest discover -s tests -p test_asset_alpha_probes.py`.

Run `python tools/build_material_review_gallery.py` after adding records. It
includes compatible `material-scale-review.json` and `*-review.json` files, not
the whole catalog or legacy manifests. Duplicate exports fail; stale hashes and
written findings stay distinct. Thumbnails fit cards, not native scale. Local
page rendering/filtering remains unverified after the earlier URL-policy block.

For directional families, index wall side, inward direction, backing edge, export
hash, registration and separate review. For state pairs, compare canvas and bounds
and record drift/shared-region proposals; independent tight crops can shift art.
Indices and matching hashes do not establish runtime transitions or owner approval.

When a review records registration path/hash, the audit verifies both against the
indexed outline. Legacy records report `review_registration_hash_verified: false`;
their passing export hashes do not establish that registration was reviewed.

Audit indexed directions with `python tools/audit_directional_family.py FAMILY.json
--output output/family-audit.json`. It checks declared coverage/facing, source and
export hashes, review links and long-axis scale, including established legacy field
names. Partial coverage stays incomplete. It never verifies fixture pixels or grants
visual acceptance. Focused tests: `python -m unittest discover -s tests -p test_directional_family.py`.
Reports must be JSON under project `output/`. Only tool-marked reports can be
replaced; use a new filename for older reports. Linked asset/record files are
protected, and validation failures replace earlier tool-owned passes with explicit
failure reports. Check exit status and `metadata`, not report existence alone.

## Native tools and limits

`tools/review_registered_wall_asset.gd` exports registered source UVs to true-alpha
PNG plus1040×900 scale board. After Godot's `--` separator, pass:
`--registration=res://...json --export=res://...png --review=res://output/...png
--reference-view=res://...gd --width=320`. Reference view is optional. Run graphically
and inspect the PNG and complete board. No room installation is performed.
Inspect the entire log for script/load errors even when a final PASS line appears.
Prefer `python tools/run_wall_asset_review.py --godot PATH --registration res://...json
--export res://...png --review res://output/...png --reference-view res://...gd
--width 320 --log output/unique-review.log`. This graphical wrapper rejects error
lines, nonzero exits and missing completion markers; preserve unique evidence paths.
Its success still requires visual inspection. Focused tests: `python -m unittest
discover -s tests -p test_wall_review_runner.py`.
If a reference renderer fails, an isolated export check can establish materials
and alpha only; leave the clean room comparison pending and preserve the failed log.

Portraits use dedicated native columns and segmented material detail. Fitted
overviews and source sections are diagnostics, not separate assets or gameplay
scale. Respect the renderer's current size guards; enlarge a board rather than
falsify scale or crop a candidate. Current code owns exact panel dimensions.

For companions, `tools/review_prop_group.gd --group=res://...json --review=res://output/...png`
checks hashes, source regions and shared scale. Its native/2x panels must contain
the whole arrangement; reject empty/nonnumeric entries, clipping and overwrite.
After changing it, run `python tests/check_prop_group_review.py --godot PATH` and
visually inspect the valid case. Static group geometry is not collision evidence.

## Maintain the workflow

At a meaningful milestone, record decisions, changed files, remaining work and
checks in the project handoff. Update a general gate only when evidence supports
it; put detailed trials in the casebook or asset README. Avoid another paragraph
for every successful asset. Keep executable tools in the project and sync only
changed skill files after comparing the maintained and installed versions.

This is an ongoing practice within authorized art tasks, not a scheduled job or
permission for unrelated bulk revisions. Do not promote candidate review to owner
acceptance, or a single-source correction to a guarantee for later art.

## Gallery context evidence

The standardized gallery exposes additional review scopes (host study, relocation study, supported group) separately from material/scale/alpha. Preserve rejected original layouts alongside later proposals; never replace a host rejection with a generic pass. Link each study evidence/report and record hashes when available. The gallery flags changed linked evidence but does not validate runtime access or infer acceptance.

September 8 south-bank polish: keep three reference roles explicit: the selected camera/silhouette, approved Tidal finish quality, and the department's established material identity. A shared pale-green base made unrelated south banks feel generic; recessed service details and department-appropriate cloth, wood, composite and steel improved the native comparison. Verify registered proportional frames separately from source boundary drift. Native Godot polygon exports provide source-canvas alpha evidence without editing original pixels. See docs/ROOM_STYLE_POLISH_2026-09-08.md.

September 8 department risers: use distinct construction and material families beneath stable editable wall mounts. Register the functional upper service band at the runtime face aspect (384:60); exclude quiet lower cabinet source areas instead of compressing the entire illustration. Short corridor faces use proportional crops. Review native room rotations and a connected station, and test both default visibility and a saved explicit override. Evidence: docs/RISER_DEPARTMENT_PASS_2026-09-08.md.

September 8 corridor variants: upright observation glazing must not be sampled onto low hull top plates. Register a quiet solid source region for top surfaces separately from the full upright face. Native raised/low captures at four rotations exposed this issue; six straight/turning sources and nine shape variants are recorded in docs/CORRIDOR_WALL_VARIANTS_2026-09-08.md.

September 8 industrial hall floor correction: owner rejected large quiet slabs in favor of smaller grating, metal panels and recessed pipes. Distinguish built-in floor construction from loose clutter; the owner requested the former after removing the latter. Keep source module size separate from editor cell size (24-unit modules within 48-unit cells). See docs/HALLWAY_FLOOR_TILES_2026-09-08.md.

## Session closeout

When the owner pauses art production, stop new generation and leave a bounded handoff: completed families, exact unresolved directions, candidate versus installed state, latest evidence and the first useful next action. Preserve concurrent session notes. Reuse existing successful checks for documentation-only closeout; do not rerun bulk exports or imply the ongoing art backlog is complete. September8 wall-asset handoff: `docs/WALL_ASSET_SESSION_CLOSEOUT_2026-09-08.md`.

## September 9 room material and declutter lessons

Apply [room materials and declutter](room-materials-and-declutter.md) for crew-scale accessories, shared-atlas structural texture preservation, runtime-only common-prop removal, current Studio wall suppression, final registration/card evidence and manifest/LFS closeout.


Construction repair lesson (September 12): retain directional `wall_contact`
metadata when replacing raster registrations. It controls actual mounting in
`full_wall_prop.gd`; correct source hashes and passing route/card tests did not
detect a south bank placed beside floor stations. Inspect fresh native captures
after the process finishes. Matte casing improvement also does not prove matte
rollers, spools or shared floor machinery; track those components separately.


Construction material refinement (September 12): a casing repaint can leave bright reflection bands on rollers and spools. Name those residual components explicitly in a second edit and preserve rib/winding readability. The refined wall passed four native views; a newly generated floor atlas is still a candidate. Never treat an untouched-looking drone row in a generated atlas as pixel-identical or replace it without verification.


Construction static-atlas lesson (September 12): use an explicit optional texture for static cradle/bench/hatch draws when a repaint belongs to one bay. Keep the default atlas and drone draw path intact. Check candidate pixels against existing source rectangles and probe both through-gaps and solid lids; matching canvas dimensions alone is insufficient. The Construction repaint passes four native material views, but material review does not establish inward-facing floor-equipment compliance.


Construction panel-storage lesson (September 12): an image edit anchored to tall upright plates retained their front faces despite overhead wording. A new low flat-storage companion produced an unambiguous top plane. Record this as a construction change, preserve the rejected elevation and both prompts, and fit inside the former maximum footprint. Point release catches toward room center and derive visual bounds from the same aspect-preserving rectangle used to draw. The live q2 pallet was inspected; other layouts omit this prop, so four room captures do not prove four pallet orientations.


Construction pallet-facing verification (September 12): when normal layouts omit a prop in three quarters, use a native component fixture invoking the production texture/bounds helpers at four placement centers. Inspect the inward release edge and measured footprint in each. Keep this evidence distinct from occupied-room/crew-clearance review. The maintained fixture is tools/capture_construction_panel_facings.gd.


Construction overhead bench lesson (September 12): show parked arm joint caps from above and place service controls on a named operator edge. Native views must verify that edge after placement-dependent rotation. Preserve genuine generated alpha even when the preview background looks black; do not apply a black color key to charcoal machinery. Aspect-preserving quarter-turn variants may occupy less of the old maximum rectangle, so inspect readability at the resulting native size.


Construction hatch camera lesson (September 12): camera conversion applies to runtime visual overlays as well as static art. The inherited hatch opening is an offset ellipse; a circular overhead lid requires a source-aligned circular aperture. Preserve the existing deployment state and timing, change only its visual geometry, and review closed/partial/open states before installation. A passing closed-room capture cannot prove aperture alignment.


Construction circular-hatch integration (September 12): register aperture center and radius in source coordinates and rotate that center with each raster quarter turn. Fit the circular source uniformly inside the former envelope. Native closed/half/open rows across four operator directions established circular alignment without altering deployment state/timing. Remove only measured negligible alpha haze (below 16 here), preserve near-opaque interior alpha, and inspect over the real floor.


Construction cradle fit lesson (September 12): review empty and occupied support machinery together. A rectangular cradle rotated inside unchanged maximum dimensions shrank its side-facing support width below the existing drone footprint. The source passed overhead/material and gap-alpha checks but failed docked fit. Preserve the rejected candidate; design a near-square support footprint and test with the unchanged drone before integration.


Construction square cradle lesson (September 12): a broad near-square support deck maintained docked support in every quarter turn where the long slotted candidate failed. Inspect both empty and occupied at actual draw size; preserve the drone offset and merge its original envelope into static bounds so deployment does not change layout. Material/style recommendations for the drone remain distinct from stationary machinery acceptance.


Tidal inventory/facing audit (September 12): existing directional companions changed inventory (three north coil returns and console versus two returns and no console south). Lock the whole-bank inventory before deriving rotations. A candidate can restore counts yet fail individual cartridge access; inspect every release edge. Check actual alpha mode because a rendered checkerboard can be baked RGB. Rear-wall palette is a separate live consumer from the machinery bank.


Tidal overhead family integration (September 12): retain three coil returns, two vessel lids, three cartridges and console through exact turns. Align cartridge long axes with the operator approach so blue releases sit on the inward edge and fixed pipes remain outward. A uniform magenta exterior enabled clean alpha after the prior baked checkerboard failed. Native q0–q3 confirms inventory, inward controls and mounting; the separate orange riser and independent machinery remain separate work.


Tidal rear-wall palette lesson (September 12): room machinery and architectural risers have separate source selection. A room-specific catalog override can match grey-blue panels and brass pipes while retaining shared face/cap rectangles and other engineering rooms. Verify both the cap seam and doorway joins in native orientations, and update the selected room card after the architectural change.


Tidal independent equipment lesson (September 12): an elevation reference can preserve the wrong camera even with an explicit overhead prompt. The rejected study retained a tall filter face. A plan-geometry brief produced a circular lid and flat controls with cartridge releases toward the operator. Preserve rejected sources, inspect pull-tab apertures during keying, and transform source-local effect anchors with the exact artwork turn. Static native fit does not prove operating or paused-state behavior.


Tidal station-state lesson (September 12): a comms dialog can legitimately hold pause and invalidate an art fixture resume sample. Dismiss the dialog and disable automatic comms polling in the isolated fixture, then prove real clock advancement before testing pause. Check both renderer clock and native pixels; fixed-clock parity alone does not establish paused station behavior. New rotated art also requires matching visual bounds for containment and retained culling.


Command riser precedence lesson (September 12): catalog files merge with Dictionary.merge default overwrite=false. A duplicate room ID in a later file does not override its existing entry. Locate and update the authoritative first registration; preserve the previous entry as provenance. A passing card-binding test cannot prove the new source was selected. Compare native imagery before claiming palette integration.


Command consumer inventory lesson (September 12): read the split-wall replaces/preserve list before identifying a small console from its silhouette. Command preserves systems and table while replacing operations and comms. A new comms sprite cannot stand in for the single-screen systems terminal. Inventory-correct sources, oriented visual bounds and common art/effect transforms are verified separately through native room fit and direct/retained state captures.


Command wall alpha lesson (September 12): a camera edit can open a new background pocket inside an older clipping polygon. Preserve the raw edit and verify alpha in the native consumer. Border-only cleanup can miss isolated pockets; removing all neutral white was appropriate for these sources only because their equipment has no authored white surfaces. Do not generalize this threshold to clinical or pale-painted art.


Observation rotation lesson (September 12): removing a fixed-camera renderer lock is insufficient when saved default layouts reapply identical furniture coordinates in every rotation. Native review exposed desk/shelf overlap and the route check exposed a blocked doorway. Remove only obsolete placement/size overrides, preserve their provenance, and verify genuinely distinct quarter-turn geometry with the desk/chair relationship intact. Architectural portholes remain separate from rotating furniture.


Observation reading-light lesson (September 12): a powered reading lamp should remain steady, not pulse with the machine clock. Keep its illumination inside the desktop and transform it with the furniture. Verify an off/on difference, identical powered samples at two clocks, and direct/retained parity; separately test cache invalidation when power changes on an existing retained room.


Observation retained-state verification (September 12): a steady powered reading
light still requires cache invalidation. Reuse existing production canvases across
off/on changes and compare every orientation against direct references; fresh
canvases alone cannot prove this. Resolve live room views from the current renderer
registry before adapting another room's station fixture. Verify actual running and
paused station state independently of fixed-clock artwork previews.


Salvage overhead conversion lesson (September 12): chroma-key edge pixels can be
much darker than the flat background. Native-scale review caught a magenta seam
missed by absolute brightness thresholds. For this source, red and blue dominance
over green removed the fringe while preserving neutral metal. Preserve raw art,
record the source-specific rule, and verify the cleaned result against the actual
room floor. Rotate source art, prop bounds and source-local effect anchors together;
remove obsolete fixed-camera layout overrides only for the affected prop fields.


Galley communal-table review (September 12): judge long seating furniture against
the production crew sprite and its actual pivot/standing-height metadata, using
the same room draw_actor scale. A source image or empty-room fit cannot establish
seat scale. Keep table/bench gaps transparent and reserve circulation separately
from the combined furniture collision rectangle. Review all orientations and
distinguish standing scale comparison from seated interaction acceptance.
Cold-effect cache lesson (September 12): deterministic vapor still changes with
the visual clock. When testing an existing retained canvas across a power toggle,
pin every compared host to the same clock before asserting equality with a direct
reference. First prove direct/retained parity at matching times, then prove temporal
change and actual station pause separately. Inspect a nearest-neighbor native crop;
whole-room contact sheets can hide restrained particles.

Battery split-bank lesson (September 12): lock inventory and split ownership before
replacing only one directional source. A shallower source aspect can improve an
overhead camera while leaving the established section frames and collision intact.
When separate GPU texture instances produce isolated one-channel differences,
record changed-pixel count and maximum delta rather than calling static artwork
animated. Confirm powered clocks are identical and distinguish retained effects on
independent preserved props from the replacement wall bank.

Shared-atlas material lesson (September 12): a generated repaint can improve color
while silently changing the silhouette, canvas and articulated joints. Preserve it
as rejected evidence. When the source atlas and UV animation are already correct,
apply a deterministic material transform only inside the named asset rectangle.
Verify that neighboring identities retain their source path, then inspect docked,
travelling and segmented working draws. A static room card cannot prove the working
UV path uses the same material correction.

Crew-scale integration lesson (September 12): use the actual runtime renderer's
authoring identity; a Studio catalog alias can point to a different layout key.
Verify resized source polygons as well as collision rectangles, and apply authored
size/position when a wrapper restores retained props after full-wall configuration.
Preserve floor foot anchors or outward wall contact; compare every supported
rotation to the selected production crew. Equal-purpose pods should use equal
footprints. Refresh cards without the review-only crew, and distinguish standing
scale review from seated/sleeping animation acceptance.

Sparse-room massing lesson (September 12): add one functional square or rectangular
anchor before multiplying loose accessories. A large anchor may pair with one
medium support piece when their purposes and operator edges differ. Preserve open
floor around the group, use explicit quarter-specific centers, and verify every
door route in the native room. Full-wall filtering may retain deliberate
`centerpiece` and `authored_anchor` items, but those flags never substitute for
route or visual review. Keep shape-mismatched candidates as rejected provenance.

Universal furnishing lesson (September 13): make reuse come from neutral construction,
matte materials and generic service function rather than identical placement in every
room. Avoid department marks and dominant department color, then demonstrate the same
family beside several distinct interiors at native scale. Universal assets remain
sparse support pieces; every room still needs its own primary themed activity.

Universal equipment-platform lesson (September 13): give neutral furniture a visible
service purpose such as parts storage, an equipment mount or a task surface. An empty
generic block reads as filler even when its material and scale fit. Use these functional
platforms sparingly, preserve the themed room anchor, and validate their lower chassis
collision separately from tall transparent or overhanging artwork.

Repeated-workbench replacement lesson (September 13): when related rooms inherit the
same support bench, replace repetition with one room-specific work anchor and at most one
neutral support piece. Let the anchor explain the local process while the support piece
supplies a generic station function. Keep both subordinate to the main machine, and prove
their paired footprints leave every production crew route open in all rotations.

Cross-department neutrality lesson (September 13): validate a universal family against
interiors with materially different palettes and purposes. Neutral graphite, warm gray,
generic latches and removable trays can sit beside engineering, clinical and cultivation
equipment without borrowing their department colors. Preserve one clear local workstation
as the semantic anchor, and keep the neutral module smaller and visually quieter.

Universal footprint-variety lesson (September 13): a reusable family should include narrow
portrait pieces as well as wide chests and tables. A tall-in-plan caddy can occupy a wall-side
gap that rejects another horizontal bench, while retaining the same neutral materials and
generic service role. Record its true portrait collision rectangle and review it independently
in every quarter; rotating the concept mentally is not placement evidence.

Light-floor separation lesson (September 13): pale clinical and biology furniture needs a
continuous dark edge, hardware rhythm or tight contact shadow so its silhouette stays legible
on sealed terrazzo and pale laboratory decking. Judge that separation at native room scale and
again in the baked card; source-scale contrast alone can hide overlap with inherited machines.

Rotating-host clearance lesson (September 13): a mathematically rotated secondary center can
track straight into a room's rotating fixed equipment. Review the neutral support as its own
silhouette in every native quarter and allow independent authored centers when the fixed host
layout is asymmetric; a passing door route does not prove visible separation from machinery.

Visual breathing-room lesson (September 13): collision-clear placement can still make a small
neutral prop read as part of a larger inherited machine. Inspect empty floor around the entire
rendered silhouette in every native orientation, then author an independent center where needed.
Keep enough separation to preserve the prop's function at card scale as well as full room scale.

Large/medium batch closeout lesson (September 13): review the runtime prop inventory as data as
well as pixels. A full-wall wrapper can silently omit an `authored_anchor` while the remaining
equipment makes the contact sheet look complete. Require every selected asset ID in every native
quarter, then inspect silhouette separation, bake cards, update primary and variant consumers,
refresh owning dependency hashes, and run the route/card/side-wall suite. Record generated,
selected, rejected, integrated, agent-reviewed and owner-accepted states separately.

## Source resolution and floor-contact diagnosis — September 13

Before replacing low-resolution animation art, inspect preserved higher-density sources and the active source region. Keep the existing registration, silhouette and floor anchor when changing the selected crop. A larger canvas alone does not establish source detail.

Check shadow ownership before tuning darkness: the BRINE tube had both a custom oval and a generic rectangular machinery shadow. Source-shaped contact belongs at the physical skirt; suppress duplicate generic shadows through the prop contract. Review common shadow changes across representative materials and rotations. Tube grounding has owner acceptance; wider grounding and crew-scale passes have bounded native review, not automatic owner acceptance.

Use the existing crew-scale integration lesson above for resizing. Recorded 65.28 world units is this revision's production reference; re-read current consumer metadata for future revisions. Later selected furnishings supersede historical scale-pass captures.
