# Veld animation handoff

Updated: 2026-09-27. Project: Brine Space. Task: Veld animation consistency.

## Objective and acceptance
Match locked v4 design, palette, proportions and equipment across readable motion.
Owner is on mobile and authorized continuing without localhost review.

## Accepted decisions and constraints
Preserve source art and poses; deterministic colour/registration only. Balanced
head, lighter skin, graphite suit/blue patches, right canisters/left scanner.
Candidates are not production acceptance. No runtime replacement yet.

## Current state
character/veld-animation-pilot-v8 contains 42 frames/seven clips: four directional
idles, two side walks and east inspection. New rear idle has explicit rear material
masks, excluding skin and front ivory. Previous 36 frames remain byte-identical.
tools/review_veld_pilot.gd supports v8, retaining its UID and earlier versions.
New raw front/rear walk sources and prompts are preserved but excluded: front
repeats a raised-foot phase; rear swaps equipment sides and has suspect leg phases.

## Verification
Manifest validator: no errors/warnings. Native player: 160 checks, zero failures,
24 captures. All 2670 real-profile files match before/after isolated APPDATA run.
Inspected generated source sheets, extracted rear frame and native 148/45px capture.
Tiny magenta fringe may remain from source keying; light-background review pending.
Technical checks do not establish smoothness or owner visual acceptance.

## Next action
Correct front/rear walk source phases and rear equipment using targeted generation;
do not mirror. Check keyed edges, loop seams and front/rear distance calibration.
Then expand role/helmet coverage using the same locked design and material ramps.
