# Material and scale casebook

## Seed bank directional drift — September 8

West narrowing overshot the 70-unit brief to45.36 units and reduced four packets to three. Record this as a slim construction variant with actual dimensions, not an exact reverse. East matched that silhouette at46.76 units but initially reduced four tins to two; V2 restores four. Check dimensions, inventory and latch facing independently after each redraw. Native review confirms visual scale/materials, not physical reach or opening motion. Evidence: `assets/botanical-seed-wall-v1/family.json` and the linked reviews.


## Reading knee-recess variant — September 8

The follow-up source removes the lower cabinet panel AND plinth beneath the
reading surface. Native review confirms a real transparent opening with retained
side supports. The measured85.36-unit aperture is wider than the60–70-unit brief;
record actual geometry instead of copying prompt dimensions. This resolves the
depicted solid-front problem, not occupied posture/reach or runtime collision.
Source and evidence: `assets/lounge-reading-recess-v1/README.md`.

## Reading stool group — September 8

Shared-scale review confirmed the small stool's proportion/palette beside the
reading bank, but also exposed its solid cabinet front with no knee recess.
Do not treat a clear silhouette gap as proof of seated posture or work-surface
reach. The group remains a static arrangement proposal; occupied seating needs
actual crew/host review. Evidence: `assets/lounge-reading-stool-v1/group.json`.

## Drone component subject transfer — September 8

The battery bank was labelled construction-only, but the first drone service
source still copied its pack silhouettes into the gripper tray. A targeted V2
replaced them with angular jaw components; native320-unit review confirmed the
changed subject. Inspect requested silhouettes individually even when material
and overall layout pass. Empty assembly cradle and jaw gaps are tray-backed,
not alpha apertures. Evidence: `assets/drone-component-wall-v1/README.md`.

Owner correction, 2026-09-08: props repeatedly drift toward oversized, shiny
rendering. Make this a production gate for subsequent room and prop work.
Dark color alone is not a matte finish. A clean surface is not a glossy surface.

## Before generating

1. Inspect a stable furnished reference at room scale and a relevant material
   reference. Record each reference's path/hash and what it supplies. Do not use
   the latest generated candidate as the only style master. An older approved
   composition may still contain the very shine the owner has since rejected.
2. Specify the department, material, condition, camera, intended ground footprint,
   displayed width/height and nearby crew/equipment scale. A wall-length assembly
   gains length through adjacent bays, not larger individual tools or tanks.
3. Classify the attachment: a self-supporting cabinet against a wall, a shallow
   hull fitting, or floor equipment. Never raise the low hull to fit new art.
   Record wall availability and door/chamber exclusions before placement.
   Record a fitting's visible height separately from the measured host face.
   The Crew notice rail is240×25.50 units; its shallow proportions alone do not
   establish low-hull compatibility. Uniform scaling or a source revision may
   be needed after host measurement, with readability reviewed again.
   Its follow-up uses the actual16-unit geometry constant and a131.74×14 uniform
   candidate. A native schematic proves size/readability only; strip depth is
   not evidence for front-face mounting orientation or render ordering.
4. Describe matte construction positively: powder-coated steel, rubber, fabric,
   broad quiet color planes, deliberate pixel clusters and sparse mid-tone edge
   steps. Preserve departmental palettes; matte does not mean universally dark.
5. Exclude chrome, white rim highlights, metallic sparkle, glossy gradients,
   wet sheen, bloom, product-photography lighting and dense scratch noise. Keep
   active emission separate from the static source.

## Review gates

Use `templates/material-scale-review.json` as a short per-asset record. Unknown
fields remain null; record failures as failures. Hash the exact reviewed export.

Initialize new records with the checkout's `tools/init_material_scale_review.py`:

```powershell
python tools/init_material_scale_review.py --registration assets/example/registration.json --export assets/example/asset.png --prompt assets/example/source.prompt.txt --asset-id example --width 328 --output assets/example/material-scale-review.json
```

