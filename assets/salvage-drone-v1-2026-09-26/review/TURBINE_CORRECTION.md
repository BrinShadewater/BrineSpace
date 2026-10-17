# East/west rear turbine correction

Owner correction: the rear turbines pointed toward the camera in east/west views.
Selected source: `sources/east-west-v3.png`, built-in image edit of v2. Original:
`C:/Users/Alex/.codex/generated_images/01a0e034-2489-7d20-95c0-c7aeb873b585/exec-e3e7a138-223c-4b08-b125-9539befb8756.png`.
Transparent 1774 x 887 sheet; prior source preserved. Exact prompt:

> Edit this exact two-cell transparent Salvage drone sprite sheet. Correct ONLY the two LARGE REAR TURBINE NACELLES on each drone: left sprite faces EAST/right with claw at right, right sprite faces WEST/left with claw at left. Currently the large rear turbines have circular fan faces pointing UP toward camera; this is WRONG. Redraw these large rear nacelles with their cylinder axes strictly HORIZONTAL in the image and PARALLEL TO THE DRONE'S FORE-AFT TRAVEL DIRECTION, like the smaller horizontal thruster pods already above/below the hull. East drone: both rear cylinders run LEFT to RIGHT, with fan openings seen as NARROW VERTICAL ELLIPSES on their RIGHT ends, pointing RIGHT toward travel. West drone: both rear cylinders run RIGHT to LEFT with narrow vertical elliptical fan openings on their LEFT ends, pointing LEFT. No upward-facing round fans. Show the side of each cylindrical housing from the unchanged overhead game camera. Keep each rear nacelle attached in its existing rear corner area; do not move the hull or change its size. Preserve ALL other artwork, both support arms, open claw, viewport, hull panels, small thrusters, texture, muted cyan/steel palette, outline thickness, exact two-cell composition and generous transparent margins. Same sheet dimensions. No text, no background, no extra parts.

Rear nacelle axes now run horizontally along travel. Their forward fan faces are
occluded beside the hull in this source; removed the old upward-facing fan masks
so the rotor layer does not spin the new cylinder walls. The two exposed smaller
thrusters retain their registered rotation. Hull anchors, claw rig, scale and
timings remain unchanged. Rebuild scope: 13 clips each for east and west.

Verification: `validation-east-west.json` passes all 26 changed clips / 1,920
body and cargo references, 120 rotor phases, atlas parity, bounds, connected
silhouettes, claw/cargo joins, exact resting pixels and source hashes.
`turbine-scope.json` confirms the 66 other clip definitions and six heading
registrations are unchanged. Browser east idle and west swimming reviewed at
enlarged/native size with no console warnings/errors; `turbines-east.png` and
`turbines-west.png` retain evidence. No controller or gameplay changes.
