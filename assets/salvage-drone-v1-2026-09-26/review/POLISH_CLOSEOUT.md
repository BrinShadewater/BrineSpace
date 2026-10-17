# Salvage artwork and motion polish review

September 26, 2026. Agent review; owner acceptance remains separate.

## Artwork, perspective and density
Compared all eight open/closed headings on dark and light backgrounds, the
accepted v10 identity, the Construction/Mining fleet board, and existing native
room/Bill sizing evidence. The viewport, paired support arms, single retrieval
claw, steel hull and muted cyan accents retain the Salvage identity. No source
redraw, recolour, enlargement or bounding-box normalization was applied.

Shared display scale is 0.34: 2.9412 library pixels per world unit. All selected
source images are reduced to 0.335-0.455 of their source dimensions. Opaque native
widths span 116.96-125.12 world units; the south baseline remains 120.36. Side views
are vertically foreshortened (93.16 versus south 110.5); diagonal poses are painted
approximations of the shared camera, not exact projections of a shared 3D model.
At native size the major panels, arms and claw remain readable, with consistent
outline/detail scale and no observed light-background matte fringe.

Evidence: polish-density.json, polish-native-directions.png, directions.png,
closed-directions.png and fleet-scale.png. Colour statistics are diagnostic only;
identity and material findings come from visual review.

## Repairs
- Export shutdown previously multiplied time by a decreasing speed, making the
  rotor reverse before stopping. Rotation now integrates angular speed; shutdown
  coasts forward to a fixed phase. Start, stop and startup also integrate ramps.
- Phase zero previously resized rotor patches through a 64px intermediate even
  without rotation. All eight resting frames now match their registered base
  artwork byte-for-byte, avoiding unnecessary softening and idle/rest changes.
- Preview startup/power-down ramps are frame-rate independent and retain phase.
  Power-down from full travel settles within 1.5 seconds.
- Stop uses the bible's red stopped-state lamp. Work/operational remains blue,
  charging yellow, power-off fades away.
- Added synchronized motion review and native dark/light board links. Audit
  canvases retain 250 CSS pixels for 250 backing pixels, avoiding accidental
  extra scaling of the native-size comparison.

## Verification and scope
The authoritative final export check is full-validation.json; polish-validation.log
records this run. It checks all 92 clips, body/cargo atlas parity, connected alpha,
bounds, cargo joins, 480 rotor phases and seam steps, exact resting pixels, and
monotonic spin samples with stopped shutdown endpoints. motion-checks.log includes
frame-rate independent power ramps from both rest and full rotor speed.

Browser motion-review coverage and console evidence are recorded separately in
polish-browser-checks.json. Review/motion-audit.html compares authored exports;
the main preview exercises continuous controller transitions. Neither is Godot
integration, gameplay clearance validation, or owner artwork acceptance.

Changed: build_full.py, motion.mjs, test_motion.mjs, validate_full.py, regenerated
full exports/manifest, index.html, polish_audit.py and review assets/page. Source
hashes and accepted world scale are unchanged. Pre-polish manifest and builder/
controller copies remain in review for comparison. No owner saves were touched.
