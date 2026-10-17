# Metal corner counter audit — 2026-09-26

Scope: six metal variants, reviewed at native export size against the refined corner family and locked game-size references sp-science-extra3-3, sp-recreation-extra3-5 and sp-engineering-extra3-3. No artwork modified.

## Findings

| Area | Assessment |
| --- | --- |
| Perspective | Consistent within this corner family. Straight horizontal backs and vertical outer returns fit square room walls visually. Top/front proportions are similar across all six. The long inner return remains a very narrow side plane, so the L reads flatter than the accepted standalone cabinets; do not call this a complete camera match. |
| Art style | Neutral steel, charcoal and modest accent colors fit the bible. Objects remain legible and the computer reads as a contemporary/futuristic tablet console. Cabinet outlines and continuous pale worktop rims are more uniform than the accepted painted references. Light worktops can read as mottled stone rather than steel. |
| Detail density | Comparable native-size accessory readability; no obvious outlier in the six. Pump ribs, hose coils and dive equipment are the busiest regions. All masters are 1380 x 1140; exports use proportional premultiplied-alpha resizing, not stretching. Matching resolution alone does not prove world-scale density. |
| Consistency | All six canvases are 353 px wide. Heights vary 285–292 px (about 2.5%); content boxes vary 345 x 277–284. Records is shortest, dive gear tallest. This is modest generated geometry drift, not a deliberate size class. Three left and three right orientations are preserved. |

## Checks and limits

check_exports.py passed for six RGBA exports, canvas limits and conservative static entry envelopes. At proposed 0.34 world units per source pixel, canvas width is 120.02 world units; heights are 96.90–99.28. This is an export convention, not proof of appropriate working height relative to crew. No native room placement, depth sorting or interaction test was performed on these six. Prior corner preview evidence covers different assets only.

## Recommended correction scope

Keep footprints, orientation, object choices and overall colors. Soften continuous bright rims and excessively uniform cabinet outlines; use subtle broad directional metal shading without adding shine or fine scratches. Clarify the inner return plane without moving exterior wall-contact edges. Align repeated cabinet dimensions to a shared reference if interchangeable placement is required. Then compare with crew in the existing native preview before marking runtime scale/perspective accepted.

Overall: coherent variations suitable for review, with a targeted material/edge and return-depth refinement still worthwhile. No need to regenerate the object concepts or enlarge all props.
