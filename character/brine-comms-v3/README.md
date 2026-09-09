# BRINE comms portrait correction

Updated: September 8, 2026

## Objective and acceptance
Remove the visible bottom tube rim and add occasional bubbles behind BRINE.

## Accepted decisions and constraints
Preserve the approved face, suit and upper tube collar. The tube extends below
the crop. Earlier portraits remain available.

## Current state
Imagegen portrait and exact prompt retained here with source hash in manifest.json.
crew_comms.gd loads v3. brine_comms_bubbles.gd draws two subtle rising bubbles
per nine-second cycle, masked against the foreground silhouette. Animation advances
only while BRINE's comms is displayed; other speakers have no bubble overlay.

## Verification
Native comms reveal/replay and layout pass at 1600x900 and 960x540.
Focused bubble clock, glass bounds and foreground checks pass.
Evidence: output/crew-comms/brine-1600.png and brine-960.png;
output/brine-v3-comms.log and output/brine-bubbles.log.

## Next action
Owner review of the corrected crop and subtle bubble cadence in Comms.
