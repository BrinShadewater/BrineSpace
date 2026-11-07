# Interactive expedition ending preview

Updated: 2026-10-24 / Project: BrineSpace

## Objective and acceptance
Owner requested an in-game preview of count-up, sparkle and sound together.

## Accepted decisions and constraints
An audible interactive window is explicitly authorized. Use a temporary APPDATA,
illustrative accomplishments and existing production report/audio/reveal code.
Leave the preview open for the owner to operate and close.

## Current state
Added tools/preview_expedition_ending.gd and its UID. The tool checks its scratch
APPDATA and --audible-preview opt-in, waits for observable startup completion,
freezes the simulation, then shows an illustrative archived expedition. Startup
is silent. PLAY REVEAL / R enables sound and replays presentation only; no repeated
reward calculation occurs. CLOSE PREVIEW uses normal audio shutdown. Production
menu controls remain available and any profile changes stay in scratch storage.

## Verification
Visible interactive process 179096 launched and responsive at handoff. Startup log
is clean and ready receipt confirms scratch user directory:
output/expedition-ending-preview-20261024/ready.json and preview.log.
The real profile and signed ZIP remain unchanged (2,971 profile files), protection
receipts D:/bs-tutorial-20261021/ending-preview-before.json and ending-preview-after.json.
This verifies startup/isolation; owner listening and button interaction review follow.

## Next action
Owner clicks PLAY REVEAL or presses R to watch/listen, repeats as desired, and closes
the preview when finished. This process is an illustrative preview, not their run.
