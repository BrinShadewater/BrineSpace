# Bought bunk contact review

Updated September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Make the bought Crew Hab bunk usable by the current cast, with natural connected
entry/rest/rise, safe routes, correct furniture occlusion and save/interruption
behavior. This static review does not establish interaction acceptance.

## Accepted decisions and constraints
Preserve owner layouts, character scale and bought source pixels. No Higgsfield.
Keep the working legacy Marsh berth profile separate from this horizontal bunk.

## Current state
Fresh native rendering confirms saved Crew Hab q3 still uses library/tileset-mb2-14
at rect (72,-126,72.46131,73.99651). Four current sleep-east sources were inspected.
The output-only bunk-fit.gd fixture now supports --head-fit, registering anatomical
head pixels to the current bunk's source pillow centers (48,834)/(48,943). It reads
current prop registration rather than a fixed world anchor. Corrected its old
extra 14.592-unit lift; removed null-metadata diagnostics. No runtime changes.

Current source head anchors: Bill (67,195), Veld (63,210), Branforth (55,208),
Marsh (43,152). Existing pivots and standingHeight=148 are preserved. Fixture-only
sleep depth=100 and full-atlas complementary foreground masks retain ladder/post
occlusion; neither setting has been installed in runtime.

## Verification
Four native runs exited 0 without script errors, each capturing empty/top/lower.
All four lower captures visually reviewed at station scale and enlarged uniformly.
Bill and Marsh fit. Veld and Branforth have visible boot pixels outside the right
post; pillow contact alone is insufficient. Their unmasked source alpha extends
approximately 0.08/1.84 world units beyond the full registration rectangle, whose
visible right post is inset further. Do not treat these small full-rectangle
numbers as visual acceptance. Upper captures exist but were not visually accepted.

Evidence: output/layout-default-audit-2026-09-21/bunk-fit/ contains
head-fit-{actor}.json, cast-fit-measurements.json, cast-pillow-contact.png and native
lower-nearest-masks-head-fit[-actor].png. Logs are in the parent audit directory
as bunk-{actor}-head-fit.log. The output-only fixture is bunk-fit.gd there.

## Next action
Develop compact bent-knee sleep poses for Veld and Branforth at unchanged body
scale, then build connected bedside entry/rise for the cast. Review the whole
motion and safe approach before adding activity registration or runtime foreground
splitting. Preserve original generic sleep clips. Bought bunk functionality,
controller/save/interruption checks and packaged verification remain incomplete.

## September 22 compact endpoint progress

Built-in generation produced two preserved compact sleep sources under
character/bunk-contact-study-2026-09-21/, with exact prompts and a local
build_study.py. Both match canonical head/torso density through a uniform 0.16
source scale, existing canvas/pivot, canonical palette and binary alpha. Deterministic
rebuild, alpha/background and border checks pass. No runtime catalog was changed.

Two further native runs (--compact) exited 0 without script errors. Both lower-bunk
captures were visually reviewed: the protruding boots are gone and pillow contact
is retained, with knees beneath the upper frame. Before/after detail is
bunk-fit/compact-before-after.png. Six captures include upper/empty, but only lower
contact was visually accepted as a staged endpoint. Runtime/owner acceptance is open.

Next: repair connected seated-to-compact motion using these endpoints, retaining
canonical idle and anatomical scale. Existing lie-down frames straighten their
knees, so merely swapping the final sleep texture would introduce a pop. Complete
approach, foreground layering, gear coverage and controller integration afterward.

## September 22 lowering study

Veld has a preserved three-pose lowering source, local deterministic builder and
staged real-player manifest (300ms holds; reverse-derived rise; same-strip sleep
endpoint) in character/bunk-contact-study-2026-09-21/veld-lowering/. The fixed-hip
final-bed-position preview exposed upper-bunk head intersection. Revised native
study starts 12 world units forward on the mattress edge, moving inward during
lowering and outward during rise. Three key contacts visually clear the upper rail.

