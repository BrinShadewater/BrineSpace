# Ore Refinery facing handoff

Updated: September 12, 2026. Project: BrineSpace.

## Objective and acceptance
Continue all room art, including missing directions. South equipment uses overhead inward operation; preserve functional inventory. Full catalog remains active.

## Accepted decisions and constraints
Preserve ore flow, closed drum, two cooling fans and four billets. Keep independent crusher/hopper at their existing sizes. No export requested.

## Current state
New source, prompt, provenance and original q3 layout in assets/refinery-directional-v1. New side-ore-refinery-wall-south registration. full_wall_prop.gd selects south for refinery q3; ore_refinery_view.gd retains independent crusher/hopper, and q3 defaults move them north while placing bank flush south. Initial registration-only capture showed no pixel change and is retained as diagnostic evidence. Other source directions unchanged. Coverage, bible, status, rollout and maintained/installed pipeline lesson updated.

## Verification
Native installed q3 reviewed. output/refinery-directional-2026-09-12/installed-comparison.json shows same prop inventory and changed positions only in q3; q0/q1/q2 RGB identical. Independent machinery sizes verified unchanged. 176 routes, 20 existing side variants and 188 layout keys pass. Card uses unchanged q0. Owner review pending; no executable rebuilt.

## Next action
Continue missing south companions and unreviewed directions, preserving actual room selection and live equipment. Do not equate new registration with native installation.
