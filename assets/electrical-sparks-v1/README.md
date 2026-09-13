# Electrical sparks v1

Eight generated pixel-art frames: blue-white short-circuit arcs and copper sparks.
Created with built-in imagegen; exact specification is in prompt.txt. Original RGB
source.png is retained. prepare.py removes the baked checkerboard, keeps bright
pixels adjacent to colored arcs, aligns roots and exports RGBA atlases.

- sparks-atlas.png: 1536x1024, 4x2 grid, 384x512 cells.
- sparks-96x128.png: 384x256, 4x2 grid, 96x128 cells; pivot (48,118).
- preview.gif: enlarged dark-background review, 12 fps burst with a quiet gap.
- manifest.json: source hash, registration and frame metadata.

All eight frames are nonempty and fit their cells. Full-size cleanup visually
reviewed. Integrated in scripts/fire_effects.gd for burning reactor, biomass digester,
galley and salvage workshop. Eight frames at 12 fps every 2.8 seconds, with
room-specific phase. Simulation time freezes bursts on pause. Visual effect
only; no additional electrical damage or spread rules.
