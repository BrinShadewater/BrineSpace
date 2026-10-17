# Corner-counter scale and clearance audit

September 26, 2026. Scope: three current square-corner counters. No artwork or owner layouts modified. These candidates need geometry/proportion refinement before treating them as installation-ready.

## Density and style
All three exports declare 2.941176 source pixels/world unit and their export hashes match. The muted painted cabinet finish, readable simple accessories and subdued palette broadly match the earlier counter family. This density convention is not a proof of correct furniture size.

## Perspective and wall contact
The L footprint now follows square-room axes broadly, but the left outer backs still taper. A placement offset cannot make the entire sloped edge flush with a vertical wall. The long return also lacks a clearly resolved inner cabinet face; it reads flatter than the horizontal run. Both issues merit a targeted artwork correction. Do not describe current assets as verified flush wall counters.

## Character-relative size
Read current grid_canvas.gd: crew standing height is cell_size * 0.17, or 65.28 world units for a 384-unit cell. Bill's south sprite has standing-height metadata 148 and pivot (92,172). The static study uses those exact scale values, not arbitrary thumbnail sizing.

At current proposed sizes, total counter canvas width is about 119–120 world units, and visible cabinet fronts read low beside a standing character. This is a visual proportion concern rather than a precise physical-height measurement: sprite art mixes projected floor depth and vertical height. Worktop wings and individual accessories also read compact. For standing work counters, revise cabinet/front proportions and countertop depth with a character comparison instead of uniformly enlarging the entire L footprint.

## Entry clearance
check_scale.py draws a static 384-unit room diagram, using a proposed northwest canvas origin (-182,-186), consistent with the bounds used in tools/lint_room_layouts.gd. It conservatively treats the entire PNG rectangle as occupied. Entry lanes are centered on each side and 106.4 units wide: grid_canvas.gd's 0.225-cell visual door width (86.4) plus 10 units per side, borrowing the navigation blocker padding in the lint tool. This is an explicit conservative study assumption, not a new runtime collision rule. The geometry module's 72-unit opening and navigation door nodes at radius 176 were also inspected.

| Candidate | North lane gap | West lane gap |
|---|---:|---:|
| Utility | 8.78 | 45.08 |
| Reading | 8.78 | 34.88 |
| Refreshments | 10.14 | 33.18 |

All three proposed bounding rectangles stay outside all four entry lanes in this isolated empty-room fixture. The north margin is modest: approximately 7–9% uniform enlargement would consume it. Thus simply scaling up to fix character-relative proportions is not a safe default.

No actual room, placement registration or collision footprint exists for these candidates, so the runtime layout lint would not test them. This is not a navigation pass, wall-contact verification or assurance for arbitrary placement, rotation, other props or different room geometry. Once corrected and registered, run the layout check on their actual target rooms and verify crew movement.

## Deliverables and next action
crew-doorway-study.png shows all three at game-relative scale with Bill and orange entry lanes; scale-checks.json stores measured gaps. check_scale.py reproduces the study. Recommended correction: straighten wall-contact edges, resolve the inner return face and increase working-height readability while preserving the safe overall footprint. Owner artwork review and actual-room placement validation remain pending.
