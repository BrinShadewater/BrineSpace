# Structural batching idle investigation — October 15, 2026

The normal-idle regression is **not consistent across repeat comparisons**. Its
original slow burst remains unexplained; no game-code fix is justified yet.
Keep the structural candidate private. Appearance, crew behavior and the normal
installed game are unchanged.

## Fresh release benchmarks

Two comparisons chosen before acceptance timing, each reference → candidate →
candidate → reference. Same frozen 24-source lanes and PCKs as the
[original structural study](STATIC_BATCH_PERFORMANCE_2026-10-15.md), including
private water V2/stable-ID V3/LOD and excluding the waveform trial. Actual release
Godot 4.7.2 `ed1daf0bf`, Compatibility/OpenGL, RTX 4070 Ti, 1920×1080, muted visible
secondary-display QA. VSync/frame cap off. Owner editor PID 46624 preserved.

Each process warms for 180 frames, then measures 120 each normal idle, normal
placement, 4× idle and 4× placement. **3,840 fresh measured frames / 16 exact
phase-state and camera-path pairs.** Existing benchmark observers remain; the
added OS collector and render counters are absent from these runs.

| Fresh pooled phase | Reference FPS | Candidate FPS | Reference p95 | Candidate p95 |
|---|---:|---:|---:|---:|
| Normal idle | 53.79 | 54.37 | 20.415 ms | 20.309 ms |
| Normal placement | 52.52 | 52.51 | 22.525 ms | 22.697 ms |
| 4× idle | 47.30 | 47.64 | 37.417 ms | 36.726 ms |
| 4× placement | 44.71 | 45.15 | 36.150 ms | 33.942 ms |

Normal-idle worst frames are 29.648–31.777 ms across the four fresh candidate
processes; none reproduces the original sustained ~30.8 ms ten-frame burst.
Fresh 4× placement phase frames above 50 ms **increase 7→10** despite the small
mean/p95 improvement. No fresh acceptance frame exceeds 100 ms. **0/16** candidate
phase gates meet both mean and p95 ≤16.667 ms. These small averages do not establish
a broadly reliable pacing gain or performance relative to the installed game.

Every valid original row remains. Pooling original plus fresh release comparisons
(5,760 frames, excluding all added-diagnostic runs) gives:

| All three studies | Reference FPS | Candidate FPS | Reference p95 | Candidate p95 |
|---|---:|---:|---:|---:|
| Normal idle | 54.27 | 54.18 | 20.211 ms | 21.059 ms |
| Normal placement | 53.10 | 53.20 | 22.169 ms | 22.699 ms |
| 4× idle | 47.85 | 48.25 | 37.102 ms | 36.426 ms |
| 4× placement | 45.21 | 45.62 | 36.150 ms | 33.821 ms |

Normal idle is essentially flat when the original regression is included; its
pooled p95 remains worse. Do not reinterpret the fresh sign reversal as a fix.

## 4× placement hitches

Action is frame 30; following window is frames 31–90, excluding action.

| Fresh series / order | Action reference→candidate | Next frame | Following mean | Following p95 | Following >50 ms |
|---|---:|---:|---:|---:|---:|
| repeat1 forward | 56.492→57.587 | 23.850→24.920 | 22.896→22.002 | 34.535→32.524 | 1→2 |
| repeat1 reverse | 58.663→56.258 | 24.649→24.204 | 22.436→22.229 | 39.617→33.821 | 1→1 |
| repeat2 forward | 58.279→57.927 | 23.246→25.393 | 22.366→22.792 | 34.430→34.510 | 0→1 |
| repeat2 reverse | 59.001→58.701 | 23.534→23.163 | 22.727→22.349 | 35.484→33.683 | 1→1 |

All timing cells are milliseconds. Mean fresh action improves **58.109→57.618 ms**
(~0.49 ms), but one order worsens. Following-window >50 ms frames total **3→5**
across 240 frames per lane, or **7→9** including the four action frames. The
original two action comparisons both worsened slightly. Placement pacing is still
mixed; no hitch fix is claimed.

## What the investigation established

The original reverse candidate's normal-idle frames 71–80 slow across drawing,
simulation and unchanged validation scopes. No changed cap/floor assembly callback
runs there. In **all 16 new processes**, normal idle retains 72 floor slots,
13 grid redraws and no floor/wall callback stages. This supplies no evidence of
extra structural invalidation. Retained polygon commands still render each frame,
so absence of a rebuild does not rule out downstream renderer or driver work.

Pinned GLES3 code uploads polygon VBO/IBO data with `GL_STATIC_DRAW` when a command
is created and retains the buffers for rendering. The two merges preserve total
vertices, indices and vertex formats. The canvas instance limit counts instance
records rather than polygon vertices; no mesh-size threshold explaining the burst
was found. See the pinned [GLES3 implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/drivers/gles3/rasterizer_canvas_gles3.cpp)
(`request_polygon`, `_render_batch`, `_add_to_batch`) and
[polygon lifetime](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/servers/rendering/renderer_canvas_render.h).

