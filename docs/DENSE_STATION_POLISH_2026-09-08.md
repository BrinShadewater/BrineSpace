# Dense-station rendering polish

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance

Owner requested another polish/optimization pass. Focus: the previously measured
49-room rendering bottleneck, preserving current water and detailed door visuals.

## Accepted decisions and constraints

No gameplay, leak-rate, oxygen, pump or repair-cost changes. Preserve authored room
art, shared door ownership, crew depth ordering and current personal layouts.

## Current state

- `scripts/grid_canvas.gd`: replace a full extra cell of room-culling padding with
  0.28 cell (~108 canonical units), retaining space for tall props, crew and risers.
  This avoids preparing/drawing a large off-screen room ring in dense overviews.
- Door aperture results share a symmetric per-render-frame cache across surface
  passes. A new engine frame invalidates it; physics/input always read live state.
- `scripts/room_flooding.gd`: active jobs now say "Repair" rather than "Repair queued";
  existing waiting/travelling/welding status explains the current phase.
- `tests/test_flood_rendering.gd`: seam symmetry, new-frame invalidation and physics
  bypass checks supplement existing geometry, live-layout and material-cache checks.

## Verification

Flood rendering checks pass. Native wet-door integration passes for real aperture,
closing effects and pause. Culling enabled/disabled viewport captures are byte-
identical at zoom 0.22 and 0.45 (1160x480 pixels, including screen edges). Native
zoomed view reviewed. Scoped whitespace check passes.

Same 49-loaded-room fixture, 30 warmup / 90 measured frames per mode. Baseline:
dry median 48.215 ms, flooded 64.418 ms, flooded p95 68.265 ms. Final dry median:
33.372 ms; flooded median: 44.584 ms; flooded p95: 46.602 ms. Both median frame
times improve by about 31%. Results are recorded in `output/dense-polish-after.json`;
baseline in `dense-polish-before.json`.
This remains a bounded rendering/water fixture, excluding crew AI and campaign
progression. It is not evidence of full-station 60 fps.

Reproducers: `output/profile_dense_polish.gd`, `output/check_dense_culling.gd`.
Evidence: `output/dense-polish-final.log`, `dense-render-check.log`,
`dense-wet-door-check.log`, `dense-cull-check.log`, `dense-cull-{22,45}-{true,false}.png`.
The corresponding diff PNGs are black (no viewport differences).

## Next action

Owner review during normal camera movement. Dense rendering still exceeds a
16.7-ms frame budget; future profiling should examine remaining room submission
and graphics work. No broad renderer refactor or export was performed.
