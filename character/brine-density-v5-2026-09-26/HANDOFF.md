# Project handoff

Updated: 2026-09-26 · BRINE color and density correction

## Objective and acceptance
Address owner's finding that BRINE's color and pixel density do not match existing animated crew, retaining slim build, recognizable identity and blue suit.

## Accepted decisions and constraints
V4 body is identity/shape reference; current Bill and Veld sprites supply shading/material references. Do not return to bulky proportions or charcoal suit. Existing float loop, tube, room and original assets stay intact.

## Current state
Imagegen repaint reduces electric-blue highlights, warms neutral skin midtones and simplifies shading. Exact prompt/provenance in production.json. Transparent body is 45x139; build.py preserves aspect and uses premultiplied alpha. Body still draws at h=168 source-coordinate units, so world height is unchanged. Preview body tint changed from 0.90/0.95/0.98 to white; original foreground water tint remains.

## Verification
Crew renderer uses 65.28 world units / 148 native standing pixels. Chamber body height is 168 * 104 / 286 = 61.09 world units at the current unscaled chamber width. At that height 139 pixels gives 2.275 pixels/world unit, within about 0.4% of crew 2.267; prior 168 export gave 2.750. This calibration applies to current preview chamber scale, not arbitrary future Studio resizing.

Body composite, normalized-height comparison and eight native motion phases reviewed. Palette is calmer; BRINE still has less surface detail than armored crew because costume is simple and exposed skin remains smoother. Owner visual acceptance is not inferred from numeric density. Comparison board normalizes visual heights and is a style aid, not a world-scale screenshot.

Native 32-frame capture and rig endpoint closure passed without script errors; owner save fingerprints unchanged (session-9e683098c53348dca97eb1c5450299f7). Shared launcher now selects v5; earlier versions remain. GIF is four samples/sec of the continuous eight-second rig.

## Next action
Owner review at native size. Preview-only; no production registration or room save changes. Additional texture/style refinement may still be needed based on owner judgment.
