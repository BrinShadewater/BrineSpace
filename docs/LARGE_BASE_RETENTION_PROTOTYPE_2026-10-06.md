# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: non-Moon large-room base retention prototype

## Objective and acceptance

Reduce repeated room preparation without changing pixels, animation timing, filtering, layering or gameplay. Continue complete PC/Mac performance/release scope.

## Accepted decisions and constraints

Private only; normal source unchanged. Current large.gd retains complete hydroponics/storage base commands when deep room snapshot/bounds/reduced-motion/Studio revision unchanged; only unread generic machine_clock omitted. Tidal keeps original immediate path because its chamber state changes every frame in measured workload. No new images/global cache/quality reduction; scene-owned nodes and original diagnostic accounting.

## Current state

output/large-base-retention-2026-10-06/ holds private helper, room/retention tests, physical reference/candidate fixtures and station-results/verified.json. Original all-three-type cache version retained as all-type-prototype.gd; current helper excludes Tidal retention. Source hydroponics/storage/common/door/wall code inspected: no generic clock/direct Time dependency. Conservative full snapshot/revision keys preserve wall/port/flood/style changes.

## Verification

Original private native135checks/80exact large-room pairs pass. Added explicit retention/wall/water/chamber tests:147checks pass after correcting wet-slot fixture parent from Window to CanvasItem to match actual shared LIVE layer. Initial failed fixture errors retained; no runtime wet bug claim. Current two-type helper143checks/80exactpairs passes cleanly; generic clock changes retain base, wall/water changes redraw; original Tidal/chamber/material/lifetime cases still covered by existing suite. Owner2936 non-log files unchanged every run, all native processes terminal.

Matched native current mixed40room/12multicell/3Moonbays six60sample phases, same private six-sheet drone/crew fixture, original all-type candidate at measurement time. Fullcrew/drone/door/light/power/zoom snapshots and everytextureendpoint identical, zero engine/missingart errors. Hydroponics3slots retain9redraws constant/hits717→1617; storage3slots7redrawsconstant/hits715→1615. Tidal3slots0hits/724→1624redraws, so no Tidal cache benefit; current helper restores immediate Tidal to avoid needless snapshot comparisons.

Complete base callbacks1.73–1.95→.72–.91ms/frame (~.98–1.06ms lower); all live-room CPU7.47–7.96→6.55–7.23ms (0.72–1.07ms lower, includes child drawing). p95reference→candidate46.141→44.394,46.640→46.221,44.179→43.196,45.474→44.950,49.958→49.718,54.868→52.320ms. Onepair/stillfailed16.7ms gates/no universalFPSclaim. Current narrowed helper has native visual/retention checks, not a new matched station comparison; retain this version distinction. Texturefinal2776.236MiB identical/private scene/no memory claim.

## Next action

Verify two-type helper in full shared LIVE composition with ordinary rooms/activecore, layout/material/lifetime checks, then normal integration/permanenttest and actual-normal matched comparison. Leave animated Tidal immediate until a measured ordered static/live split is validated. Remaining seabed/wave preparation and steady renderer/backend costs, private drone Main lifecycle, normal memory/loading budgets, original packaged bugs/endurance and actual Windows/Mac certification remain open.
