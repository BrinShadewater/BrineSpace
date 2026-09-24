# Hydroponics composition integration

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Give Hydroponics a readable production area using large/medium bought props,
distinct growth stages and usable approaches. R3 is installed for playtesting;
owner visual acceptance and the broader polish objective remain open.

## Accepted decisions and constraints
Preserve ten named owner reference rooms and all library marks. No Higgsfield,
source raster edits or blanket upscaling. Saved Hydroponics differed from defaults;
its original state is preserved in both the snapshot and install backup.

## Current state
Four room-hydroponics_bay keys updated in the owner room_layouts.json and
rooms/full-wall-v1/default-layouts.json. All other layouts are unchanged.
assets/room-cards-v2/hydroponics_bay.png rebaked and inspected.
Evidence/backups: output/hydroponics-composition-2026-09-21.
R3 uses mb-87 at [-174,-180], scale .97, for developed foliage and spa-06e at
[-174,-96], scale 1.5, for sprouts. mg-124 nursery rack is [56,-180], scale 1.3;
mg-27b potting trolley [-174,48], scale 1.2; spa-461 culture vessel [110,58], scale 1.15.
The loose seed bag and tiny tray are hidden. R1 duplicated seedlings; R2's enlarged
mature tray was coarser than the selected 149-pixel source at almost native size.

## Verification
R3 four-view native review: 640 walking samples, zero failures. Fresh installed
defaults pass the same checks and all four PNGs pixel-match the reviewed candidate.
Live captures at 52% and 75% zoom completed; focused native-scale crop inspected.
Four controlled hunger trips each complete 92 clear movement samples and start a
meal break. Hydroponics uses clear-floor meal destinations, not an authored harvest
station; no gameplay behavior was changed. The funded route fixture forces hunger
and is not autonomous/balance acceptance. The ten protected room layouts and every
other layout remain unchanged; all library JSON hashes match the pre-install record.
One-room card bake exited 0 and the final card was visually inspected.

## Next action
Gather owner composition feedback and continue other room/animation polish.
Existing action-polish Windows/Mac packages predate this layout and the navigation
rebuild cancellation fix. Do not export again for this layout alone.
