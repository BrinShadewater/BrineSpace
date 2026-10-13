# Terrain cell retention prototype

Updated: October 5, 2026 · BrineSpace · R5

Later same-day milestone: [runtime integration](TERRAIN_CELL_RETENTION_2026-10-05.md)
is now enabled after native parity and matched station measurements. The prototype
scope and results below remain historical evidence.

## Objective and acceptance

Reduce terrain command rebuilding during excavation without changing progress
animation, transparency, cross-cell edges, buried-site reveal or selection.

## Accepted decisions and constraints

Prototype only; no runtime changes enabled. Preserve the existing complete rock
pass, its final selection outline, then the wreck pass. Retain commands per cell
rather than moving every progress overlay above every terrain object. Use the full
field for neighboring geometry and visibility even when drawing one cell.

## Current state

`output/terrain-retention-2026-10-05/` contains the generator, isolated native
probe, source-derived rock/wreck renderers, JSON results, logs and paired images.
The only renderer change in those copies adds an optional cell subset; draw
arithmetic and textures are unchanged. Reference and candidate share textures.
Candidate keys include exact progress, cleared state, kind, visibility, neighbor
connections and local selection. Original insertion order is retained. Slot
preparation happens on each tested update; only changed slots rebuild commands.

Current production `_environment_terrain_key` includes all progress values and
selection. Its dirty pass calls both entire-field renderers plus glow plants.
This prototype addresses that rebuilding mechanism; it does not establish how
often it dominates actual station frames.

## Verification

- Native Godot 4.7.2, guarded scratch profile: **208/208 byte-exact comparisons**.
  Two scales, two subpixel offsets and nearest/linear filtering cover continuous
  rock/wreck progress, selected-cell changes, clearing, buried-site reveal,
  restoring a rock and unchanged frames. Representative image inspected.
- During progress steps, median instrumented reference draw time **2,215 us**;
  candidate key preparation plus changed-slot drawing **479 us**. Median two
  slots invalidated; final unchanged steps invalidate zero. These are samples
  from one native fixture run, not independent station benchmark runs.
- Draw calls match in all cases (median 311). This changes CPU command rebuilding,
  not the cost of displaying retained GPU commands. Node traversal/lifecycle
  overhead is outside these instrumented sections.
- Zero engine errors; **2,936 owner non-log files unchanged**. No gameplay,
  runtime source, art, packages or release acceptance changed this interval.

## Next action

Integrate a scene-owned terrain content host under STATIC_TERRAIN with explicit
rock/selection/wreck/plant order. Preserve the original path for comparison.
Count deferred child drawing in diagnostics, preserve parent zoom transforms,
and manage cell insertion/deletion and scene exit. Validate first rendered frame,
pan/zoom settling, plants, field replacement, owner scene transitions and node
overhead before enabling. Then run matched active-excavation station workloads.
Do not infer an overall FPS gain or memory remedy from this fixture.
