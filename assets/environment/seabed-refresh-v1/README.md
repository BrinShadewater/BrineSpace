# Seabed refresh pilot — September 29, 2026

September 30 continuation: the shared view now also loads the two original
alternatives in `assets/environment/seabed-variants-v1`. All four procedural
scenery choices use original art; see that pack for current selection and native
evidence. The September 29 counts and unchanged alternatives below are historical.

Three original painted replacements, generated with built-in imagegen using the
accepted September 26 prop board as a material/detail reference. Exact briefs are
in prompts.json. Masters remain immutable; bake.py trims transparent margins and
resamples once to 512px width. Rebuilding requires no generation service.

- Basalt outcrop replaces procedural scenery uw1-188. mb-210 remains unchanged.
- Wreck timbers replace procedural scenery mat-130. mat-131 remains unchanged.
- Overhead ribbon kelp replaces the habitat's kelp-ribbon-kelp texture.

Placement, widths, underwater tint, nearest sampling and existing gameplay remain
consumer-owned. These are decorative sprites, not new collision or salvage. Library
IDs, owner marks and saved placements remain intact. Original bought art is retained.

Source/alpha/hash audit: 3 identities, 11 recorded raster versions including review
evidence, zero unregistered candidates. Runtime environment: 66 checks, zero failures.
Native station: 3 textures loaded, 1600x900 production lighting/fog capture reviewed.
Native density sheet checks all three textures, two scenery mappings and the habitat
binding on pale/dark backgrounds in source color and production tint. Screen widths
are 95px for rocks/timber and 120px for kelp; v2 fixes the viewport content scale so these are physical capture pixels.

Evidence: output/seabed-refresh-v1 and output/seabed-refresh-20260929-214901 (see
the dated summary directory for the density check). Full station process prints its
PASS and exits zero with ObjectDB/resource teardown warnings; no runtime script error.
An earlier attempt caught a concurrent Studio syntax error, later corrected externally.
Every process uses scratch APPDATA/LOCALAPPDATA. Station-run owner fingerprint deltas
were log rotation and large_revision.meta/.bak during concurrent Studio work; an
unchanged-profile claim is unavailable for that interval. First density-run full
fingerprint is unchanged (2745 files). The later v2 interval has concurrent profile deltas; no full-session unchanged claim. No save restoration or owner-file writes.

Selected locally and agent-reviewed; owner visual acceptance and packaged/release
verification remain pending. No release export, commit or push performed.

Next candidates: remaining rock/timber alternatives, overhead cold coral and sponge
clusters, quiet seabed materials, then room-sized basalt and wrecks with their existing
clearance geometry. Do not treat this pilot as replacement of the full environment.