Use `--height 328` instead for a vertical bank; the other visual dimension comes
from the registered region, not transparent margins. Optional repeated
`--reference PATH ROLE` captures reference hashes and their roles. The command
checks source hash, native export dimensions, positive scale and nonempty alpha,
then writes metadata without overwriting existing files. It never assigns visual
or owner acceptance. Fill department, condition, facing, bays, exclusions and
actual review findings afterward; metadata checks are not silhouette acceptance.
Focused tests: `python -m unittest discover -s tests -p test_init_material_scale_review.py`.

For comparison across standardized records, run
`python tools/build_material_review_gallery.py`. It writes a local HTML gallery
and export-hash audit under `output/`, with links to native evidence. Thumbnails
fit cards and are not native scale. It includes `material-scale-review.json` and
compatible per-asset `*-review.json` records, not legacy manifests or the whole
asset inventory. Duplicate export paths fail rather than inflate coverage; written
findings preserve qualifications alongside verdicts. Rebuild after adding records; hash matches do not
confer visual or owner acceptance. The initial local browser preview was blocked
by URL policy, so only file/link/hash checks were completed for that page.

For continuous banks, name `functional_bays` in spatial order. Record
unequal bay widths where the task needs them: the Battery service wall gives
inspection more room than cable storage and uses broad lower storage fronts.
Do not let a repeated equal-bay reference dictate every new composition. Record
`runtime_behavior` separately: depicted washing, nutrient mixing or diagnostics
does not establish a working simulation. The cultivation service wall records
five visually distinct bays and static, uninstalled art. This supports later
placement and interaction planning without implying functionality from imagery.

- **Source:** inspect highlights on cylinders, helmet rims, handles, glass and
  broad panels. Check each material separately. Reject shiny surfaces even if
  the overall histogram is dark. Bright-pixel statistics may flag candidates;
  they cannot decide whether a surface looks glossy.
  For ore samples, review the stones independently of the machinery. The sampling
  bank V2 replaced glittering micrograin with broad angular faces; this preserved
  three sample groups at320 units while reducing sparkle. Tools needed separate
  removal of silver edge lines in the same revision.
  For wood, inspect long golden edge lines as well as broad tabletop shading.
  Lounge reading V2 replaced those lines and reduced grain while keeping warm
  color; inspect ceramic mugs and radio knobs separately from the repaired wood.
- **Native scale:** draw with nearest filtering at the proposed display width
  over a representative room floor. Inspect against existing furnished art and
  crew scale. Do not enlarge the sprite merely to expose tiny source details.
  An isolated scale board is diagnostic, not proof of actual room placement.
  Small seating needs a separate approach/interaction check when installed. The
  Lounge stool is26 units wide; fabric detail simplifies at that scale while its
  seat and leg opening remain readable. Do not enlarge it for texture visibility.
  Review task space as well as object size: the Storage dispatch wall retains a
  clear wrapping surface beside its scale and trays. Do not fill that surface
  with extra dressing or enlarge the companion38-unit dolly to expose details.
- **Alpha:** inspect the exported silhouette on dark and light grounds, including
  enclosed hose, shelf and frame openings. An alpha channel alone proves nothing.
  Distinguish through-holes from backed recesses: the acoustic service bank's
  cable centers and headphone opening reveal solid trays/worktop, so remain
  opaque. Do not add aperture seeds solely because a shape forms a loop.
  Check long rear rails for isolated background spikes, not only exterior corners.
  Medical supply wall neutral extraction passed corner tests but retained tiny
  fragments above a straight backing. A reviewed source-space exclusion repaired
  that edge; retain the earlier registration and recheck real trim/contents. Never
  generalize that exclusion to actual protruding fixtures or different sources.
  Cryo recovery V1 also had pale/colored exterior flecks. A generated V2 edge
  repair produced a clean rail before fresh neutral registration; retained pale
  rail alpha255 was checked. Source-alpha presence is not an edge-quality pass.
- **Integration, when requested:** inspect actual wall contact, visual height,
  ground footprint, entrances, chamber access, depth and crew routes in every
  supported orientation. A horizontal front sprite is not a side-wall variant.

Repair the failed material or proportion through the image-generation editing
workflow, using the same stable references. Do not substitute global tinting,
extra grime or desaturation for a material correction. Re-register any changed
source dimensions. Preserve rejected sources and review reasons.

