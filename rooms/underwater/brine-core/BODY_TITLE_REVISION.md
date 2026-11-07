# BRINE title likeness revision

Owner requested a tank figure closer to the starting-screen BRINE and more legible in the room. New body-title-v1.png uses cover-character.png as identity reference: brown bob, pale face, blue high-neck suit, bare legs. The original body asset and chamber source remain preserved.

Built-in image generation produced the sprite, followed by a background-extraction request. Generated haze persisted, so the renderer uses an explicit source-space silhouette, including the spaces between arms and torso and between legs. No threshold-based raster cleanup was applied. The final body is taller than the old figure, uses white modulation instead of a dim translucent tint, and sits below the tank cap. Card-v3 is the matching offline bake; card-v2 records an intermediate placement.

Generation brief: Create only the adult BRINE woman from the starting-screen reference, preserving her short chestnut bob, pale face, blue eyes and blue high-neck long-sleeved one-piece suit with bare legs. Full body including feet, suspended upright front-facing pose with arms separated, slight overhead game-camera view, crisp simplified pixel clusters and strong silhouette for small gameplay size. Transparent background; no tank, water, text, logo, glow or scenery. Follow-up requested removal of all surrounding haze while preserving the character.

Validation: title-body-v1 and v2 requested1600 but captured2560; dimension assertions correctly failed. These runs are retained as placement diagnostics only. Final title-body-v3-2560 tests actual2560 with four rotations, host containment, body/bubble/light state comparisons and pause. Current revision has not repeated the Windows export or smaller viewport acceptance.

Final result: exit0, zero assertions, no ERROR/SCRIPT ERROR entries. Native room crop reviewed: head below cap, feet above base, stronger skin/suit contrast.

Follow-up complete: actual1280/1600 state checks and the new34-identity Windows export pass with the revised body. See docs/BRINE_AND_ROOM_POLISH.md.
