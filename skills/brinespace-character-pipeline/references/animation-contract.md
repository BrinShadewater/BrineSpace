# Animation contract and packaging

Inspect `character/dr-veld-v1/final/manifest.json`, the pack README, and the actual
consumer before writing a new contract. Bill and Veld are examples with different
coverage, not mandatory frame-count targets.

## Record the required data

- Stable character/version ID and canonical reference/source paths.
- Canvas dimensions, foot pivot, intended standing scale, alpha/palette policy.
- Required states and directions, ordered frame paths and counts, per-frame
  duration, loop/one-shot behavior, and action meanings.
- Transition chains and compatible endpoints; locomotion stride distance where
  the player advances frames by movement rather than elapsed time.
  A full state/direction key may override the state-wide stride when authored gait
  reach differs; consumers must retain the state-wide fallback for other clips.
- Source hashes, authoring method, exact prompts for generated sources, build
  settings, and derived/mirrored/reversed-frame provenance.

Extend the current manifest deliberately when needed. Do not replace a working
schema with a generic engine export example. Keep playback metadata authoritative
in one place and derive exported timing and previews from it.

Legacy humanoid profile: 92 × 92 canvas, (46, 86) foot pivot, 74-pixel standing
height, 64-color base palette, binary alpha. Bill's selected `major-bill-v3`
declares standingHeight 148, with canvas/pivot profiles appropriate to each pose.
Inspect `character/ACTIVE_ASSETS.json` and the active loader before selecting a
reference or calibration. Keep legacy profiles for compatible crew. Do not
stretch individual poses to equal heights or center each frame independently.

Veld uses four-direction idle/walk, east-facing scanner interaction, and
idle → kneel → repair/sample inspection → stand → idle. Her 12 clips contain
72 frames. Bill's original base had 17 clips/102 frames; his complete selected
library has 175 bare states/1,134 frame references and 168 equipped states/1,080
references, including runtime joins. These are coverage counts, not unique authored
pose counts. Generate states needed by the requested controller, not the union of both.
Six frames per clip is a current choice, not a smoothness requirement.

Cryopod lesson (September22): a gameplay wait and a physical exit need separate
timing. Hold the closed/thawing pose, then play the short exit from saved wake
progress; do not stretch a handful of exit poses across the whole thaw timer.
Review the actual display clock: the core subtracts its power-up stage before
passing wake/duration to the shared pod renderer. Verify release and pause/save
behavior separately from pose pacing. Retiming is not newly authored in-between
coverage. A populated action catalog also does not prove readable actions or
consistent source detail across directions.

Cryopod handoff (September23): the empty pose must keep the exit pose's housing,
lid, canvas and anchor. Switching to an unrelated closed equipment crop at release
caused a snap despite correct exit timing. Spent human pods now stay open, driven
by existing saved recovery state; no extra timer is needed. Preserve visible lid
pixels while reconstructing concealed padding. Rebuild with
`python tools/build_cryo_open_pods.py`; source and exact prompt are in
`character/cryo-open-study-2026-09-23/`. Check native pause/Continue and the actual
paid-release handoff separately from asset/manifest coverage.

For a one-knee transition, register the planted boot against that same boot in
the standing endpoint. A two-foot midpoint is not a single-boot contact anchor:
centering either one at the pivot can move the whole torso sideways. Preserve
actual idle endpoints and exact kneel/action/stand joins, and calibrate head/body
proportions before promotion. Reject source sheets that skip descent stages even
when they contain the requested number of cells. See the Branforth south repair
integration dated September22 for the selected example.

## Production and revision

Prove representative poses and timing early. Inspect opposite views rather than
assuming mirroring is safe. Share compatible endpoint frames when it improves the
intended transition; reverse a kneel only if the resulting stand motion is credible.
Record reused frames so an export count is not mistaken for a generated-source count.

Preserve accepted regions/rows during repairs. Retiming an existing motion does
not necessarily require new art. Treat repeated identity drift or expensive pose
retakes as evidence to propose a different authoring method, not permission for
an unsolicited pipeline migration.

## Existing tools

From the checkout root, the selected complete Bill rebuild and read-only check are:

```powershell
python tools/rebuild_bill_art.py
python tools/validate_bill_art.py
```

