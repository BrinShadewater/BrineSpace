# Project handoff

Updated: October 3, 2026. Project: Brine Space. Task: Marsh full animation consistency.

## Objective and acceptance

Finish the full master-matched animation set, including identity, material grade,
camera, proportions, action joins and physical behavior. This milestone admits
West walking only; the full goal remains active.

## Accepted decisions and constraints

Six reviewed whole-pose edits are exact copies of the staged contact bank.
No anatomical fitting, repainting, alpha cleanup or timing change. Sole levels
remain exact. Crown bounds are 27,24,25,25,24,24 versus original
26,24,25,26,24,25: maximum adjacent/closing change 3 versus 2 source pixels.
The extra pixel equals 0.441081 world units at 65.28/148; retained explicitly
after fixed-scale closing-join review. Browser observations establish sampled
advancement and pause, not continuous watched cadence.

## Current state

- Normal bank: `character/marsh-v2/supplemental/west-walk-polish-v1`.
- `character/marsh-v2/catalog.json` adds one body manifest; only six `walk-west`
  drawings change. Other 227 effective states retain exact metadata/source hashes.
- Current inventory: `character/marsh-selected-normal-audit-2026-10-03-post-west-walk/inventory.json`,
  228 states, 1190 slots, 91 body manifests. Post-East inventory is the historical baseline.
- Tools: `install_marsh_west_walk_family_v1.py`, `prepare_marsh_west_walk_selected_v1.py`,
  `review_marsh_west_walk_selected_v1.gd` with paired UID, fingerprint/publish/record
  helpers and `review_marsh_west_walk_closing_v1.py`.
- Pipeline, visual bible, current status and canonical/installed repair skill
  append this acceptance. Acceptance receipt binds native, inventory, closing
  board and browser evidence. Do not rerun the append recorder.

## Verification

Normal catalogue loads without a candidate override. Actual actor/main/grid/player
check: 1579 checks, zero failures, 260 movement samples, two arrivals,
36 paired captures, three moving actor restores. Scratch APPDATA;
5524 bounded inputs and 2931 owner non-log files unchanged. Engine exit 0,
no errors/warnings; terminal session 48735 completed.

All six complete native boards and first full 1600x900 capture inspected.
Original comparison actor is absent from several walking crops: those rows
support source review and selected-actor placement, not complete paired world
comparison. Exact source sole-depth checks remain separate evidence.
Full 2D planted-foot, autonomous jobs, all rooms, water/equipment/furniture and
disk full RunSave/Title Continue acceptance remain open.

Browser tab 2 is paused at quarter speed, phase 0, clock 64010, draw 13756;
marked for handoff. Local server port 8764, session 5008. Viewer and screenshot
are beside the current inventory. Sampled screenshot: phase 4, clock 11451,
draw 1142. No continuously watched cadence claim.

## Next action

Review North/South walking against their own accepted idle and direction-specific
masters, preserving authored gait and contact. Continue cross-family consistency
and broader gameplay acceptance. Reuse retained West evidence; no native rerun
needed without a new change, failure or unresolved concern.
