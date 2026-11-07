# Animated water performance — October 15, 2026

Installed a small **water CPU reduction**, with exact geometry and appearance.
The installed-source release sweep saves **0.099–0.128 ms**, or **9.7–15.6%** of
its water drawing time. Whole-station FPS and placement hitches remain mixed:
**no reliable FPS improvement, hitch remedy or 60 FPS acceptance** is established.

## Change and attribution

Fresh release instrumentation places normal idle Moonbay water-body work at
1.523 ms, dynamic water at 1.465 ms, command generation at 1.295 ms, packet
stroke assembly at 0.855 ms and packet submission at 0.119 ms. These are nested
diagnostic scopes, with instrumentation overhead; they must not be added together.

`scripts/water_stroke_triangles.gd` prepares the exact rounded half-width and
feather values once for water's three literal widths: 1.1, 1.0 and 1.3. Three
static `Vector2` values replace repeated scalar preparation; other widths retain
the original calculation. The same float conversions, arithmetic order, path
acceptance, endpoint scans, joins, antialiasing, vertex/colour bytes and triangle
order remain. There are no new textures, image caches or growing collections.
Animation clocks, water levels, pumping, doors, warnings and crew are unchanged.

The existing packet/index batching is retained. A further private trial reused
normalized segment lengths; it passed exact-buffer/pixel checks, but its additional
benefit was not established clearly enough to admit. Only width preparation was
installed. The prior Moonbay retained-base and Bill navigation changes remain.

## Controlled water measurement

The first editor-binary sweep was pixel-exact and saved 0.13–0.17 ms. It is not
the accepted release timing. Actual release sweeps confirmed a smaller saving.
Final `installed-release-sweep` uses the installed source in the frozen release
executable, verifies `debug=false`, actual OpenGL and both loaded helper identities,
and archives its inputs. Two viewports draw identical water in both drawing
orders; every one of **720 animated image pairs** is exact. Readback occurs outside
the drawing timer. Full water and a continuous filling/pumping sweep are covered.

| Order / water state | Reference mean | Installed mean | Saving |
| --- | ---: | ---: | ---: |
| Forward / full | 1.194 ms | 1.066 ms | 0.128 ms / 10.76% |
| Reverse / full | 1.149 ms | 1.038 ms | 0.111 ms / 9.70% |
| Forward / filling and pumping | 0.775 ms | 0.654 ms | 0.121 ms / 15.63% |
| Reverse / filling and pumping | 0.732 ms | 0.633 ms | 0.099 ms / 13.53% |

All four p95 values improve. Forward full-water maximum worsens 1.650→1.892 ms,
so even this local result is not a universal hitch improvement. Index storage is
unchanged: one full-water layout / 92,400 bytes and 22 pumping layouts / 975,000
bytes. Existing bounded ownership and eviction remain. Sample water image reviewed.

A release diagnostic also verifies the actual Grid→Moonbay→WaterStrokes constant
chain, not just a separately loaded script. All 47,859 observed calls use the
literal-width fast path; source hashes match. Floating-point representation was
investigated and is not a missed-fast-path explanation for the mixed frame result.

## Large-station FPS and placement

Windows, Godot 4.7.2 `ed1daf0bf`, RTX 4070 Ti, actual OpenGL Compatibility,
1920×1080. Same frozen QA cohort, latest accepted Bill and Moonbay base changes.
Each run has 180 warm frames, 120 measured frames per phase and normal/4× speed.
Each series runs reference→candidate→candidate→reference, using isolated profiles.

- `ab1`: idle, zoom, placement, demolition; **3,840 release frames**, all 16 phase
  gameplay/camera endpoint/path pairs exact. Guard: 334 samples, no foreign Godot,
  duplicate game or error; maximum gap 0.755 s.
- `focused1`: idle and placement directly after the same warm-up, to investigate
  the mixed result; **1,920 release frames**, all 8 phase state/camera/path pairs
  exact. Guard: 250 samples, no foreign Godot, duplicate game or error; maximum
  gap 0.628 s. These additional runs do not replace the full-workload result.

FPS is 1,000 divided by pooled mean frame milliseconds.

| Normal idle context | Reference mean | Candidate mean | FPS reference → candidate |
| --- | ---: | ---: | ---: |
| Full workload | 19.756 ms | 19.976 ms | **50.62 → 50.06** |
| Focused idle/placement | 19.643 ms | 19.555 ms | **50.91 → 51.14** |

