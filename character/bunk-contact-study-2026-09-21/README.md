# Compact bunk endpoints - staged study

Updated September 22, 2026. These are not bound into runtime catalogs.

The original Veld and Branforth sleep-east sprites put boot pixels outside the
bought bunk frame after pillow alignment. New built-in image-generation sources
bend the knees while retaining torso/head density. No Higgsfield or API CLI used.
Exact prompts are veld-prompt.txt and branforth-prompt.txt; raw RGBA sources,
processed endpoints and extraction recipes are preserved alongside this file.

Rebuild from the project root:

    python character/bunk-contact-study-2026-09-21/build_study.py

The builder scales each complete source uniformly by 0.16 using nearest sampling,
registers the head on the existing 256px canvas/pivot, maps to its canonical sleep
palette and thresholds alpha. It does not replace or modify any runtime source.
validation.json records deterministic rebuild, binary alpha, zero transparent RGB
and no border touches. PNGs use repository LFS attributes.

Both lower-bunk native captures visually fit behind the ladder at the saved q3
layout scale. Source poses and native contact were reviewed; this does not prove
connected transitions or equipment compatibility. Existing lie-down intermediate
frames were inspected and straighten their knees toward the old endpoint. Do not
append these new endpoints and claim animation acceptance without repairing that
motion. No upper-bunk interaction is approved or installed.

Native fixture: output/layout-default-audit-2026-09-21/bunk-fit.gd with
--actor=veld or --actor=branforth plus --masks --nearest --head-fit --compact.
Evidence: bunk-fit/compact-before-after.png and lower-nearest-masks-head-fit-
compact-{actor}.png under that audit directory. Runtime registration, foreground
splitting, connected entry/rise, gear variants and controller validation remain.

## Veld lowering study (September 22)

veld-lowering-source.png and veld-lowering-prompt.txt preserve a built-in generated
three-pose strip: elbow-supported lean, lower shoulders, compact sleep. Rebuild with
`python character/bunk-contact-study-2026-09-21/build_lowering.py`. One uniform 0.22
scale and reviewed source hip anchors produce three 256px frames at hip (122,219).
The staged manifest uses 300ms holds, reverse-derived rise and the sheet's own final
pose for sleep, avoiding a last-frame jump to the separately generated endpoint.
The original standalone endpoint remains preserved as a reference/candidate.

The fixture's --lowering option samples the real CrewSpritePlayer. Fixed final-bed
position failed visual clearance: initial head intersects the upper bunk. With
--edge-tuck, entry starts 12 world units forward at the lower mattress edge and
moves inward over the first 0.6s; rise reverses this. Three pose contacts now fit
beneath the upper rail in native inspection. This is a staged three-key-pose study,
not proof of a smooth complete entry or a controller implementation.

Evidence: 19 native samples per variant, logs bunk-veld-lowering.log and
bunk-veld-edge-tuck.log, contact sheet bunk-fit/veld-edge-tuck-contacts.png and
GIF bunk-fit/veld-edge-tuck.gif in output/layout-default-audit-2026-09-21.
Both native runs exited 0 without script errors. Three-frame rebuild is byte
reproducible. The GIF is native captures, 100ms/sample, no optical interpolation.
Remaining: standing-to-seat approach/ducking, motion refinement, Branforth's
transition, gear, runtime rendering and controller checks. Do not call this a full
floor-to-bed transition or replace any current generic sleep animation with it.

## Installed renderer support (September 22)

Crew Hab now splits the bought bunk into cached back/foreground texture masks in
both direct and retained queues. Staged lowering states mark furniture=bunk; the
player supplies crew_bunk_layer. Only these opt-in poses receive bed-interior depth
for a nearby unmirrored bunk. Generic poses retain old depth. The lowering fixture
now works without --masks. This installs rendering support, not sleeping behavior,
a runtime art binding, or finished standing-to-seat animation.

## Veld full entry candidate (September 22)

veld-entry-source.png and veld-entry-prompt.txt preserve the new built-in source.
Run build_entry.py after build_lowering.py to reproduce seven staged frames and
1.84s entry/reverse-exit manifests. Exact canonical idle is padded onto the 256px
canvas; three source poses use one 0.22 scale; the selected lowering sequence
supplies the last three frames. The source's fourth pose is retained but omitted
in favor of the selected lowering start. No generic/runtime catalog art changes.

The fresh production-graph probe checked all four cast members at six front gaps.
At the selected point (125.2307,-36.00349), each actor can stand, route from a room
center node and traverse the final segment. This is geometry evidence, not an
actual walk/chooser test. An earlier 8-unit candidate is blocked; the probe now
checks missing graph IDs rather than logging invalid path calls. Final clean log:
output/layout-default-audit-2026-09-21/bunk-entry-right-probe.log; numeric results
in bunk-entry-right-probe.json. The user's actual saved q3 layout was read only.

The --entry fixture renders 47 native actual-player samples with installed bunk
layers. First review caught a disconnected shin: one-leg-lift pose was prematurely
placed behind the rail. The corrected study draws frames 0-3 in front, frames 4-6
between bunk layers. The manifest now encodes that switch in furnitureFrames; the production player
reads it, and the fixture no longer assigns per-frame flags. choreography.json preserves anchors,
phase intervals and the 16-unit edge-to-rest tuck. Existing three-pose study used
12 units; this full entry candidate supersedes that contact timing only.

Seven-frame rebuild, binary alpha/borders, exact canonical idle and native first/
last framebuffer equality pass (validation.json). Revised hanging-leg native
capture was inspected. Final log: bunk-veld-full-entry-final.log. GIF:
bunk-fit/veld-full-entry.gif (47 real captures at 80ms each). The earlier contact
sheet records the rejected shin layering; it was deliberately not overwritten.

