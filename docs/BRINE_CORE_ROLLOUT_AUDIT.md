# BRINE Core rollout audit

## Initial inventory (historical)

The selected base/card is `rooms/brinecore.png`. The grid loader also reads body,
bubble, console, glass and glow PNGs under `brinecore-animation/assets`. The
current overlay method draws body, bubble, glass and glow; the loaded console
sheet is not consumed there. Hash inventory is recorded in
`output/room-rollout/brine-core-asset-inventory.json`.

Visual inspection of the base shows dense dark peripheral machinery and baked
cyan lighting. The current bible instead calls for a symmetrical pearl-white
ceramic/glass chamber, minimal peripheral machinery and a dark framing floor.
The current whole-room bitmap also carries its own walls and doorway gaps.

The remaining work is a registered underwater source revision preserving BRINE's
existing body identity, shared shell/door integration, and explicit component
validation. An exported card hash alone would not prove the body or overlays
render correctly. No base art or character asset was changed during this audit.

## Integrated revision and corrected viewport evidence

The active station renderer and card now use the registered pearl-white chamber
under `rooms/underwater/brine-core`, preserving the existing BRINE body asset.
The engine owns the room shell and operating body drift, bubbles and light cues.
The old base inventory above describes the starting state.

Four-rotation operating, offline, pause and containment checks pass at actual
1280x720 and 1600x900, including independent body, bubble and light comparisons
(49 full frames at each size). Earlier checks captured actual 2560x1440 despite
smaller requested widths; they support only the 2560 scope. Corrected records:
`output/brine-core/viewport-correction.json`, `windowed-1280` and `windowed-1600`.

The 34-identity Windows debug fixture verifies the chamber/card source assets and
BRINE body component, with 51 controlled room arrivals. This is scoped export
and controller evidence, not final aesthetic acceptance or autonomous navigation
coverage. See `ROOM_ROLLOUT_CURRENT_CONTROLLER_EXPORT.md` and the room manifest.
