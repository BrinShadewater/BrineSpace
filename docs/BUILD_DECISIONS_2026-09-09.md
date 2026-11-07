# Building decisions and new discoveries

Updated: September 9, 2026 · Project: BrineSpace · Task: clearer decisions, placement feedback, adaptive guidance and new synergies

## Objective and acceptance
Prioritize useful inspector information, explain placement problems beside the preview, guide the opening from actual station state, and add discoverable placement rewards.

## Accepted decisions and constraints
Paid construction, failures, matching doors, hidden recipes and three consecutive functioning cycles remain unchanged. No monolith refactor or new assets. Unknown connected recipes no longer change the guide; only discovered names/progress appear.

## Current state
Changed `scripts/main.gd`, `scripts/station_ui_insights.gd`, `scripts/synergy_manager.gd`, `tests/test_ui_workspace.gd`, and `tests/test_discovery_progression.gd`; existing UIDs preserved.

Blueprint inspector starts with cost/shortfall, output and upkeep. Installed-room status/remedy precedes descriptive text. Removed duplicated blueprint cost/output sections. Placement feedback is visible on the map, constrained to map bounds; it shows exact missing resources, matching doors and learned links, using the configured rotate key. Guidance responds to power construction, paid jobs, falling supplies and discovered stabilization progress, without revealing unknown pairs.

Three new recipes (implementation spoilers): Cold Store + Life Support gives Chilled Air Recovery (+1 Oxygen); Galley + Crew Lounge gives Shared Table (+1 Food); Observation Room + Data Archive gives Field Notes (+1 Data). Each pays 3 Research on stabilization through the existing once-only reward path. All pairs have legal matching-door layouts with existing orientations. Normal-play balance acceptance remains pending.

## Verification
Final discovery progression suite passes cleanly: `output/build-decisions/test_discovery_progression-1788940554054648200.log`. Includes real room-pair orientation, disconnected/nonfunctioning rejection, discovery, interrupted-progress reset, three-cycle stabilization, existing reward persistence and hidden-hint coverage. Updated stale foundation expectation for already accepted Workshop/Galley/Cold Store rooms.

Native UI workspace assertions pass: `output/build-decisions/test_ui_workspace-native-1788940516115899100.log`. Checks paid-job guidance, recipe secrecy, stabilization progress, affordable oxygen suggestion, material shortfall, ready/disconnected placement, inspector ordering and visible guide bounds. Reviewed `output/build-decisions/placement.png`.

Native run is NOT globally clean: concurrent Marsh integration now references absent `character/marsh-v1/final/manifest.json` and `assets/material-polish-cryo-recovery-v1/marsh/wake-0.png` (and companion frames), producing JSON/image errors. Those sources were not changed by this pass. Earlier local test failures in guide layout and expected resource ordering were corrected and rerun. Existing raw-image warnings remain.

## Next action
Playtest new placement guidance and synergy pacing after Marsh assets are complete. Local source only; no new executable or packaged acceptance.
