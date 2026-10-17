# Marsh dry carry chain source prompts

Built-in image generation, September 29, 2026. Selected source sheets live in
`sources/`; rejected turn sheets with the old black eye mask are retained there
with `-rejected` names. The input reference images are in
`output/marsh-animation-audit/`. The extraction recipes are
`tools/prepare_marsh_carry_chain.py` and
`tools/prepare_marsh_carry_turn_match.py`.

## Pickup south

> Edit this transparent four-column, two-row pixel-art sprite sheet. Top row is the exact approved clean-shaven Marsh identity and cargo-held end pose. Leave top row unchanged. Redraw ONLY the bottom row as a four-phase SOUTH-facing pickup action by the SAME clean-shaven blond android with the same fitted ivory/slate suit, muted sage shoulders and black gloves. Frame 1: upright empty-handed. Frame 2: knees bend and torso reaches down toward a small dark-gray rectangular case on floor. Frame 3: grips the same case with both hands and begins rising. Frame 4: upright carrying that same case at waist height, matching top-row first frame. Keep his boots registered to same ground line where planted, proportional bend (do not shrink entire figure), same case design and hand contact, four separate complete figures in their cells. No beard, black eye mask, bulky armor or dark collar. Preserve transparent background and even grid; no floor, text, borders or extra objects.

## Pickup east

> Edit transparent 4-column 2-row pixel-art sprite sheet. Keep top row unchanged as exact clean-shaven EAST-facing Marsh identity and carried-case endpoint. Redraw only bottom row as 4-phase case PICKUP by the SAME android, strict right-facing side profile in every frame. 1 standing empty-handed, 2 bending knees and reaching down to dark-grey equipment case on floor, 3 grasping same case and rising, 4 upright holding case with both black gloves at waist, matching top-row first frame. Fitted ivory/slate suit, muted sage shoulder, anatomical-right temple implant, clean face, same scale, boots registered to floor; actual knee/hip bending, do not shrink body. Preserve four separate complete sprites on transparent background, no text, floor, borders or other objects.

## Pickup west

> Edit transparent 4-column 2-row pixel-art sprite sheet. Keep top row unchanged as exact clean-shaven WEST-facing Marsh identity and carried-case endpoint. Redraw only bottom row as 4-phase case PICKUP by the SAME android, strict left-facing side profile in every frame. 1 standing empty-handed, 2 bending knees and reaching down to dark-grey equipment case on floor, 3 grasping same case and rising, 4 upright holding case with both black gloves at waist, matching top-row first frame. Fitted ivory/slate suit, muted sage shoulder, clean face, anatomical-right temple implant hidden, same scale, boots registered to floor; actual knee/hip bending, do not shrink body. Preserve four separate complete sprites on transparent background, no text, floor, borders or other objects.

## Pickup north

> Create a one-row strip of FOUR pixel-art frames showing ONLY the BACK of the same blond android in the reference as he picks up a compact dark-gray equipment case from the floor in front of him. Strict REAR view in ALL four frames: blond back of head, rear backpack panel, rear suit and legs; NO face, eyes, chest or frontal case surface visible. Frame 1 upright empty-handed, frame 2 bends knees and reaches toward case on floor ahead (mostly hidden by his body), frame 3 grips it and rises, frame 4 upright holding case in front of chest with elbows forward, case mostly hidden from rear. Keep the reference fitted ivory/slate suit, sage shoulders, black gloves, exact character scale and planted boot line. Show actual bending through knees and hips, not shrinking. Four separate complete evenly spaced figures, transparent background, no floor, text, front views or extra people.

## Selected turn east to north

> Complete this one-row five-cell transparent pixel-art sprite strip. Existing first and fifth cells are exact identity references for clean-shaven blond android Marsh holding compact dark-gray equipment case: first faces EAST in strict right profile, fifth faces NORTH with only BACK of hair and rear suit panel visible. Draw only the three missing middle figures, one centered per empty cell, as a smooth right-profile to rear-three-quarter to back rotation in place. Show progressively less face and case; the case remains held in front of his chest and is hidden by his body at the end. Same fitted ivory/slate suit, muted sage shoulders, black gloves, crisp pixel art and scale as references. NO black eye mask, goggles, beard, bulky armor, front-facing figure or extra objects. Preserve first and fifth figures and transparent background; five complete evenly spaced figures, fixed foot ground line.

## Selected turn west to north

> Complete this one-row five-cell transparent pixel-art sprite strip. Existing first and fifth cells are exact identity references for clean-shaven blond android Marsh holding compact dark-gray equipment case: first faces WEST in strict left profile, fifth faces NORTH with only BACK of hair and rear suit panel visible. Draw only the three missing middle figures, one centered per empty cell, as a smooth left-profile to rear-three-quarter to back rotation in place. Show progressively less face and case; the case remains held in front of his chest and is hidden by his body at the end. Same fitted ivory/slate suit, muted sage shoulders, black gloves, crisp pixel art and scale as references. NO black eye mask, goggles, beard, bulky armor, front-facing figure or extra objects. Preserve first and fifth figures and transparent background; five complete evenly spaced figures, fixed foot ground line.

