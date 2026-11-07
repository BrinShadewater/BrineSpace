# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: sustained draw cost

## Objective and acceptance

Improve sustained frame time toward60FPS while preserving selected animation
pixels,timing,scale,layering and default quality. Full original release scope stays
open. Diagnose actual drawing before changing retained layers or worker scheduling.

## Accepted decisions and constraints

No new rendering optimization this pass. Normal sources/UIDs remain unchanged.
Do not re-admit the three-water-job experiment from its CPU draw gain alone: prior
reverse runs lost overall FPS. Water pixel/timing reductions remain unauthorized.
Static layer reuse needs exact motion/ordering/material/pixel regression proof.
Shared private controls limit the actual release probe's certification scope.

## Current state

Frozen Moon.draw source gains64frame instrumentation at engine1400..1463. Disjoint
labels:shell/floor,floors/locker,airlock water,bay water,threshold floor/water,sub,
walls/corners/windows,doors,beacons,finish. No changed drawing commands or ordering.
Each canvas stores at most72events; collection overhead separately reported.
Compiled inherited Moon source SHA
aea5a79f3a14996a6d721a9b92d9fcbc429701d11b5a149f677e193a46c85fdd verified
through existing source guards; detail pack overrides the actual worker renderer
path before compilation. Normal Bill SHAcac60f... remains unchanged.
Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/moon-draw-components/:
moon.gd,candidate.json,component-summary.json,prepared-identity.json,owner-pair.json.
Helper output/renderdoc-tools-2026-10-08/prepare-moon-draw-components.py.

## Verification

Actual debug=false1080p40room idle1x/2x/4x completes cleanly. All three canvases
record exactly64consecutive frames1400..1463,allboarding phase. Phase crew/drone/
mission endpoints and final missions match the preceding boundary candidate.
Existing source/branch/upload/worker/cleanup guards pass. Texturepeak2345.481MiB /
exit228.259MiB;crewuploads4074. Owner2936unchanged/adaptersrestored/logsclean/
processesterminal. Probe is attribution,not an FPS gain or release acceptance.

Median sum across the three rooms PER FRAME (sum disjoint scopes first,then median):

| Component | Time |
|---|---|
| Total Moon.draw |4.700ms|
| Bay water |1.618ms|
| Walls,corners,windows |1.003ms|
| Beacons |0.550ms|
| Shell/floor |0.474ms|
| Doors |0.351ms|
| Airlock water |0.321ms|
| Threshold water |0.124ms|
| Floors/locker |0.104ms|
| Sub |0.067ms|
| Collection outside total |0.009ms|

Individual room totals:(15,25)2.561ms,(16,19)1.005ms,(21,23)1.052ms. Room(15,25)
has no prepared-water hits and bay water1.378ms. Other two have189additional prepared
hits each during64frames and bay-water playback0.109/0.128ms. This quantifies the
existing two-worker limit's third synchronous room; concurrency alone already had
mixed/rejected overall FPS evidence. Static shell/walls together roughly1.48ms
across three rooms; optimizing these alone cannot meet the full frame budget.

## Next action

Extract and inspect the ACTUAL compiled frozen grid/large-room setup sources before
instrumenting them. Narrow live-room preparation outside child draws:ordinary
trace live_rooms~10.3-10.8ms includes Moon base~4.5-4.9ms plus other children and
preparation; these scopes overlap and must not be summed. Time room appearance /
ports,large-canvas configure/deep snapshots,Studio equipment maintenance and modular
room setup separately. Prefer measured repeated-work removal; any static Moon layer
trial follows exact raster/motion/lifecycle proof and matched runs. Full-source
packages,broad workloads,original bugs,loading/memory/endurance and Windows/Mac
certification gates remain open.
