# Ore Refinery remaining directions handoff

## Objective and constraints
Continue the full room catalog. Preserve industrial charcoal/orange materials,
ore and ingot inventory, independent machinery, and inward wall access.

## Changed state
North source now has clean exterior, quiet amber lenses and solid ingots.
Rejected white-frame material drift is archived. Side loading gates, furnace
service handles and lower drawers face inward. All sources, prompts and original
registrations are in assets/refinery-directional-v1. Three q0 card bindings
updated; this room's q0 is west, q1 north, q2 east and q3 south.
Coverage, current status, bible and project/installed pipeline lesson updated.

## Verification
Native north/east/west and card reviewed. All prop IDs and rectangles retained;
independent machinery visual bounds unchanged. Mount flags do not move saved
placements. South q3 RGB-identical. 176 furnished layouts, 20 side variants and
47 card identities pass. Off/on and two powered timestamps verify vessels q0,
sorters q0/q1/q2 and crushers q1/q2/q3; hopper q3 and fitted banks stay static.
Evidence: output/refinery-remaining-2026-09-12/final/runtime.json, comparison.json,
state-checks.json, mounting-checks.json and tests.log.

## Remaining
All four refinery directions reviewed. Continue other catalog families and
missing art. Goal remains active; no export or executable rebuilt.

## Owner playtest repair amendment

The later owner request to reduce orange and remove white cutouts is complete.
All directional banks and the independent machinery atlas now share restrained
burnt-orange paint; edge-connected neutral backgrounds are transparent while
enclosed trim, gauges, yellow logistics markings, copper billets and ore remain.
Real-display q0-q3 captures were inspected and the q0 card was refreshed. Current
validation passes 176 furnished layouts, 20 side variants, 47 catalog cards and
both production-ten route suites. See `REFINERY_OWNER_REPAIR_2026-09-12.md`.
