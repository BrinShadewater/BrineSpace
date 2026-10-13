# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: retained Moonbay native commands

## Objective and acceptance

Avoid repeated native water submissions without changing appearance or layering. Require actual mixed-station execution, measured benefit, complete relevant visual/lifecycle checks before normal admission. Overall PC/Mac release plan remains active.

## Accepted decisions and constraints

Private prototype retains the entire Moonbay base as one Node2D command list, preserving all internal floor/water/submarine/wall/door order. A deep room snapshot, exact bounds, Reduced Motion, layout revision and live merged Moonbay layout determine invalidation. Only generic machine_clock is omitted: current Moonbay base does not read it. Mission clock/progress/water/gates, flooding, helmet visibility, rotation, ports and all other room data remain in the key. No animation quantization or frame/detail reduction.

## Current state

Private helper and native probe: `output/moonbay-retained-base-2026-10-06/{retained.gd,probe.gd,run.py,results.json}`. Normal renderer and test index unchanged this turn. The helper has not been integrated into GridCanvas. Its key intentionally favors broad correctness over minimal per-frame copying.

## Verification

Native 385 checks, zero failures; 256 exact full-room raster comparisons across four rotations, eight mission phases (idle/flood/boarding/launch/outbound/return/drain/unload), two fractional scales, Reduced Motion on/off, partial chamber water, damaged submarine, raised/lowered walls, shelf helmet visibility, peripheral flooding, partial station-port opening and inherited translucent modulation. 128 initial redraws, 128 cache hits; repeat submissions changing only generic machine_clock do not redraw. Scene owner release observed. Each viewport uses the same current normal Moonbay renderer, so this verifies command retention/state invalidation for the represented cases rather than an independent art oracle.

Actual merged owner layouts were not imported into this scratch fixture. All 2,936 owner files unchanged; clean process exit. No engine upgrade, export, art or gameplay changes. No station timing or FPS saving established yet.

## Next action

Integrate private retained base into the physical mixed-station Grid. Preserve inter-room order as well as internal order: baseline large-room bases/props currently paint on LIVE parent, while ordinary retained contents paint on its children. Adding a Moonbay child above the parent can wrongly overlay neighboring props; putting it behind can reorder it against other large rooms. Prefer explicit ordered large-room containers for the existing large-room sequence, with base before its live props, and verify full neighboring-room appearance before admission. Account for child callback cost in timings, guard actual retained execution, remove/hide obsolete slots on demolition/culling/replacement, and cover wet-equipment children and offline overlay. Recheck layout mutation, filter/material inheritance and active mission progression. Only then accept or reject a measured station comparison.
