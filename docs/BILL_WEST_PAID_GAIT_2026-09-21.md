# Bill westward walk and stop capture

September 21, 2026. Broad objective remains unfinished.

## Objective and constraints
Review the independently authored west gait in station gameplay with normal costs
and resource failures. No sprite/timing edits, generation, owner-room edits or release.

## Evidence
The paid-opening fixture exchanges the Solar/Hydroponics positions and lets Bill
choose goals autonomously. Capture begins on a west-walking observation and records
150 samples / 50 screenshots (five seconds of manual 30 Hz game stepping), with
camera following and normal dialogue minimization. Current recorded states are
56 walk and 94 idle; facing is west for 136 samples, south for 14. Thus this is a
westward walk/stop/idle capture, not five seconds of uninterrupted west walking.

Forty consecutive walk-west pairs have no negative phase delta; phase per travelled
unit is .0221646-.0221964, consistent with the independent east review. The walk-to-
idle boundary moves 1.43799 units on its final step; all consecutive idle samples
have exactly zero displacement. There are no paused samples. Complete=true, exit 0,
free_build=false, failures_disabled=false, clean engine log.

Full station frames 0 and 20 were inspected. The GIF uses an unscaled station crop
at the sampled 100 ms interval. The first narrow contact sheet clipped the actor
at the beginning and is unsuitable for pose review; walk-contact-complete.png
expands the crop to include the whole path. Do not use the rejected crop as evidence
of missing body parts. No new controller timing defect was established; subjective
gait smoothness and owner natural-motion acceptance remain open.
Evidence: output/bill-west-paid-gait-2026-09-21, summary.json and review.json.

## Next action
Use the current north/east, west/stop and north work-transition clips for owner
motion feedback. Avoid repeating the same narrow fixture without a new question.
Return to broader room/style consistency and package the accumulated verified
renderer/layout repairs at the next release milestone. Native Mac and full
expedition acceptance remain distinct requirements.
