# Higher-density badge icons v3

October 3, 2026. Built-in imagegen redraws of the four hull-ui-v1 source atlases,
with finer illustrated contours and shading. Not an upscale of the 96px exports.
59 new transparent 256px exports; the accepted 128px v2 Archived Data cartridge
remains the badge for that resource. The unused old archival chip redraw stays
in the source atlas only. Original icon sources and older exports are preserved.

Live integration: scripts/ui_badges.gd and shared widgets use the new
scripts/ui_badge_icons.gd registry. scripts/ui_icons.gd now selects 52 distinct
256px redraws for resources, actions and navigation throughout the game. The
seven accepted v2 draft-hand utility icons and v2 Archived Data cartridge remain
selected. The density audition explicitly loads the legacy exports for its
before comparison. Native PNG imports are generated from an isolated minimal
project; the runtime registry also supports raw PNG loading.
Display extents: compact 20px / standard 26px, within existing 28/36px badges.
Regenerate with tools/export_badge_icons.gd in scratch APPDATA. The exporter
cuts the authored row gutters (rather than assuming perfect grid spacing),
trims transparent bounds and downsamples directly to a 224px maximum silhouette
on a 256px transparent canvas. It never enlarges source pixels. Whole runtime
paths are in the registry. Raster files retain repository Git LFS attributes.

Source lineage (built-in imagegen):
resources: exec-0fa4fecb-b2bb-45dc-9b45-080153f6cdf6.png
hazards-actions: exec-13d8132a-0eb6-4e4d-b59e-a8baf79ad52c.png
navigation-utility: exec-9e2016ed-bd88-4845-81b5-0e1827c24465.png
draft-crew: exec-569e15c0-b9b7-4545-9586-dd7e20cdbcab.png;
transparency pass: exec-e24203a0-7cf5-4024-a840-4a6ab43435bf.png.
The crew source appears to have a backdrop in the rendered preview, but the
exported alpha is transparent; native gutter checks and preview confirm this.

Prompt direction: preserve every symbol, reading order and grid membership;
redraw coarse pixel steps as finer anti-aliased illustrated contours and subtle
shading; matte gunmetal, muted green-blue, cream/ochre and original accent colors;
recognizable at 24px and detailed at 64px; transparent background, no labels or
extra icons. Follow-up crew pass requested removal of backdrop/glow while
preserving all sixteen glyphs. The redraw also changes some bevels/highlights;
live integration requested by the owner; final visual acceptance remains theirs.

Native before/after comparison, slicing report and badge previews:
output/ui-badge-icons-2026-10-03. Rights: project NOTICE.md.
