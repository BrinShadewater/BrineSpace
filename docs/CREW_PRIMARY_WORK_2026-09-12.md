# Primary workplaces and autonomous daily routine

Updated: 2026-09-12. Project: BrineSpace.

## Objective and accepted decisions
Owner wants mostly autonomous crew with one primary workplace, a suitable crew/room synergy, and meals/sleep. This first implementation covers workplace assignment, routine work, needs and return to work. Existing emergency responses and ordered jobs retain priority. Automatic generation of mining/repair orders is later scope, as proposed and accepted.

## Current state
Room inspector now offers crew selection and Assign Primary Workplace / Clear Primary Job. One living present crew member per workplace; a deceased occupant does not block reassignment. Assignment survives Continue. A primary job is a preference rather than confinement: crew use real routes, work in eight-second bouts, leave for needs or existing higher-priority work and return afterward. No workplace means the existing autonomous roaming routine remains.
Matching attendance adds +1 Data (Bill/Veld) or +1 Metal (Branforth/Marsh) per functioning cycle. The worker must physically be working in a dry, operating room. Matching work also slows fatigue gain by 20%. No essential Power/Oxygen output is tied to attendance, so a meal break cannot remove base life support. Existing storage caps still apply.

Specialties:
- Bill: BRINE Core, Command Center, Crew Hab, Crew Lounge, Galley.
- Veld: Research/Bio/Xeno/Anomaly Labs, Data Archive, Med Bay/Center.
- Branforth: Reactor, Maintenance Bay, Salvage Workshop, Life Support, Pressure Control, Diving Airlock.
- Marsh: Mining/Salvage/Construction Drone Bays, Battery Array, Listening Post.
Other room assignments are allowed but have no specialty bonus.

Humans seek meals/rest at 65% hunger/fatigue, finishing their current ordinary work bout first. Hunger rises 0.12 points/s, fatigue 0.10 (0.08 at matching work). Existing meals/rest relieve 45 points on completion. Existing per-cycle Food consumption pays for meals; no second meal charge was added. No Food means no hunger relief; helmeted hungry crew seek a locker to remove the helmet before eating. Needs also advance during emergencies and dives; exterior trips finish/recall using their existing safety rules before indoor routines resume. Existing construction can finish safely, but crew with high needs take an available reachable meal/rest break before claiming a new construction order. Marsh retains battery/pod behavior rather than requiring human meals and sleep.

Changed: scripts/crew_primary_work.gd and scripts/crew_work_panel.gd (with UIDs), scripts/bill_npc.gd, scripts/main.gd, scripts/crew_room_activity.gd. Galley and cold-store fixed interaction points were covered by current furniture; cached nearest clear navigation-grid approaches now follow current blockers. tests/test_crew_primary_work.gd with UID and crew subsystem registration covers the new routine. No new raster art or executable export.

## Verification
Headless full routine passed: physical work attendance, real cycle bonus, fatigue benefit, assignment/work save and restore, autonomous meal and berth sleep, return to work after each, pause, offline/off-duty bonus exclusion and clearing assignment. Native work, meal and sleep captures reviewed; log output/crew-primary-native.log, images output/crew-primary-{working,meal,sleep}.png. Urgent needs were set by the fixture to exercise the transitions without waiting several minutes.
Room-life suite passed all 72 room/rotation/human cases. Diver mining and hull repair regressions passed. Inspector dispatch passed; construction regression has the unresolved navigation failures detailed below. The earlier save failure was a fixture removing recovery wrecks referenced by the roster; preserving those unrelated wrecks fixed it. No save-validation bypass was added.

Final checks: output/test-runs/20260912-094956-headless confirms the primary routine passes after reachable-service break gating. Construction remains failing for four Branforth direction cases (eight assertions); the temporary state probe in output/test-runs/20260912-095431-headless shows him idle at (7824,8032), waiting for a clear route, with unclaimed orders. The first case fails at hunger 44/fatigue 55, below the break threshold. This is an unresolved navigation concern, not a passing construction regression. Probe removed from the fixture.

Break policy: existing construction finishes safely. High needs prevent claiming another job only when an appropriate reachable, operating meal/rest service exists. Otherwise crew can continue working and build missing facilities; the inspector explains unmet needs.

## Next action
Owner review of pacing and bonuses in ordinary play; optional next step is autonomous repair/mining order selection. Room staffing competition and full expedition balance are not established by the bounded fixture. Source checkout only; previously delivered hazards EXE predates this work and diver mining.
