# Remaining rock and timber variants

Original overhead painted rounded basalt boulders and pale driftwood replace
procedural scenery `mb-210` and `mat-131`. The earlier basalt-outcrop and
wreck-timbers variants remain installed, giving all four scenery choices original
art. Bought library records, pixels, owner marks and saved placements are retained.

Exact built-in briefs: prompts.json. Four immutable masters and two runtime
exports are registered by SHA256 in manifest.json; choices are explicit.
Selected driftwood v2 retains minute coloured edge pixels in its full master;
the 95px native density review has no visible red fringe. V1 and the alternative
v3 remain unselected. The cleanup request improved edges but did not eliminate
every coloured source pixel; don't claim source-perfect extraction.

`python assets/environment/seabed-variants-v1/bake.py` checks master hashes,
trims fully transparent margins and resamples isotropically to 512px width.
No paint, colour grading, stretching or baked underwater tint. Production widths
stay 0.20–0.38 cells for rocks and 0.35–0.55 for timber; quiet tint/fog and nearest
sampling remain consumer-owned. No new collision, salvage or resource behavior.

Runtime paths are named whole in seabed_refresh_view.gd; site_scenery.gd binds
the existing scenery IDs. The source audit uses tools/audit_environment_pack.py.
Native verification uses tools/verify_seabed_variants.py with scratch profiles:
three station zooms, close-ups of the two new variants and a four-family native
95px density sheet on pale/dark backgrounds, before/after production tint.
Output: output/seabed-variants-v1. Agent review is separate from owner acceptance
and release packaging; no export/commit/push.