For registered standalone wall sprites, `tools/review_registered_wall_asset.gd`
exports source UV polygons to a true-alpha PNG and a native 1040x900 board. Pass
`--registration=res://...json --export=res://...png
--review=res://output/...png --reference-view=res://...gd --width=320` after the
Godot user-argument separator. It verifies source hash and native export size;
the reference view is optional. Run graphically, inspect the complete board and
PNG, and record your material findings. The board deliberately does not place the
candidate into the reference room. It cannot validate doors or crew clearance.

Airlock trial: V1 still rendered bright cylinder spots/stripes and helmet-glass
streaks despite a matte prompt. A targeted V2 edit reduced those to quiet stepped
planes. Both sources remain in `assets/airlock-wall-v1`; native source/export
review supports this bounded correction, not a guarantee for subsequent assets.

## Continuous improvement within each art task

The native review tool supports portrait props and full-length side banks. Fitted
overviews use a 980x310 area without cropping and may be smaller than native.
Native previews preserve exact proposed world width; assets taller than 140 units
use two 230x400 columns. Candidates beyond 210x380 in that layout are rejected;
enlarge the board rather than falsify display scale. Galley horizontal (328 wide),
west (328 tall) and meal trolley (38 wide) provide reviewed examples. Fitted
overviews never establish gameplay readability.

West galley trial: correct left backing still accompanied downward-facing drawers,
knobs and drink appliance. Audit each operator touchpoint separately. V2 corrected
handles, knobs and faucet but retained the downward coffee nozzle; a focused V3
redraw replaced it with an overhead side-tap boiler. Preserve failures and prompts.
This is verified candidate-facing evidence, not owner or room-placement acceptance.

East galley follow-up: naming each handle/control/tap position in the initial brief
produced the correct opposite-facing candidate on its first pass. This is one
observed result, not a reliability guarantee. Its darker checkerboard needed a
different neutral threshold from west. The registration helper now records
`neutral_min_channel` and `neutral_max_channel_spread`; keep these source-specific
and verify pale interior retention and exterior removal visually. Geometry equality
was checked when adding this metadata; do not rerun unrelated asset registrations.

For directional families, keep one index mapping wall side to inward direction,
backing edge, export hash, registration and separate review record. Verify links
and hashes before reporting orientation coverage. `assets/galley-wall-v1/family.json`
is the four-view example; it deliberately records candidates as not installed.
South galley V1 retained the north backing despite corrected cooker knobs, and
V2 lost a small tap. Check both structure and fixture completeness after each edit.

Repair trolley trial: a matte cabinet prompt still yielded silver spanner rims;
name the finish of individual hand tools. V2 corrected tools but returned opaque
checkerboard, including an enclosed push-handle gap. Record reviewed aperture
seeds alongside the source-specific neutral threshold, and verify both polygon
exclusion and exported alpha at the seed. A clean exterior alone is insufficient.
The trolley seed500,1117 passed these checks and native light/dark review.

Crew utility wall trial: stacked drawer descriptions generated upright facades
despite an overhead camera prompt. A targeted revision replaced them with broad
overhead cabinet tops, side-by-side vent panels and shallow bottom drawer lips.
This preserved low equipment and readable folded fabric at328 units. Specify
surface proportions in storage briefs; correct handle direction alone does not
prove the projection matches the game's camera.

Heat Recovery wall trial (2026-09-08): repeated rounded ribs retained reflective
pinstripes after a generic matte edit. A targeted plate-fin design with broad
flat slats removed the repeated bright rib pattern at native scale. Simplifying
fabric insulation separately reduced photographic grain. Preserve both failed
sources and the changed construction brief (`assets/power-wall-v1`); do not claim
the successful design substitution was a material-only edit or a pixel lock.
For compact exchangers, specify the intended flat plate construction up front
when it fits the equipment, rather than repeatedly requesting darker shiny coils.

