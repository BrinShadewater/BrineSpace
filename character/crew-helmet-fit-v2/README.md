# Fitted crew helmet source revisions

Four edited source sheets cover Veld and Branforth pickup and donning. Their
fitted interior poses are now selected by `tools/rebuild_human_crew_art.py` through
`tools/fitted_crew_helmets.py`. The `candidate-01` filenames are immutable source
identifiers. Original underwater sheets and frozen source contracts stay intact.

The final clips start/end on exact selected idle frames, translated from the
172-pixel idle foot pivot to the 196-pixel locker pivot. Pickup joins the first
donning pose; removal reverses that same progression. Source-scale and station-
scale review is in `review/motion.html`, generated from selected catalogs by
`tools/review_crew_locker_motion.py`. `tests/test_fitted_crew_helmets.py` checks
world-registered idle joins, reverse sequence identity and retained pose coverage.

Branforth and pickup prompts are stored beside their source PNGs. Pickup edits
reference the actor's original pickup sheet and the edited donning sheet. The
Branforth donning edit references his original sheet and selected helmeted idle.
The Veld donning prompt below remains the exact generation prompt.

Generated with the built-in image generation tool on 2026-09-12, using
`character/crew-underwater-v1/generated/veld-equip-helmet-east-candidate-03.png`
and `character/dr-veld-v2/frames/helmet/idle-east/000.png` as references.

Exact prompt:

> Edit the FIRST image: a production six-pose sprite strip of Dr Veld putting on her diving helmet. Preserve its exact aspect ratio, six separate poses, camera direction (east/right), body silhouette/scale, head and face size, female identity, dark ponytail, uniform, skin, detailed material shading, foot baseline and pose centers. Flat pure magenta #FF00FF background. ONLY correct the oversized helmets and the hands immediately gripping them. Make the helmet shell approximately 70% of its current width and height in ALL six poses, held and worn, with a snug neck seal. Preserve the character's face at its ORIGINAL size within the visor, never shrink her head or body. The SECOND image is only a helmet-to-head size reference: the shell is just a little wider than the head, comfortably fitting it, not a huge diving bell. Pose1 holds the smaller helmet at waist, pose2 lifts to chest, pose3 raises above head, pose4 lowers onto head hands touching sides, pose5 secures neck, pose6 arms at sides with correctly fitted helmet. Keep gloves gripping the resized shell naturally, no floating hands. Keep every unaffected body pixel/design region as close to the first image as possible. No new equipment, no labels, no floor or shadows, no layout changes or extra figures. This is a localized source-art correction, not a character redesign.
