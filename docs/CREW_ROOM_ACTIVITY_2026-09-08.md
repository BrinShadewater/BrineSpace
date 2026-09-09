# Crew activity at room installations

Pressure Control, Listening Post and Crew Hab now offer furniture-relative destinations to the existing needs controller. Bill and Branforth include both instrument rooms in maintenance preferences; Veld includes Listening Post. Curiosity can also use these destinations. Crew Hab fatigue visits stop beside its installed berth.

Approaches follow actual full-wall visual bounds or the retained flush-back geometry, with three candidate positions along the operator edge. Existing navigation selects reachable graph points and keeps collision rules. Missing installations do not invent a service target. On arrival crew face north/south/east/west according to the authored installation, rather than always east. Actions use existing timer, goal, direction and state fields, so save format is unchanged.

The authored east interaction plays at east-facing control approaches. Other directions use existing directional idle/breathing poses for observing instruments. Rest is a ten-second standing breathing break beside the berth. There are no new seated, lying-down, or multi-direction hand-work sprites in this change; those remain separate animation production work. These behaviors grant no staffing bonuses and change no resource economy.

Validation: tests/test_crew_room_activity.gd passes 36 combinations (three rooms, four rotations, three actors), using production route selection and movement from a doorway-side graph point. Every case checks final facing, action and save validation. Three disk round-trips restore activity/facing/timer; power loss interrupts the service goal. Twelve Bill station previews are in output/crew-activity at initial 52% zoom. Final log: output/crew-activity-final.log; no script errors in final stderr. This is a bounded single-crew doorway approach fixture, not an autonomous multi-crew congestion soak.

Fixture lessons: arbitrary farthest graph points may be isolated pockets and are not representative doorway starts. UI refresh recalculates power, so restore explicit fixture power before each actor case; do not change normal gameplay power rules to satisfy a visual fixture.
