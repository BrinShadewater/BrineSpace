# Project handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: unlockable Marsh

## Objective and acceptance
Owner accepted Marsh portrait V3 and requested an unlockable character. Marsh is a fourth architect in local source. Functional checks pass; owner normal-play and sprite-motion acceptance remain pending.

## Accepted decisions and constraints
Human-looking male android, blond hair, steel temple plate, off-white suit. Uses existing derelict recovery: repair hull, provide power, spare berth, Food and Oxygen, then recover occupant. Recovery persists the unlock for future loops. Starting cache: +4 Data and +4 Metal, once per loop. No survival immunity or free construction added.

## Current state
New loops use architect schema 3 and distribute three unselected architects across the two existing cryo wards. Old schema 1/2 checkpoints keep their three-person roster; start a new loop to find Marsh.

Added scripts/marsh_npc.gd and UID. Registered actor, selection, independent playback, drawing/depth/doors and optional compatible save fields in architects.gd, architect_selection.gd, main.gd, grid_canvas.gd and run_save.gd. Updated crew_construction.gd, flood_safety.gd, hull_repair.gd, drone_fleet.gd, station_hardware.gd and crew_life.gd for identity, peers and measured sprite clearance. Added dialogue/comms voice and dedicated architect_cryo_art.gd occupant source.

character/marsh-v1 contains five generated sources with exact prompts, deterministic build_pack.py, 96 distinct body frames, fitted helmet frames, shared-pose manifests, clearance, cryo art and reviews. Uses approved character/marsh-portrait-v3/portrait.png for UI. Built-in image_gen used; LFS attributes confirmed.

Added tests/test_marsh_unlock.gd and UID; updated recovery/selection fixtures for four identities and construction fixture with --marsh for all four directions.

## Verification
Passed: native test_marsh_unlock.gd including four active peers and disk restore (output/marsh-coexist-clean.log); test_architect_recovery.gd including legacy schema (output/marsh-recovery-final.log); native test_architect_selection.gd (output/marsh-picker-final.log); test_crew_construction.gd -- --marsh with four directions, costs, pause, power/doors, death, checkpoint and completion (output/marsh-construction-final.log). These final stderr companions contain no SCRIPT ERROR or ERROR entries. Existing wreck-image import warnings remain. Earlier concurrent checks saw missing Marsh cryo art during integration; that asset is now present and tested.

Agent visually inspected native station/comms, unlocked picker at 960x540, source sheets, cleaned cryo image, helmet frame and walking contact sheet. Reviews in character/marsh-v1: review-{960,1600}.png, review-picker-{960,1600}.png, walk-review.png and walk-review.gif. Four-peer check establishes short coexistence and avoidance participation, not exhaustive congestion safety. No executable export or commit.

## Limits and next action
First playable animation pack: secondary activities share work, kneel/rest or swimming poses, recorded in provenance.json. They are not bespoke equivalents of every crew expansion. Cryo occupant is static until release. Owner can test recovery in a new loop; unique activity/helmet-transition animation expansion and full visual motion acceptance remain polish work.
