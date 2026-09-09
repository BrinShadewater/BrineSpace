# Layout editor performance and tray polish

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance
Improve editor responsiveness and remove backgrounds from tray artwork.

## Accepted decisions and constraints
Preserve original art and room rendering. Transparent thumbnails use the registered
art silhouettes; no raw source-sheet crop is shown while loading. Editing behavior,
undo, personal layouts and saving remain supported.

## Current state
- `scripts/room_layout_editor.gd`: translation-only drag updates avoid rebuilding
  artwork and tray/list contents. Default thumbnail work uses a finite queue instead
  of scanning every tray item every frame. Transparent placeholders keep rows stable
  while loading. Thin outlines replace solid selection/hover blocks behind artwork.
- `scripts/room_asset_library.gd`: removes the unmasked AtlasTexture fallback.
- `tests/profile_layout_editor.gd`: profiles the same fast update used by dragging.
- `tests/test_layout_performance_guards.gd`: verifies full/fast geometry and canvas
  pixel parity, and completed transparent tray previews.

## Verification
Populated native fixture (40 additional props), median drag-update CPU time:
0.933 ms before, 0.058 ms after (about 94% lower). Forced render-inclusive timing
remains about 6.06 ms; startup remains about 0.9 seconds. This is an update-cost
improvement, not a claim of 94% higher frame rate. Evidence: performance-polish-before
and performance-polish-after JSON files under `output/layout-editor/`.

Performance guards pass: nine transparent previews, exact fast/full room pixel and
geometry parity, retained tray selection, recovery/undo limits, safe thumbnail
shutdown, and light parity. Native workflow covers movement/undo and save/recovery.
Visually reviewed `output/layout-editor/polished-tray.png`; no rectangular background
or solid selection fill surrounds the displayed art. Scoped whitespace check passes.

## Next action
Owner review while dragging and browsing asset categories. Startup and overall
render time were not materially improved. Existing raw-image import warnings remain.