Both native variants rendered 19 samples and exited 0 without script errors; this
is capture evidence, not controller testing. Rebuild reproduces the three PNGs.
See bunk-fit/veld-edge-tuck-contacts.png and veld-edge-tuck.gif in the audit directory.
Raw source and exact prompt are preserved. No runtime catalog or room layout edits.

Next is standing-to-seat/ducking contact and motion refinement; the three staged
key poses are not a complete smooth floor-to-bed animation. Branforth's lowering,
gear variants, foreground runtime integration and save/interruption remain open.

## September 22 renderer installation

Foreground masks are now installed in Crew Hab's direct and retained queues, with
opt-in bunk pose depth. Native layer checks (17) and crew activity regression (36)
pass. See BOUGHT_BUNK_LAYER_INTEGRATION_2026-09-22.md for exact scope, changed files
and cache/parity evidence. The interaction and complete entry motion remain open.

## September 22 full Veld entry candidate

Added preserved four-pose entry source/exact prompt and build_entry.py. Seven-frame
1.84s staged entry uses exact registered canonical idle, three new supported poses
and three existing lowering frames; exit reverses poses/durations. Source fourth
pose remains preserved but unused. Contact phase data is stored in
character/bunk-contact-study-2026-09-21/veld-entry/choreography.json.

Fresh q3 production geometry: all four cast can stand at (125.2307,-36.00349), route
from a central room node and traverse the final approach segment. Six candidate
gaps were examined; gap8 is blocked. Final probe guards missing node IDs; no script
errors in bunk-entry-right-probe.log. No owner data edited or NPC walking claim.

47 actual-player native entry/exit samples revealed premature foreground masking
of a hanging shin. Fixed fixture classification: frames 0-3 stay in front of the
bunk; frames 4-6 enter its interior layers. Revised shin contact inspected. Seven
frames rebuild identically; alpha/borders pass; canonical idle and first/last native
captures match byte-for-byte. Final GIF bunk-fit/veld-full-entry.gif and log
bunk-veld-full-entry-final.log under output/layout-default-audit-2026-09-21/.

Next: assess/refine full motion and equipped fit, encode per-frame furniture depth
in production metadata, and bind a furniture-specific controller profile with exact
arrival/save/interruption tests. Branforth and remaining cast contact still open.
This remains a candidate, not accepted live bunk behavior.

## September 22 per-frame contact metadata

Production CrewSpritePlayer now reads furnitureFrames; build_entry.py encodes the
front/interior switch in both entry and exit. Removed the fixture's manual marker
mutation. Explicit per-frame values override the whole-clip marker; malformed
arrays and unknown values keep ordinary depth. Thirty focused checks pass,
including real forward/reverse playback and negative controls. Native captures
match all 47 manual-marker reference frames exactly in every RGBA byte. Tests are
indexed with a Godot-generated UID. Logs: sprite-furniture-metadata-final.log and
bunk-metadata-native.log in the audit directory.

The next integration step is the furniture-specific controller profile and equipped
coverage; station/normal travel, save/interruption and other cast remain unfinished.

## September 22 Veld equipped entry/exit

Added build_equipment.py and veld-entry-helmet/ with seven deterministic fitted
frames and matching precomposed manifest. Reused the existing east 30x32 shell,
recorded per-pose centers/angles and preserved exact canonical equipped idle.
Hair outside tilted shells is cleaned only in recorded equipped head regions,
preserving visor transparency. Bare source frames remain unchanged. No generation.

Normal equipment loader and per-frame depth checks pass (52 checks total).
Forty-seven native equipped captures, exact first/last RGBA equality, canonical
idle equality, deterministic rebuild, binary alpha and border checks pass. Inspected
leaning/rest native fit under the upper bunk. Evidence: bunk-fit/veld-equipped-entry.gif,
sprite-equipped-metadata.log and bunk-equipped-native-final.log under the audit
folder. Recipes and validation are beside the staged art. The next work remains
controller/catalog integration, sleep hold/loop, checkpoints/interruption/travel and
remaining cast; this is not live bunk interaction acceptance.
