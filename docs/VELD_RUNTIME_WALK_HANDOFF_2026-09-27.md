# Veld walk integration handoff

Updated: September 27, 2026 · BrineSpace

## Objective and acceptance
Install the reviewed four-direction bare walks and matching idles, then verify playback in the game. Owner authorized integration after the cadence review. New native motion review is available; no new owner visual acceptance claimed.

## Accepted decisions and constraints
Preserve all approved pixels, identities and equipment sides. No generation, palette remapping or anatomy changes. 184×184 frames, pivot [92,172], standing height 148. Four 1500 ms cycles; distance-driven stride 69/384 cells yields that cadence at normal 46 world units/sec. Helmet and other action art remain the earlier selection.

## Current state
- `character/veld-runtime-walk-v1/`: 159 exact copied frames, manifest, source hashes/acceptance, native review GIF/contact.
- `scripts/grid_canvas.gd`: explicit manifest override after existing Veld base/equipment loads.
- `scripts/crew_sprite_player.gd`: retain equipment timing/strides separately so the old helmet rows work alongside longer bare walks; equipment selection saved in playback snapshot, backwards-compatible default.
- `tests/test_veld_walk_integration.gd` (+ UID), registered in tests/index.json: real loader, exact pixels, metadata, timing, equipment, pause, teleport, direction and snapshot coverage.
- `tests/test_crew_complete_packs.gd`: superseded bare idle/walk migration expectations delegated to the focused test.
- `tools/review_veld_runtime.gd` (+ UID): isolated native room fixture using NPC.move(), clear cardinal paths and native renderer, idle/walk/idle captures.

## Verification
159 source hashes identical; manifest clean and PNGs covered by LFS. Focused test 415 checks/0 failures; test_dr_veld and test_crew_polish (including Continue/playback restore) pass. Carry turn regression 72 cases/0 failures; swim smoothing facing passes. Native capture 240 frames/0 failures; all requested walk facings confirmed. Agent inspected sampled frames for scale, identity, placement and transitions; GIF retains motion for owner review. Logs/trace in `output/veld-runtime-integration/`.

Broader test_crew_complete_packs stopped on the existing equip-helmet-east ten-versus-eight-frame contract mismatch, documented by the earlier HELMET_TRANSITION_HANDOFF; not treated as a pass. No release/export validation.

All test/probe processes used scratch APPDATA. Profile comparison: progress/checkpoint/layout data unchanged; concurrently running normal game/editor processes changed session breadcrumbs, Studio recovery/config and a bug report. Open live logs prevented a complete log hash comparison. Do not restore these concurrent owner changes.

## Next action
Review `character/veld-runtime-walk-v1/in-game-walk-review.gif` for movement feel/foot sliding at game scale. Tune stride only if review identifies sliding. Remaining visual scope: matching helmet walks/idles and other action transitions. Repair the older full-pack test's helmet transition contract separately using the accepted eight-frame selection.