Laboratory wall trial (September 8): a material-only edit reduced the bright
specimen-chamber reflection but changed true-alpha RGBA into opaque RGB with a
checkerboard. Recheck mode and exterior pixels after every edit, even when the
input had alpha. Preserve both sources. In this case exterior-neutral vector
registration at 195 isolated one continuous silhouette, and the native exported
PNG passed visual review on light/dark grounds. That threshold is source-specific;
it is not a default for pale equipment or checkerboards with different values.
Record material correction and alpha recovery separately in the review template.

Crew linen follow-up: darker checkerboards had neutral cells near 100-130, so
the earlier laboratory threshold could not be reused. Inspect actual exterior
pixels and resulting silhouette bounds before choosing a source-specific value.
Neutral100 plus a reviewed handle-hole seed worked for this pair; verify pale
fabric retention as well as removed background. The original hamper had true
alpha, its matte-frame edit did not. Keep the raw revisions and never infer alpha
from the input or preview appearance. See `assets/crew-linen-wall-v1`.
The Quarantine preparation source needed neutral90 for darker exterior cells
measured down to93. Its basin and garment were checked as retained alpha255 after
export. These values are evidence for those sources, never shared cleanup defaults.

At a substantive milestone, record owner corrections, the observed defect,
the specific prompt/reference/registration change and evidence from the result.
Update the maintained project skill and relevant bible section, then compare and
sync only the changed skill files to the installed snapshot. Keep executable tools
in the project. Consolidate repeated lessons here instead of appending contradictory
defaults to multiple files. Do not promote agent-reviewed candidates to owner-
accepted references or call guidance proven before visual comparison.

This is an ongoing habit during authorized art work, not a scheduled background
job or permission for unrelated bulk asset revisions.


## Fitted-interior reference roles

Airlock side-bank trial: a long portrait shape can be a vertical stack of frontal
equipment rather than a floor-depth view. Reject that projection even when the
backing edge is straight. Explicit top-surface dominance plus a geometry-only
side-wall reference produced a useful low packed-suit/tank bench. This changed
the design from hanging lockers; record it as a companion design, not an exact
alternate view. Review openings, valves, couplings and helmet visors individually
for inward access, then compare both directions at equal length. See
`assets/airlock-side-wall-v1` for rejection and native evidence.

Tall sprites need both a full-length scale view and readable material detail.
The native review tool now splits portrait banks into top/middle/bottom diagnostic
panels with uniform scaling; it does not enlarge the actual-scale comparison to
make detail visible. Horizontal source export remains pixel-identical in the
bounded Reactor regression. A diagnostic source section boundary is not an asset
seam or a separately usable cutout.

Reactor/Loom source pass (2026-09-08): review material hotspots by component,
including pipe caps and control handles, even when broad panels already pass.
Reactor required a targeted correction. For precision-service walls, vary the
silhouette through supported task objects and useful working heights: Loom's
probe, raised instrument column and open case distinguish it from a flat console
row. Keep overall depth/height budgets modest. A pale worktop or ceramic reference
ring can remain matte; do not normalize it to Engineering charcoal. See
`assets/reactor-loom-wall-v1` for source and native evidence. Rings backed by a
tabletop and foam-lined cases are opaque artwork, not alpha holes.

For the owner supplied September 8 interior images, read
`docs/ROOM_REFERENCE_DIRECTION_2026-09-08.md` in the checkout. Use them for
functional bay sequences, tactile interfaces and inhabited material contrast.
Do not copy their camera, ceiling geometry or bright lamp density into gameplay.
Review room identity separately from construction consistency: the same repeated
cartridge-bank/console pair is not a distinct functional design. Wall length comes
from adjoining human-scale bays; preserve matte finish and restrained indicators.

For operator-side projections such as the salvage workbench vise, record the
protrusion in placement exclusions. Native cutout review can show that the handle
survives export, but only actual placement can establish working and walking
clearance. Cabinet backing alignment alone does not establish a clear operator edge.

Specimen carrier: alpha registration retained the dark inspection window while
opening the handle gap. Pair one transparent-aperture sample with one retained
interior sample after export; dark glass is not background. At 28-unit width the
case silhouette survives but tube details simplify. Record that limit instead
of enlarging a portable object for detail. The metadata initializer was used
before adding these actual visual findings, keeping its verdicts unset until review.

