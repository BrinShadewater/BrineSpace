# Survey Probe animation handoff

Updated: September 26, 2026 · BrineSpace · Survey probe mission animation

## Objective and acceptance
Owner requested torpedo-style movement, resource scanning and return to its probe
bay. Delivered as a standalone animation pack/preview, continuing the drone work.
New directional art and motion await owner visual review; no gameplay installed.

## Accepted decisions and constraints
Use the existing Survey Probe Bay study's charcoal steel torpedo, muted cyan panel,
glass nose and rear nozzle/fins. Four cardinal probes and launchers were copied
from the Desktop concept study. Four diagonal views were generated independently,
with no whole-body bitmap rotation/mirroring. Shared display scale .34; existing
study's probe/cradle ratio preserved. Actual native room scale remains unverified.

## Current state
`assets/survey-probe-v1-2026-09-26/`, http://127.0.0.1:8772/ (localhost server PID
270340). 32-second cycle: charge/prelaunch, accelerate, cruise, brake, scan, turn,
return, align, reverse into cradle, receive survey data. Four bay orientations;
eight travel/scan headings. 52 reusable state/heading combinations and 960 separate
wake/sonar effect frames. Rigid hull poses deliberately remain stable; motion is
root travel, direction changes, wake/scan effects and independent lamp animation.
Review controls include close-up/native inset, pause, quarter speed and timeline.

Main files: build.py, manifest.json, mission.mjs, preview.mjs, index.html,
test_mission.mjs, validate.py, sources/, poses/, effects/, atlases/, README.md and
PROVENANCE.md (exact generation prompts and original paths). Older drone previews
on 8767/8768/8771 are preserved. No live game scripts, rooms or owner saves changed.

## Verification
All 52 combinations, 960 effect frames and atlases pass path/alpha/geometry/hash
checks; no source upscaling. 5,120 mission samples across four bay orientations
pass position continuity, nose-first travel, reverse-only docking, stationary scan,
survey retention and exact loop join. Browser representative scan and docking
checks are stored in review. Artwork board covers all eight headings.

## Next action
Latest owner follow-up: strengthened the sweep into a blue holographic projection
sheet with a bright core, soft halo and horizontal striations. Preserved the
approved contour/grid uncovering behavior. Beam clears at completion; map remains.
All effect exports pass validation; right-to-left motion is identical in all eight
headings. Evidence: review/hologram-preview.png and hologram-checks.json.

Owner follow-up replaced the forward sonar pulse with a four-second right-to-left
topography scan over the surrounding area. A vertical sweep reveals contour lines
and a faint grid; mapped contours persist during return. The overlay is world/
screen aligned in all headings. Eight scan effects rebuilt, 60 frames at 15 fps;
scan state is 120 ticks at 30 fps. Export validation and monotonic sweep/heading
independence checks pass. Terrain contours illustrate scanning, not live elevation.

Owner review in the mission preview and close-up. Then native room/world-scale,
wall occlusion and clearance calibration before gameplay integration. Existing
launcher views are painted studies with varying fittings, not a common 3D model;
the preview masks tube passage but does not articulate hatches. No actual resource
discovery/persistence, pathfinding or bay gameplay has been installed.
