# Airlock low side-wall preparation banks

Updated: 2026-09-08. Ongoing BrineSpace wall-asset production.

## Objective and direction

Create inward-facing west/east Airlock banks with modest scale and matte finishes,
and refine the directional production workflow. These are two views of one new
low preparation design, not exact side views of the original hanging-suit wall.

## Current state

- `west.png`: left backing, right/east access; 55.85 units wide at 320-unit length.
- `east.png`: right backing, left/west access; 54.88 units wide at equal length.

Both are 887x1774 true-alpha exports. Six bays run along the floor: two packed-suit
drawers, fitting bench, horizontal strapped cylinders, hose tray and helmet cradle.
The sequence remains north-to-south in both views. All original sources, exact
built-in imagegen prompts and hashes are retained in this folder.

West V1 was rejected: it stacked frontal lockers vertically instead of depicting
floor depth. West V2 uses the galley side reference for geometry only and changes
the subject to low preparation furniture. East V1 was newly generated with reversed
working faces; no horizontal sprite was rotated or stretched. The original
hanging-suit installation remains unchanged and separately available.

## Verification

Neutral195 source registration excludes the baked checkerboards without rewriting
sources. The trays have actual backing; hose centers remain opaque intentionally.
Native source/hash/dimension/alpha checks PASS in `output/airlock-side-west-final.log`
and `output/airlock-side-east-final.log`, with no ERROR/SCRIPT ERROR lines. Native
1040x900 light/dark boards and source images were visually inspected, including
drawer openings, tank valves, hose coupling and helmet visor direction. Alpha
corner samples pass. Small hardware highlights remain subordinate at native scale.

The review tool now shows top/middle/bottom material segments for long portrait
banks, with uniform scaling. Full-length native panels remain unchanged. A
horizontal Reactor export regression passes and is pixel-identical to its prior
export. The source/refinement lessons are added to the skill and bible.

## Next action

Select actual room placement and verify wall contact, depth, helmet-fitting access,
pressure chamber clearance and actor routes before installing. No floor collision,
card, gameplay or package binding is changed. Owner aesthetic acceptance remains
open. Continue the active wall-asset production goal; do not count these as two
new room identities or as installed coverage.
