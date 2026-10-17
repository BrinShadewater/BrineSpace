# Project handoff

Updated: 2026-09-26 · BRINE cleanup and smoother float

## Objective and acceptance
Preserve the owner-preferred v5 likeness/colors and improve cleanup and animation smoothness.

## Accepted decisions and constraints
Keep slim proportions, muted blue suit, 139px export height and existing in-world height. Preserve previous versions, tube and owner layouts. No production installation.

## Current state
Conservative imagegen cleanup of v5: facial/hair edges, hand readability and suit folds. Prompt and provenance in production.json. Output remains 45x139. build.py reproduces alpha-aware proportional export and hashes.

preview_room.gd softens limb displacement and replaces the arm spatial sine/clamp envelope with smoothstep ramps. Eight-second continuous body motion retained with slightly reduced sway/bob/hair amplitudes. Whole-body motion uses the existing mesh approach, not newly drawn frame-by-frame animation. Nearest texture filtering remains to preserve sprite detail; small raster steps may still occur at native scale.

Preview captures increased from 32 at 4 fps to 200 at 25 fps over eight seconds. build_preview.py creates a shared-palette GIF without dithering, avoiding independent palette flicker. Capture PNGs now contain the chamber region; full room-preview.png is separate.

## Verification
Native-size body, full room capture and eight phase sheet reviewed. Native 200-sample run and endpoint rig continuity assertion passed without script errors; owner saves unchanged (session-2d70fbf679cf413283c2da467071dad9). Both structural motion and review sampling were improved; no claim of new skeletal articulation. Existing bubble clock is not exactly eight-second periodic. Owner review remains necessary for perceived smoothness.

## Next action
Review updated live preview and 25 fps GIF. Production migration remains pending. Shared isolated preview launcher selects this revision.
