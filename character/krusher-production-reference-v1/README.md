# Krusher Dom production references

System Administrator · AI & Robotics · matte muted grey-cyan markings.

- `character-sheet.png`: four directions, bare and helmeted, with display size references.
- `head-registration-sheet.png`: separate direction heads, native dimensions, idle neck anchors and cyan target.
- `equipment-reference-sheet.png`: terminal and cartridges, source density, idle placement and far-side visibility.
- `terminal-key-pose-sheet.png`: the current west raise/type/lower sequence with every declared hold.

These sheets use the existing candidate sprites without painting new anatomy. They are production references for the reusable Bill-body trial. The original concept remains in `character/krusher-concept-v1/concept-04-krusher-dom.png`; the runtime-sized sprites are the reference for pixel density and registration.

Use `reference-manifest.json` to locate exact source files and hashes. Rebuild with `python character/krusher-production-reference-v1/build_references.py`, then run `validate_references.py` in the same folder. Source images remain in their existing packages. The sprites are not selected in the normal game.

## Reuse rules

Keep source gait, durations, foot pivot and suit shading. Apply the `#527C80` target by source luminance. Fit each head by its neck, retaining per-frame head registration. Do not mirror asymmetric heads or equipment. Walking equipment follows the recorded torso translation; gloves and cuffs draw in front.

The west terminal bare/helmet pair is compatible below source row 62. This boundary has only been proved for that family. Other directions, actions and body families require their own checks.

Bill is the demonstrated base for Krusher. Bill, Veld, James and Marsh are the proposed future body families, selected for likeness and build; Veld is the owner's suggested default for female characters. Compatibility and animation coverage for a new derivative must be established from that family's actual sources before reuse.

## Current limits

Four-direction idle/walk and west terminal action are packaged. Native timing and contact-sheet evidence exists in the related review folders. Continuous artistic motion acceptance remains separate. Expression changes and authored turning inbetweens are not supplied here. These sheets do not establish game integration or owner acceptance.
