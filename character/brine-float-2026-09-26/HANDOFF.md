# Project handoff

Updated: 2026-09-26 · BrineSpace · BRINE suspended float

## Objective and acceptance
Redo BRINE's appearance and suspended animation using the owner's supplied image, translated to the game's painted style and displayed inside the matched tube.

## Accepted decisions and constraints
Adult human proportions, pale skin, swept-back dark hair, cobalt high-neck long-sleeved suit and relaxed suspended pose. Reference is identity/outfit/pose, not photographic rendering. Preserve room layout, tube footprint and separate foreground glass, bubbles and rim layers. No other character assets changed.

## Current state
Imagegen master, cleanup master and proportional 54x168 body export. Original character preserved. Exact initial/cleanup prompts and provenance are recorded. build.py reproduces the export and manifest; RGB outside transparent alpha is intentionally ignored by premultiplied resizing. body-review.png composites the export for silhouette inspection.

preview_room.gd subclasses the core renderer for this isolated study. It replaces only occupant drawing with a 10x24 continuous textured mesh: eight-second sinusoidal body rise/fall, lateral sway, arm/hand drift, trailing legs and very slight hair movement. This is one generated sprite with procedural deformation, not separately drawn animation frames or full skeletal articulation. Rig remains behind the existing glass/front layers and retains power-state dimming. Explicit room identity and floor-profile mapping keep the inherited room context intact.

tools/preview_brine_corners.gd now uses this study. Native screenshot, 32 quarter-second full-room samples, an eight-second GIF close-up and an eight-phase motion review are saved here. Normal native playback updates continuously; GIF is a lower-rate review sample.

## Verification
Body export on gray background, native full-room capture and eight cycle phases visually reviewed. No exterior halo appears in composited export. Body fits inside glass and stays clear of the front rim through captured phases. Asserted eight-second rig endpoint continuity at representative vertices. Native capture passed without script errors; owner save fingerprints unchanged (session-9c1983bbc7f3439d857657862a9899be). Initial transient mesh lifetime error was corrected by retaining the mesh reference and the capture rerun passed.

The original bubbles use their existing separate clock, so the entire chamber composite is not mathematically eight-second periodic. Owner visual acceptance and production integration are pending; no gameplay controller, saved layouts or live character registry changed. Body proportions are more realistic and slimmer than the earlier stylized BRINE; review this intentional reference-driven change beside crew.

## Next action
Review the native animation and GIF. If accepted, integrate the occupant renderer and art in the production core with tests for powered/unpowered states, pause and rendering cache behavior. Current study is self-contained and reversible.
