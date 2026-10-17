# Matched wreck room artwork

Engineering, medical, habitation and hydroponics wrecks have paired full/stripped
painted sources, overhead equipment, neutral matte materials and modest department
accents. Damage belongs to equipment and floor. Each opaque interior sits inside a
transparent square hull footprint. No light emission is baked into derelict art.

`bake.py` registers significant-alpha outer hull bounds to .04–.96 of one cell;
both stages export at 1024 square. Existing renderer owns tint, interior clipping,
progress crossfade, blocker data and cutting effects. Original paths remain fallback.
The compositor now keeps the original hull perimeter separate from the interior
blend, preventing removed machinery from showing through the final floor fade.
Crossfade timing and total opacity remain unchanged. Native pixel comparison proves
late interiors are independent of the full equipment layer.
Sources, exact prompts and fixed-hash ledger preserve provenance. Alpha and native
stage comparisons establish quality; resolution alone does not establish density.

Native fixture uses existing room cell size at multiple scales, full/stripped and
progress stages, unchanged field data and deterministic repeated frames, plus a
production-fog station. Scratch APPDATA/LOCALAPPDATA protects player progress.
Owner and playable-release acceptance remain separate.
Evidence: 48 source checks, eight byte-identical exports, 89 runtime loader checks
and the existing wreck-clearance paid-rebuild regression pass. Final native review:
`output/wreck-refresh-v1/native-stages-v3.png`; profile gate:
`output/wreck-refresh-20260930-003651/summary.json` (2,774 real files unchanged).
