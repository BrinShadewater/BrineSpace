# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: compact portrait popup

## Objective and acceptance

Owner requested a smaller rectangular comms popup, only Next and X, automatic appearance for dialogue, disappearance five seconds after writing, and a dedicated side-panel COMMS button.

## Accepted decisions and constraints

This supersedes the earlier expanded popup, contact/history/speed/reply controls and floating inbox. Keep portraits, slow typewriter text and normal gameplay rules. The side button reopens the current/last message. X hides the popup; a new incoming message opens it again. Next reveals unfinished text, then advances queued dialogue or closes the final message. The five-second completed-text interval automatically advances queued dialogue, otherwise hides the popup. Blocking overlays suspend its presentation/timer.

## Current state

`scripts/crew_comms.gd`: 520x170 logical rectangle, 96x108 portrait, only Next/X visible, five-second completed-text timer. Existing archive/context helpers remain internal; they are no longer popup controls. `scripts/main.gd`: dedicated COMMS button below diagnostics, with queued count. No new portrait art or economy changes.

## Verification

`tests/test_compact_comms.gd` and its UID: native pass for typewriter, five-second expiry, manual Next/X, new-message reopening, automatic queue advance, side-button access, exactly two popup buttons and 1600/960 containment. Agent reviewed output/compact-comms/960.png. Existing conversation fixture UI expectations are adjusted for the new owner direction. Logs are output/compact-comms*. Existing raw-image warnings remain; no package rebuilt.

## Next action

Owner review the compact popup in normal play. Displayed history remains persistent; pending dialogue is still scene-local. Do not restore the former popup controls without a new request.
