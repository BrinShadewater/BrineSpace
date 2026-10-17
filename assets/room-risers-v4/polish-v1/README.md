# Wall-decoration polish — September 26, 2026

## Objective and accepted constraints

Polish style, physical sizing, perspective and consistency while retaining the
square centre-panel direction, shallow side panels, north-door exclusions and
exposed-ocean windows. Preview-only; preserve owner layouts and all source art.

## Changes

Nine selected assets made with built-in OpenAI image_gen; exact briefs in `prompts/`,
untouched outputs in `masters/`, hashes and assignments in `manifest.json`.
Seven older fittings were replaced: pressure gauges, tool rack, oxygen masks,
key rack, handset, intercom and alarm beacon. Two square designs received focused
material edits: pressure panel and telemetry panel. These update 41 placements
across 32 room designs. Other square designs also receive consistent sizing.

- Perspective: front-facing north-wall attachments, shallow top lips and parallel
  mount edges; no rotation into the floor plane or nonuniform stretching.
- Art style: clearer grouped silhouettes, charcoal powder coat and dull hardware.
  Bright square-panel brass becomes subdued bronze/steel; lamp and screen colors
  no longer imply conspicuous baked illumination. Amber alarm lens remains colored
  static glass; runtime illumination is not implemented.
- Sizing: all six square families target 60 world units high, with a 66-unit width
  cap, preserving aspect. Oxygen masks increase from 27 to 44 units maximum width
  while remaining at most 28 high. Other fittings keep individual physical limits.
- Placement: visible-alpha registration and optical centering shared by native and
  browser renderers. Original wall faces, caps and guides remain unchanged.
- Consistency: clocks, framed pictures, noticeboards, remaining displays and windows
  were reviewed in room context and retained. No claim of one common source pixel
  grid; rendered detail weight was judged beside furniture and crew.

## Verification

Reactor, Research Lab and Crew Lounge pilots preceded full verification. All 47
designs / 185 captures completed; 44 ordinary-room internal walking routes passed,
zero failed segments, fitting bounds contained, and real owner save fingerprints
unchanged. Evidence: `output/riser-room-preview/session-5ecad827671c4bceb4ac7c36736f1630`.
All six refreshed `../review/panels-*.png` sheets visually reviewed. Three corridor
entries remain segment studies. Browser Life Support checked for sizing/materials.

All nine selected masters have transparent exterior (minimum alpha 0) and opaque
or near-opaque surfaces (maximum alpha 254–255). The initially suspected key/tool
haze was RGB under transparent pixels: actual alpha compositing in `source-review.png`
showed clean gaps and edges. Two speculative `*-clean.png` image edits were not
selected because the originals already composited cleanly and those edits altered
presentation. Preserve them as evidence, not active assets.

`before-after.png` compares four room contexts at native capture scale. Previous
assignments, profiles and nine room screenshots are retained beside this report.

## Next action

Owner visual review of the polished gallery. Production integration, neighbour
exposure detection and rotated corridor shapes remain separate work. No export,
commit or changes to the paused production-decoration switch.
