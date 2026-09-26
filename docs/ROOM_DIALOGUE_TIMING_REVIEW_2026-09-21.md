# Room-completion dialogue timing review

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Investigate owner note 17: room dialogue reportedly arrives before construction
finishes. Identify a reproducible offending line before changing gameplay timing.
The original owner-session issue remains unconfirmed, not declared fixed.

## Accepted decisions and constraints
Preserve paid costs, failure conditions, room layouts and authored dialogue.
Use isolated meta/run/settings paths. Do not force the trace writer into the owner's
profile. The initial timing audit made no runtime change. The subsequent diagnostic
bundle change below preserves dialogue timing and source assets; no new release was made.

## Current evidence
The available owner dialogue_trace.log is 236 bytes, dated September 20 at 20:26:37,
and contains only awake/bill with no outstanding construction. Preserved read-only
as output/room-dialogue-timing-2026-09-21/available-owner-trace.log.
Current _place_room inserts the completed room before COMPLETE and room_built;
crew completion removes its order before calling _place_room and refreshes the grid.
The renderer reads the current fleet order list, not a copied old build-order list.

## Verification
Controlled paid crew construction exercised all three explicit completion lines:
Crew Hab (269 steps), Pressure Control (944), Listening Post (1,319). Every accepted
built/<room> key was first observed with its room present; no premature announcement
was observed. Free building and disabled failures remained false. Evidence:
output/room-dialogue-timing-2026-09-21/accepted-events.json and scoped logs.
This is per-simulation-step, headless evidence; it does not certify the original
visual/UI timing, identify an unkeyed ambient line or replace owner-session capture.

## Fixture corrections
The first Listening Post position did not fit its doorway. A second above-core run
still failed; all-rotation/resource diagnostics showed q0 was valid immediately after
the last waiting step acquired the sixth Data. The helper reported only q3's door
error, obscuring the boundary condition. The accepted run waits explicitly for
naturally generated Data before paid construction, without grants or relaxed rules.
Failed attempts remain in their original logs/reports and are not passing evidence.

## Diagnostic bundle follow-up
`scripts/bug_report.gd` now includes the optional dialogue_trace.log tail as
logs/dialogue_trace.log in F8/crash report bundles. It uses the existing 2 MiB
per-log cap, never creates or writes a trace, and leaves an absent trace out.
This is diagnostic collection, not a fix for dialogue timing. A trace may predate
the report; read its session header and correlate it with the engine/session logs.

`tests/test_bug_report.gd` now verifies absent-file handling, no trace creation,
ZIP inclusion, capped size and newest ordered completion/dialogue markers.
The complete existing native report fixture passes in a fresh isolated profile:
C:/Users/Alex/AppData/Roaming/BrineSpaceTraceFixture20260921-bceff7aa.
Evidence: output/bug-report-trace-2026-09-21/native-final.log (0 failures, exit 0,
no script errors). Earlier harness attempts were not accepted: missing source
preloads caused errors even alongside a misleading zero-fail summary; reusing a
profile also invalidated the fixture's previous-log expectation. Logs are retained.
The final harness includes the real transitive source/shader/JSON dependencies and
uses application/config/custom_user_dir_name, with OS.get_user_data_dir logged.
The owner's game profile and trace were not modified by this test.

## Next action
Keep note 17 open until its exact dialogue line/session is captured. No timing
patch is justified by the current evidence. Continue independent polish work;
the current packages predate this diagnostic addition and later room/card polish.
Remove the optional bundle attachment along with the temporary trace writer once
the offending dialogue is identified and the diagnostic is retired.
