# Shell shoal terrain study

Current status: integrated as a fixed decorative patch centered at cell (10,16),
with radius (3.5,3). Three selected textures and five unequal prop placements use
the existing feathered world-space ground mesh. The ledger audits the renderer's
explicit source registry. Earlier study notes below preserve revision history.

`tests/playtest_shell_shoal_station.gd` verifies three loaded textures, captures
1280/1600/2560 windows with a room on the patch, and checks unchanged occupancy and
resources. Evidence: `output/shell-shoal-station-v1.log` and
`output/shell-shoal-station-v1/group-1-1600.png`. The 1600 capture was visually
reviewed. Owner approval and a new packaged export remain pending.

Packaging follow-up: `output/environment-export-v4/` now verifies this pack in an
isolated Windows debug executable. All 73 library PNGs match source hashes and
dimensions; all 49 runtime textures load. The exported shell-shoal habitat capture
was visually reviewed. Owner art approval remains separate.

One original ground source begins a new seabed material family: cool grey-beige
sand, shallow broken ripples and embedded shell chips. The overhead projection
and restrained natural materials fit the existing seabed sources. Pale chips
are denser than plain silt and need station-scale contrast review.

The source is preserved unchanged with its exact prompt and immutable hash.
`manifest.json` selects the candidate for this study, not the live renderer.
`output/shell-shoal-source-audit-v1.json` records actual dimensions and mode.
No seamless edge claim is made. Repeated-world sampling, mirrored-pattern review,
native station integration remain pending. The prior seven-pack
export evidence predates this study and does not cover it.

Next review: compare normal and mirrored repetition at the same world scale as
existing ground, then evaluate shell highlights under the station's runtime tint.
Keep shell grit embedded in the ground; larger intact shells belong to separately
registered scenery, with no implied resource yield or obstruction.

## Cobble source and native repetition review

The second source adds five unequal rounded limestone cobbles with embedded shell
scars. Its 1254-square RGBA original has verified transparent exterior pixels;
the ledger preserves its hash and exact brief. It is decorative scenery.

`tests/playtest_shell_shoal.gd` loaded both sources and captured a 1600x900 Godot
sheet at four cells per ground repeat and 0.4 cell per cobble cluster. The log is
`output/shell-shoal-native.log`; the image is
`output/shell-shoal-v1/repetition.png`. The cobbles remain subtle at this scale.
Ground mirroring exposes conspicuous diamond bands. Do not promote this ground
unchanged to broad live regions: revise the directional bands or review a smaller
authored patch. The script's PASS confirms loading and capture, not aesthetic
acceptance. A station-overlap review remains necessary.

## Ground revision v2

The selected ground is now `shell-hash-ground-v2.png`: disconnected sparse shell
grit replaces the long directional bands. The same Godot repetition fixture
produced `output/shell-shoal-v1/repetition-v2.png` with no conspicuous diamond
bands on visual inspection. The tinted surface stays quiet at four cells per
repeat. `output/shell-shoal-native-v2.log` records successful loading and capture;
`output/shell-shoal-source-audit-v3.json` verifies all three preserved sources.
The original ground remains in the ledger with its rejection reason. This review
selects v2 for the study; station integration and owner approval remain pending.

## Shell debris

`shell-bed-v1.png` adds a transparent scatter of worn shell halves and fragments.
The native sheet now includes it at one-third cell width beside 0.4-cell cobbles;
dark interiors distinguish the shells from rounded stone without enlarging them.
The generated scatter differs from the requested exact seven-piece arrangement;
piece count is not a gameplay requirement. Its original source and prompt remain
preserved, with alpha and hash evidence in `output/shell-shoal-source-audit-v4.json`.

The three-source capture is `output/shell-shoal-v1/repetition-v3.png`, with loading
and capture evidence in `output/shell-shoal-native-v3.log`. Raw-image export warnings
remain; this checkout preview does not extend the previous packaged-build evidence.
The prop adds no salvage, collision, fauna or resource mechanic.
