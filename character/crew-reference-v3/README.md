# Crew identity and diving references

Owner direction, September 27: use Marsh's natural facial rendering. Veld uses the same graphite cloth, dark straps and steel hardware as Bill/Branforth, with blue highlights and patches. Her Balanced head size and lighter skin remain the direction.

## Names and roles supplied by owner
- Dr. Maria Veld - Xeno-Marine Biologist
- Major Alexander Bill - Operations Officer
- Lt. James Branforth - Exo-Hull Technician
- Marsh - Android Botanist

## Scope
Four static design-review sheets: bare front, equipped front/side/rear and face-through-visor detail. Existing crew-underwater-v1 front/east/north helmet cutouts provide hardware references. Existing natural-face studies provide identities. Veld additionally references Bill and Branforth for shared materials. Marsh keeps his distinct ivory/sage body; his helmet sheet is an equipped proposal, not evidence of runtime helmet support.

Built-in imagegen produced the sheets. Exact prompts and references are in prompts.json, names in cast.json, and saved output hashes in manifest.json. Generated sheets are not exact numeric palette locks; material colours still require deterministic remapping before animation production. Generated labels do not supersede the owner-provided names above.

No runtime animation, portrait, gameplay role or palette file is replaced. Review helmet fit, visor visibility, back connections and equipment sides before using these as animation masters.

Owner follow-up: helmet-mounted lights must be neutral white, not amber. Initial amber sheets are superseded studies. White-lamp edits use white-lamp-prompt.txt and the corresponding initial sheet; suit instrument lights and coloured patches remain character-specific.

## Exact colour reference strips
The gallery now uses self-contained `*-reference-palette-01.svg` sheets, embedding the existing PNG artwork unchanged with 24 flat labelled HEX swatches below. `palette-reference.json` is the editable sRGB material specification; `build_palette_sheets.py` deterministically rebuilds all four sheets. Shared graphite/straps/steel/ivory/white and character-specific skin/hair/eyes/accent/instrument ramps are explicitly defined. These are authored target colours for the new direction, not the old runtime palettes and not a claim that the generated illustrations have been remapped. Veld hair light means her silver streak; visor tint is a suggested 8 percent overlay. `palette-sheet-manifest.json` records source/output hashes.
