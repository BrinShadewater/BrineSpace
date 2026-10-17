# Project handoff

Updated: September30,2026 · BrineSpace · Bill standing reader service integration

## Objective and acceptance
Complete Bill's full master-consistent animation set, then cross-animation polish.
Standing inspection art and service draw/loop/stow are now normally installed.
The full goal remains active; this is an integration milestone.

## Accepted decisions and constraints
24states/144refs; shared256plane/pivot128,224/H148/dry depth0; native master helmets.
Source matte/detail/size grading remains unchanged.480ms draw/stow,960ms loop.
Original cold-store6s,workshop2s,equipped meal6s/drink3s service clocks remain.
Sealed helmets use the reader; bare meals and other actors retain their behavior.

## Current state
scripts/bill_inspection.gd derives poses from saved service timer, never cosmetic
time. BillNPC/CrewLife/normal grid renderer select draw/loop/stow. At arbitrary
loop-to-stow boundaries, retain the displayed whole source pose for first60ms.
Power loss cancels goal and reverses partial draws or completes remaining stow;
inspection_return_pose is snapshot validated/default-1 and restored. Untouched
zero-length draws clean up; floating boundary return timers clamp to480ms.
No new economy rule, actor selection, art generation or service duration change.
Both manifests and ACTIVE_ASSETS retain normal family selection.

## Verification
80source checks; prior1,036 normal selected pixel/metadata/idle-join checks.
1,454 actual-service/native checks pass42.10s: five physical station/gear cases
(cold-store bare/helmet,workshop bare/helmet,galley helmet), all service phases,
240 power-loss entry/loop/stow boundary cases over scripted four directions,
25actual RunSave disk round trips and exact selected pose/contact restoration.
Normal drink transition/completion checked; full drink-specific boundary matrix
is not separately covered.15actual room draw/loop/stow images and native82 timeline
board retained; representative cold-store/workshop/galley loops visually reviewed.
Five targeted regressions pass128.83s,including72 room/rotation/actor service
cases and48 actual approaches. All2,914 owner non-log files unchanged in both
scratch-profile runs. Native evidence is not autonomous all-direction contact proof.
Source candidate fixtures' old cosmetic elapsed=-1 assumption predates the new
saved service clock; current activity fixture is authoritative for runtime timing.

## Next action
Audit selected inspection silhouettes against real contacts in all room rotations,
with interruption/restore contact invalidation and hazard takeover. Add dedicated
equipped drink boundary coverage. Then replace bare meals, generic rest and dry
death; finish full-set material/proportion/pacing polish,including remaining2–3px
source interior motion variation. Keep provenance and source/native/runtime scopes
separate; no full-set completion claim. No commit/export requested.