Full-workload idle worsens in both individual orders; focused idle improves
forward and is slightly worse reverse. Therefore the small water saving has no
dependable whole-station FPS benefit in these runs. Full-workload mean across all
actions/speeds is 22.591→23.274 ms forward and 22.091→22.154 ms reverse. Focused
whole-run mean is 21.572→21.642 and 21.597→21.633 ms. Preserve these slowdowns in
the evidence; do not report only the favourable pooled focused idle value.

| Actual placement action frame | Reference | Candidate |
| --- | ---: | ---: |
| Full workload / normal / forward | 55.974 ms | 57.125 ms |
| Full workload / normal / reverse | 55.447 ms | 57.371 ms |
| Full workload / 4× / forward | 72.439 ms | 74.843 ms |
| Full workload / 4× / reverse | 74.753 ms | 73.996 ms |
| Focused / normal / forward | 57.321 ms | 56.018 ms |
| Focused / normal / reverse | 58.268 ms | 57.605 ms |
| Focused / 4× / forward | 81.754 ms | 76.778 ms |
| Focused / 4× / reverse | 78.733 ms | 85.398 ms |

Focused normal placement p95 is 22.412→21.921 ms, maximum 58.268→57.605 ms;
4× p95 worsens 39.273→40.555 ms and maximum 81.754→85.398 ms. All focused
placement action frames have zero sampled drone upload time. In the full workload,
4× placement overlaps about 9.5–12.0 ms of sampled uploads. Its two >100 ms candidate
frames are normal placement-phase frames 13 and 15, before the action at frame 30;
they include 52.143/59.368 ms of sampled atlas uploads. These are separate from
water's roughly 0.1 ms local CPU saving.

Across both series: **5,760 measured release frames, 24 exact phase pairs**,
and **0/24** candidate mean-plus-p95 60 FPS gates passed. Current idle mean is still
about 2.9–3.3 ms above the 16.67 ms budget, depending on workload context.
Texture counter peaks are identical within each series: 2,776.859 MiB full,
2,775.782 MiB focused. These OpenGL logical counters are not physical VRAM proof.

![FPS and placement results](../output/animated-water-20261015/animated-water-results.png)

## Verification and scope

- Installed `test_water_packet_assembly`: **21,076 checks**, zero failures. The
  independent-strip oracle checks every ordered vertex/colour byte, acceptance
  and ownership. Added 75 checks cover nearby double widths, float32-expanded
  widths, branch thresholds and duplicate/tiny segments. Existing UID preserved.
- Installed native `test_water_stroke_triangles`: 180 exact pairs, zero failures;
  `test_moonbay_water_commands`: 493 checks; `test_moonbay_retained_walls`: 597 exact
  pairs, including rotations, clocks, flood/material/tint and live door cases;
  `test_large_room_retention`: 163 checks. All pass.
- Frozen station: 12 cross-process image pairs and 12 within-process repeat pairs
  exact, across three zooms and lights on/off, with equal state/camera/sidecars.
- Thirty-three saved owner guards preserve all 2,948 non-log files. Every Godot
  job used scratch APPDATA; source/paired UID match the admitted candidate. Scoped
  whitespace checks pass. Independent source review found no correctness issue.
- Early release-sweep adapter setup failures (unsupported path override, stale
  benchmark autoload, incorrect debug-query API) are excluded. The failed native
  job was stopped by its exact task-owned executable path; runtime config restored.
  Accepted release sweep and normal checks complete without script errors.

This admits a contained CPU reduction only. It does not establish a whole-frame
speedup or solve placement hitches. Private room-image LOD stays private; no art,
quality, gameplay, renderer, export or delivery change. These Windows QA results
are not Mac or current-roster packaged-release certification.

Evidence: `C:/bs-animated-water-20261015/`: `admission.json`,
`installed-release-sweep.json`, immutable sweep inputs, `ab1-analysis.json`,
`focused1-analysis.json`, process guards, source/identity/owner files, native logs
and `visual-parity.json`. Helpers and chart: `output/animated-water-20261015/`.

Next high-value work remains first-time room/capture setup and atlas upload bursts.
Further water changes need a larger measured saving in the actual release runtime;
do not repeat an unchanged timing series to seek a favourable FPS result.
