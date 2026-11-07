# Project handoff

Updated: 2026-10-03 · Project: Brine Space · Task: Marsh lower-bunk contact and full-set continuation

## Objective and acceptance

Complete Marsh's master-matched animation set, then cross-family consistency/polish.
Goal remains active. Resolve the measured low-seat concern without repainting
correct body sources or equating scoped contact/save checks with full-set acceptance.

## Accepted decisions and constraints

Keep the selected whole bodies, masters,39-row source support,timing and navigation.
Furniture contact follows current art geometry. Preserve action geometry through
saves and retain old missing-field fallback; no owner save migration or edits.
All native runs use scratch APPDATA with real-profile fingerprints.

## Current state

Probe measured the seated support12.007world units below the lower mattress.
Current bunk art360x334,mattress edge row239; prop rect121x112.2611. Old rest+16
was too low for that geometry. `scripts/crew_room_activity.gd` now supplies a
Marsh-specific seat offset scaled by prop height. `scripts/marsh_npc.gd` stores
optional `seat_offset`, uses it during seating/reclining and blends back to the
unchanged final sleep placement. Numeric finite0..64 validated; absent field16
fallback retained. `tests/test_marsh_bunk.gd` checks independent source/prop contact
and missing/invalid saved offsets. No artwork or catalogue change.

Added paired Godot coordinate probe/corrected review tools and
`tools/publish_marsh_bunk_seat_correction.py`. Before/after geometry,14full native
captures,two visual comparison boards and verification are retained in
`character/marsh-bunk-seat-correction-2026-10-03/`. Logs and scratch saves in
`output/marsh-animation-audit/bunk-seat-probe-2026-10-03/` and
`output/marsh-animation-audit/bunk-seat-corrected-2026-10-03/`.
Pipeline,bible,current status and matching canonical/installed skill updated.

## Verification

Before112checks; corrected117checks/seven full disk restores,pause/reversal,
interruption/completion/lowbattery/invalid saves. Support gap reduced to floating
coordinate tolerance below0.00001world units. Both before/after boards inspected:
seated/reclining placement visibly improves; final rest retained. Legacy berth
regression86checks/six disk restores after change. All three runs0errors/warnings/
failures/exit0;497bounded inputs and2931owner nonlogs unchanged per interval.
Probe source hashes separately retained after runs,not retroactive before coverage.
New full saves preserve offset; old absent field accepted by validation and defaults
to previous16 behavior. No title Continue/continuous playback/allrotations/ownerlayout
or full228-state/1190-slot acceptance established.

## Next action

Continue the wider unreviewed families and continuous construction/furniture/
expedition joins and save/continue. Preserve this measured correction and private
South drain06; do not keep revisiting successful local measurements without a new
concern. Cross-reference masters,material/head proportions and neighboring states
at actual station scale before coherent normal admission of remaining staged art.
