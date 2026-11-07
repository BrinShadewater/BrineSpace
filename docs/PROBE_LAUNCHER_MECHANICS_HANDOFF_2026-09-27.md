# North launcher base and mechanical motion

Fin-clearance follow-up: tunnel clip now centred on the shifted probe axis (x=-4)
with 40-unit clear width; measured opaque north probe span is 27.88 units. Its
rounded narrowing occurs only within the existing 12-unit depth fade, preventing
fully visible fins from being sliced at the mouth. Four native rotation checks
and 265 updated frames pass; entry frame reviewed. Preview refreshed.

Tunnel cleanup: replaced the stepped rectangular aperture bands with a rounded
throat and a 12-unit depth fade. The probe disappears into darkness before the
upper clip boundary, removing the square cutoff. Native motion captures and four
rotation checks pass; deep-entry frame reviewed and animated preview refreshed.

Latest correction: north probe visual pose now centres at x=-4 on the shifted
rails, blending back to the unchanged ocean route behind the upper wall. Tunnel
pixels are redrawn after the props-pass platform to prevent its rear edge cutting
a black stripe across the launching probe. Centre checks use float tolerance;
four orientations and 265 motion frames pass. Entry frame visually reviewed;
card and animation preview updated. Owner profile unchanged in isolated checks.

Latest alignment follow-up: owner likes the shortened version; platform and cradle
moved four units left and two units toward the wall. Rear edge now y=-178, giving
a two-unit overlap with the riser foot. Four rotation checks and 265-frame capture
pass, docked join visually inspected, card/preview refreshed. Isolated native run
and card bake both report the owner profile unchanged.

Owner follow-up: platform shortened from 126.58 to 68 world units, with rear
edge exactly at the riser foot (y=-176). Source rail segments retain their pixel
scale while omitting excess length. Cradle travel reduced to 32 units. Probe is
now rendered within two registered tunnel aperture bands, without underwater wake
inside the tunnel, so entry and return read continuously across the wall edge.
Four orientation checks, rear-edge/length assertions and 265 updated native frames
pass; docked and tunnel-entry views inspected. Card/preview refreshed.

Updated: September 27, 2026 · Project: BrineSpace

## Objective and acceptance
Owner requested a launcher base matching the special riser, then reanimation.
Clarification: launcher mechanics only; probe swimming remains unchanged.
Owner approved the launcher visually on 2026-09-28 (Studio launch sequence and all four rotations reviewed).

## Accepted decisions and constraints
North base plugs into the existing wall portal without duplicating its large ring
or accumulator. Retain mission timing, route, original collision and other views.
Use generated stationary rails and a separate mechanical cradle; no paid video jobs.

## Current state
`assets/probe-launcher-v2` contains raw base/cradle PNGs, exact prompts, hashes,
265 native frames, motion contact sheet, and launch/recovery WebP review.
`scripts/probe_launcher_mechanics.gd` registers the two layers and drives the
hydraulic release and cradle travel from survey_clock. `survey_probe_art.gd` uses
the new base only for the north-facing, exposed raised special wall; low walls,
other rotations and explicit wall materials retain their previous launcher.
`painted_shell.gd` overlays matching mechanical art at the wall join. Room visual
bounds include the new rails; original collision geometry stays unchanged.
Probe Bay card and special-wall gallery are refreshed.

## Verification
Four native rotation checks pass; release-before-launch, throat travel, return to
dock and cycle closure assertions pass. 265 native frames captured at 24 fps:
0–6 seconds launch, followed by 27–32 seconds recovery (ocean excursion omitted).
Motion checkpoints visually reviewed. Source bytes match generated originals.
Maintained card baker passed. Runs used scratch APPDATA; concurrent live session
changed last_session.json. No real-profile byte-equality claim.

## Next action
Review http://127.0.0.1:8812/special-north/launcher/.
No probe animation edits, gameplay changes, release export, commit or push.
