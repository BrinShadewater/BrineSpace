# Project handoff

Updated: 2026-09-21 · Project: BrineSpace · Task: Cargo turn playback endpoint

## Objective and acceptance
Remove a proven leg-pose jump when an authored carry turn finishes. Broader Bill
gait anatomy, cargo detail and visual acceptance remain open.

## Accepted decisions and constraints
No sprite pixels, owner layouts, stride values or authored durations changed.
The initial fix covered completed carry turns. The swimming follow-through below
extends it to completed ordinary swim turns; direct facing changes remain unchanged.

## Current state
scripts/crew_sprite_player.gd detects a completed carry-turn clip for the same
state/direction, then resets the ordinary clip selection before sampling it. This
starts at destination frame zero, matching the authored turn endpoint, and resets
last position through the existing initialization path. Previously the old gait
fraction and movement accumulated during the turn advanced directly to another pose.
Added tests/test_carry_turn_handoff.gd, UID and crew index entry.

## Verification
output/carry-turn-handoff-2026-09-21/before.log reproduces four Bill endpoint
failures. after.log passes those four after the fix. Final authoritative result:
final-checked.log, 12 cases, zero failures and no script errors. Both turn directions
for Bill/Veld/Branforth, bare/helmet, use actual selected catalog frames. Checks
compare last turn/first resumed pixels, snapshot restoration during the turn, and
exact subsequent distance-derived phase using per-direction stride fallback.
Expanded early fixtures assumed Marsh helmet/turn coverage and state-wide strides;
those assumptions caused script errors, so their printed counters are not passes.
Marsh has no matching authored turns and is excluded from this endpoint check.
No new native temporal visual acceptance is claimed; this is exact pose/clock evidence.

## Next action
Continue ordinary gait anatomy repair and review cargo turns in live context when
next collecting gameplay motion. Test start-of-turn matching separately; this fix
addresses exit only. No release package refreshed.

## Swimming follow-through
The same stale-phase exit bug was reproduced for ordinary swim turns. Runtime
completion reset now covers carry and swim turns, with matching state/direction;
swim-carry already reset via its existing branch and remains a regression control.
No swimming start/stop behavior or direct-facing-turn rules changed.

output/water-turn-endpoints-2026-09-21/report.json checks 144 actual registered
swim/swim-carry turn endpoints, all matching destination pose zero. Baseline swim
playback fails endpoint/next-distance checks; cargo-swimming baseline passes.
Final maintained test now covers 36 cases: carry/swim/swim-carry, east-west and
west-east, three actors, bare/helmet. final.log exits zero with zero failures and
no script errors. Compare endpoint pixels after pivot registration: swim turns
and destination clips can have different transparent canvas sizes. The earlier
raw-buffer comparison failed despite equal registered imagery; that fixture was
corrected. No new sprite or owner-layout changes, and no broad gait acceptance.

## Restore and native follow-through
The maintained guard now serializes the mid-turn snapshot, restores it into a
fresh player, samples the unchanged clock/position, then completes the turn. All
36 cases pass, including paused-pose preservation and subsequent movement phase.
Missing expected non-Marsh clips now fail rather than silently reducing coverage.
Evidence: output/turn-restore-2026-09-21/check.log.

Native before/current carry playback captured 60 samples with Bill in both turn
directions, bare/helmet. Frame 024 (last turn pose) and 025 (first resumed pose)
were inspected: the old path jumps to another leg phase while the corrected path
retains the authored endpoint. native.log contains no script errors. The printed
capture counter is not an independent parity check; endpoint guards above establish
correctness. turn-exit-comparison.gif is available for owner review. Row labels
name the starting direction. This is controlled player playback, not a full save/
continue expedition or a claim that ordinary gait is natural.
