# Project handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: fresh BRINE portrait

## Objective and acceptance
Owner rejected the previous direction and supplied Brine Template_Export_2026-06-08_11-05-41.png as a fresh identity reference. V11 is generated and installed for owner review, not accepted yet.

## Accepted decisions and constraints
New photo reference supersedes the earlier brown bob: dark center-parted hair swept into a low bun, pale long oval face, blue-gray eyes, blue high-neck suit, submerged chamber. Retain crew pixel-art rendering and prominent face framing. Prior portraits remain available.

## Current state
character/brine-comms-v11 contains untouched generated portrait, copied identity reference, exact prompt, reference/hash manifest and native captures. Built-in image_gen used with only the new reference and Veld/Bill style sheets. scripts/crew_comms.gd loads V11 at the existing enlarged portrait size. scripts/brine_comms_bubbles.gd uses the full source image and revised foreground polygon; tests/test_brine_comms_bubbles.gd checks the new hair boundary. Caustics and source bubbles are painted; procedural bubbles also animate.

## Verification
Native playtest_crew_comms.gd passes at 1600x900 and 960x540. test_brine_comms_bubbles.gd passes. Agent inspected source and small native capture; identity is closer to supplied reference, with face prominent and features readable. Captures: character/brine-comms-v11/review-960.png and review-1600.png. Logs: output/brine-v11-native.log, output/brine-v11-native-errors.log and output/brine-v11-bubbles.log. No package export or commit.

## Next action
Owner liked V13's darker face. Review of smaller animated bubbles remains pending. No further changes to unrelated ongoing UI work.

## Follow-up: smaller animated bubbles
Owner liked the portrait but rejected the large animated bubbles. scripts/brine_comms_bubbles.gd reduces radii from .016/.012 to .006/.0045 (62.5% smaller diameter), opacity from .9 to .55 and stroke width from .85 to .6. Existing timing and silhouette masking remain. Native comms at both sizes and bubble mask/clock checks pass (output/brine-small-bubbles-native.log and output/brine-small-bubbles-mask.log). Agent inspected native small-size still; captures saved as character/brine-comms-v13/review-small-bubbles-{960,1600}.png. Still capture establishes scale, not visual motion acceptance. Painted source bubbles remain part of V13.

## Follow-up: slightly darker face
Owner requested a small darkening after V12. V13 lowers facial midtone brightness while preserving soft shading, identity, expression and framing. Built-in generation source, exact prompt and reference/hash manifest saved in character/brine-comms-v13; scripts/crew_comms.gd loads V13. Bubble mask unchanged. Native comms checks pass at both sizes (output/brine-v13-native.log), with review-960.png and review-1600.png preserved in V13. Agent visually reviewed generated art and small native portrait. Owner acceptance pending; no package export.

## Follow-up: softer facial shadows
Owner requested less shadow on her face. V12 edits V11 with diffuse facial fill and reduced caustic contrast, preserving pose, identity and silhouette. Source, exact built-in image-generation prompt and hash manifest are saved in character/brine-comms-v12; scripts/crew_comms.gd now loads V12. Existing bubble mask is retained. Native comms checks pass at both resolutions (output/brine-v12-native.log); review-960.png and review-1600.png are preserved with V12. Agent inspected source and small native portrait for readability. Existing unrelated wrecked-room image-loading warning remains in output/brine-v12-native-errors.log. No package export; owner acceptance pending.
