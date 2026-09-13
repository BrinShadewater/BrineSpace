# Hull crack development

Updated: 2026-09-12. Project: BrineSpace.

## Objective and acceptance
Owner accepted gradual deterioration, three visible damage stages and emergency patches using the existing physical crew repair system.

## Accepted decisions and constraints
Unpatched existing cracks gain 0.0005 severity per simulation second (3 percentage points per minute), capped at 1. Stage boundaries remain 0.35 and 0.70. Stage changes enter the journal. No new random crack source or full pressure simulation was added.
Emergency patches cost 1 Metal and 3 seconds of crew work, plus travel. They reduce crack inflow by 80% and arrest gradual deterioration. Fresh fire or containment damage can still increase severity. Full welding retains existing costs and durations and removes the patch and damage. Existing water still needs draining. Reachability, oxygen checks, cancellation refunds and pause behavior use the existing repair system. Crew air estimates include projected deterioration during travel and work.

## Current state
Changed scripts: hull_repair.gd, room_flooding.gd, flood_visuals.gd, main.gd, room_fire.gd and local_incidents.gd. Inspector exposes cause, stage, inflow and patch/full-weld actions. Fire and containment events record their causes. Hairlines drip, larger fractures stream, patches show a bolted metal plate and reduced dripping. Cracks are rendered even before water accumulates. Save validation accepts optional patch and cause fields and patch jobs while preserving old repair jobs.
Tests changed: test_hull_repair.gd and test_room_flooding.gd.

## Verification
Headless hull repair, flooding and fire tests passed. Native repair coverage includes physical crew work, patch cost, duplicate refusal, inflow reduction, arrested deterioration, save-field validation, permanent repair, underwater oxygen and cancellation. Native screenshots reviewed for hairline, rupture and patch; evidence in output/hull-variant-0.png, output/hull-variant-2.png and output/hull-emergency-patch.png. Final native log: output/hull-cracks-native-final.log.

## Next action
Tune deterioration and patch usefulness through ordinary play. This is a source checkout change; the previously delivered BrineSpace-fire-20260912 executable has not been rebuilt with these changes. Audio creaks and additional damage sources remain future scope.
