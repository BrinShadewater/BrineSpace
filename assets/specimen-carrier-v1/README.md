# Specimen carrier handoff

Updated September 8, 2026. Small supporting laboratory prop.

## Objective and constraints

Portable sealed case with restrained inspection window, matte teal-gray shell and dark handle. Intended width 28 units; support it on a counter or cart. A medical wall/cart already existed in the current worktree, so this complementary piece was created instead of duplicating them.

## Current state

`specimen-carrier.png` is a transparent 1484x1060 export. Original source and exact built-in imagegen prompt are preserved. The new `init_material_scale_review.py` command created hashes and scale metadata; actual visual findings were added afterward without owner acceptance.

## Verification

True-alpha source registered at 128; one component decomposed into six polygons. Native Godot source/hash/export checks pass with no script errors. Light/dark review at 28 units shows a compact case; individual tube caps simplify to small marks. Handle sample700,775 has alpha0; window sample600,450 retains near-opaque alpha253. Evidence: `output/specimen-carrier-review.png` and matching log. Existing reference-room raw-image packaging warnings remain, with no packaged acceptance implied.

## Next action

Owner review and supported placement with clearance checks. No transport behavior or carrying animation is installed. Continue additional wall and prop production.
