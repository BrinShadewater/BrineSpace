# Room riser variation handoff

Updated: September 26, 2026 · Project: BrineSpace · Task: room-specific risers

## Objective and acceptance

47 room-specific riser designs with baked fittings and clear mounting panels.
Owner accepted the earlier taller reactor study's appearance; this full set is
ready for owner review, not yet accepted or installed in production catalogs.

## Accepted decisions and constraints

66-unit rise, 16-unit skirt, actual host-room cap material. Central 92-unit door
bay and two 80-by-32 window/mounting reserves. Fittings stay on ends or low bands.
Windows and working doors remain separate components. Preserve owner layouts.
Owner subsequently requested that end details no longer be covered by the walls.
Native decorated faces now fit x=-184..184, y=-255..-176. Side spans narrow from
154 to 138 units; the central 92-unit door bay stays fixed. Structural returns
are drawn outside the artwork. Raw masters and nominal source guides are unchanged.

## Current state

- `masters/`: 47 untouched transparent generation outputs; `prompts/`: exact briefs.
- `registrations.json` and `manifest.json`: complete database coverage, source and
  prompt hashes, sampling rectangles, alpha records, pending owner acceptance.
- `review/page-*.png`: six light/dark source sheets with reserve guides.
- `review/native-*.png`: six sheets of all 44 ordinary room tops, closed/open doors.
- `review-gallery.html`: searchable gallery with individual native captures.
- `tools/preview_riser_variations.gd` and shared `preview_riser_room.gd/.ps1`:
  native room picker, current props, animated crew, comparison and opening doors.
- `tools/build_riser_v4_review.py`: reproducible registration and source sheets.

Run `pwsh -NoProfile -File tools/preview_riser_room.ps1 -Variations` from the root.
Gallery: http://127.0.0.1:8796/assets/room-risers-v4/review-gallery.html
The local server must remain running. Full captures are in `output/riser-room-preview`.

## Verification

47/47 database IDs covered; all originals decode as RGBA and have transparency.
All six source sheets visually reviewed, including door and mounting reserves.
Native all-room verification passed: 44 usable walking routes, zero failed movement
segments, 91 closed/open/segment captures; real save fingerprint unchanged.
Evidence: `output/riser-room-preview/session-516f663a45144323ba5d29f2cd89c281`.
All 44 native wall-top pairs visually reviewed. BRINE's host renderer initially
added a second socket to the long cap; splitting the cap into contiguous spans
fixed it. Targeted BRINE verification and visual review passed in
`session-561963af2d1e403cbf1fb2833549c457`, with save fingerprint unchanged.
Browser gallery shows 47/47 and search, reserve/background toggles and native
preview links work. Original pilot pause/door-animation checks remain applicable.
After the owner-requested inset correction, all 47 captures and 44 movement
routes passed again with zero clearance failures and unchanged owner saves:
`output/riser-room-preview/session-a6bf87a0d41340b4874f2a14ae39a3ae`.
Lounge and Cold Store full-room visual checks confirm visible end fittings and
unchanged door width. Native sheets/gallery captures were refreshed.
Door alignment/port-mask correction: all 47 designs and 44 internal walking
routes passed with unchanged owner saves in
`output/riser-room-preview/session-2dac5693fccb487c9ecd31b177ab8ae2`.
Cold Store and Galley visually confirm north/south versus south-only openings,
continuous closed side walls, and leaves aligned with their jambs. No new art
generation was needed to fix the preview placement errors.

## Next action

Panel decoration follow-up: `panel-decorations.json` assigns existing style-v2
wall/hull fitting artwork to every room's left, right and centre panels. No new
raster generation. Centre decoration is suppressed for north connections; closed
interior and exposed-ocean states show centre dressing or an ocean window.
Both gallery and native picker select these states; exposure is manual in this
preview, not a station-neighbour implementation. Production decoration remains
paused. Windows and readouts are static art.

Three-room pilots (Reactor, Research, Lounge) preceded all-room validation.
185 state captures, all 44 ordinary-room walking routes, fitting-bound assertions
and save isolation passed in `session-59b921f7136b42df91310a185fec9bfd`.
All six `review/panels-*.png` sheets visually reviewed. Browser ocean mode and
Reactor's empty connected bay verified. Corridor entries remain segment studies.
Owner review and station integration are the next steps.

Owner reviews individual variants. Corridor/corner/T-junction art is a straight
segment study; shape integration remains open. Preview doors now use database
port masks at quarter 0, with low leaves centered at 192 units rather than 184.
They share the wall-top 3-unit lift and existing jamb caps; nonexistent ports
stay walled and northless rooms retain a blank riser panel. This is not a
connected-station test. Owner layouts were preserved. Walking checks verify an
internal route, not passage through every port. Production integration still needs
connected doors, rotations, window components and card review. No export or commit.


## Fitting audit and expansion milestone — September 26

Latest owner request: review perspective, sizing, density and style; improve centering and add more art. Completed 12 new transparent fitting masters/prompts with provenance, assigned across 43 rooms. 39 active fitting profiles supply visible bounds, optical centroids and per-slot size limits, shared by the native preview and gallery. Previous assignments preserved in `panel-decorations-before-fit-audit.json`. Changed renderer: `tools/preview_riser_variations.gd`; calibration utility: `tools/audit_riser_fittings.py`. See `FITTING_AUDIT.md` for density findings and retained coarse-art candidates.

Verification: three room pilots, then 47 designs / 185 captures / 44 internal walking routes, zero clearance failures and unchanged owner fingerprints in `session-39931ab487f248c38c9d7a8685d387c8`. All six refreshed panel sheets visually checked. This supersedes the earlier no-new-generation panel pass. Owner acceptance and live integration remain pending; corridor entries are segment studies. No commit/export.


## Square fitting milestone — September 26

Owner requested square decorations that fill the panels. Six new masters and exact
prompts in `square-fittings/` now dress 43 centre slots, with a 62 x 62 world-unit
limit. Blue side slots retain wide fittings; connected north bays stay empty and
ocean mode keeps windows. Previous assignments preserved in
`panel-decorations-before-square.json`. Updated `panel-decorations.json`,
`fitting-profiles.json`, gallery cache version and `tools/audit_riser_fittings.py`.
41 profiles include retained available wide assets, not 41 unique active placements.
Three pilots followed by full native verification passed: 47 designs, 185 captures,
44 internal walks, zero clearance failures; owner saves unchanged. Evidence in
`session-3b334d6d46814c988ef0bbeca0ac0e60`. Six-family native visual review recorded
in `square-fittings/native-review.png`; six full-room panel sheets refreshed.
Owner visual acceptance and production integration remain next, with no export/commit.


## Style, sizing and perspective polish milestone — September 26

Latest request completed in `polish-v1/`: seven replacement utility fittings and
material edits to square pressure/telemetry, 41 placements across 32 room designs.
All six square families now target 60 units high (66 wide cap); breathing masks
get a 44 x 28 side limit. Changed `tools/audit_riser_fittings.py`, panel assignments,
fitting profiles, gallery cache version and six review sheets. Original sources,
before metadata and nine context captures preserved; exact prompts and provenance
recorded. See `polish-v1/README.md` and `before-after.png`.
Three pilots and full 47-design verification passed (185 captures, 44 internal
walking routes, zero clearance failures, owner fingerprints unchanged), session
`5ecad827671c4bceb4ac7c36736f1630`. All 44 furnished contexts visually reviewed.
Two unnecessary alpha-edit candidates are preserved but unselected; compositing
confirmed their originals' apparent haze lies beneath transparency. Owner review
and live integration remain next. No export/commit.
