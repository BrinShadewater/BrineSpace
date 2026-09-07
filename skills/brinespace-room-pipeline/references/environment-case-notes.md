# Historical environment case notes

Preserved from the pre-consolidation environment reference on 2026-09-06.
Use [the production workflow](environment.md) for current instructions and each
pack ledger/README for current status. Historical pending statements below are
retained as evidence of the sequence, not current acceptance claims.

# Underwater environment assets

Read the project's visual bible and `docs/ENVIRONMENT_PRODUCTION_CONTRACT.md`.
Inspect current source PNGs before writing briefs; the original pipe fragment is
a useful industrial material reference, not a universal layout template.

Separate ground materials, low scenery, room-sized blockers and stateful hazards.
Read `sub_biome_view.gd`, `rock_view.gd`, `wreck_view.gd` and `scripts/wreck_field.gd`
for their actual responsibilities. Take cell scale from `game.get_cell_size()`;
historical pixel dimensions in documents are not the current world scale.

Ground uses continuous world sampling with feathered geometry. Mirroring matches
edge pixels but can reveal bilateral repetition; do not call such sources a
seamless TileSet. Adjacent blockers need matching boundaries and shared texture
coordinates, with cliff rims only on exposed sides. Test all four-neighbor masks
and excavation of an interior cell. Props never imply collision or salvage rules.

For wreckage, author a physical story and unequal grounded groups before placing
sprites. Small debris stays below construction; full-room wrecks use the canonical
footprint and authoritative clearance stages. Keep the starting core readable.
Never rotate a tall camera-dependent sprite merely to add visual variety.

Persist exact briefs before generation and copy each returned source to its
versioned project path immediately. Record native dimensions and original SHA256
once in a source ledger. Revisions add entries; audits must not refresh the
expected hash. Explicitly record selected versions and rejected/unreviewed status.
`tools/audit_environment_pack.py` checks hashes, real prop alpha, pack-relative
paths and a runtime `const SOURCES` mapping against the ledger. It writes a new
report without modifying the source ledger. Its tests demonstrate that a newly
named candidate cannot promote itself. The sub-biome pack now uses
`source-ledger.json` as its immutable input; `manifest.json` is derived metadata.
Its catalogue audit verifies hashes before writing outputs. For older packs,
compare files against previously recorded hashes before migrating; never call
changed bytes a new baseline merely to make an audit pass. The one-time biome
migration refuses to replace an existing ledger.

Measure alpha before native review. A checkerboard illustration is opaque even
when the prompt requested transparency. Regenerate the failed exterior with
imagegen, preserving the source; do not discard dark object pixels by threshold.
Inspect overhead projection separately: a repaired camera can introduce a new
opaque background. Passing one revision criterion does not accept the asset.
If an alpha-only edit keeps reproducing an opaque reference background, a fresh
brief can break that failure pattern. Record the failed edits and recheck both
camera and alpha on the new source, as in the service-wreckage tank v1–v4 study.

Use native Godot sheets and station views for scale, alpha edges and layer order.
Keep original source colors on the sheet and runtime tint in station captures.
Isolate title settings and save paths, set windowed mode, and assert actual PNG
dimensions after capture; saved display preferences can override requested sizes.
Wait for the actual Godot process and scan logs for errors as well as PASS text.
Keep `.gd`/`.uid` pairs, raw-PNG loading and the environment export bridge intact.
Native checkout tests do not establish packaged-export or owner art approval.

Low-life batches need distinct silhouettes at room scale: fine seagrass, broad kelp,
flat crusts and shell clusters have different roles. Reject a new identity that
simply repeats an existing plant's shape. Keep distant-view subtlety intentional;
do not inflate small organisms to room size just to show source micro-detail.

Water-effect ledgers use `kind: effect` to require partial alpha as well as empty
exterior pixels. That does not certify motion: compare actual rendered pixels at
different times and identical pixels at a frozen time. Feed the existing game
visual clock into the renderer; verify pause and speed changes. Fade drifting
copies fully out before their positions wrap. Keep ambient water beneath opaque
station geometry and distinguish it from gameplay leaks or hazard cues. Review
source alpha multiplied by runtime tint at station scale; technical loading can
pass while an effect is functionally invisible. State whether motion uses static
sprites, a frame atlas or simulation, and preserve original source pixels.

Update both repository and installed skill copies with focused patches; compare
existing files before syncing so unrelated concurrent additions survive.

For packaged checks, run `tools/validate_environment_export.ps1` with a fresh
output name. Verify prior source hashes before building the export contract,
then run only the exported executable and package from an isolated directory.
Use the environment_validation feature's dedicated startup scene: an exported
template may ignore an editor-style --script launch and open the title instead.
Require the fixture completion marker, exact packaged PNG hashes/dimensions,
runtime texture loads and captures to an absolute writable directory. Raw-load
warnings alone do not prove failure or success; inspect actual bytes and errors.
Preserve logs and executable/package hashes. A debug export is not release or
owner art approval.

Ground-source review should compare ordinary and mirrored repetition at a fixed world scale before live adoption. Pale shell chips can dominate after repetition even when one source looks quiet; assess their density under runtime tint. Keep newer source studies outside historical packaged-verification claims.


