# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James next-task turns

## Objective and acceptance
Continue James's full animation set and cross-family polish. This milestone verifies
normal console departure into the next task; it is not owner acceptance of the full set.

## Accepted decisions and constraints
Keep selected masters, matte material, anatomy and helmet/body registration. Existing
reversible-work authorization applies. No new raster, mirrored pose, layout, export or commit.

## Current state
`scripts/bill_npc.gd` holds the intended facing for each waypoint instead of deriving it
from rounded microsteps; optional validated `movement_heading` survives snapshots and
older saves remain readable. `scripts/branforth_npc.gd` includes the selected ordinary
turn envelope in empty-hand wet route clearance, using recorded family bounds plus the
four installed compact overrides. `scripts/grid_canvas.gd` checks all twelve selected
ordinary turns rather than the unrelated transition-action union. Conservative full-clip
checks remain during playback. Selected pixels and clocks are unchanged.

## Verification
Normal next task: 87,210 checks, eight journeys, 25 turns, no skipped
starts or unfinished turns. Actual disk restores: 57,746 checks/eight console journeys,
including moving egress. Dry equipment: 29,629 checks/192 cases. Furnished swimming:
2,036 checks/eight routes. Movement trace (including misleading rounded diagonal steps,
saved-heading validation and older snapshots), segment clearance and owner-report
regressions pass. All native runs serial, scratch APPDATA; real profile unchanged and
engine logs clean. Initial next-turn native screenshots reviewed in both gear modes;
they are contextual stills, not a complete visual review of all moving turn slots.

Preserved `prior-step-heading-*`, `pre-tail-envelope-*`, `tail-envelope-diagnostic-*`,
`pre-route-turn-envelope-*` and diagonal-failure logs record investigation, not acceptance.
Exact-start checks alone missed six mid-turn cancellations at275ms. A remaining-pose
union and current-pose-only gate did not resolve the route defect; those approaches
were removed. Waypoint-heading tolerance alone also failed the exact-diagonal regression;
the retained fix stores each segment's intended heading. Post-check hashes are snapshots,
not a claim of whole-file stability during concurrent unrelated actor work.

## Next action
Continue task-selector/traffic and full furniture, meals, equipment and exterior journeys,
including airlock return and mortality context. This fixture covers seed17 only and
does not establish every layout, destination, gear change or traffic interruption.
Full animation goal remains active; prior source coverage is not completion.
