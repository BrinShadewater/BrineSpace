# Four-crew bunk sharing review

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Exercise normal movement/activity updates with all four crew competing for the
reviewed lower bunk. Require every actor to sleep and rise with at most one
occupant, and inspect correctly centered native captures.

## Accepted decisions and constraints
No owner furnishing edits. This fixture starts four awake crew at high fatigue,
uses controlled powered rooms and stops the cycle timer. It exercises main._process
and ordinary crew choices, traffic and activities; it is not full economy or
unbiased expedition acceptance.

## Current state
scripts/bill_npc.gd now yields the reviewed bunk to an eligible nearby colleague
with fatigue at least 65 and more than five points above the choosing actor.
The check excludes dead/inactive/self crew, remote expeditions and urgent repair,
recharge or retreat goals, and requires a matching sleep station in peer geometry.
The local scope is within three cell widths. Existing route/rest claims remain.
No queue state is serialized. tests/test_bunk_multi_crew.gd preserves the 180-second,
3600-update native fixture in the crew test lane.

## Verification
Initial evidence: output/crew-activity/bunk-multi/report.json and
output/layout-default-audit-2026-09-21/bunk-multi.log. Occupancy stayed at one, but
Bill slept three times, Veld eight, and Branforth/Marsh never slept; both remained
at fatigue 100. Veld kept reusing the berth with fatigue near zero. Initial images
also missed the room due camera interpolation; they are not visual acceptance.

After the fix, the identical seeded setup in bunk-multi-r2.log and
output/crew-activity/bunk-multi-r2/report.json passes with zero failures:
Bill, Veld and Marsh each complete one sleep/rise; Branforth completes two. Maximum
occupancy is one. Fifteen phase captures assert the room is centered; native
resting contact inspected. Focused whitespace check passes. Promotion to tests/
preserves the exact validated script.

## Next action
Broaden station layouts and normal paid expedition play; the three-cell local
priority rule is not a global bed scheduler. Continue remaining furnishing,
performance and current release validation. Four-cast profile/controller work
is installed, but owner visual acceptance and complete game acceptance remain open.
