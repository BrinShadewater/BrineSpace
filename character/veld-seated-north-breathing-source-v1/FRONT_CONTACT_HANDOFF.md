# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld aligned chair approach

## Objective and acceptance
Remove the observed sideways chair-entry/rise glide while preserving masters,
furniture, collisions, saved contact and the full Veld animation objective.

## Current change and constraints
crew_room_activity.gd prefers a clear front for fallback lounge sofa/lounge_seat
props. Starting at the existing28-unit front gap, try4-unit insets up to16; use
the actual blocker rules. Station-local service_limit admits that clear band;
exact_approach appends the registered contact via existing clear-path checks.
No furniture, wall, collision mask or physical foot teleport changed. Blocked
fronts retain the old side fallback, still a distinct motion context to improve.
Games-table stations are unchanged.

crew_life.gd uses seated_contact only for already seated/down/rise offset/depth.
It retains former side contacts for checkpoints without offering them to new goal
selection. Normal at/stations still prefer the new clear front. Save schema and
player clocks unchanged. Shared chair resolver affects other crew; this native
motion proof covers Veld. Existing selected art/palette/standing ruler unchanged;
16bound breathing files remain byte-exact. North source pack remains staged.

## Verification and visual review
Actual four-quarter approach probe:4checks/37.62sec, shows rotation2 front153..165
clear and169wall-blocked, node128/160 joins.11static contract/contact/retained
offset/depth assertions pass in4.68sec. Latest normal chooser/path/movement/down/
breath/rise journey:6375checks0failures,80.69sec engine0/no errors,72native+72source
captures. Both gear versions arrive tick900, held948, rise1393, final idle1441.
Old63.5px lateral shift becomes <.1px (observed ~.0693), matching existing contact
tolerance; vertical chair join32px. Paired native/source boards reviewed: large
sideways entry/exit glide removed, held source/materials/hardware unchanged.
Initial75.38sec interval failed an unnecessarily strict .01px fixture threshold;
kept evidence, adjusted to existing .1px contact tolerance, no movement change.
Earlier6375/81.72sec pass precedes retained-side compatibility helper.

Four actual disk/fresh-scene restores, front and retained-side held contacts in
both gears:81checks0failures/154.51sec engine0/no errors. Exact source pixels,
foot, offsets, depth, paused visual clock/action/gear retained. Prescribed checkpoint
cases distinct from natural journey. Native before/after chair board reviewed:
3crops byte-exact; first bare-front max5/255 shade difference with exact source.
Known first-render shade uncertainty remains; no source-grade adjustment or
whole-room shade equality claim. All isolated runs retain2931non-log owner files.

Changed shared scripts, paired fixture/runner/UID, static contact fixture/runner,
four-quarter diagnostic, tests/index.json, review builders/media/hand-off/notes.
Previous failing-entry boards/page/handoff and shared resolver preserved under
revisions/front-contact-v1; old test intervals stay in their output folders.

## Next action
Review/resolve fully blocked-front side fallback motion without moving owner
furniture; ordinary facing switch remains inherited. Independent East/West
seated sources, South room contexts, more hazards/rest/death joins and full-set
cross-animation polish remain. No normal selection of new seated artwork,
all-layout/all-crew motion/owner acceptance/full-goal completion claim.