Emergency wall visor trial: a broad matte-glass correction subdued the frame but
left pale visor streaks. Restricting the next edit to the two visor interiors and
requesting flat charcoal removed them. Preserve outline, hoses and straps while
correcting the failed surface; native review then checks that dark masks still read.

Cargo packing candidate: the generator depicted open dispatch trays although the
brief requested sealed bins. For incidental furniture variants, record the actual
configuration and review it on its merits; never copy prompt claims into metadata.
If open/closed state controls gameplay or was an explicit owner requirement, repair
the mismatch before acceptance. Here no logistics behavior or state was installed.

For loaded carts and carriers, record `depicted_state` separately from runtime
behavior. The cargo dolly depicts one strapped parcel; no empty view or unloading
animation exists. Do not reuse loaded art for empty gameplay states by assumption.
Include wheels and projecting handles when establishing later placement clearance.

For state pairs, compare native canvas and registered bounds, not just apparent
similarity. Cargo dolly's empty edit kept its canvas but grew1 source pixel wide
and3 high. `assets/cargo-dolly-v1/states.json` records that drift and a proposed
shared region. A later native/2x shared-crop comparison passes static review with99.1% binary silhouette overlap and0.05x0.15-world-unit bounds drift; see state-silhouette-review.json and state-review-group.json beside the index. Actual runtime switching is still unverified. Avoid independently
tight-fitting states during integration, which can shift or resize a shared frame.


Tidal matching pass: the owner selected the repainted Tidal room as the material
and wall-quality reference. For atlas-based rooms, inspect structural wall UV
samples as well as furniture: replacing a wall installation alone can leave bright
old wall caps and auxiliary instruments. Repaint the donor at its actual native
dimensions, preserve UV coordinates, then inspect the native hull, riser end returns
and foundation together. Clone Lab inherited another room's wall material; its
local wall draw now samples its own repaint without changing hull geometry.
Plain-neutral output can be integrated through read-only silhouette registration,
but explicitly review enclosed pipe/handle gaps. Retain gauge faces and backed
recesses. Reference quality, alpha/registration, geometry and native acceptance
remain separate gates; successful source generation does not complete a full set.

For companion furniture, use `tools/review_prop_group.gd --group=res://...json --review=res://output/...png` to compare registered exports at shared world scale. The operator-stool `group.json` demonstrates export hashes, source regions, widths and relative positions. The board shows native and 2x diagnostic views; neither establishes occupied crew space or collision. Include stool footrests in later clearance checks and let fabric weave simplify at native scale instead of enlarging the seat.

Pressure-seal maintenance trial: gauge faces may stay pale while rims and wrench heads need separate matte corrections. Recheck image mode and canvas after every edit: V2 introduced a baked checkerboard despite a transparency-preservation prompt. Register the new source independently, and preserve the opaque backing inside O-rings and test windows; their dark centers are not through-holes. Native-scale review also checks that repair mats retain usable empty area.

Group-preview guardrails: source regions must fit the export canvas and the complete arrangement must fit both panels (currently490x150 world units). Increase the board for larger groups; never falsify display scale to bypass clipping. Reject empty entries and nonnumeric positions before rendering. Run `python tests/check_prop_group_review.py --godot PATH` after changing this tool: its eight graphical cases include clipping and export-overwrite rejection, with a valid board requiring visual review.

Portable-case trial: reject a surrounding glow even when the object materials are usable. A targeted edit can remove halo and excessive chipped-edge loops together while preserving the closed-case identity. Re-register the edited silhouette and explicit handle aperture; do not reuse the first revision's mask or presume an unchanged canvas. Keep portable cases modest and record closed state separately from inventory behavior.

Water-assay faucet trial: a material-only repaint retained the rounded spout's bright center. A targeted flat-sided replacement removed that highlight while retaining the outlet direction and basin. Where the exact hardware shape is incidental, a local geometry change can resolve repeated material failure; record it as a shape change, then recheck facing, silhouette and native scale. Preserve broad preparation areas between task zones.

Archive restoration trial: even an explicit subject-only role did not prevent older archive trim from influencing the first candidate. A targeted all-trim/bolt repair reduced metallic outlines while preserving pale paper labels. Inspect material transfer from every supplied reference; role declarations do not isolate style automatically. See `assets/archive-restoration-wall-v1` for preserved revisions and native review.