Still staged: visual smoothness/owner acceptance, equipped coverage, Branforth
entry, cast-specific behavior, NPC station selection, save/interruptions and live
travel. No claim of complete bunk integration or final animation acceptance.

## Per-frame contact metadata installed (September 22)

CrewSpritePlayer accepts furnitureFrames with one marker per frame: an empty string
keeps ordinary depth; bunk selects interior layering. This overrides the optional
whole-clip furniture field. Malformed array length/type or unknown markers remain
outside furniture instead of silently inheriting interior depth. build_entry.py
writes the switch in both forward and reversed order.

Tests: test_sprite_furniture_metadata.gd passes 30 checks headlessly, including
real entry/exit playback at the hanging-leg boundary, whole-clip compatibility and
negative controls. Native fixture without manual flags matches all 47 previously
reviewed captures byte-for-byte. Logs: sprite-furniture-metadata-final.log and
bunk-metadata-native.log under output/layout-default-audit-2026-09-21/. No NPC
activity binding, equipment or packaged verification is implied by this milestone.

## Equipped entry/exit study (September 22)

build_equipment.py fits the existing canonical east helmet overlay (30x32) to the
seven entry poses, with recorded head centers/angles and an exact padded canonical
equipped idle. Source hair protruding through tilted shells is tucked inside the
equipped silhouette; the authored visor opening remains clear. Only recorded head
boxes are cleaned, and all bare frames are unchanged. No generation was used.

veld-entry-helmet/ contains seven PNGs, a precomposed manifest with matching timing,
pivots and furnitureFrames, the source/fit recipe and validation.json. The normal
load_equipment_manifest path accepts it. Fifty-two sprite furniture/equipment checks
pass, including matching per-frame depth and reverse pose samples. The complete
47-capture native equipped entry/exit returned to its first frame exactly; canonical
equipped idle pixels are identical, rebuild is deterministic, alpha is binary and
no frame touches a canvas border. Native leaning/rest fits were reviewed beneath
the upper bunk. GIF: output/layout-default-audit-2026-09-21/bunk-fit/veld-equipped-entry.gif.
Logs: sprite-equipped-metadata.log and bunk-equipped-native-final.log in that audit
directory. Earlier helmet-head-review images preserve the diagnosed hair protrusion.

This covers staged entry/exit equipment only: no runtime catalog or controller
binding, looping sleep/equipment behavior, NPC travel, checkpoint acceptance or
other cast completion is implied. Continue profile integration and full acceptance.


## Runtime integration (September 22)
The staged-only limits above describe earlier milestones. Veld now has runtime
bare/equipped entry, sleeping hold and exit via tools/build_veld_bunk.py and her
NPC contact profile. See docs/VELD_BUNK_INTEGRATION_2026-09-22.md for current
controller, disk-restore, visual and deterministic-rebuild evidence. Other cast
profiles, full expedition and packaged acceptance remain open.


## Branforth full bare entry candidate (September 22)
branforth-entry-source.png preserves the built-in generated six-pose sheet and
branforth-entry-prompt.txt the exact request. build_branforth_entry.py extracts at
uniform scale and adds exact canonical idle. branforth-entry/ records recipe,
manifest, choreography and validation. The 47-frame native study fits the bunk,
returns to identical idle and keeps hanging limbs in front of the rail. Equipment
and runtime controller integration remain open; see docs/BRANFORTH_BUNK_MOTION_2026-09-22.md.


## Branforth installed equipment/controller (September 22)
The preceding staged-only milestone is superseded by runtime integration.
build_branforth_equipment.py preserves the existing helmet source and records
per-pose head fits; tools/build_branforth_bunk.py installs the supplement through
the canonical rebuild. Native controller, exact source-pixel, restore, regression
and deterministic checks pass. See docs/BRANFORTH_BUNK_INTEGRATION_2026-09-22.md.


## Bill bare bunk candidate (September 22)
bill-entry-source.png and bill-entry-prompt.txt preserve the built-in six-pose
source. build_bill_entry.py uses current idle palette, uniform 0.28 extraction and
exact idle. A 256x272 canvas prevents clipping the boarding boot without moving
the pivot or shrinking him. Native contact and deterministic checks pass; equipment
and runtime binding remain open. See docs/BILL_BUNK_MOTION_2026-09-22.md.


Bill's equipped candidate is now in bill-entry-helmet/, rebuilt by
build_bill_bunk_equipment.py with the selected 48px shell cap and exact equipped
idle. Native 47-sample contact and deterministic/alpha/border/endpoint checks pass;
bare art is unchanged. Bill controller integration remains open.


Bill's bare/equipped profile is now installed through tools/build_bill_bunk.py and
scripts/major_bill_npc.gd. Native controller and production-renderer checks pass;
see docs/BILL_BUNK_INTEGRATION_2026-09-22.md. Staged-only statements above preserve
prior milestones. Full expedition and release acceptance remain open.


## Marsh bought-bunk candidate (September 22)
marsh-entry-source.png and marsh-entry-prompt.txt preserve the built-in source.
build_marsh_bunk_entry.py extracts six poses at uniform 0.28 scale and adds exact
idle on 256x272 canvas. Native contact and deterministic checks pass. No helmet
variant, live controller change or modification of the legacy berth is included.
See docs/MARSH_BOUGHT_BUNK_MOTION_2026-09-22.md for evidence and integration tasks.


Marsh's bought-bunk profile is now installed via tools/build_marsh_bunk.py, separate
from the legacy berth. Native restore, contact, low-battery and legacy regressions
pass; see docs/MARSH_BOUGHT_BUNK_INTEGRATION_2026-09-22.md. All four reviewed cast
profiles are installed; autonomous expedition and release acceptance remain open.
