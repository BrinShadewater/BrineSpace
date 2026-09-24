# Marsh berth contact handoff

Updated September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Repair Marsh's sleep and connected lie-down/get-up motion against actual furniture.
Completion requires visible, continuous bed contact, registered endpoints and native
runtime timing/occlusion checks. The broad animation and furnishing goal remains open.

## Accepted decisions and constraints
Preserve owner layouts and canonical runtime art until a candidate works. No
Higgsfield. Source generation and deterministic extraction are separate from acceptance.

## Current state
The six-pose staged source is rejected for installation with the current linear
placement. Native previews show the seated intermediate pose floating beside the
bed, then sliding onto it. A plausible final sleeping pose does not fix that motion.
The diagnostic now records approach/rest anchors in
`output/layout-default-audit-2026-09-21/marsh-bed-motion/contact-measurements.json`.
No runtime source, metadata or room layout changed in this review.

## Verification
The native probe completed 44 samples across four room quarters without logged
errors. Visual inspection covered q0 standing/intermediate/rest and q3 intermediate.
The staged anchor travels 83.27 room units, 1.28 standing body heights, in every
quarter. This is a fixture measurement, not an autonomous animation acceptance.
The runtime also interpolates furniture offsets in `scripts/crew_life.gd`, so a
replacement source must be designed together with the contact path. Simply shrinking
the displacement or changing depth is not a demonstrated repair.

## Next action
Establish a reachable bed-edge entry and explicit seated hip contact, then author
or select a connected turn/sit/leg-lift/recline sequence for that path. Validate
contact before expanding directions or fitting equipment. The saved q3 bought bunk
still needs its own registered sleeping interaction; this single-berth study does
not supply it. Pause/save/restore and actual NPC playback remain pending.

## Later contact source study
A focused built-in image-generation call produced `marsh-contact-six-raw.png` in
the same audit directory. Exact prompt: `marsh-contact-source-prompt.md`. No
Higgsfield. `extract-marsh-contact.py` retains one scale, maps the canonical suit
palette and registers six manually reviewed source pelvis landmarks to (92,115).
Raw hash, crop boxes and landmarks are retained in `marsh-contact-extracted/recipe.json`.
The source contains side-on sitting followed by a leg swing and vertical recline.

`marsh-contact-motion.gd` rendered 44 native samples across four quarters with no
logged errors. Reviewed q0 standing, seated and final frames: seated/reclining
contact is substantially improved, but the provisional standing entry is hidden
by bedside furniture. Its shortened entry was an unvalidated presentation offset,
not an established reachable floor point. Do not install it or describe the shorter
slide as a completed repair. Next connect an actual reachable approach to this
contact sequence and verify occlusion throughout; keep the existing layouts.

## Installed berth footprint correction
The entry probe proved that the old single collision rectangle includes empty floor
below the bedside cabinet. `rooms/whole-room/crew_hab_view.gd` now gives
`hab_berth_east` two conservative normalized collision boxes: full-length bed and
short cabinet. This changes navigation only; no layout or artwork changed.

`marsh-entry-probe.gd` passes four-quarter production `can_stand` checks for solid
bed/cabinet, clear floor notch and Studio routes into the notch. The closest sampled
reachable point to the rejected entry changes from (-72,-96) to (-88,-88).
The original provisional entry remains blocked: do not reuse it as valid.
The probe's first attempt incorrectly freed a RefCounted NPC; corrected before the
reported successful run. Final log has zero failures/errors.

Persistent regression assertions were added to `tests/test_crew_room_activity.gd`.
Its native run passes all 36 room/rotation/actor approach, facing and save cases,
including the new solid/clear footprint checks. All 44 staged native PNGs remain
byte-identical after the collision correction (`footprint-visual-parity.json`).
The new Marsh sources remain staged; reachable animation entry, endpoints and
actual Marsh playback are still open. Release packages predate this correction.

