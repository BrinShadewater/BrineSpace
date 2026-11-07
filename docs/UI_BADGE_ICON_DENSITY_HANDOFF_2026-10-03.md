# Badge icon density handoff

Updated: 2026-10-03 · Project: BrineSpace · Task: Higher-resolution badge icons

## Objective and acceptance
Replace visibly coarse badge icon contours with finer-detail artwork, preserving
recognizable symbols and the muted UI. Native comparison and both badge sheets
reviewed locally; owner visual acceptance pending.

## Accepted decisions and constraints
Scope is badges. Existing global shared icon registry stays unchanged. Existing
128px Archived Data cartridge retained. New redraws remain alongside old masters;
no live screen badge deployment, gameplay changes or save writes.

## Current state
brineui/badge-icons-v3: four generated atlases, 59 transparent 256px exports and
README lineage/prompt notes. scripts/ui_badge_icons.gd (+UID): whole-path registry.
scripts/ui_badges.gd uses the new registry and 20/26px icon extents.
tools/export_badge_icons.gd (+UID): trim/downsample from authored sources, explicit
row gutters avoid neighbouring fragments. tools/audition_badge_icon_density.gd
(+UID): native 64px original/redraw and 26px redraw comparison.
Deliverables: output/ui-badge-icons-2026-10-03/{comparison.png,before.png,after.png,
slicing.json}. Both dated badge audition PNGs refreshed with new icons.

## Verification
Final Godot 4.7.2 native: 182 icon/alpha/density checks + 74 extended and 98 first
badge checks = 354 checks, zero failures/errors, exit 0. Atlas export checked 60
cells and wrote 59 new glyphs without upscaling. Comparison and both full boards
visually reviewed for fragments, fit and clarity. All isolated wrapper runs used
scratch APPDATA, all 2,931 owner non-log files unchanged. Full logs/guards in
output/ui-integration-2026-09-30/badge-density-* (final export/review, extended,
first and UID runs). Initial review exposed adjacent-row fragments; corrected
cuts and final recaptures retained as evidence.

## Next action
Owner visual review; apply accepted density/style to other UI icons when requested.
Some illustrated bevel/highlight details differ from the old pixels; this is a
redraw, not an exact source-preserving resample.