Water-assay south trial: reversing the backing and faucet left analyzer and case access facing outward. V2 shows the analyzer rear housing with a foreshortened north display strip and puts case latches north. Inspect each fixture independently; accept reduced screen visibility when the fixed camera is behind the instrument. North/south family evidence is in `assets/water-assay-wall-v1/family.json`; side views remain absent.
# Botanical seed bank: background/material collision, September 8

`assets/botanical-seed-wall-v1` V1 used dark checkerboard beside pale low-chroma
sage corners. Neutral95 removed exterior but also cut valid cabinet edges. V2
requested a plain white exterior; neutral228 then preserved full corners in native
review. Do not lower a universal threshold until it consumes similar-colored art.
The generated background repair redrew details; source and geometry revisions remain
separate, with no pixel-lock claim. This reinforces the existing alpha visual gate.

## Seed bank actual host study - September 8

The slim45.36 by320 west bank still overlaps three retained Hydroponics props at the hull edge. An open west wall also crosses its central72-unit doorway. Small native scale is not sufficient for placement. Inspect an overlay on the actual configured room with its furniture retained, including closed and open wall cases. Use overlap results to author split sections or choose another host; do not hide furniture merely to obtain a passing screenshot. Evidence: output/seed-bank-host-study.png and JSON.

## Short seed section - September 8

A short module should redistribute task bays, not scale the whole long cabinet down. V1 sorting-only section was too narrow at28.43 by136; V2 provides55.24 by136, still wider than the45-unit brief. Keep measured size explicit and reassess host fit. A136-long section starting at-184 stops at-48, twelve units before the72-unit central door bay. This proves only axial separation, not furniture or crew clearance. Evidence: assets/seed-sorting-west-section-v1/README.md.

## Short storage companion - September 8

Seed storage V1 had bright repeated lid rims; V2 reduces those and flattens broad shading. Native finish passes, but actual depth67.84 differs from sorting55.24 at equal136 length. Matching references and a material pass do not establish matching module depth; keep this difference visible before paired host review. Evidence: assets/seed-storage-west-section-v1/README.md.

## Split seed bank host result - September 8

The two136-unit sections leave96 units between them at y=-184 and48, clearing the72-unit door bay by12 units per end. The sorting section still overlaps crops; storage overlaps nutrients and harvest stand. Report doorway and furniture findings separately: splitting resolves the former without resolving the latter. Evidence: output/seed-sections-host-study.json and PNG.

## Seed section relocation proposal - September 8

Keeping all six Hydroponics furniture IDs, moving crops68 units right and nutrients/harvest stand96 right clears seed rectangle overlaps and moved-prop visual-bound intersections. Native overlay confirms separation. This applies only to west-open/other-walls-closed configuration; do not infer north-door compatibility, crew reach, service connectivity or runtime integration. Retain original and proposed inventories in evidence. See output/seed-sections-relocation-study.json.

## Seed carrier handle aperture - September 8

The small carrier has an enclosed white opening beneath its north handle. Exterior flood alone does not remove enclosed background; register the reviewed source seed700,240 and verify zero alpha there after source-UV export. This proves the aperture, not a folded handle or carry pose. Evidence: assets/seed-packet-carrier-v1/README.md.

## Seed carrier simultaneous support - September 8

Carrier group retains the existing propagation tray instead of reusing its occupied position. At shared world scale, carrier24 wide at187,17 and propagation tray28 wide at81,17 leave the central sorting tray clear. Check companions together and include protruding handles/latches in support silhouettes. Static support does not establish hand access or lifting. Evidence: assets/seed-packet-carrier-v1/group.json.

## Parts-cleaning bank - September 8

Dry charcoal basin avoids reflective liquid as a default static material. V2 corrected the reference-copied nut to a washer, but retained some muted bottle shoulder facets: record actual material outcome rather than claiming every prompt edit succeeded. Drain and washer holes sit over opaque backing, unlike the carrier handle aperture. Evidence: assets/parts-cleaning-wall-v1/README.md.
