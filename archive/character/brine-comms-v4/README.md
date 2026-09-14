# Spacious tube portrait

Updated: September 8, 2026

## Objective and acceptance
Give BRINE more space in the tube; fill the portrait with tube interior rather
than showing the room outside it.

## Accepted decisions and constraints
Keep her scale, face and suit; no bottom rim. Preserve occasional animated bubbles.

## Current state
Built-in imagegen background edit retained here with exact prompt and hashed
manifest. crew_comms.gd loads v4; previous versions remain available.
The glass fills the frame and the outer supports sit beyond the crop.
The unchanged foreground silhouette remains compatible with the bubble mask.
Follow-up: bubbles now use five staggered phases, larger bright outlines and the
wider side glass. Some are already rising when Comms opens, eliminating the
initial invisible period. Native 960x540 review confirms visible bubble rings;
comms checks pass in output/brine-visible-bubbles.log.

## Verification
Native comms test passes, including other-speaker bubble visibility and BRINE
reveal/replay. Portrait reviewed at native size. Evidence:
output/brine-v4-comms.log and output/crew-comms/brine-960.png, brine-1600.png.

## Next action
Owner review of the wider tube framing.
