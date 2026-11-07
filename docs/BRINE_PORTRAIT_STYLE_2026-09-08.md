# Project handoff

Updated: September 8, 2026 · Project: BrineSpace · Task: BRINE portrait style pass

## Objective and acceptance
Owner requested another BRINE portrait pass matching the other portraits, then preferred the previous portrait after V10 and requested closer framing. V9 is restored with 25% closer runtime framing; owner review of the crop remains pending.

## Accepted decisions and constraints
Use actual Bill, Veld and Branforth portrait sources for style. Preserve brown buoyant bob, blue eyes, navy high neck, faint composed smile and cropped submerged glass chamber. Earlier V8 acceptance remains historical; all earlier sources are retained.

## Current state
Added character/brine-comms-v9 and character/brine-comms-v10 with untouched generated portraits, exact prompts and reference/hash manifests. Built-in image_gen used. V9 improved pixel clustering but retained oversized eyes; V10 reduces eye size, shine and saturation. scripts/crew_comms.gd now loads V10. Bubble mask remains suitable for the preserved silhouette. No gameplay changes, commit or package export.

## Verification
Native playtest_crew_comms.gd passes at 1600x900 and 960x540; captures preserved in V10 as review-1600.png and review-960.png. Agent visually reviewed generated source against peers and native small portrait. test_brine_comms_bubbles.gd passes. Logs: output/brine-v10-native.log, output/brine-v10-native-errors.log and output/brine-v10-bubbles-check.log. Native run reports an unrelated wrecked-room image-loading export warning; no packaged validation claimed. Hair and refraction remain painted; only bubbles animate.

## Next action
Owner review of V9 closer framing and larger panel portrait. Retain V8 and V10 for comparison.

## September 9: fill the comms window
Owner requested much more portrait coverage. BRINE's TextureRect now uses 150x150 instead of 96x108, filling the existing panel's interior height and displaying the square portrait 56% wider. V9 and the 25% closer crop remain. Other speakers retain their previous sizing. Native comms check passes at both resolutions; agent reviewed review-fill-960.png, with both native captures retained in character/brine-comms-v9/. Log: output/brine-v9-fill-native.log. No new raster edit or export.

## Follow-up: restored portrait and closer framing
scripts/crew_comms.gd now loads unchanged V9 through an AtlasTexture with normalized crop (0.10, 0.10, 0.80, 0.80). The shared crop in scripts/brine_comms_bubbles.gd maps bubble occlusion back to source coordinates. tests/test_brine_comms_bubbles.gd covers the changed hair/glass boundary. V9 manifest status updated. Native comms checks pass at 1600x900 and 960x540, and bubble checks pass; source-size art and review-close-960.png visually inspected by agent. Captures are saved in character/brine-comms-v9/review-close-{960,1600}.png. Logs: output/brine-v9-close-native.log and output/brine-v9-close-bubbles.log. No new generation or raster edits. Earlier V10 installation details above describe the superseded pass.
