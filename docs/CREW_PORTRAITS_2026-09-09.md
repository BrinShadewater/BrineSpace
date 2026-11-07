# Project handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: matching crew portraits

## Objective and acceptance
Owner accepted BRINE's smaller bubbles and requested matching replacement portraits for the other characters. Bill, Veld and Branforth portraits are generated and installed; owner visual acceptance pending.

## Accepted decisions and constraints
BRINE V13 is the rendering reference. Preserve each crew identity and original pressure-suit gear, with face-dominant close framing, readable soft shading and quiet teal station backgrounds. Crew are in dry station air. Prior concept sources and gameplay sprites remain intact.

## Current state
character/crew-portraits-v1 contains bill.png, veld.png, branforth.png, exact per-character prompts, reference/hash manifest and native reviews. Built-in image_gen used; generated rasters unmodified. scripts/architects.gd replaces selection concept-sheet crops with full dedicated portraits, also supplying comms and checkpoint previews. scripts/crew_comms.gd uses 150x150 for every speaker. tests/playtest_crew_comms.gd now exercises all crew portraits at both resolutions. output/review_crew_portrait_picker.gd provides the narrow native picker review fixture.

## Verification
Native comms check passes at 1600x900 and 960x540 for all speakers, loaded textures, panel containment and hidden bubbles for crew. Narrow picker check passes both sizes with confirm control on-screen. Agent visually reviewed all three generated sources, all three small native comms captures and small picker. Logs: output/crew-portraits-v1-native.log and output/crew-portraits-v1-picker.log (stderr companions retained). Reviews saved alongside portraits as review-{identity}-{width}.png and review-picker-{width}.png. Checkpoint preview uses the same updated loader but was not separately exercised. No package export or commit.

## Next action
Owner review of the three portraits. No remaining implementation work for this scope.
