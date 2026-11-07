# Settings tutorial guide

Updated: October 21, 2026 · BrineSpace

Latest milestone: [coverage audit and illustrated guide](TUTORIAL_COVERAGE_2026-10-21.md)
supersedes the section counts and latest verification receipts below.

## Objective and acceptance
Add an optional mechanics guide to the options menu, accessible before and during play.

## Accepted decisions and constraints
Use the shared Settings category layout. Explain fundamentals without naming hidden recipes or changing discovery rules, costs, artwork or gameplay. No forced onboarding.

## Current state
`scripts/settings_panel.gd` adds Tutorial Guide with eight short sections: pause and reserves, construction, functioning rooms, crew access, recovery, placement experiments, progression and troubleshooting. Shortcut text follows current bindings. Uses existing scrolling, typography and menu text scaling; no Restore Defaults action on the read-only page.

## Verification
`tests/test_tutorial_guide.gd` and paired UID; registered in `tests/index.json` as native. Passed 16 checks across title/in-game archive modes at 1600×900 and 1280×720 with 130% menu text: page selection, focus, remapped pause key, horizontal fit, final-section access and return to other settings. Opens/closes shared archive twice. Native screenshots reviewed under `output/tutorial-guide-20261021/`. Receipt: `output/test-runs/20261021-011124-native/`. Test used isolated APPDATA. This exercises the shared menu, not a full gameplay pause/resume playthrough.

## Expanded coverage requested by owner
Guide now has eleven sections, including explicit flooding/fire response, mining versus clearance, drone delivery/recharge and finite deposits, surveying for survivors, thaw requirements, station Data versus Archived Data, upgrade purchases and permanent character/blueprint unlocks. Checked wording against live flooding, fire, harvest, recovery and shop code. Corrected the earlier implication that all crew wards require a separate thaw button; crew thaw automatically when their requirements are met, while companion containers have explicit actions. No hidden recipes or locations named.

Expanded native fixture adds intermediate-section captures. All 16 checks still pass at both sizes; expanded compact text visually reviewed. Latest receipt: `output/test-runs/20261021-011615-native/`. Owner-file protection receipts: `D:/bs-tutorial-20261021/expanded-before.json` and `expanded-after.json`.

## Next action
Navigation pass: added a twelve-topic picker and Back to Topics buttons in `settings_panel.gd`. Topic jumps transfer keyboard focus and align the section after the shared archive's follow-focus scroll settles. Initial native checks caught double scrolling from stale geometry; fixed by waiting one frame before alignment. Updated fixture passes 24 checks across both sizes, including mining jump and return, and compact captures reviewed. Latest receipt: `output/test-runs/20261021-015721-native/`. Protection receipts: `D:/bs-tutorial-20261021/navigation-before.json` and `navigation-after.json`.

Continued completeness pass: twelve sections now cover shared reroll charges and cycle recovery, power reserves/blackouts and suspension, meal/rest access and limited diving air, plus Save/Continue versus End Expedition. Corrected the guide to use the actual End Expedition button caption. Verified against current main, crew and hardware code. Expanded capture coverage; all 16 native checks pass, normal/compact layouts captured and new compact paragraphs reviewed. Latest receipt: `output/test-runs/20261021-015426-native/`. Protection receipts: `D:/bs-tutorial-20261021/final-before.json` and `final-after.json`.

Source implementation ready for player review. No export updated. Assess clarity in the next opening playthrough; recovery-button request remains separate.
