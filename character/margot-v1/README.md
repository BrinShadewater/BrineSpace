# Margot V1 runtime pack

Canonical identity: the owner's photo referenced by `../margot-portrait-v1/manifest.json`.
Selected portrait: `../margot-portrait-v2/portrait.png`, copied unchanged to
`../companions/margot-portrait.png`. White/tabby cat, asymmetric muzzle patch,
pale green eyes, moss-green frog bonnet. Companion, separate from architects.

8 clips / 24 frames: idle (2 x 650 ms) and walk (4 x 160 ms), south/west/north/east.
92x92 transparent canvases, ground pivot (46,86), walk stride 0.07 cells. Source
height 28-34 pixels including raised tail/hat. Opposite directions generated
separately; no mirrored frames. Idle depicts a standing pause, not sitting.

Sources and exact imagegen prompts live in `sources/`; hashes are in the manifest.
South idle/walk was reviewed before the other-direction source was generated.
`tools/build_margot_assets.py` slices authored gutters, removes magenta, registers
frames, and packages four pod props without touching the robot packs. Rebuild:
`python tools/build_margot_assets.py` (Pillow and NumPy).

Native rescue, route clearance, movement, pause, picker and Save/Continue checks
pass; contact art reviewed at game scale. The GIF is a directional motion preview;
owner gait/pacing review remains open. No pet survival or special tasks in this pass.

Pet-pod correction: `sources/pods-v2.png` supplies only the occupied pet-pod
region, revised to one clearly curled cat. Both pet states now use 29-pixel width
instead of 34 (about 15% smaller), with a matching reduced collision footprint.
Human pods continue to use the original source; their exported hashes are unchanged.
