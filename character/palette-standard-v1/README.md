# Shared character palettes

Installed in source on September 27, 2026, using the owner's requested deterministic remapping with poses preserved. Executable exports have not been rebuilt.

Seven locked palettes use the existing canonical idle references: Bill burgundy/charcoal; Veld cobalt/charcoal/ivory; Branforth orange/charcoal; Marsh ivory/sage; Margot fur/green bonnet; Josh lavender/charcoal; River ivory/sage/amber. Reference PNG hashes and material ramps are recorded in `palettes/*.json`.

## Scope and method

8,575 PNG paths were processed, including selected crew body/equipment, all three companions, and 200 unselected Veld candidate files. The candidate remains unselected. Robot rescue composites were rebuilt from the same corrected robot frames: 24 images changed, with crate pixels and alpha preserved.

Each character uses one deterministic RGB mapping across every frame. Neutral cloth follows a fixed 256-shade reference ramp; coloured materials follow reference chromaticity at the source luminance. Bright cyan lights retain authored values. These are continuous material shade ramps, not an indexed posterization. No frame-specific exposure or palette learning is used. Colour classification is RGB-based rather than hand-painted semantic masks.

Canvas sizes, alpha, transparent pixels, silhouettes, poses, timing, pivots and selection manifests remain unchanged. Existing anatomy differences, softness and neck gaps remain outside this colour pass.

## Review and evidence

Serve the repository and open `character/palette-standard-v1/index.html` (current server: http://127.0.0.1:8791/character/palette-standard-v1/). The viewer compares the canonical idle, frozen original and mapped result across 939 current body states, with shared playback timing. Equipment is included in processing and native checks.

- `review/before-after.png`: seven-character comparison board.
- `review/native/`: native source-game captures and 527 passing checks.
- `review/checks.json`: installed hashes and manifest verification.
- `review/rescue-checks.json`: 52 rescue files checked, 24 changed only within robot bounds.
- `review/helmet-baseline-checks.json`: both idle joins remain exact. The existing helmet fixture fails on eight distinct poses (requires ten), and Branforth removal already differs from reversed equipment. Frozen originals reproduce these failures; this pass did not create them.
- Isolated robot rescue fixture passed. Both Godot runs preserved every real profile file.

## Future exports

Always preserve an unmapped source and apply the existing actor palette once, after extraction and before game installation. Do not learn a new palette for each animation or process an already mapped frame. Example:

```powershell
python character/palette-standard-v1/standardize.py map-file --actor veld --source path/to/original.png --destination path/to/new-mapped.png
```

The destination must be new. Dependencies: Pillow, NumPy, SciPy. Compare the resulting animation against canonical idle, then use the normal asset installation and native review process. Rebuild robot rescue composites after changing robot sources.

For the frozen batch, `prepare` stages from preserved originals and `install` publishes only when all manifests and live input hashes still match the recorded baseline or staged output. Never replace `baseline.json` or the original bank with already mapped art. Unknown edits cause installation to stop. The original bank and mapping record allow a targeted restore, but first check for intervening edits; there is deliberately no blind rollback command. Earlier style audits retain their pre-palette image hashes and are historical evidence, not the new installed baseline.

## Later source correction

The [Veld continuity and walk-tone revision](../veld-consistency-v1/README.md)
explicitly supersedes 130 image hashes and accounts for the newer helmet timing
manifests. The original bank stays frozen. Use the whole-cast colour-lock audit
for current hashes; the viewer now displays current installed artwork.