Separate diagnostic fixtures record configured item-buffer size 16,384 and
phase-mean render objects/primitives/buffer bytes. Object means are about
7,006–7,268, below that configured limit. In diag1, both lanes have identical
buffer-byte phase means for normal idle, normal placement and 4× idle:
~39.22 / 39.27 / 39.28 MB. Fresh acceptance normal-idle draw calls remain
2,116.75→2,076.70 (~40 fewer). There is **no demonstrated persistent buffer-growth
regression**. Phase means cannot exclude transient allocations, and object counts
are not a complete accounting of all internal instance-buffer behavior.

## CPU diagnostics and their limits

Two additional four-process diagnostic series contain **3,840 measured frames /
16 exact state-camera pairs**; they are excluded from every release FPS table.
Game source/PCK bytes remain unchanged. The fixture adds one UTC/tick marker,
render counters and an external query-only earliest-created-thread sampler.

- `diag1`: all-process CPU polling proved too heavy: mean collection cycles
  ~35.6–39.4 ms, followed by a 100 ms wait. Its reverse candidate frames 81–90
  average **30.872 ms** with approximately one main-thread CPU core accounted for
  over that interval. A reference ten-frame window containing a **172.535 ms**
  hitch accounts for ~0.57 main CPU core. These are different observed signatures:
  the candidate burst is approximately CPU-busy; the reference hitch spends
  substantial elapsed time outside that main-thread CPU accounting.
- Coarse top-process samples show increased desktop CPU activity coincident with
  the diag1 candidate burst. These are censored, unweighted sampled observations,
  not exact-window lower bounds and not proof that any named process caused it.
  The collector itself adds load. No diagnostic is discarded to favor a lane.
- `diag2`: removes all-process polling; target-process/system-only collection
  averages **0.26–0.54 ms per sample**. The reverse candidate normal-idle burst
  does not recur. Other slow phases remain, including >100 ms in diagnostic
  4× idle; none is silently included in clean acceptance statistics.
- Nominal 5 ms thread polling actually samples around **15.6 ms** apart, with
  15.625 ms CPU-accounting granularity. UTC/tick alignment and interpolated
  interval estimates are adequate for broad busy/wait distinctions, not individual
  frame causality. Cycles are not retired instructions or proof of clock speed.
  Blocking versus OS preemption, core migration and driver waits remain unproved.

These observations do not retrospectively identify the original burst's cause.
No power-plan, process-priority, affinity, game logic or crew changes were made.

## Scheduler trace limitation

WPR is installed and initially reported no active recording. Its built-in verbose
CPU profile requests ~3.2 GiB of buffers, so a bounded custom context-switch profile
was prepared instead (64×256 KiB, no stacks). An initial `CPUConfig` spelling was
schema-rejected; corrected `CpuConfig` is valid. The valid start then failed with
**0x80070005 — Access is denied**. Status again confirmed **not recording**. No
ETW trace or extra game run started. A local TraceEvent parser is available, but
capture permissions block the next discriminating scheduler/core-migration check.
This is an OS diagnostic limitation, not evidence of a scheduler fault. The custom
profile follows the documented [system-provider configuration](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/systemprovider).

## Verification and handoff

- Both 24-source lanes and PCKs are byte-identical to the original structural
  study. All physical loaded-source checks and native ABI/counter guards pass.
  Same EXE/base-PCK hard links; authoritative relocated native descriptor hashes.
- All 17 protected-profile guards and 16+16 native DLL guards pass. Final **2,948**
  non-log protected files equal initial and prior accepted fingerprints. Existing
  [profile-incident caveat](TEST_PROFILE_INCIDENT_2026-10-15.md) persists.
- Installed source, paired UIDs and protected tests remain unchanged. Existing
  **1,148 focused raster pairs, 38 cache checks, 17 station/first-paint pairs and
  12 repeats** are reused for byte-identical lanes, not claimed as fresh visual
  tests. The original representative image was inspected.
- Every new process passes release/window/render/state/camera/log guards.
  At least 20 GiB free storage remains. No export, Mac acceptance, RSS/native
  transient memory acceptance or long-soak claim.

Evidence: `C:/bs-static-idle-20261015/` (`repeat1/2-analysis.json`,
`pooled-summary.json`, `diag1/2-diagnostic-analysis.json`, raw `*-os.json`,
`wpr-start-valid.log`, `wpr-status-final.log`, `final-audit.json`). Helpers and
bounded trace profile: `output/static-idle-20261015/`.

Next discriminating check: an administrator-enabled bounded scheduler trace of
the same isolated frozen fixture, aligned to a recurring burst. Establish running
CPU/core transitions and wait reasons before another speculative batching change.
