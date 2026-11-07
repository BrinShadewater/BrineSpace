# Marsh north-idle integration

Updated: September 13, 2026. Project: Brine Space.

## Objective and constraints
Match the older north idle to the reviewed whole-body walk. Preserve Marsh's rear-facing blond male identity, right-edge implant, gloves and helmet-free behavior. Original two-frame 650/650-ms timing remains unchanged; this is not a directional start/stop replacement.

## Current state
Source `character/marsh-motion-polish-v1/sources/idle-north-video-01.mp4` completed: 871,783 bytes, 97 frames, 24fps, 1248x1664. Exact prompt/job retained. Recipe `idle-north-cycle-recipe.json` selects frames 8/43 at fixed scale 147/1481, position 67/63, pivot 128/224. Contact and selected-walk comparison reviewed. `tools/veld_scanner_revision.py` now selects north idle; `tools/rebuild_marsh_art.py` exports it to the existing runtime pack, retaining all supplemental transitions.

## Verification
Art validation passes: 143 body states, 691 references, no errors/border touches, all 211 original frames and original manifest unchanged. Native source check passes in `output/crew-replacement-2026-09-12/marsh/north-idle-selected-final.log`, including exact anchored source pixels. Its old original-only coverage assertion was updated to include explicit supplemental keys/counts/timing. Native idle/walk/idle run passes 51 frames in `north-idle-live-after.log`; boundary page reviewed in `live-idle-transition-north-production-01`. Earlier baseline remains in `live-idle-transition-north`, showing the broader/darker replaced idle. Real battery drain and no-helmet checks pass. These are bounded agent reviews, not owner acceptance or export validation.

## Next action
Replace Marsh south idle, then continue older actions/run/carry and missing directional starts/stops. Veld carry and Branforth older kneel/carry also remain open. No active generation/test job.

South idle follow-up: source idle-south-video-01 is generating with the dedicated start-image binding to south-standing-identity-01.png. Exact-prompt provider status in_progress recorded in sources/idle-south-video-01.job.json; active wait session 86742, log idle-south-generation-01.log. Resume existing request. Native baseline south-idle-baseline-live.log passes 51 samples; live-idle-transition-south/state-transition-00.png reviewed and shows the older broader idle against the new walk. Source is not yet selected. No production change in this follow-up.

South follow-up completed and selected: see HANDOFF_MARSH_SOUTH_IDLE_2026-09-13.md. Session 86742 exited successfully; no active south generation job remains.
