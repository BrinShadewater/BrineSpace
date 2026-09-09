# BRINE crew-style portrait

Updated: September 8, 2026

## Objective and acceptance
Smaller bubbles and portrait rendering closer to the other crew.

## Accepted decisions and constraints
Preserve BRINE's brown bob, blue eyes, navy suit and spacious tube background.
No bottom rim or exterior background. Prior portraits retained.

## Current state
Built-in imagegen edit uses v4 for identity and Bill/Veld concepts for style.
More angular pixel shading, muted skin highlights and matte suit rendering.
Exact prompt and hashed manifest retained here; crew_comms.gd loads v5.
brine_comms_bubbles.gd reduces radii from .025/.019 to .016/.012 and stroke
from 1.2 to .85, retaining visible staggered phases and foreground masking.

## Verification
Native comms checks pass at 1600x900 and 960x540 (output/brine-v5-comms.log).
Agent inspected full-size art and small native portrait; identity remains readable
and smaller bubbles visible. Revision-specific captures: review-960.png and
review-1600.png. Style acceptance remains with the owner.

## Next action
Owner review of the closer crew rendering and smaller bubble size.