## Selected turn west to south

> Complete this one-row five-cell transparent game sprite strip. Existing first and fifth cells are exact identity references for clean-shaven blond android Marsh carrying a small dark-gray equipment case: first is strict WEST left profile, fifth is SOUTH frontal. Draw only the missing three middle figures, one centered in each empty cell, as a smooth left-profile to left-three-quarter to front rotation in place. Same clean-shaven face as the two references, fitted ivory/slate suit, sage shoulders, black gloves, hair shape, case design, both-hand grip, ground line and crisp pixel art. The face has ordinary natural eyes with NO black eye mask or goggles; no beard or bulky armor. Preserve existing first and fifth figures and transparent background. Exactly five complete equally scaled figures total, no text, borders, floor, extra people or objects.

## Selected turn east to south

> Complete this one-row five-cell transparent game sprite strip. Existing first and fifth cells are exact identity references for clean-shaven blond android Marsh carrying a compact dark-gray equipment case: first is strict EAST right profile, fifth is SOUTH frontal. Draw only the missing three middle figures, one centered in each empty cell, as a smooth right-profile to right-three-quarter to front rotation in place. Same clean-shaven face, slim fitted ivory/slate suit, muted sage shoulders, black gloves, hair shape, case design and both-hand grip as the two reference figures; keep their exact anatomical height, head size, lighting and crisp pixel-art finish. Ordinary natural eyes, NO black eye mask, beard, bulkier armor or chest redesign. Preserve first and fifth figures, transparent background and fixed foot ground line. Five complete evenly spaced figures, no text, borders, floor or extra objects.

## Rejected turn edit prompts

The first edit-target approach carried the old eye mask into the generated
interiors. Its exact prompts are retained below.

East to south:

> Edit this transparent ONE-ROW FIVE-FRAME pixel-art sprite strip. It is a 400 ms CARRY TURN by the same android Marsh, from strict EAST-facing right profile in frame 1 to strict SOUTH-facing front in frame 5. Frames 1 and 5 are the exact selected clean-shaven identity and cargo case; leave them unchanged. Redraw ONLY frames 2, 3 and 4 to match their clean-shaven blond face, fitted ivory/slate suit, muted sage shoulder, black gloves, dark-grey case design and crisp pixel-art style. Preserve the progressive right-profile to three-quarter to frontal rotation, one complete figure per equally spaced cell, both hands holding the same case at waist, consistent scale and ground line. Remove dark eye mask, beard and bulky old armor in middle frames. Do not replace the turn with walking; show rotation in place. Transparent background, no floor, shadows, text, borders or extra people.

East to north:

> Edit transparent one-row FIVE-FRAME pixel-art sprite strip. A CARRY TURN by clean-shaven blond android Marsh from EAST-facing right profile frame 1 to strict NORTH-facing BACK view frame 5. Preserve first and last selected identity/case frames. Redraw only middle frames 2-4 in the same fitted ivory/slate suit, sage shoulders, black gloves and crisp pixel style. Show a smooth right-profile to rear-three-quarter to back rotation; gradually hide the face and carried dark-gray equipment case behind his torso as he turns away. Frame 4 must show mainly the back of hair and back panel; no frontal face in frame 4 or 5. Both hands keep holding the same case at waist. Fixed scale and foot ground line, five complete evenly spaced figures, transparent background, no beard, black eye mask, bulky armor, text, floor or extra objects.

West to north:

> Edit transparent one-row FIVE-FRAME pixel-art sprite strip. A CARRY TURN by clean-shaven blond android Marsh from WEST-facing left profile frame 1 to strict NORTH-facing BACK view frame 5. Preserve first and last selected identity/case frames. Redraw only middle frames 2-4 in the same fitted ivory/slate suit, sage shoulders, black gloves and crisp pixel style. Show a smooth left-profile to rear-three-quarter to back rotation; gradually hide the face and carried dark-gray equipment case behind his torso as he turns away. Frame 4 must show mainly the back of hair and back panel; no frontal face in frame 4 or 5. Both hands keep holding the same case at waist. Fixed scale and foot ground line, five complete evenly spaced figures, transparent background, no beard, black eye mask, bulky armor, text, floor or extra objects.

West to south:

> Edit transparent one-row FIVE-FRAME pixel-art sprite strip. A CARRY TURN by clean-shaven blond android Marsh from WEST-facing left profile frame 1 to SOUTH-facing frontal view frame 5. Preserve first and last selected identity/case frames. Redraw only middle frames 2-4 in the same fitted ivory/slate suit, sage shoulders, black gloves and crisp pixel style. Show smooth left-profile to left-three-quarter to frontal rotation while both hands hold the same compact dark-gray equipment case at waist. No back view or change of facing direction. Fixed scale and boot ground line, five complete evenly spaced figures, transparent background, no beard, black eye mask, bulky armor, text, floor or extra objects.
