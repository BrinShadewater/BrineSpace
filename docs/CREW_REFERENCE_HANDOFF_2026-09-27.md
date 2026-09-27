# Crew reference handoff

Updated: 2026-09-27. Brine Space.

## Objective and acceptance
Prepare helmet-off/on design references for four crew members, with current names and roles, shared suit materials and white helmet lights.

## Accepted decisions and constraints
Dr. Maria Veld - Xeno-Marine Biologist. Major Alexander Bill - Operations Officer. Lt. James Branforth - Exo-Hull Technician. Marsh - Android Botanist. Natural facial style follows Marsh. Veld retains Balanced head size and lighter skin; suit uses Bill/Branforth graphite cloth, steel hardware and dark straps with cobalt highlights and full shoulder patches. Owner changed helmet lamps from amber to neutral white.

## Current state
`character/crew-reference-v3/` stores source prompts/hashes, versioned sheets and a review gallery. Front barehead, front/side/rear equipped and face details are included. Old amber candidates are preserved and superseded. Marsh keeps distinct ivory/sage armour; his helmet sheet is a concept proposal, not proof of runtime coverage.

## Verification
Visual review checks identity, visible single face through visor, white lights and department materials. PNG/header/hash and gallery checks are recorded in manifest.json. Static concepts only; no Godot tests or runtime changes. Generated colours are not an exact numeric palette lock.

## Next action
Review the new sheets with the owner. Once selected, freeze material palettes and validate a representative equipped/unequipped sprite pair at actual station scale before generating animation coverage.

Final displayed versions: Bill/Branforth/Marsh white-02; Veld white-03 also corrects rear helmet lamp placement to match shared hardware. All four PNGs, reference links and HTTP gallery checked.

Owner authorized exact colour strips. Four self-contained SVG reference sheets now include 24 labelled sRGB HEX swatches each; shared materials are identical. Editable specification: palette-reference.json; deterministic rebuild: build_palette_sheets.py. Embedded PNG byte equality and SVG validity checked. These are authored new-design targets, not runtime remapping.
