# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: wall redraw fidelity and preparation cost

## Objective and acceptance
Continue the full PC/Mac performance/release plan. Improve large-station pacing without changing selected animation/art pixels, timing, layering or default quality. Original packaged FPS, memory, loading, endurance, bug and Mac gates remain open.

## Accepted decisions and constraints
Keep canonical wall scaling private: the valid raster comparison fails exact pixel preservation. Do not promote a pass from an empty capture. Existing release and owner-profile isolation constraints remain in force.

## Current state
Normal runtime source/art unchanged. Private canonical-wall prototype and raster evidence: `output/canonical-walls-2026-10-07/`; normal-source preparation probes: `output/wall-context-profile-2026-10-07/` and `output/wall-stage-profile-2026-10-07/`.

First fixture did not bind SceneTree.current_scene; rejected engine errors/blank output. Second fixture bound the scene but its 768px capture excludes all wall edges at cell986.4; empty shell was a fixture limitation. Enlarging to1536px makes the comparison meaningful. At Brine core rotation0, low walls, zoom1.37, no fractional shift, shell comparison differs at7,224pixels/max channel delta4; both images have154,406nontransparent pixels. Nine pairs reached before stopping, not a full768-pair pass. Exact-transform cause has not been proved; no acceptance or speed claim.

## Verification
Normal-source native microprofile: eight room types/four rotations; 3,200 context checks pass, ten warmed shell draws per combination. Context construction median15us versus shell-call median334us; median per-row fraction4.4%. No context-cache implementation: too small to prioritize. Follow-up existing-stage instrumentation also3,200checks/32rows, clean engine logs. Median stage durations (over room/rotation medians): detail_room_setup=85us, actors=7us, companions=4us, configure=47us, doors=26us, shell=242us. Preparation/detail scope overlaps child stages and must not be added to them. Measurements are isolated microprofiles, not full-frame/package comparisons or visual acceptance. Both microprofiles and raster trial preserve all2,936owner non-log files; processes terminal.

## Next action
Measure inside nursery_south_facing.render_into: layout-store application, retired-prop filtering, after-layout hooks and shell command assembly at the original transform. Shell stage dominates this focused measurement; context and actor preparation are minor. Then trial only the measured larger hotspot and require exact raster/state parity plus matched active40-room packaged workload before admission. Current crew compressed provider remains private; release p95 still31–63ms and fails60FPS.
