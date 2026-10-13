# Rounded boulders and pale driftwood replacement

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Continue environment replacements with original art consistent with installed
overhead basalt and wreck timbers. Both remaining procedural scenery variants
are installed and agent-reviewed at source/native density and production lighting.
Owner visual acceptance remains separate.

## Accepted decisions and constraints
All four procedural scenery choices now use original paintings. Existing scenery
families, positions, widths, tint, nearest sampling, saved geography and decorative
behavior remain unchanged. Bought library assets/records and owner marks retained.
No collision, salvage yield, resource or gameplay changes; no commit/export.

## Current state
New pack `assets/environment/seabed-variants-v1`: rounded-boulders v1 and
pale-driftwood v2 selected, four preserved generated masters, exact built-in
briefs and immutable manifest hashes. Isotropic alpha-margin bake produces two
512px-wide runtime sprites. Rejected/unselected wood studies are retained.
Shared `seabed_refresh_view.gd` names whole runtime paths; `site_scenery.gd`
maps mb-210 and mat-131 to the new sprites alongside earlier original variants.
`tests/review_seabed_variants.gd` plus UID and `tools/verify_seabed_variants.py`
provide isolated native captures and source-loading/binding/occupancy checks.

## Verification
Source audit: 2 identities, 6 recorded raster versions, zero unregistered
candidates; immutable rebuild matches runtime hashes. Git LFS attributes and
scoped diff whitespace checks pass. Three native station zooms (.25/.45/.65),
two centred close-ups and a four-family 95-physical-pixel density sheet reviewed
on light/dark surfaces in source colour and production tint. Decorative sprites
stay below station geometry; the supplied fixture does not establish paid gameplay.
Native review: zero failures. Initial fixture assumed a scenery list in authored
mode and failed; corrected by explicit supplied scenery, then both reruns passed.
Final evidence: `output/seabed-variants-20260930-093809/summary.json`.
Scratch APPDATA/LOCALAPPDATA throughout. Earlier passing interval compared all
2,924 owner files unchanged; final close-up interval changed two log files only,
attribution unknown. No progress/checkpoint/layout delta, no restoration.
Selected wood master still has minute coloured edge pixels; native 95px review
shows no visible red fringe. Preserve this distinction from perfect extraction.

## Next action
Owner review of `output/seabed-variants-v1/native-density.png` and station
close-ups. Audit current harvest-site graphics or remaining habitat materials
before the next replacement batch; legacy paths alone do not prove bought art.
Release packaging remains a separate workflow.