The first writes the new revision from preserved sources; the second checks it.
The original native migration inventory is frozen in
`tools/bill-art-source-contract.json`; do not replace it with a dump of the new
consumer. The historical base-only rebuilds below do not update the selected Bill
revision:

```powershell
python character/dr-veld-v1/build_pack.py
python character/major-bill-v2/build_pack.py
```

These commands write the corresponding pack outputs. Use them for that pack's
authorized rebuild, not as read-only validation. They require Pillow and NumPy.
Veld's builder imports Bill's helpers; inspect that dependency before adapting
it. For a new character, give the builder its own source/output root so it cannot
overwrite Bill or Veld. Do not refactor game architecture to create a pack.

For a single-clip repair, note that the current Veld builder processes the whole
pack and recomputes its shared palette: one changed source can alter accepted
clips. Preserve the accepted palette/unrelated frame pixels or account for an
explicitly intended pack-wide change. Its `--partial` option skips missing sources;
it is not a selector for one animation. Verify affected and unaffected outputs.

When `sprite-animation-maker` is installed, locate its directory from the skill
catalog and run its existing validator:

```text
python <sprite-skill>/scripts/validate_sprite_manifest.py --manifest <pack>/final/manifest.json
```

Check its actual supported schema/options when adapting inputs. If unavailable,
perform equivalent image/manifest checks with project tools and identify that
the generic validator was not run. Do not assume a tool's success proves checks
outside its documented coverage.

Preserve sources, cleaned frames, strips/atlas, manifest, requested Godot resource,
contact sheet, and motion previews. Keep script/UID pairs and project LFS rules.
For Godot SpriteFrames conversion, durations are relative to animation FPS, not
milliseconds; verify absolute playback timing against the manifest. Existing raw
PNG consumers also need verification even if a generated `.tres` loads correctly.

Bill's mixed limb-surface repair was rejected for disjointed feet. base_frames()
preserves connected original poses; repair_walk=True is historical comparison
only. East and west now select independently authored alternating whole-pose
recipes through build_bill_alternating_east_walk.py and
build_bill_alternating_west_walk.py in the canonical rebuild. build_bill_connected_walk.py exports both selected recipes, and the normal
repair_bill_walk.py CLI delegates to it. Each uses its own per-pose helmet fitting.
Retain historical sources/helpers without silently reinstalling them. Frozen
source/decoded hashes and the review-command parity test protect the selected art;
owner gait acceptance and complete contact review remain separate.

Archived provenance is still a build dependency. The construction source folder moved under archive/; use the narrowly scoped source_path resolver in rebuild_bill_art.py and retain frozen hash checks. Do not silently regenerate missing originals or rewrite their contract from current outputs.

South Bill kneel/repair/stand now rebuild from sources/south-actions-style-2026-09-21
through build_bill_south_style_actions.py; the previous south helper is historical. Review adjoining actions as one sequence:
equal height/pivot metadata did not prevent the old action sheet's face/suit mismatch.
Match work endpoints and retain the supporting body while repairing tool motion.
Inspect anatomical boot contact separately from actor foot coordinates; a fixed
controller anchor concealed a seven-pixel source-pose slip. Preserve intermediate
registrations and verify selected outputs against the reviewed candidates.

North action repair uses the same endpoint principle with independently authored
back-view sources. When shifting a planted limb locally, preserve the stationary
foreground limb at overlaps; moving a masked limb over every destination pixel can
erase the folded knee. Compare anatomical contact across all poses, bare and equipped,
and record direction-forced native captures as rendering evidence rather than
autonomous-facing behavior. Selected recipe: build_bill_north_actions.py.

For side-facing action sheets, extending a tool arm changes the whole-sprite bounding
box. Register the planted boot before diagnosing limb deformation; bounding-box
centering moved Bill's west body sideways even with a common scale. Preserve the
recorded contact band and offsets, check that registration clips no pixels, and
review the torso/boot relationship across the lowering arc. West source recipe:
build_bill_west_style_actions.py (the earlier build_bill_west_actions.py is
historical). Opposite views remain independently authored.

