# Marsh run and carry source prompts

Built-in image generation, September 29, 2026. The edit target for each selected
sheet is `output/marsh-animation-audit/<direction>-<action>-edit-target.png`,
except the selected north sheets, whose edit targets are the corresponding
`north-<action>-reference-row.png`. Source PNGs are preserved under
`character/marsh-<action>-match-v1/sources/`. The first north edits were
rejected for reversing the facing and are retained with `-rejected` names.

## Selected run south

> Edit this existing transparent two-row pixel-art sprite sheet. It is Marsh, a clean-shaven blond male android in an ivory/slate fitted suit with muted sage shoulders, black full gloves, and no helmet. The TOP ROW of six walk poses is the exact identity, face, proportions, palette, line density and sprite style reference; leave that row unchanged. In the BOTTOM ROW, redraw each of the six running poses so it is unmistakably the same clean-shaven Marsh and the same fitted suit as the top row. Keep each bottom-row pose's distinct leg and arm phase, direction facing the viewer, foot ground line, 184x184 cell registration, six separate frames, and one complete figure per cell. Remove the beard, dark eye mask, bulky armor silhouette and dark collar from the old bottom row. Preserve the transparent background and the precise 6-column/2-row grid with no text, borders, shadows, floor, or extra objects. Pixel-art game asset, crisp sprite edges, no smoothing. Do not copy the walking poses into the run row; retain a visibly faster, higher-knee running gait.

## Selected carry south

> Edit this transparent 4-column by 2-row pixel-art sprite sheet. TOP ROW is the exact clean-shaven blond android Marsh identity and fitted ivory/slate suit reference; leave it unchanged. BOTTOM ROW is the same Marsh walking toward viewer while carrying a compact dark-grey rectangular equipment case at waist height with both black-gloved hands. Redraw only bottom row to match the top row's exact clean-shaven face, head proportions, fitted suit, muted sage shoulders, palette, and crisp pixel-art style. Preserve the four distinct stepping phases, case dimensions, hand grip and constant case placement relative to his torso, straight south facing, original foot ground line, and one full figure centered in each of four equal cells. Remove beard, dark eye mask, bulky armor and dark collar. Keep transparent background, precise grid registration, no text, borders, floor or extra objects.

## Selected run east

> Edit this transparent sprite sheet with six columns and two rows. Keep top row of selected EAST-facing Marsh walk untouched. Redraw bottom row only: six phases of EAST-facing running, strict right-facing profile in every frame, NO face toward camera. Same clean-shaven blond male android as top row, identical fitted ivory/slate suit, sage shoulder, black gloves, anatomical-right temple implant, palette and pixel style. Keep six distinct alternating running leg and arm phases, clear foot line, 184x184 cell registration. Remove bottom row's old bulky armor, black eye mask and oversized head. Transparent background, no floor, text, grid lines or extra objects.

## Selected carry east

> Edit this transparent sprite sheet with four columns and two rows. Keep top row of selected EAST-facing Marsh walk untouched. Redraw bottom row only: four phases of EAST-facing walking while holding the same small rectangular dark-grey equipment case with both gloves at waist height, strict right-facing profile in every frame, NO face toward camera. Same clean-shaven blond male android as top row, identical fitted ivory/slate suit, sage shoulder, anatomical-right temple implant, palette and pixel style. Retain alternating steps, constant case/grip and foot line, 184x184 cell registration. Remove bottom row's old bulky armor, black eye mask and oversized head. Transparent background, no floor, text, grid lines or extra objects.

## Selected run west

> Edit transparent six-column two-row pixel-art sprite sheet. Preserve the top row. In bottom row make six distinct fast RUNNING poses of precisely the same clean-shaven blond android as top row, strict WEST-facing left profile in every frame, face pointing left, never toward camera. Match fitted ivory/slate suit and sage shoulder, gloves, clean face, hair shape, palette and outline to top row. Keep original six run phase order, foot registration and spacing. Remove old bulky armor, black eye mask and oversized head. Transparent background; no shadows, labels, floor, extra objects.

## Selected carry west

> Edit transparent four-column two-row pixel-art sprite sheet. Preserve the top row. In bottom row make four distinct walking-while-carrying poses of precisely the same clean-shaven blond android as top row, strict WEST-facing left profile in every frame, face pointing left, never toward camera. His two black-gloved hands grip the same compact dark-gray rectangular equipment case at waist height throughout. Match fitted ivory/slate suit and sage shoulder, hair, face, palette and outline to top row. Keep alternating step phase, cargo contact and foot registration. Remove old bulky armor, black eye mask and oversized head. Transparent background; no floor, labels or extra objects.

## Selected run north

> Create one horizontal strip of SIX game sprite frames, all showing the BACK of the same android in the reference image, as he RUNS AWAY from the viewer toward the top of the screen. Strict rear view for every frame: only back of blond hair, rear suit panel, rear shoulders, back of legs and soles; NO face, eyes, nose, chest or front of case visible in any frame. Preserve exactly the reference identity, ivory/slate fitted suit, muted sage shoulder plates, black gloves, pack panel and pixel-art rendering. Six distinct alternating running leg phases with bent knees and arm swing, even cell spacing, complete figures, fixed world-scale foot registration. Transparent background, no top row, no text, no ground, no extra people or objects. The visible rear backpack panel is the defining feature in ALL SIX frames.

## Selected carry north

> Create one horizontal strip of FOUR pixel-art game sprite frames. Show ONLY the BACK of the same blond android in the reference, walking AWAY from viewer toward the top of screen while carrying a compact dark-gray equipment case IN FRONT OF HIS CHEST. Therefore the case is almost completely hidden by his torso from this rear view, with elbows slightly held forward at his sides; do not draw a case on his back or behind him. Strict rear view in every frame: back of hair, rear backpack panel, back of suit and legs; absolutely NO face, eyes, nose, chest or front of case. Match the exact reference fitted ivory/slate suit, muted sage shoulder plates, black gloves, proportions and crisp pixel style. Four distinct alternating walk phases, fixed foot ground line, evenly separated full figures. Transparent background, no extra people, floor, labels, borders or other objects.

## Rejected north attempts

Run:

> Edit this transparent two-row six-column pixel-art sprite sheet. Top row is the exact approved back view of Marsh, a blond clean-shaven male android in a fitted ivory/slate suit with sage shoulders, black full gloves and no helmet. Preserve the top row. Redraw only the bottom row as six distinct NORTH-facing running phases of the same Marsh with identical back-of-head hair, compact fitted suit, backpack panel, palette and crisp style as the top row. Retain a clear alternating fast running leg and arm cycle, original fixed foot registration and six separate complete sprites. Remove the old bulky dark armor/collar proportions. Exact 6 by 2 evenly spaced grid, transparent background, no shadows, floor, labels or extra objects.

Carry:

> Edit this transparent two-row four-column pixel-art sprite sheet. Top row is the exact approved back view of Marsh, a blond male android in a fitted ivory/slate suit with sage shoulders, full black gloves and no helmet. Preserve the top row. Redraw only the bottom row as four distinct NORTH-facing walking-with-cargo phases of the same Marsh; match his hair, fitted back panel, suit proportions, palette and crisp style to the top row. His hands hold a compact dark-grey equipment case in front of his torso, naturally mostly occluded from the rear. Keep the same cargo through all frames and a clear alternating step, original foot line and four complete centered figures. Remove bulky dark collar/armor. Exact 4 by 2 even grid, transparent background, no floor, text, borders or extra objects.
