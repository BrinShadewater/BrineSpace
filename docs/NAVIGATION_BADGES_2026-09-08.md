# Navigation badge integration

Latest layout: Archive, Diagnostics, Journal and Menu form a four-button row at the HUD top right, with centered44-unit badges above compact labels. Archive remains visible with zero unread records. Top cycle and resonance displays removed; underlying gameplay remains unchanged. Native fixture asserts row order/count and absent displays, exercises Journal/Diagnostics, and captures both HUD sizes; visually reviewed after label compaction.

Updated: 2026-09-08 · BrineSpace

## Objective and acceptance
Use the owner's clean colored badge artwork in the existing UI. Cream Codex computer retained.

## Decisions and implementation
scripts/navigation_badge.gd draws the v3 RGB sources through per-asset octagonal UV silhouettes, excluding the baked checkerboard without modifying source artwork. It caches textures and supplies pressed, hover and disabled visual feedback. Existing Button focus, signals, text, shortcuts and counts remain in place.

scripts/main.gd adds badges to Archive, Diagnostics, Journal, Menu and the pause-page Codex entry. scripts/title_screen.gd replaces Codex and progression tile icons with the new Codex and Archive badges. Source art remains in brineui/navigation-badges-v3.

## Verification
Native tests/test_navigation_badges.gd passes badge bindings, Diagnostics tab selection and Journal signal actions, and captures HUD at1600x900 and960x540 plus title. All three captures visually inspected; no checkerboard visible or badge-label overlap. No script errors. Headless editor parse and targeted diff whitespace checks pass. Existing direct-image-load export warnings remain; no exported build tested. Menu/Archive actions retain their connections but were not clicked in this fixture.

## Next action
Owner review in game. Standalone transparent sprite exports remain optional follow-up; runtime silhouette clipping handles these source backgrounds.
