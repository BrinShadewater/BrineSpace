# Current crew gait comparison

Updated September 22, 2026. Broad animation/room-polish goal remains unfinished.

## Objective and constraints
Compare current Bill, Veld and Branforth walks using production playback and a
shared moving ground reference. Preserve selected art, controller speed, owner
rooms and manifests. No generation or Higgsfield.

## Evidence
Output: output/crew-gait-comparison-2026-09-22. Native review.gd loads each selected
catalog through crew_sprite_player.gd and renders 90 frames at fixed30Hz for all
12 actor/direction combinations. Exit0, no missing textures or script errors.
Each actor travels46world units/sec. Display normalizes declared standingHeight
to148pixels; dots move opposite travel at that same display scale. comparison.gif
uses30/30/40ms frame durations to preserve three-second total playback.
This is a bare-sprite player comparison, not autonomous pathing or helmet review.

## Findings and limits
Bill north/south takes1.00174seconds per stride, identical to Veld. Branforth takes
1.06852seconds. Bill east/west takes0.88216seconds versus0.97805/1.03558 for Veld
and1.01640/1.03558 for Branforth. These derive from selected distance metadata;
a clip's authored millisecond total alone does not determine walking cadence.
The inspected rear-view contact sheet shows connected legs and alternating lifted
boots. It does not establish zero foot sliding or owner visual acceptance. No
runtime defect is established by these cadence differences; no speed/art change
was made to force the characters to match.

## Next action
Review inline current motion with the owner; refine a specific disliked pose or
transition if identified. Keep this comparison as current evidence rather than
reusing older pre-repair animation GIFs. Continue room/animation polish separately.
