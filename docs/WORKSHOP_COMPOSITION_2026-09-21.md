# Project handoff

Updated: September 21, 2026 · BrineSpace · Salvage Workshop composition

## Objective and acceptance
Natural large/medium furnishing with supported tools, recognizable activity,
usable circulation and gameplay-scale review. Broad project goal remains active.

## Accepted decisions and constraints
Preserve owner rooms and marks. No Higgsfield, source repaint, registry changes,
publication or new release. Existing source detail is retained; no blanket upscale.

## Current state
Installed four complete room-salvage_workshop keys in defaults and the owner layout
file, guarded against concurrent edits. All other keys compare unchanged to backups.
Restored the existing directional overhead bench (320x115 footprint, unit scale),
which already includes supported tools, sorted bearings and an exposed motor.
Kept bought milling machine and adjacent drill bench as machining equipment.
Grouped ore cart with cargo crate; reduced crate scale0.8 to0.5. Hid the empty
steel table, unsupported tool board and redundant loose scrap box. Quarter-specific
positions keep equipment clear of the actual port. Original bench/tote PNGs and
all bought source pixels are untouched. Refreshed the Workshop card.

Changed project files: rooms/full-wall-v1/default-layouts.json,
assets/room-cards-v2/salvage_workshop.png and current-status/bible/skill reference.
Evidence/backups: output/workshop-composition-2026-09-21/.

## Verification
Candidate native-r1 and installed defaults each pass four views/640 walking samples,
zero route failures and no reported prop overlaps. All four native images reviewed.
Full RGBA parity exact in four quarters (parity.json). Funded isolated live fixture
completed 52/75-percent views; native room crop and full75-percent station reviewed.
The completed single-room card bake was inspected. Separate four-quarter fixture
checks existing bench on/off indication stays inside bench bounds, off-state ignores
clock and held-clock images match. This is a static powered indication, not new
mechanical motion or actual station-pause verification. No paid-balance claim.

## Next action
Review Holographic Core's projection/analysis composition. Workshop remains a
provisional installed composition: mixed source detail and owner aesthetic acceptance
are open. Current c09c exports predate this and other recent room changes; batch the
next release after the furnishing pass. Continue Bill/animation acceptance and other
bug/performance work under the unchanged broad objective.
