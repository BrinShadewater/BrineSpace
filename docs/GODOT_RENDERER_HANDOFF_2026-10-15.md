# Project handoff

Updated: October 15, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: renderer and pacing comparison

## Objective and acceptance

Compare Compatibility/OpenGL, ANGLE and Mobile on the frozen large station with
unchanged appearance. Include zoom/placement p95/p99, worst frames and hitch
counts, not only average FPS. **Comparison complete; keep OpenGL default.**

## Accepted decisions and constraints

Keep production OpenGL, artwork, settings and delivery unchanged. Use the previous
private LOD candidate explicitly, not a claim about normal-source delivery or Mac.
Actual release runtime/driver identity, loaded-source checks, isolated APPDATA,
owner fingerprints and serial native jobs remain mandatory. Foreign Godot runs
invalidate timings; never stop another session's process without authorization.

## Current state

- Added `docs/GODOT_RENDERER_COMPARISON_2026-10-15.md`, this handoff and a status entry.
- Private drivers: `output/renderer-compare-20261015/`; artifacts: `C:/bs-renderer-compare-20261015/`.
- Overlay SHA256 remains `fa65dc5329ad6e93436e15d448581afd8f341980dfe9e2b9669bffa84df41939`.
- All three real release backends verified: native OpenGL, ANGLE/D3D11, Mobile/Vulkan.
- Corrected the private fixture's orphan synthetic Bill pilot by using existing
  checkpoint-owned Branforth; no production changes. Frozen visual checkpoint,
  sidecar, light switches and comms now deterministic across processes.
- Owner confirmed other runs paused. Fresh `pacing3` completed in both orders;
  report contains normal/4× pacing tables and reviewed, unclipped plots.
- Plot helper now accepts speed and scales each row to all three backends.
  Full 42-row phase CSV: `C:/bs-renderer-compare-20261015/pacing3-phase-results.csv`.

## Verification

Final images: `visual-gl-j`, `visual-angle2`, `visual-mobile2`, `visual-gl-k`.
Identical full state/camera/sidecar in every case, 24 exact self-repeat pairs,
6 exact cross-process OpenGL pairs. ANGLE differs by at most 1/255; Mobile by
95/255 fitted and 18/255 closer. Both fail strict pixel parity. Reviewed the
standalone comparison/difference-map figure. Prior 29 owner guards preserve 2,948
non-log files; all six fresh timing guards also preserve every one of those files.

`pacing1`: six runs / 10,080 measured frames, **excluded in full**: three foreign
Godot processes detected. Do not cite its preliminary FPS or gain claims.
`pacing2`: initially refused while Krusher repair test PID 330128 was active, later
resumed during a process gap. Three forward runs / 5,040 frames completed, then the
guard stopped the series because PID 325688 appeared during Mobile (18:55:29 UTC).
No reverse runs or accepted three-way result in that set. Do not cite it as a gain.

`pacing3`: six serial runs / 10,080 frames; 723 process samples, no foreign Godot,
duplicate game or monitor error. All source/runtime/backend guards pass. All 56
cross-backend phase snapshots and camera endpoints match; 52 paths match. The
four intermediate-path differences are confined to 4× wide sweeps, which are
interaction pacing rather than identical rendered load.

Normal-speed idle: OpenGL 49.7 FPS, ANGLE 38.8, Mobile 59.2; p95 22.9/28.2/19.2 ms.
Normal placement event maxima 62.4/67.5/59.0 ms; fitted-zoom maxima 90.4/120.8/81.4 ms.
None passes mean+p95 ≤16.67 ms in any of its 28 phases. Mobile is faster here but
still has appearance differences and hitches. ANGLE has no performance benefit
here. No production renderer, game source/art, settings or delivery changed.

## Next action

Read [follow-up research](GODOT_FOLLOWUP_RESEARCH_2026-10-15.md) for memory-counter
and shader-counter caveats, image isolation and private journal admission work.
No benchmark code or cohort was changed by that research. Current comparison and
documentation verification are complete. Do not repeat the renderer series without
a new change or unresolved concern; preserve `pacing3` and the discarded cohorts.

Next useful investigation is an event-aligned Windows thread/GPU scheduling trace
on OpenGL during zoom and placement, with game markers. Direct placement action
costs only ~8 ms of the ~60 ms event frame; remaining time is not yet attributed.
Subsequent [OpenGL tracing and lookup reuse](OPENGL_STALL_HANDOFF_2026-10-15.md)
completed the application-side investigation and installed a measured navigation
change. Kernel recording was blocked by Windows policy; full scheduling
attribution remains open. Use that handoff for the newer source and results.
Measure the topology/hazard, mask-preparation and terrain-rebuild candidates in
the [methods report](GODOT_PERFORMANCE_VISUAL_METHODS_2026-10-15.md) as appropriate.
No alternative passes strict appearance parity; Mac and current normal-source
release validation remain separate. Benchmark windows have exited; other sessions
no longer need to remain paused for this completed comparison.
