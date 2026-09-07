# BRINE rendering, floor batching and large-station profiling

## Changes

BRINE now supplies ordered retained drawing passes for its tank housing, floating
occupant, glass, bubbles and front rim/cap. Workstation bodies are retained while
their display pass remains live. The starter pod remains live during thawing.
The original composition and depth order are preserved. No textures, animation
rates, appearance settings, simulation rules or save format were changed.

Compatible floor commands are grouped within the existing material renderer:
disjoint panel fills, inset outlines, edge highlights and bolts. Each panel's
details stay inside it, so the groups can preserve local paint order without
crossing another panel. Seams, drains, route lines and rug details use multiline
commands. Line batching alone did not lower GPU submissions; grouping compatible
panel commands is the measured draw-call improvement. The reference switches are
`--redraw-brine-parts --unbatched-floor-lines` (the latter disables all new floor
grouping, not just multiline calls).

Save restore no longer builds unused navigation graphs for inactive or dead
architects. Active crew still rebuild and validate saved routes against current
geometry. Dormant crew retain their state; release/update constructs navigation
before they can move. Architect recovery and movement regressions cover this path.
No navigation objects are read from a save or trusted without geometry checks.

## Large-station measurements

`tests/profile_large_station.gd` exercises nominal 50- and 100-room fixtures at
1600×900 with VSync disabled, actual crew updates, animated rooms and active
construction drones. Each scenario warms for 90 frames and measures 180 frames.
Construction grows the second fixture to **101 rooms** before its measured sample.
Resources and building are fixture-controlled; this is not a balance playtest.

Reference and final runs were sequential on the local RTX 4070 Ti machine. Both
include the previous static-surface and room-content caches. These are local
samples rather than hardware-independent FPS guarantees.

| Scenario | Reference mean | Final mean | Final p95 | Draw calls before → after |
|---|---:|---:|---:|---:|
| 50-room Fit | 42.89 ms | 38.61 ms | 40.34 ms | 7,129 → 6,109 |
| 50-room close | 16.39 ms | 15.77 ms | 16.68 ms | 2,316 → 1,986 |
| 101-room Fit | 76.86 ms | 77.72 ms | 83.11 ms | 13,524 → 11,605 |
| 101-room close | 21.17 ms | 19.84 ms | 20.94 ms | 2,260 → 1,960 |

Draw submissions fall by roughly 13–14%. The 50-room Fit sample improves about
10%; **the 101-room Fit sample does not improve measurably**. Fewer submissions
alone do not resolve the remaining large-station frame cost. Close views remain
substantially faster because room/prop drawing is culled.

## Interaction stalls

Each interaction records synchronous CPU time and the next twelve rendered
frames. This is one cold transition per action, not a percentile distribution
across repeated user interactions. Values below are the first affected frame.

| Interaction | Reference | Final |
|---|---:|---:|
| Construction completion | 29.86 ms | 28.63 ms |
| Open menu | 39.38 ms | 38.52 ms |
| Close menu | 29.71 ms | 28.97 ms |
| Zoom to Fit | 233.02 ms | 235.70 ms |
| Zoom to close | 47.51 ms | 48.60 ms |
| Write save | 10.05 ms | 9.78 ms |
| Restore saved state | 718.90 ms | 604.27 ms |

Save restore improves about 16%, but remains visibly synchronous. This measures
restoring state into an already-loaded game, **not total title-screen Continue
startup or loading all art from disk**. Zoom-to-Fit still rebuilds retained drawing
commands at the new scale and remains a roughly 236 ms stall. Neither remaining
stall is claimed fixed. Next investigations should separate cold navigation-build
cost from rendering rebuild cost before choosing another cache or scheduling change.

## Verification and evidence

`tests/test_brine_batch_parity.gd` and `tests/check_brine_batch_parity.py` compare
33 native RGBA image pairs with the two reference switches disabled/enabled:
rotations, close/Fit, power, partial light fades, placement/removal, doors, camera
changes, powered animation times, and busy crew/drone/construction snapshots.
Animation is warmed before time advances so a freshly rebuilt cache cannot mask
an incorrectly static prop. Panning may retain the same floor set without rebuilding;
image parity still checks the actual viewport result.

Logs: `output/large-reference.*`, `output/large-final-batched.*`;
structured comparison: `output/large-render-comparison.json`.
The benchmark asserts successful save and restore, writes isolated PID-specific
fixture saves, and removes them when finished. It does not overwrite player saves.

Final verification: all 33 pairs are pixel-identical, with no script errors.
Shared menu, workspace, placement previews, menu recovery and Architect selection
native suites pass. Embedded geometry, NPC clearance/movement, Architect recovery,
drone fleet and production walker-path regression suites pass. Existing raw-image
loading warnings remain; raw runtime art loading and LFS assets were preserved.
