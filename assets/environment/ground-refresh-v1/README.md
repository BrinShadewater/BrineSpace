# Matte seabed and basalt refresh

Original neutral matte silt and basalt top surfaces replace older ground sources.
Both export at 1024 square: silt spans three cells; basalt uses the existing mirrored
four-cell world UV field. Color tint and fog remain consumer-owned. Source masters
are opaque and unchanged; no seam or color repaint is performed in the bake.
Existing silt tiles use explicit alternating UVs instead of negative rectangles,
retaining identical world bounds while making the intended reflected joins explicit.

Tube worms export into a transparent 512-square footprint, preserving aspect inside
the existing square scenery draw. That binding belongs to legacy scenery; current
composed sites bypass it. No worms are added to current site placement.

`prompts.json`, immutable masters, `bake.py`, hash ledger and isolated `verify.py`
preserve provenance and reproducibility. New sources use explicit paths through
`scripts/environment_art.gd`; failures are cached and retain original source fallbacks.
`tests/preview_ground_refresh.gd` and its UID check selected bindings, placement
determinism, read-only drawing and paused-frame equality, then capture a real fogged
station. Its free solar arrays are dedicated art fixture setup, not paid-run evidence.
Runtime loader covers all 89 selected environment textures. Native comparison and
station captures live in `output/ground-refresh-v1/`. Owner/release review is separate.
