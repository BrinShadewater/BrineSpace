# Environment production contract

The sub-biome library includes sulfur, sponge, brine, kelp, cold coral, manganese
nodules and iron seep. Iron seep contrasts muted rust stains with low mineral
plates and pale hydroid fronds. Keep terrain quieter than station interiors.
Source colors and the live underwater tint are separate review targets.

Author broad ground materials and isolated transparent props in the overhead
camera. Measure alpha and native dimensions. Preserve original pixels and exact
prompts; select source revisions explicitly rather than promoting new filenames.
Record actual rejection reasons and keep unreviewed candidates distinct.

The renderer feathers irregular meshes and maps one continuous source field over
each authored habitat patch. This replaced mirrored tiles on September 9 because
mineral patterns formed repeated bilateral diamonds. Shared shell, ash, clay and
ripple patches use the same field mapping; source images and prop placement remain
unchanged. Connected blocker materials retain their own world-space sampling. Decorative rocks and debris imply no
blockage or salvage reward. Connected basalt blockers and wreck clearance use
authoritative room-cell occupancy in `scripts/wreck_field.gd`.

Review native source sheets and station views with real room scale. Check actual
capture dimensions, stable placement and layering. Keep source review, gameplay
verification, owner approval and packaged-export verification distinct.

The iron expansion passed `tests/playtest_sub_biomes.gd`, documented in
`output/iron-seep-native.log`: 21 textures, seven habitats, three resolutions.
Hazard simulation and procedural site generation remain separate work.

## Service wreckage and provenance

`assets/environment/service-wreckage-v1` adds a collapsed support, torn cable
harness, ruptured pressure tank and detached hatch. Three unequal authored groups
suggest a broken service frame, failed pressure line and loose access cover.
Keep small scenery under room geometry; its presence does not create salvage
jobs. The native fixture verifies normal paid construction over the debris.

The tank study exposed independent failure modes: v1 had too much vertical side
face; v2 corrected projection but introduced an opaque checkerboard, and v3 kept
that background. A fresh overhead brief produced transparent v4. Do not accept a
camera correction without rechecking alpha, or repeatedly assume an extraction
prompt removed an illustrated background. Preserve all failed sources and record
the evidence that caused each rejection.

New packs use `tools/audit_environment_pack.py`: expected source hashes are recorded
once, selected files are explicit, runtime source maps must agree, and each audit
writes a new report. `tools/build_environment_catalogue.py` reuses that verification.
The biome pack now has an immutable `source-ledger.json` input. Its migration
verified all 24 existing files against previously recorded hashes, and the
catalogue builder checks those hashes before updating derived metadata. The
remaining older packs still need their provenance workflows assessed separately.
Neither tool infers art approval from dimensions.

`output/service-wreckage-native.log` records four alpha sprites, three groups at
three verified resolutions, unchanged occupancy and paid build-over.
`output/service-wreckage-rock-regression.log` confirms the existing connected-rock,
excavation, pause, shared-rig, save and paid-rebuild behavior still passes.

## Low seabed life

The low-growth pack adds fine seagrass, flat encrusting algae and attached mussel
clusters in eight small placements at meadow and reef margins. Distinguish shape
roles: the first grass candidate was rejected for repeating the broad kelp
silhouette. Narrow blades with transparent gaps remain subtle at distant zoom;
small organisms should not be inflated merely to expose their source detail.
Mussels are static attached fauna in this pack, with no food-yield mechanic.

`output/low-growth-native.log` records three alpha sprites and three groups at
three verified resolutions, with no occupancy or resource changes.
`output/biome-ledger-native.log` verifies all seven existing habitats after the
source-registry migration. Ten pipeline tests cover hash drift, explicit source
selection, alpha, path boundaries, LFS pointers and stopping catalogue writes
before failed provenance can replace prior output.

## Ambient water motion

Three water sources supply a current ribbon, drifting silt and fine bubbles.
They animate through short translations and staggered fades using the existing
pause-aware visual clock. These are static textures with runtime motion, not a
fluid simulation. Water stays below rocks, wrecks and rooms. Fixed ambient cues
do not advertise gameplay leaks, resources or hazards.

The native fixture compares pixels at different and frozen times, checks loop
fades, exercises pause and speed, and captures three effects at three verified
resolutions plus room overlap. Initial opacity values loaded correctly but were
too faint; final values are in the pack README. `kind: effect` now requires
partial transparency in the immutable audit. Twelve pipeline tests pass,
including two new effect-alpha cases. Technical checks do not imply owner approval.

## Packaged environment verification

The actual Windows debug export now verifies all 69 preserved PNGs across seven
packs and 46 runtime textures outside the checkout. Three station resolutions
and seven habitats are captured. Use `tools/validate_environment_export.ps1`
with a new output name to preserve evidence. See
[export validation](ENVIRONMENT_EXPORT_VALIDATION.md) for the command, results,
startup-scene requirement and remaining review boundaries.

The shell-shoal addition extends this to eight packs, 73 preserved PNGs and 49
runtime textures in `output/environment-export-v4/`. Include both its ledger
verification and its live texture/capture checks when extending the export
fixture; merely packaging a new PNG does not demonstrate that its renderer uses it.

## Current game release gate

The debug package counts above describe their dated fixture scopes. For Windows
Game releases, follow [the runtime asset and release contract](RELEASE_ASSET_CONTRACT.md):
regenerate selected dependencies, audit immutable packaged bytes outside the
checkout, and exercise the actual release executable. Retain native environment
appearance and motion review separately; package integrity does not establish it.