## Installed close bedside approach
`scripts/crew_room_activity.gd` now chooses the clear notch at normalized (0.95,0.67)
for the unmirrored compound berth. It retains the prior approach if that point is
blocked or outside the service band; mirrored layouts retain their previous behavior.
No room layout changed. The native 36-case activity test passes again, including
actual approach completion, and explicit blocked-notch/mirrored negative controls.
Final evidence: `crew-activity-bedside-final.log` in the audit directory.

`marsh-reachable-motion.gd` uses that actual station point. All 44 staged captures
complete; reviewed q0 entry/sit/recline and q3 lowering. The diagnostic depth offset
starts at 32 and reaches 96 by the seated pose, preventing the combined prop from
covering entry. Neither that depth curve nor the new source is installed. Travel is
57.00 room units versus 83.27 in the first study. This reduces displacement but does
not prove a natural timed transition. The output-only GIF `marsh-reachable-motion/
bed-contact-preview.gif` holds endpoints for inspection and reverses the pose list;
it is not actual NPC playback. Canonical idle joins, runtime timing and the approach
to bedside draw-order transition still need verification before source installation.

## Animation-player trial
`build-marsh-bed-trial.py` packages output-only lie-down/sleep/get-up clips. Frame
zero is the exact canonical idle-east PNG, sleep shares the final new pose, and
get-up explicitly reverses the same frames. Lie/rise each total 800ms, matching
current `CrewLife.STAGES`. No runtime catalog entry was added.

`marsh-player-bed.gd` exercises `CrewSpritePlayer.frame_at_elapsed` at 50ms intervals
over both transitions in four quarters: 136 native samples, zero missing frames or
endpoint/duration failures. Initial run emitted a fixture-only image-load export
warning; the probe now uses the project's PNG-buffer loading convention. No claim
of packaged verification is made. Native images q0 at 0,100,200,250ms were reviewed.

Visual acceptance fails despite exact endpoints. Holding canonical idle until 80ms
then reaching the seated anchor at 224ms moves 57 units in 144ms (about 396 units/s).
The body slides into place before reclining. Earlier slow pose-hold GIFs concealed
that timing problem. Preserve the trial as negative evidence; do not promote it.
The next source/contact pass needs an actual intermediate bed-edge seated contact
and a timed scoot/leg-lift rather than collapsing all displacement into the first
lowering frame. Any changed action duration must also update the actor's timer,
visual offset, interruption and save/restore behavior; changing clip timing alone
would truncate it. East-entry-to-north-rest selection also remains unimplemented.

## New two-part timing candidate
`build-marsh-bed-slow.py` retains the same source and exact idle endpoint, with
durations [120,300,300,300,300,280]ms. `marsh-player-bed-slow.gd` reaches a bed-edge
seat offset (+20,+18) over 300ms, holds it, then shifts inward over 600ms while the
legs swing and torso reclines. This replaces the rejected all-at-once entry.

Corrected a preview-only coordinate error: `main.get_marsh_position` subtracts the
lift added by GridCanvas, leaving NPC foot coordinates unchanged. Earlier probes
added 14.592 units a second time. Their reported displacements describe those
fixtures, not exact live motion. The new probe starts directly at station.point.

Final native run: 264 player-timed samples, zero failures/errors/warnings. Reviewed
entry/seat/leg-swing/recline stills; the seated pose remains at the mattress edge.
Twelve exact PNG checks confirm fixed seated contact during its hold and identical
sleep/idle joins across four quarters (`native-contact-checks.json`). The GIF uses
50ms captured intervals with extra endpoint holds. This establishes a usable staged
candidate, not NPC integration or owner acceptance. Runtime remains unchanged.

Next implementation must keep this optional bed profile specific to Marsh and
compatible furniture. Existing clips retain 0.8s timing. Check actor stage timing,
save validation and restore (which currently cap life transitions at 0.8s), rising
on interruption, and simulation pause. Preserve ordinary locomotion and all other
character packs. The candidate's east-facing entry needs explicit selection; generic
stations still report north. Do not solve that by changing every crew member's facing.
