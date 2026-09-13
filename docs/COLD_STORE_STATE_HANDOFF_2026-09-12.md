# Cold Store state handoff

## Objective
Preserve functioning cues while completing room-facing art rollout.

## Change
Cold Store side-bank props now opt into custom_library_draw. The existing cyan
indicator code is reached through the shared renderer. No source or layout edits.

## Evidence
Native fixed gameplay q0 OFF and two powered frames captured. Differences confined
to pixel rectangle(139,289)-(141,291). Offline RGB matches retained card exactly.
Source: output/cold-store-state-2026-09-12/checks.json and comparison.png.
Additional diagnostic q1/q2/q3 captures do not imply playable rotation coverage.

## Remaining
Continue the full room/direction ledger. No whole-goal completion or export claimed.
State lesson and bible updated along with current status and rollout record.
