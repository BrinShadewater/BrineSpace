# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Veld north lounge contact/depth

## Objective and acceptance
Full master-matched Veld animation set and cross-animation polish remain active.
North seated candidate must meet actual furniture and retain correct depth through
lowering, held rest and rising. Source/controller proof alone is insufficient.

## Accepted decisions and constraints
Candidate remains unselected. Preserve master-relative source scale, palette,
native helmet, physical navigation foot and owner layouts. No production edits,
export, commit or push. Default lounge only; scratch profile, both equipment variants.

## Current state
New tests/test_veld_seated_north_station.gd/.uid and scratch runner exercise real
main scene, actual RoomActivity lounge station resolver, first clear north seating
approach per room rotation, and fixture-only paired source overrides. Output:
output/veld-seated-north-station-v1. Four normal phases in both gears/four rotations,
32 full captures; eight additional held-pose foreground depth diagnostics.
review_station.py creates five boards of unmodified room crops and hash evidence.

## Verification
Latest native run:192 checks,0 failures,44.31s,engine0/no script/art errors.
All2,931non-log owner profile files unchanged. Confirms candidate renderer admission,
actual retained crew slot/source texture, standing ruler and unchanged navigation
foot. Waits for observable retained submission before frame_post_draw; earlier112
and176-check intervals retained separately, not retroactively strengthened.

Visual review FAIL: normal held pose is hidden in both gears/all four rotations.
With identical source/position but temporary +200 world-unit sort offset, the same
pose appears on the chair. Offset restored immediately; only fixture metadata is
temporarily changed, not source pixels/manifests. This isolates furniture depth as
an issue, not a missing source. The diagnostic is deliberately excessive and is
not a production fix or final seat/depth acceptance. Entry/lower/held boards and
one full foreground diagnostic inspected; full corrected motion is still pending.

## Next action
Derive the correct chair/actor contact and depth from registered furniture and
seated anatomy; repair the complete lowering/held/rising depth path without
forcing foreground over unrelated props or changing artwork merely to hide the
issue. Recheck four rotations/both gears, joins and interruption/Continue before
selection. Other directional seated sources, held breathing, rest/death joins,
world journeys and whole-set polish remain incomplete.