South action standing endpoints now use frozen canonical idle pixels at the action
pivot, verified against live idle. Preserve the original146-pixel opaque height
when calibrating generated source scale; standingHeight148 is a runtime contract,
not the exact opaque bounding-box height. Fixed work anatomy is preserved outside
a hand/tool mask. Do not replace connected source legs with independently scaled
boots to satisfy contact metrics.

Bill authoring sources remain required locally for reproducible builds but are
excluded from broad release discovery. Explicit runtime references override that
exclusion. Do not assume sources/ always means disposable: other actor manifests
reference real frames there. Preserve sources and distinguish collector closure
checks from actual packaged playback acceptance.

Alternating gait gate: connected boots do not prove a complete two-step cycle.
Trace the same foreground knee and boot through contact, passing and opposite
contact before slicing or fitting equipment. Bill's eight-frame source requests
repeated the same half-cycle even with opposite-contact references. An isolated
opposite-contact pose worked, but expanding it into a row did not. Retain rejected
sources and move to individual missing poses instead of treating frame count or
prompted stage names as proof. This is observed authoring guidance, not a measured
skill evaluation or a claim that the staged source is ready for gameplay.
Individual Bill passing-pose requests produced the two support-leg relationships,
but a subsequent reach request swapped leg ownership again. Review every pose;
success on an isolated contact does not certify its derived frame. Native four-key
studies can test anatomy and playback without becoming the final frame count or
timing contract. Keep knee-lift amplitude and character detail as separate gates.
For independently authored full-body poses, preserve a common physical source
scale and register a stable head band/sole baseline; bounding-box centering shifts
the torso when a boot or arm extends. Apply candidate bindings after fixture room
setup, then check the actual render getter during motion. An initially loaded
texture table alone is weaker evidence. Bill's six-pose west study passes these
native checks but still differs from idle/work in lower-body detail; do not let
playback success erase that visual limit.
When a generated surface-detail edit has useful shading but changes unrelated
pixels, a recorded RGB-only mask can retain the reviewed body's exact alpha and
upper body. Use overlapping opaque pixels, verify the registered alpha as well as
source alpha, and review internal knee/boot contours. This preserves the silhouette,
not automatically the anatomical interpretation or full-cycle consistency. Bill's
down-B study establishes this only for one staged pose; previous native checks do
not transfer to a newly edited frame.
Before candidate native review, check the selected library's actual alpha contract.
Bill's validator requires only0/255; Lanczos-resized authoring previews may retain
partial alpha even after source fringe cleanup. Finalize the candidate with the
required threshold, preserve the soft study separately, and re-review the final
bare/helmet pixels. Hash source inputs and decoded final outputs so the maintained
rebuild reproduces the reviewed artifact, including any surface-detail mask.

For independently authored side walks, trace the near thigh strap and support leg
through both contacts and both passing poses. An apparently varied six-frame sheet
can repeat the same leg ownership. Preserve rejected source cells and record each
replacement explicitly. East uses its own directional gear and authored 46x56 registration canvas, not
a mirror of west or its 48x56 canvas. The owner-requested smaller shell policy
below now controls visible helmet size within those canvases. Hard-threshold source alpha before
resampling when generated glow inflates bounds, then finalize binary alpha and
verify decoded output hashes. This does not prove world-space foot locking.

When reviewing locomotion turns, distinguish preserved clock fraction from matched
anatomical phase. Exercise all ordered facing pairs at several cycle fractions,
then inspect contact/down/passing order in the selected art. Silhouette bottom
extents can flag inconsistent phase grouping but do not establish foot contact.
Try a source-preserving order study before creating new limbs for an ordering defect.

Bill south walk now selects order [0,4,5,3,1,2] after the base/equipment rebuild.
Use build_bill_south_walk_order.py and its frozen original RGBA hashes; do not
reorder base extraction before helmet composition or alter historical source art.
The recipe preserves all six whole poses exactly once in both variants. Frozen
source copies and expected hashes distinguish a permutation from pixel edits.
Contact slots 0/3 remain unchanged; only four slots per variant change.

For north/south motion, do not register each pose to its lowest boot while
evaluating foot depth: this can erase the support-foot progression. Keep a shared
scale and canvas registration, then identify anatomical toe contact separately
from lifted-heel silhouette. A better passing pose does not justify a different
backpack/body silhouette. Record motion-only drafts as unselected when identity
or stance travel remains unresolved; do not fit stride to opaque bounds alone.

