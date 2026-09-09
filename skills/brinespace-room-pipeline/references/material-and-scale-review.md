# Material and scale review

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
