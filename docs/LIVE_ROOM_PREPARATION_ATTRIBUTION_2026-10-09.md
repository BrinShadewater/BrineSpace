# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: actual live-room preparation

## Objective and acceptance

Reduce sustained drawing cost toward60FPS while preserving selected pixels,timing,
layers and explicit quality choices. Full original release scope/gates remain open.
Measure actual packaged code before changing snapshots,cache keys or render layers.

## Accepted decisions and constraints

No production optimization this pass. Large appearance/deep snapshot preparation
is not the large suspected cost in this workload; do not broadly rewrite it.
Parent dispatch and nested per-room timings overlap and must not be summed.
Rejected graph-delta and three-water-job experiments remain private.

## Current state

Extracted compiled Script.source_code from the actual frozen scene's GridCanvasScript
binding. The grid is created at runtime,so initial unstarted-scene tree search found
no grid and exited without extraction. Corrected to inspect the scene's binding,
not substitute current checkout code. Saved-byte SHA matches compiled source for:

- res://output/all-crew-storage-2026-10-07/candidate/grid.gd:
  117740cfed0f9924d454ebd9aa2eaac805513d9a85c666ba80a8dd2ddf5c8ecc
- res://scripts/large_room_canvas.gd:
  de11dee4583449a712872b77b2870895d3833fff5b2cd12c2e0b565b89fcaf69
- res://rooms/large-rooms/studio_view.gd:
  5e115f19c42237e6accefe2b4be10eac5bbecb8ad42550a87cd4414c03d9cf95

Private64frame parent LIVE probe splits slot synchronization,wet-equipment hiding,
contents maintenance,appearance/ports,canvas tree work,configure and modular-room
dispatch. Child draw callbacks remain separate. Detail pack re-mounted after crew /
badge overlays before Router compilation; actual grid SHA guard enforces execution:
b8f63324d1ad666077373d6b22b34a92ac1cb8b0a133d3e83186cb4b3b8ff857.

Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
live-room-preparation/{grid.gd,large.gd,studio.gd,identity.json,extract-owner.json};
live-room-probe/{grid.gd,candidate.json,component-summary.json,owner-pair.json}.
Helpers output/renderdoc-tools-2026-10-08/extract-live-room-source.py and
prepare-live-room-probe.py. Normal sources/UIDs unchanged; processes terminal.

## Verification

Actual debug=false1080p40room idle1x/2x/4x completes cleanly;64consecutive frames
1400..1463 with40visible rooms. Compiled grid/source guards pass. Phase crew/drone/
mission endpoints and final missions match preceding Moon component candidate.
Texturepeak2345.481MiB/exit228.259MiB,crewuploads4074,existing worker/cleanup guards
pass. Both extraction and gameplay owner2936unchanged;logs clean/adapters restored.
This is attribution,not a matched speedup or release acceptance.

| Parent LIVE scope | Median |
|---|---|
| Total parent live |3.444ms|
| Room dispatch (inclusive below) |3.371ms|
| Contents maintenance |0.051ms|
| Large slot synchronization |0.018ms|
| Wet-equipment maintenance |0.002ms|
| Report collection outside total |0.005ms|

Nested aggregate labels by ROOM TYPE (not per instance):

| Type/work | Median |
|---|---|
| Salvage workshop modular dispatch |0.525ms|
| BRINE Core modular dispatch |0.362ms|
| Storage bay modular dispatch |0.260ms|
| Crew hab modular dispatch |0.237ms|
| Research lab modular dispatch |0.234ms|
| Reactor modular dispatch |0.227ms|
| Mining drone bay modular dispatch |0.215ms|
| Solar array modular dispatch |0.203ms|
| Life support modular dispatch |0.191ms|
| Moonbay appearance/ports |0.147ms|
| Moonbay configure incl submit |0.134ms|
| Hydroponics appearance/configure |0.129/0.056ms|
| Tidal appearance/configure |0.111/0.016ms|
| Storage depot appearance/configure |0.089/0.045ms|

These identify many small costs,not one multi-millisecond snapshot hotspot.
Moonbay child draw~4.7ms remains separate; total grid18-19ms still needs reduction.

## Next action

Profile remaining grid/environment/foreground and native submission costs,including
diagnostic overhead with actual low-instrumentation controls. Read exact frozen
modular-room retained-path inputs before caching more work; preserve actors,doors,
flood/light changes and owner layouts. Static Moon layer reuse has only~1.48ms
measured potential and needs native raster/motion/invalidation proof before matched
acceptance. Full-source packages,broad workloads,original bugs,loading/memory/
endurance and Windows/Mac certification gates remain open.
