# Live-room redraw reduction — October 15, 2026

Installed a small, repeatable CPU saving in Moonbay drawing, with exact appearance
parity. Normal-speed idle improves from **49.83 to 50.17 FPS** in the frozen large
station. Placement hitches remain; this is not 60 FPS acceptance.

## Change and evidence

The fresh instrumented reference separates Moonbay base drawing (1.57 ms at
normal-speed idle) from its water work (1.33 ms, nested within that base time).
The non-water prefix is a useful bounded target. The three placement submissions
cost 2.67 ms in total; five solar-room visits are not five submissions. Placement
adds one new room, whose private LOD path creates ordinary slots and capture
slots/viewport. Existing solar rooms mostly retain their cheap update path. No
layout mutation serial or rotation guard was bypassed.

`rooms/large-rooms/moonbay.gd` now exposes the contiguous base prefix and the live
water/sub drawing separately. `scripts/moonbay_base_canvas.gd` retains the prefix
on the existing parent, followed by one owned water child, then the existing
walls/gates, then room props. Threshold grating remains between the original water
layers. Every draw establishes its own transform. Water, sub, crew, doors and
warnings keep their existing clocks and rendering.

The retained key excludes only the mission and unused generic equipment clock.
External port poses, peripheral flooding, helmet visibility, Studio props/layout,
rotation, bounds, walls and other room inputs still invalidate the prefix.
Explicit self-tint uses the complete immediate fallback. The diagnostic
`--reference-moon-base` flag also restores that path. No new image/texture cache,
art, gameplay, renderer or quality change. At most one new child per Moonbay;
existing bounded water command/topology caches remain owned by their canvas.

## Benchmark

Windows, Godot 4.7.2 `ed1daf0bf`, RTX 4070 Ti, actual OpenGL Compatibility,
1920×1080. Four serial release processes: reference → candidate → candidate →
reference. Each has 180 warm frames and 120 measured frames per action/speed:
idle, zoom, placement, demolition at normal and 4× speed. **3,840 measured frames**,
all **16 phase state/camera endpoint/path pairs exact**. Source and PCK hashes are
verified; reference includes the previously accepted Bill lookup patch. The
process guard has 338 samples, no foreign Godot/duplicate game/errors and a
maximum sample gap of 0.659 s.

FPS below is 1,000 divided by pooled mean frame milliseconds, rather than an
average of instantaneous FPS readings.

| Workload | Reference mean | Candidate mean | Reference → candidate FPS |
| --- | ---: | ---: | ---: |
| Normal idle | 20.069 ms | 19.932 ms | **49.83 → 50.17** |
| Normal, all four actions | 21.770 ms | 21.542 ms | 45.94 → 46.42 |
| All actions, both speeds | 22.858 ms | 22.559 ms | 43.75 → 44.33 |

Normal idle improves in both orders: 49.85 → 50.06 and 49.81 → 50.28 FPS. Moonbay
base plus live-water callback time falls by **0.179/0.198 ms** in the two orders;
total live-room callback time falls by **0.120/0.171 ms**. The static prefix has
zero redraws during the measured normal idle phases. Draw counts and delayed
render CPU time stay essentially unchanged: retained commands are still rendered.

Across the whole mixed workload, mean frame time improves 2.39% forward and 0.21%
reverse. These unequal results include upload/scheduling variation; do not
attribute the entire mixed-workload gain to this roughly 0.2 ms component saving.
Whole-run p95 improves forward (34.652 → 33.284 ms) but worsens reverse
(32.669 → 33.419 ms). Frames over 50 ms are 13 → 11 and 11 → 12.

| Actual placement action frame | Reference | Candidate |
| --- | ---: | ---: |
| Normal, forward | 57.835 ms | 54.323 ms |
| Normal, reverse | 58.391 ms | 57.587 ms |
| 4×, forward | 71.350 ms | 78.858 ms |
| 4×, reverse | 73.733 ms | 74.994 ms |

Normal placement-phase p95 is 29.374 → 32.720 ms; maximum is 84.425 → 73.103 ms.
Those phase maxima include other frames: reference frame 17 carries 38–42 ms of
sampled atlas uploads before the placement action at frame 30. Normal placement
action frames have no sampled uploads. At 4×, placement actions overlap uploads
of 10.585 → 14.846 ms forward and 10.961 → 11.070 ms reverse. Their p95 is
33.804 → 31.194 ms, but the maximum worsens 73.733 → 78.858 ms. There is **no
consistent hitch remedy** here, and the larger normal event differences cannot
be attributed solely to the small retained-prefix saving.

Normal idle still needs about **3.27 ms less per frame** to reach the 16.67 ms
60 FPS mean budget; its p95 is 22.372 ms. Candidate passes **0/16** mean-plus-p95
60 FPS phase gates. The engine's peak texture counter is identical at 2,776.859
MiB in all four runs; this OpenGL logical counter is not physical VRAM proof.

![Average frame time and placement events](../output/live-redraw-20261015/live-redraw-results.png)

## Verification and limits

- Initial regression fails exactly three expected mission-only static-redraw
  assertions on the original code. The first private candidate passes 588 exact
  native image pairs. Final installed oracle passes **597 exact image pairs**,
  including rotations, ocean sides, walls, filtering, mission transitions,
  Reduced Motion, moving water/sub/doors, tint round trip, parent materials/flood
  shader, ports, flooding, helmet/locker/bounds/layout invalidation and fallback
  toggle. The added child is released on scene exit.
- Frozen release station: **12 cross-process images exact**, plus 12 within-process
  repeat pairs, across three zooms and lighting on/off. Full state/camera/visual
  sidecars match. The fitted station image and result plot were visually reviewed.
- Normal-source `test_large_room_retention`: 163 checks, zero failures.
  `test_moonbay_water_commands`: 493 checks, zero failures on a real display.
  `test_moonbay_missions` and `test_moonbay_save`: pass. Water commands were first
  correctly skipped by the headless runner, then explicitly run natively.
- All saved owner guards report all 2,948 non-log files unchanged. Every job uses
  scratch APPDATA and copied layouts. Source hashes match the admitted candidate;
  paired UIDs remain unchanged. Independent source review found no correctness
  issue. Scoped whitespace check passes.

This is the established **frozen private LOD QA cohort**, including the latest
accepted Bill lookup change. It is not a new Windows export, current-roster
release certification, Mac measurement or production admission of private LOD.
The normal-source native checks establish the installed rendering change's
appearance and invalidation separately.

Evidence: `C:/bs-live-redraw-20261015/ab1-analysis.json`, `ab1-process-guard.json`,
`source-snapshot.json`, `admission.json`, `visual-parity.json`, per-run identity/
owner/trace files and native logs. Reproduction helpers are in
`output/live-redraw-20261015/`. Headless batch:
`output/test-runs/20261015-134816-headless/`.

Next useful targets are the remaining animated-water CPU work and measured
first-room canvas/capture setup. Atlas upload bursts and the private LOD journal
bound remain separate open work. No further timing series is needed for this
unchanged patch without a new concern.
