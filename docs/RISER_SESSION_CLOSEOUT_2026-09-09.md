# Project handoff

Updated: 2026-09-09 · Project: Brine Space · Task: Riser and floor art session closeout

## Objective and acceptance
Apply new walls to suitable rooms, coordinate doors, remove separate wall decorations for now, and consolidate production lessons. User authorized rollout and session closeout; final visuals remain available for review.

## Accepted decisions and constraints
Six V3 walls belong to reactor, cryo chamber, data archive, storage bay, crew lounge and research lab. Window props remain separate future assets with reserved mounting rectangles. All separate wall dressing is paused in gameplay and Studio, including airlock attachments. Preserve saved mounts and raw art; baked source fittings and older V2 baked windows remain. No gameplay or door geometry changes.

## Current state
Dedicated paints in rooms/doors/department_door.gd and door_finish.gd feed existing default and animated door consumers. Shared decoration pause in rooms/whole-room/decoration_props.gd gates north_wall.gd and rooms/underwater/airlock-v4/fittings.gd. Seven fresh cards and 28 rotation previews in assets/riser-session-closeout, with card hashes in manifest.json; primary/grid/variant mappings updated. Six V3 room-specific registrations remain installed. Earlier V3/V4/V5 floor packs and V2 risers are preserved; floor variants remain selectable rather than being reassigned globally.

Bible, CURRENT_STATUS and maintained corridor-riser/handoff skill references updated. Those two references synchronized to the installed skill, preserving unrelated files.

## Verification
Native fixture output/riser-session-closeout/review.gd passed all-room hidden-mount checks (including saved coordinates), six room/door assignments, neutral corridor joins, source geometry/reserves and 28 captures across seven rooms. Seven default views and lounge opposite view visually inspected. Door polish test passed with all 12 finish variants, both orientations and ten motion frames; its legacy console label understates coverage. Card consistency result is recorded in output/riser-session-closeout/cards-test.log. Original art preserved and new PNGs use LFS attributes.

## Next action
Session work closed in the source checkout. No executable rebuilt, no commit or push performed. Future window authoring should use assets/room-risers-v3/WINDOW_PLACEMENT.md and verify furniture occlusion. Re-enabling separate decorations is a future owner decision.
