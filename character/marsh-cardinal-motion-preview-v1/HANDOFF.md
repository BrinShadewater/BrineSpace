# Marsh native motion preview handoff

Updated: 2026-10-04 | Project: BrineSpace | Task: Four-direction walking playback

## Objective and acceptance
Provide a short playable native preview after Marsh's completed bounded animation closeout and representative four-direction Save/Continue checks.

## Accepted decisions and constraints
Existing art, pivots, timing, controller and minor accepted visual variations retained. Isolated APPDATA, no owner-save access by Godot. Rendering samples advance the actual normal controller and visual clock in 40ms steps; this is a controlled route fixture, not autonomous goal selection or real-time performance.

## Current state
Four actual 96-unit dry routes in a furnished cold store captured from idle through start/walk/stop to idle. Movies and sampled join boards in this folder; verification.json binds sources/boards/movies and run report. Native scripts: review_marsh_cardinal_motion_preview_v1.gd + UID, fingerprint_marsh_cardinal_motion_preview_v1.py, publish_marsh_cardinal_motion_preview_v1.py. No game or selected artwork edits.

## Verification
Final v3: 1,611 checks, zero failures; engine exit 0/no errors/warnings. 319 rendered samples; East76/West73/North86/South84 frames. Durations3040/2920/3440/3360ms, respectively. Every source slot present, unchanged across render; full viewport and actor crop margins checked. All four complete sampled join boards inspected and Marsh visible. 5,691 frozen runtime/art inputs and all2,931 owner non-log files unchanged. APNG decoded duration expansion reproduces every native sample byte-exact. Combined viewing video800x848,25fps,86frames,3440ms. Two Python syntax checks, unique paired UID and all10published media LFS attributes pass. Evidence: output/marsh-animation-audit/cardinal-motion-preview-v3-2026-10-04/.
Failed v1 crop coordinate mapping (1288/319) and visually rejected v2 early East camera settling (1288/0) retained, including rejected publication media. V2 also had five concurrent UI/main changes; no full input-stability claim. V3 freezes camera after observable settling and actual native draw before registration and asserts a whole-figure margin each sample.

## Next action
Preview ready for visual motion review; agent inspected sampled joins, not continuous playback. No claim of every stop phase, route, room/camera or full2Dplanted feet. Bounded animation closeout remains complete; target concrete visible defects if reported. No export, commit or upload.
