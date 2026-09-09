# Dialogue pause handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: pause while reading dialogue

## Objective and acceptance
Opening dialogue pauses the station; closing restores the prior pause state.

## Accepted decisions and constraints
Dialogue remains open until explicit Next/close; no timed dismissal. Queued messages retain the pause. Previously manual-paused games stay paused after closing. Menus layered over dialogue retain their pause.

## Current state
Changed `scripts/crew_comms.gd`, `scripts/main.gd`, `tests/test_compact_comms.gd`, and the pause stub in `tests/test_comms_context.gd`. Existing UIDs retained. No export built.

## Verification
Native compact-comms fixture passes: held pause and timer, pause-shortcut guard, menu round trip, manual-pause preservation, queue, reopen, dismiss and two-size bounds. Context and archive headless fixtures pass. Native capture reviewed. Evidence in `output/dialogue-pause`; final native log `test_compact_comms-native-1788937334396768000.log`. Existing image-loading warnings remain. Fixture polling is isolated to avoid unrelated ambient messages changing its expected queue.

## Next action
Owner normal-play review of dialogue pacing. Packaged validation pending if a new executable is requested.
