# Tutorial coverage and illustrated guide

Updated: October 21, 2026 · BrineSpace

## Objective and acceptance
Audit the current guide for missing player-facing mechanics, explain useful gaps, and add annotated native pictures for building, resource forecasts, mining, recovery and permanent progression. Keep recipes hidden and player saves untouched.

## Accepted decisions and constraints
Optional Settings guide, shared before/during play. Existing mechanics and artwork remain unchanged. Static pictures are controlled examples, not the player's current state. No room-combination recipes, secret location map or authoring-tool manual.

## Coverage audit
The following covers the main player-facing system families, not every individual room's special case. Room inspectors remain the reference for exact current costs, prerequisites and blockers.

| System | Guide coverage | Implementation checked |
| --- | --- | --- |
| Pause, camera, Journal, diagnostics | 1 and troubleshooting; remapped shortcuts | `main.gd`, `title_settings.gd` |
| Placement, doors, physical construction, rerolls | 2; connected doorway picture | `main.gd`, `crew_construction.gd` |
| Inputs, outputs, Power reserve, blackout, suspension | 3; forecast/readout picture | `main.gd`, `station_hardware.gd` |
| Crew access, meals, rest, primary workplace | 4; added attendance requirement | `bill_npc.gd`, `crew_primary_work.gd`, `crew_work_panel.gd` |
| Flood, leak repair, fire, sprinklers, Integrity, Corruption | 5; added containment and loss warnings | `room_flooding.gd`, `room_fire.gd`, `local_incidents.gd`, `main.gd` |
| Mining, salvage, finite deposits, clearance, cargo, recharge | 6; bay/battery inspector picture | `drone_fleet.gd`, `harvest_sites.gd`, `main.gd` |
| Survey, finding survivors, repair, thaw/recharge | 7; revealed companion-site checklist picture | `site_discovery.gd`, `underwater_visibility.gd`, `cryo_recovery.gd`, `companions.gd` |
| Discovering and stabilizing patterns | 8; only generic rules, no recipe names | `synergy_manager.gd`, `main.gd` |
| Archived Data, upgrades, blueprint/character purchases | 9–10; owned/available/unmet shop picture | `meta_shop.gd`, `research_tree.gd`, `title_archive.gd` |
| Save, Continue, concluding a loop | 11; separate save from End Expedition | `main.gd` menu actions |
| Diving gear, refill, airlock cycle, dispatch and recall | Added 12 | `airlock_panel.gd`, `airlock_service.gd`, `crew_expedition.gd` |
| Moonbay orders, return/unload and repair | Added 13 | `moonbay_panel.gd`, `moonbay_missions.gd` |
| Scrap refund, confirmation, blockers and storage | Added 14 | `room_scrap.gd`, `main.gd` |
| Advanced branch controls and room-specific actions | Added 15; broad explanation without recipes | `rare_branch_control.gd`, room inspectors |
| Reporting a problem | Final troubleshooting topic; Diagnostics, Journal, F8 | Shared Settings and `main.gd` |

No claim that every rare-room interaction is exhaustively documented. Development-only tools, hidden combinations and unreleased mechanics are intentionally excluded. Future feature changes should update the relevant topic and its capture if necessary.

## Current state
- `scripts/settings_panel.gd`: sixteen topics, revised mechanics copy and five illustration placements.
- `scripts/tutorial_picture.gd` + UID: raw PNG loading only when visible, numbered captions, inline thumbnail and enlargement dialog.
- `assets/tutorial/{building,resources,mining,recovery,progression}.png`: five 1600×900 native captures, about 4.3 MB total, covered by existing Git LFS attributes. Full literal runtime paths are declared in the picture helper.
- `tools/capture_tutorial_pictures.gd` + UID: reproducible, guarded isolated-profile capture; labels rendered in Godot before capture. Uses fixed fixture rooms, a surveyed recovery example and an unsaved example shop balance. No player progression changed.
- `tests/test_tutorial_guide.gd`: checks all topics, navigation, remapped shortcuts, all image loads and visible thumbnail heights, enlargement/close, compact layout and final-section access.

## Verification
Native fixture passes at 1600×900 and 1280×720 with 130% menu text. Latest receipt: `output/test-runs/20261021-024517-native/`. Native screenshots and compact thumbnail/enlargement reviewed. Final capture log `D:/bs-tutorial-20261021/pictures3.log` is clean; an earlier capture attempt had shutdown-only resource warnings and was superseded. A collapsed thumbnail layout found visually was fixed and guarded by a height check. Recovery visibility and folded forecast presentation were corrected before final capture.

Owner folder fingerprints: `D:/bs-tutorial-20261021/pictures-before.json` and `pictures-after.json`. No export, signing or publication performed. Menu testing does not establish fresh-player comprehension or full gameplay pause/resume acceptance.
All 2,971 owner files and the signed ZIP stat are unchanged. Read-only `build_release_manifest.collect()` finds all five literal PNG paths; no manifest or export preset was rewritten. Scoped diff whitespace check passes.

## Next action
Real-expedition integration follow-up: added `tests/test_tutorial_gameplay.gd` with paired UID and native `tutorial-guide` registration in `tests/index.json`. The actual main scene keeps its normal processing enabled. From both running and paused states, 20 checks cover opening Settings/guide/image, three successive real Escape events, no resource/cycle/hand changes while reading, restoration of the prior pause/timer state, selected blueprint and gameplay input. Pass: `output/test-runs/20261021-110451-native/`. No runtime fix required. This closes the earlier gameplay pause/resume coverage gap, but is still automated integration rather than a comprehension playtest. Owner fingerprints: `D:/bs-tutorial-20261021/gameplay-before.json` and `gameplay-after.json`.

Navigation audit follow-up: native fixture now opens the real topic popup, captures it, dismisses it with Escape, visits all sixteen targets and checks their focus/visibility, then verifies that switching from the guide's bottom to Audio starts at the top. Both window sizes pass; the full compact 130% topic popup was visually reviewed. No additional runtime changes were needed. Latest receipt: `output/test-runs/20261021-031340-native/`. Owner protection receipts: `D:/bs-tutorial-20261021/navigation2-before.json` and `navigation2-after.json`.

Usability follow-up: `tutorial_picture.gd` retains numbered explanations in enlargement, applies menu text scaling, prevents stacked dialogs and restores the originating button's focus plus guide scroll position. `test_tutorial_guide.gd` now sends an actual Escape key through the input system and checks window bounds, visible image height, captions, duplicate prevention and return position. Initial caption sizing produced an offscreen dialog; a starting wrap width fixes it. Latest passing receipt: `output/test-runs/20261021-030240-native/`; compact enlarged picture visually reviewed. Protection receipts: `D:/bs-tutorial-20261021/usability-before.json` and `usability-after.json`.

Review the illustrated guide during a fresh opening playthrough. No more encyclopedic expansion is needed before seeing which explanations a player actually uses. Include these literal-path assets in the next maintained release build.