The shell-shoal native study showed that directional shell bands become conspicuous diamonds under mirrored sampling. Inspect multi-repeat captures before promoting a ground source; a loading/capture PASS is not visual acceptance. Keep the original and record the failed repetition criterion separately from prop review.


Shell-shoal v2 replaced long directional bands with sparse disconnected grit and removed conspicuous diamonds in the same native repetition fixture. Keep comparison scale and tint fixed across revisions; preserve the rejected source and record why the new version was selected.


Review small shell debris beside its companion rocks at authored cell fractions. Dark shell interiors can preserve material separation without inflating the prop. Record differences from requested piece counts honestly; counts are not automatic visual acceptance or gameplay semantics.


When moving a separate terrain study into the station, reuse the existing feathered world-space mesh and audit its explicit source registry against its own ledger. Preserve historical captures and distinguish native integration evidence from earlier packaged exports.


When adding a pack, extend both the pre-export ledger audit and the exported renderer fixture. Counting packaged PNGs alone misses an unreferenced runtime asset. Capture the new habitat from the isolated executable and retain earlier evidence unchanged.


For collapsed equipment, keep attached cables connected to a visible damaged socket and review the pale functional face under station tint. A complete small assembly can be its own authored group; do not add redundant loose props just to equalize group counts.


Packaged environment review now captures every authored service-wreckage group as well as terrain regions. A region panorama can omit small debris; center dedicated captures on group anchors and record their names in the result report.


Dark-ground studies need a separate readability review for dark blockers and debris under habitat tint. Do not automatically brighten them into the same value as pale sediment; test material contrast and object separation at fixed cell scale.


Repetition previews should cross ordinary/mirrored sampling with source/runtime tint in four panels. Changing sampling and tint together confounds the visual comparison. A light limestone sample does not establish dark-blocker visibility; name exactly which objects were reviewed.


Porous volcanic scenery can separate from dark ash through broad mid-grey top surfaces and dark vesicles. Verify it at authored cell width; readable decorative stones do not prove room-sized blocker clearance silhouettes.


For a dark habitat's initial integration, preserve its material value and sparse authored companion placement. Verify actual room overlap at several window sizes, and keep the separate blocker-visibility check explicit when the fixture clears wrecks for isolation.


For terrain/blocker contrast, move an isolated native clearance formation onto the new ground instead of substituting a decorative stone. Review exposed rims after excavation as well as intact faces; exercise pause and paid rebuilding without changing normal-run balance.


For new plant identities, compare branch structure as well as hue: short forked algae, broad kelp and fine seagrass should remain distinguishable at cell scale. Check pale tips and red saturation under runtime tint before integration.


Plant comparison sheets should show several cell fractions with the same tint and backdrop for every species. Choose an authored placement size from the rendered silhouette, then verify it against actual terrain; a flat backdrop does not establish live contrast.


Place new small plants beside existing vegetation for native review, using unequal authored sizes and spacing. Confirm material/branching distinction on actual terrain and room hierarchy, not just source-sheet separation.


When concurrent gameplay adds new wreck categories, keep export invariants scoped to the original kinds instead of asserting a global count. Preserve failed builds separately, inspect first script errors, and rebuild only after the failed executable is confirmed stopped and current sources are corrected.


Export helpers must bound their own child-process lifetime: monitor error logs during execution, retain a timeout, and verify the executable path before stopping a failed child. Test normal exit, logged failure and timeout independently; process-control checks are not art verification.


Mooring debris review should follow the physical chain from attachment eye to broken terminal link. Check negative spaces through links at native scale, not just exterior transparency; dark steel also needs comparison on both light and dark ground.


A debris source may be suitable on one ground family and weak on another. Record the placement constraint from same-scale terrain comparisons instead of brightening all copies or claiming universal readability.


For static sediment scours, crescent or horseshoe wording can produce an unintended ring. Judge displacement direction and object relationship separately from alpha; preserve rejected sources even when their transparency audit passes.


For grounding decals, compare opacity with the receiving object already layered above. Inspect where the trail meets the object's contact surface; an offset that looks plausible in isolation may attach the scrape to a cable or chain instead of the heavy body.


Register a grounding decal with explicit normalized source anchors on both decal and receiving body. Record canvas sizes and offsets from the native trial, then convert them to room-cell units for integration rather than baking preview pixels into world placement.



Small organisms: distinguish sprite canvas width from visible body diameter when transparent margins differ. Review silhouette at authored cell fractions before integration. A source can have an empty exterior yet no fully opaque pixels; record this separately and inspect textured-terrain contrast under runtime tint before placing it. The short-spine urchin native study is a source-scale review, not a station or package pass.


The urchin terrain comparison supports pale-shoal placement at 0.20–0.25 cell canvas widths; dark ash weakens its compact spiny silhouette. Review habitat-specific contrast before altering the shared tint or enlarging small life. Native room-adjacent captures then check that the chosen placement remains readable in context.


Dense rock variants should change silhouette and fracture structure, not merely recolor porous stones. The fractured-basalt study uses broad flat plates and a real open gap; review those features at cell scale on both pale and dark terrain before placement. Decorative geology does not inherit blocker occupancy from its material name.


Run the immutable source-registry audit as a hard prerequisite to native fixtures and check the command exit code. Broad text substitutions can accidentally rewrite filename suffixes; inspect the resulting SOURCES mapping before launch. Use the existing process monitor for native fixtures too so assertion failures do not leave a Godot window running.