Bill north now selects build_bill_north_walk.py: original canonical upper-body,
arm and helmet pixels are retained under recorded per-pose vertical translations;
a single connected pelvis/leg region is transferred from the motion study and
quantized to the original palette. No knee/shin/boot transforms are applied.
The whole-body generated drafts remain rejected for identity. Test preservation
against the translated canonical frame, verify every replacement pixel connects
through the waist to the torso, and retain independent original/motion/output hashes.
This improves pose differentiation at unchanged speed/stride; it is not full
anatomical foot locking. Compare the cast before imposing a new motion standard.

Owner update: Bill helmet was too large overall. Selected normal shells now cap
at48source pixels high (about14percent below the prior56), with41pixel width for
front/north/west and39for east. HelmetRebaker(max_height=48) preserves the authored
registration canvas and scales only shell artwork about its visor anchor. Already
compact fits remain unchanged. Canvas dimensions are not visible shell size.
The canonical rebuild verifies historical recipes first, then recomposes selected
equipment with the new fit. Preserve south idle/action endpoints, south walk order
and north canonical-upper registration in this final pass. Default historical
helpers remain reproducible; review commands must explicitly use the selected fit.
Six walk tests, work-shell/compact-fit tests and171paired native bare renders guard
body preservation and consistent equipment. Selected-fit hashes are frozen under
sources/helmet-size-2026-09-21. No head/body scaling or Higgsfield is involved.


### Standing action identity (September 21, 2026)
North/west kneel0 and stand5 now use the selected idle body/equipment pixels,
aligned by profile pivots in the final canonical rebuild pass. Current 184 -> 256
canvas offset is (36,52); derive this from metadata, not canvas bounds. This removes
the fully standing wardrobe change but does not harmonize moving work suit or
backpack shapes. Preserve that distinction in acceptance claims. Exact endpoint
pixel tests complement contact checks: canonical west idle starts two source
pixels behind/one above the independently authored lowering contact. Do not shift
canonical idle just to preserve an obsolete generated-pose bounding box. Native
full-sequence review remains required. Historical gear hash freezes predate later
endpoint selections; retain each dated selection rather than rewriting history.

Furniture boarding may change depth inside a single action. CrewSpritePlayer's
optional furnitureFrames array supplies one marker per frame (empty = ordinary,
bunk = interior); it overrides the whole-clip furniture marker. Reverse both the
markers and pose timing for exit. Malformed overrides stay outside furniture.
Prove actual-player boundary samples and native parity after removing fixture-only
metadata mutations; this establishes renderer integration, not NPC save/arrival
or complete animation acceptance.

For profile repair, preserve canonical face/helmet pixels when a new motion source
changes age or identity. Keep the generated body's anatomical scale fixed and
check the neck/shoulder seam. Inspect actual source bounds before equal-grid
slicing: Branforth west's top-row boots cross the nominal row midpoint. Record
explicit crop/boot windows. Repeated settling poses and reversed tool motion are
valid derivations, but report unique poses honestly rather than claiming new
in-betweens. See BRANFORTH_WEST_REPAIR_INTEGRATION_2026-09-22.md.

Check the controller meaning before replacing a generic action: Marsh's legacy
kneel/repair/stand names represent equipment maintenance, separate from welding.
His selected maintenance chain reuses authored diagnostic draw/check/stow poses
through an explicit state override. Never replace shared old weld source paths:
unrelated eating and other aliases still refer to them. A powered service is a
fixture precondition; an unpowered maintenance interruption is intended behavior.
Audit requested transition keys through the production player: a non-null ordinary
movement fallback proves texture availability, not authored transition coverage.
See MARSH_MAINTENANCE_REPAIR_2026-09-22.md.

For gait comparisons, report the effective cycle from strideDistanceCells and
actual world speed, not only frameDurationsMs: production locomotion is driven
by distance. Render selected catalogs through independent players, normalize using
declared standingHeight/pivot, and move the ground reference at the corresponding
scale. Same cadence does not prove anatomical contact or owner acceptance; do not
change NPC speed merely to make differently authored clips look identical.
