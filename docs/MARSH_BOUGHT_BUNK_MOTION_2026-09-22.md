# Marsh bought-bunk motion candidate

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Connect Marsh's standing appearance to the bought lower bunk while preserving
his separate working legacy berth, battery behavior and body proportions.
This milestone is a staged native-reviewed motion candidate, not runtime binding.

## Accepted decisions and constraints
No owner layout edits. Built-in image generation supplied missing poses; no
Higgsfield/API. No helmet variant: Marsh remains a sealed android. Preserve the
legacy berth source/catalog and ordinary swimming/locomotion clearance.

## Current state
character/bunk-contact-study-2026-09-21/ contains marsh-entry-source.png, exact
marsh-entry-prompt.txt and build_marsh_bunk_entry.py. marsh-entry/ stores seven
frames, manifest, recipe, choreography and validation. The builder uses canonical
idle palette, uniform 0.28 scale, binary alpha, recorded foot/hip anchors and exact
padded idle. Canvas 256x272, pivot (128,224), standingHeight 148. Entry is 1.84s;
exit reverses the same sequence. First four frames remain in front of the rail,
fully boarded frames use interior depth. No live catalog/controller changes.

## Verification
output/layout-default-audit-2026-09-21/bunk-fit/marsh-existing-sleep-board.png
records the earlier floor-sitting transitions. marsh-bunk-native.log records 47
actual-player native captures of the candidate. Boarding, leaning and rest were
inspected: complete hanging boot and compact fit beneath the upper mattress.
Deterministic rebuild, exact canonical idle, binary alpha, clear borders and
identical native first/last pixels pass in marsh-entry/validation.json.
Review: output/layout-default-audit-2026-09-21/bunk-fit/marsh-full-entry.gif.

## Next action
Integrate a distinct bought-bunk contact profile into Marsh's controller and
canonical build. Check ordinary chooser/arrival, partial reversal, save restores,
low-battery exit, shared bunk claims and existing legacy berth regressions.
Exclude furniture contact frames from shared movement clearance. Full expedition,
owner visual and packaged acceptance remain open.
