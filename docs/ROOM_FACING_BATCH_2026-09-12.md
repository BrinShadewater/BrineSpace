# Room-facing batch handoff

Updated: September 12, 2026 · BrineSpace

## Objective and acceptance
Owner accepted the Tidal top-down south bank and requested more rooms using the
new wall-facing contract. Three additional engineering south banks completed.

## Accepted decisions and constraints
Side banks may be flush, every appliance faces inward. North banks are flush with
slight riser overlap when overheight. South banks face inward and are viewed from
above. Preserve department materials and owner layouts.

## Current state
Pressure Control, Thermal Power Control and Maintenance Bay now select overhead
south artwork. [Sources and exact prompts](../assets/room-facing-repair-v2/README.md).
Five candidates, three selected; originals/rejected studies preserved. Maintenance
keeps its original placement frame to avoid a furnishing fallback change. No
runtime code, owner saves, other directional artwork or card bindings changed.

## Verification
Native room review complete, nine unaffected rotations pixel-identical in RGB.
176 preferred-layout crew-route cases pass after final correction. Side-wall
regressions, 47 card bindings and 188 layout-key checks pass. Three source hashes
match, LFS filters apply, and read-only release dependency collection includes
each selected source. No executable rebuilt, commit, push or publication.

## Next action
Owner review of `output/room-facing-batch-2026-09-12/comparison.png`. Continue the
remaining south banks, then inspect side/north wall fit against the same contract.
This batch does not establish acceptance of the whole room catalog.
