# Underwater environment assets

Use this workflow for production. [Case notes](environment-case-notes.md) preserve
the studies behind these rules; their historical status statements are not the
current asset inventory. Current selection and integration status live in each
pack's ledger and README, with passing evidence in the referenced logs.

## Establish the asset contract

Read the project visual bible and `docs/ENVIRONMENT_PRODUCTION_CONTRACT.md`.
Inspect actual source PNGs before writing briefs. The original pipe fragment is
an industrial material reference, not a universal layout template.
Read the relevant `sub_biome_view.gd`, `rock_view.gd`, `wreck_view.gd` and
`scripts/wreck_field.gd`. Take scale from `game.get_cell_size()`.

Separate ground, decorative scenery, room-cell blockers, wreck clearance and
stateful hazards. Material names do not grant gameplay behavior. Keep the core
readable; small scenery belongs below construction. Full-room wrecks retain
canonical footprints and authoritative clearance stages. Do not rotate tall
camera-dependent sprites simply for variety.

## Preserve and audit sources

Save exact briefs before generation. Copy returned originals immediately to
versioned project paths; record native dimensions and immutable SHA256 values.
Add revisions and explicit selection/rejection reasons without refreshing old
expected hashes. Keep failed candidates. Inspect camera and alpha independently:
a projection repair can introduce an opaque illustrated checkerboard.

Use imagegen for failed-exterior repair; never threshold away dark object pixels.
If alpha-only edits repeat the same opaque background, try a fresh brief and
recheck both camera and transparency. Empty exterior does not imply opaque
interiors: record partial alpha and inspect the final composite.

Run `tools/audit_environment_pack.py` and stop on a nonzero exit before native
fixtures. Inspect the resulting `const SOURCES` map after edits: broad text
substitution can corrupt filename suffixes. Audits check hashes, alpha, paths
and registry selection, not visual acceptance. Reports use fresh output paths.

The sub-biome pack uses immutable `source-ledger.json` and derived
`manifest.json`. Catalogue generation audits first. For legacy migration,
compare against earlier recorded hashes; never bless changed bytes as a new
baseline. Preserve `.gd`/`.uid` pairs, raw-PNG loading and the export bridge.

## Choose the visual review

| Asset | Required comparison |
|---|---|
| Ground | Four panels: ordinary/mirrored sampling crossed with source/runtime tint, at fixed world scale. Inspect multiple repeats for bands and bilateral diamonds. |
| Small life | Several cell fractions beside existing species, with identical tint/backdrop; compare branching and silhouette, then actual terrain and room hierarchy. |
| Rocks and debris | Same-scale pale/dark terrain comparison; distinguish broad faces, fracture structure, vesicles and material values. |
| Blockers | Actual room-sized formation on the new ground, all four-neighbor masks, exposed rims and interior excavation, pause and paid rebuilding. |
| Grounding decals | Opacity comparison beneath the receiving object; verify the trail meets its heavy contact surface. |
| Animated water | Rendered pixel change over time, identical pixels at frozen time, pause/speed behavior and fade before wrapping. |

Mirror sampling matches edge pixels but is not proof of a seamless TileSet.
Reuse feathered world-space ground meshes. Blockers need shared texture
coordinates, matched boundaries and rims only on exposed sides. A decorative
stone comparison cannot prove blocker readability or clearance behavior.

Keep fine seagrass, broad kelp, crusts, shell clusters and compact organisms
distinct through shape, not hue alone. Canvas width differs from visible body
diameter when margins differ. Do not enlarge small life merely to display detail.
Record habitat-specific placement constraints instead of brightening every copy.

Wreckage needs a physical story and unequal grounded groups. Trace attached
cables to damaged sockets and mooring chain from eye to broken end; inspect
negative spaces at cell scale. A complete assembly needs no redundant loose
props. Record requested-versus-produced piece counts honestly.

For decals, judge displacement direction separately from alpha; a crescent may
read as a ring. Record normalized anchors on decal and receiving body, then
convert reviewed sizes/offsets into cell units. Keep static scours separate from
animated water and excavation state.

Water ledgers use `kind: effect` for partial alpha, not automatic motion approval.
Use the existing visual clock, preserve original pixels, state the technique
(static sprite, atlas or simulation), and check alpha multiplied by runtime tint.
Keep ambient water below opaque station geometry and distinct from hazard cues.

## Compose places from the library

Choose an anchor and physical story before adding props. Group debris along a
failure trail, reserve open ground along currents, and attach life to structure.
Suppress random scatter within authored footprints. Reuse existing caches and
preserve authoritative wreck cells; background composition is not salvage logic.
Review whole sites with actual wrecks and rooms present at several viewport sizes.
Record named site captures in the exported fixture, not just individual assets.

## Verify native integration

Use Godot sheets and actual station captures. Preserve source-color comparison
alongside runtime tint. Isolate title settings and save paths, use windowed mode,
and assert actual capture dimensions. Confirm room overlap at several sizes and
unchanged gameplay state for decorative integration. A fixture that removes
wrecks does not verify blocker visibility.

Use `tools/wait_environment_process.ps1` for native and export child processes:
monitor logs, bound runtime, and verify the executable path before stopping only
the owned failed child. Check errors, exit status and PASS together. Preserve
failed logs. Retry only after the previous process is terminal and the first
failure's current source condition is corrected.

## Verify packaging and record the result

The pre-export audit discovers raster pack folders automatically and requires a
source ledger; register every PNG, including rejected versions, before export.
The three legacy schemas retain dedicated hash checks. Extend the exported
renderer fixture for new runtime assets: PNG counts alone miss unreferenced assets. Run
`tools/validate_environment_export.ps1` with a fresh output name. Use the
`environment_validation` startup feature; exported templates may ignore
editor-style `--script`. Run only the executable/package from an isolated folder.

Require exact packaged hashes/dimensions, runtime loads, fixture completion and
absolute writable captures. Derive reported runtime totals from checked renderer
caches, validate each entry is a nonempty texture, and retain per-renderer counts
in the result. Keep explicit expected counts so a missing load cannot silently
reduce the reported total. Capture new habitats and dedicated small-scenery
anchors; record group names. Build the reported habitat list from completed
captures so a parallel name list cannot claim an uncaptured region. Raw-load
warnings alone prove neither outcome.
Preserve logs and executable/package hashes. Keep invariants scoped to the
original wreck kinds when concurrent gameplay introduces new categories.

Update current pack status, catalogue and bible from reviewed evidence.
Refresh `docs/ENVIRONMENT_SOURCE_INVENTORY.md` with
`python tools/build_environment_inventory.py` after ledger changes. It audits
modern source ledgers before writing; declared stages are not fresh verification.
Historical-schema packs remain linked separately without inferred identity totals.
Distinguish source, native, package, release and owner approval. Retain historical
failures without contradictory present-tense status. Update both skill copies
after comparing them so concurrent additions survive. Put reusable rules here
and study-specific observations in case notes; avoid appending duplicate rules.

## September 9 verified ground sampling correction

Large salt and sulfur motifs formed bilateral diamonds under mirrored tiling. The current shared habitat mesh maps each authored patch to one continuous source field, keeping its irregular feather mask and prop coordinates. Native source/tint comparisons and eleven-patch unique-UV checks pass; source PNGs remain unchanged. This applies to habitat fields, not connected blocker sampling. See docs/ART_FIXES_2026-09-09.md.
