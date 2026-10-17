# Room riser variations

The owner's accepted reactor study establishes the 66-unit face and reuse of the
existing room's top-cap artwork. This collection gives each of the 47 database
rooms its own baked wall fittings, preserving quiet north-door and window panels.
It is an art and native-preview pack; production room catalogs remain unchanged.

## Review

The latest style/scale pass is documented in `polish-v1/README.md`, with nine
polished fittings and a native `polish-v1/before-after.png` comparison.

Panel dressing uses the existing reviewed `wall-dressing-style-v2` and
`riser-wall-kit-style-v2` sprites, curated for all 47 rooms in
`panel-decorations.json`. These are separate conditional layers over the baked
wall faces. The subsequent fitting audit added 12 new front-facing fittings across
43 designs. `fitting-profiles.json` supplies visible bounds, optical anchors and
individual size limits. The latest `square-fittings/` addition supplies six
near-square centre designs across 43 rooms, now calibrated to 60 units high
with a 66-unit width limit;
wide fittings remain in the shallow side panels. See `FITTING_AUDIT.md` and
`square-fittings/README.md`.

Native and browser previews have three north-wall states: room door layout
(a north port represents a connection), closed interior (all panels decorated),
and exposed ocean (framed painted ocean views). A connected north door always
suppresses centre decoration. Exposed ocean removes the north connection and
uses windows. The native viewer also toggles panel dressing on/off.
Exposure is a manual preview setting; station-neighbour detection is not installed.
Windows are static artwork. Production's paused decoration switch remains unchanged.

- Interactive gallery: `review-gallery.html`, served from the project root.
- Printable light/dark comparison sheets: `review/page-*.png`.
- Native interior/ocean panel comparison sheets: `review/panels-*.png`.
- Native room picker: from the project root, run
  `pwsh -NoProfile -File tools/preview_riser_room.ps1 -Variations`.
- Add `-Verify` to capture every available design with automated movement checks.

The launcher copies room layouts into a unique scratch save directory and
fingerprints the real save folder before/after. No player progress is loaded.
Native preview keys: Tab compares original/new, D opens/closes doors, Space pauses
walking, S saves a capture. Previous/Next and the room picker change room; the
reservation button outlines the door bay in amber and window panels in blue.

Corridor, corner and T-junction entries are **straight segment art studies**, not
completed installation on their different hull shapes. Other rooms show quarter 0
with the current layout, current crew sprites and available accepted clean prop
exports. Preview openings now use each room's database door layout at quarter 0.
Side and south leaves sit on the actual 192-unit wall centerline with the same
3-unit screen-up lift as the wall tops. Existing jamb caps frame those openings.
The raised north doorway is shown only for rooms with a north port.

## Geometry and sources

- Face rise: 66 world units above y=-192; skirt continues 16 units to y=-176.
- Rendered segment spans x=-200 to 200, including end pieces.
- North-door reserve: x=-46 to 46, full face/skirt height, for a 72-unit aperture.
- Window/mount reservations: x=-152 to -72 and 72 to 152; y=-249 to -217.
- These are reserved mounting areas, not holes or installed window components.
- Ordinary room top caps reuse the host's `draw_wall` and `draw_cap` functions.
- Owner fit correction: ordinary-room artwork fits x=-184..184, y=-255..-176,
  below the cap and inside the side returns. The central 92-unit bay stays fixed;
  each side compresses from 154 to 138 units, preserving all baked end fittings.
  Source/gallery guide coordinates above remain nominal; native window guides
  follow the fitted panels at approximately 72-by-31 units.
- `registrations.json` names whole source paths and source sampling rectangles.
- `masters/` preserves untouched transparent image-generation outputs;
  `prompts/` preserves exact prompts and `briefs.json` names all intended subjects.
- All generations use `engineering-v2.png` from the September 26 riser study as
  geometry/subject reference, and `docs/art-style-reference-2026-09-26.png` as
  accepted material/style reference. Reference roles are not interchangeable.
- `manifest.json` records SHA-256 hashes, alpha counts, coverage and acceptance.
- `preview-props.json` maps the already-accepted Desktop exports into the preview
  texture cache; it does not alter installed art, registrations or owner layouts.

Regenerate registration records and sheets with `python tools/build_riser_v4_review.py`.
That tool samples originals for presentation; it never changes the source artwork.
Further integration needs the normal connected-door, rotation and card checks.
No export, commit, publishing or owner acceptance of this full set is implied.
