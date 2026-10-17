# Installed drone fleet and v10 docks — 2026-09-26

Production source integration of construction motion v2, mining rover v1 (selected diagonal/tyre polish), salvage drone v1 and approved-v10 dock components. The original raster artwork is unchanged. Three normalized manifests register 252 clips and 541 explicit image paths. The renderer selects states matching existing jobs; this does not add new repair, reverse-driving or other gameplay commands merely because the art pack contains them.

The built-in bay props and catalog dock props both use the new dock renderer. Native pad scale sets vehicle scale; the same scale continues into exterior travel. Docks open, lower, retract cables and seal while away, then lift on recovery. The old separate service covers remain static. Work/cargo layers, distance-driven mining wheels, heading/turn/start/stop clips, independent salvage turbines and status lamps use the simulation and pause-aware visual clocks.

Launch and recovery retain the existing 1.2-second simulation phases. The accepted 23-second art study is mapped into those phases without changing throughput, costs, battery rules or rewards. New visual fields are optional and checkpoint-validated. Rendering never awards cargo or advances jobs. The texture cache has a 256 MiB eviction target; active draw resources stay pinned and may exceed that target to prevent missing textures.

Review: http://127.0.0.1:8780/drone-runtime-2026-09-26/
- 180 native review frames with play/pause/scrub.
- 48 native in-game captures: three bays, four rotations, four phase samples, with Bill.
- 12 native room/card views.
- Fleet, battery, jobs, lifecycle/checkpoint, work-face and finite-harvest tests passed.
- 252 clip records / 144 directional phase samples passed; 541 image paths exist.
- Six native exterior handoff comparisons passed; 12 room/rotation layout lint: zero findings.
- Owner layouts and all four Studio mark files remain byte-identical to pre-install backups.

Native visuals were inspected, including correction of a texture-lifetime white-rectangle bug. Owner visual acceptance is still pending. A follow-up Windows build, brinespace-073f851880d1bda9, is verified; see docs/DRONE_WINDOWS_BUILD_2026-09-26.md. No commit or push was made. Open project.godot to use the installed source version.

Mac counterpart: builds/BrineSpace-mac-drone-runtime-2026-09-26/BrineSpace.zip (brinespace-073f851880d1bda9). Universal 2 and exact PCK audit pass; PCK matches Windows byte-for-byte. Native Mac playtesting remains pending. See docs/MAC_DRONE_BUILD_2026-09-26.md.
