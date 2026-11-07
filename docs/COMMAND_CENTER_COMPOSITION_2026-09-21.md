# Command Center composition

Updated September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Make the bought-art Command Center read as a monitoring and briefing workspace,
using substantial equipment and clear circulation. Installed for playtesting;
owner visual acceptance and normal expedition review remain open.

## Accepted decisions and constraints
Preserve the ten named owner rooms and all library marks. No Higgsfield, source
raster edits, library removal, export, commit or publication in this pass.

## Current state
Four room-command_center keys in saved layouts and
rooms/full-wall-v1/default-layouts.json now use sf-04 monitoring console at
[-174,-180], scale .8; spa-109g targeting display at [50,-180], scale 1.25;
and spa-52b briefing station at [-64,-12], scale 1.35. The small wooden crate
(ns-154) and former round console (spa-120) are hidden in this layout. Old retained
furniture is also explicitly hidden. No library entries were removed.
assets/room-cards-v2/command_center.png was rebaked for this room only.
Backups, source shortlist, candidate files and captures:
output/command-composition-2026-09-21/.

## Verification
First candidate placed the briefing station at y50 and blocked the south approach
in all four quarters; rejected. Revision 2 moves it inward to y-12. Candidate and
fresh defaults each pass four production views/640 walking samples. All four
candidate/default images match every RGBA channel using NumPy array equality.
Native live fixture captures at 52% and 75% zoom completed; the 52% room crop and
four-view composition images were inspected. The fixture is synthetically funded,
not normal expedition/balance evidence. One-room card bake completed exit 0 and
the result was inspected. Every other saved/default layout is semantically
unchanged; every library JSON hash is unchanged, preserving owner marks.
No activity-service binding changed. Subsequent operating feedback adds restrained
traces to the bought monitors through the existing library screen registration;
briefing hologram and machine bodies remain static. See the feedback checks below.
The current Windows/Mac packages predate this layout and the fan-card changes.

## Operating feedback follow-up
Only sf-04 and spa-109g registrations gain operating_screens and
operating_screen_color. Absolute sheet rectangles are [188,28,14,9] (muted cyan)
and [492,155,30,12] (muted amber). Source PNGs and physical registration are unchanged.
These are shared prop effects wherever the assets occur in an operating room.
No renderer change or new image was needed. All other library JSON hashes match.

`tests/test_command_console_feedback.gd` and its paired UID are registered in the
room-art group and native lane. Native four-view checks pass: both displays move,
changes stay inside registered screens, off-state ignores the clock and held-clock
frames match. Installed native q0 still inspected; library validation checks 10,507
entries with zero problems. Evidence: output/command-operating-feedback-2026-09-21.

The isolated live probe invokes the actual pause-button signal, manually steps the
normal game process, and confirms visual/retained-room clocks hold then advance
from .25 to .65 on resume. It uses funded construction and is not normal expedition
acceptance. The initial probe used the wrong renderer dictionary, then checked the
reusable renderer's stale clock; both failed probes were stopped/finished and their
logs retained. The successful probe checks the actual retained canvas state.
This is live control/clock evidence plus separate native pixel evidence, not a claim
that a human mouse click or continuous expedition was recorded. Existing exports
predate these effects as well as the layout and card sampling work.

## Pipeline finding
The source review found ns-154 titled 'Office chair, navy, side' although its
actual source crop is a wooden crate. A subsequent focused repair changes only
its title to 'Wooden storage crate' and category to 'Storage'. No owner name or
category override existed for this ID. All other entries, every owner-mark file,
stable ID, label, source, pieces and footprint are preserved. The source image hash
is unchanged. Registry validation passes (see registry-after-label-fix.log).
ns-154-before.json and ns-154-repair.txt preserve the exact repair evidence.
The earlier all-library-hashes-unchanged claim describes the composition install;
this subsequent two-field metadata repair is the only library exception.

## Next action
Get owner composition feedback; continue room operation/animation and ordinary
expedition review. Keep the first rejected placement as evidence of the doorway
constraint. The specific ns-154 title mismatch is now repaired; no wider label sweep was run.
