# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: live-room surfaces

## Objective and acceptance

Owner requested live-room surface optimization toward 60 FPS with unchanged
appearance, followed by a large-station benchmark. Require exact native pixels,
matched release workload and bounded memory; crew, doors and warnings remain live.

## Accepted decisions and constraints

Install bounded ordered Moonbay primitive packets on Windows. Keep every existing
rectangle, texture/sampling rule, transform, alpha order and AA line/polyline
boundary. Native platform fallback stays intact. No raster or animation reduction.
Private LOD remains private; Windows delivery and Mac acceptance are unchanged.
No commit/export/publication requested.

## Current state

- `rooms/large-rooms/moonbay.gd`: packet only adjacent corner triangles, window
  bolt circles and contiguous beacon primitive groups. All other drawing and
  gameplay functions retain their existing behavior. Reference switch:
  `--reference-moon-surface-packets`.
- `scripts/room_surface_packet.gd` plus UID: original native polygon triangulation,
  per-vertex float colors/UVs and the previously verified Windows circle fan.
  Immutable circle index offsets use a 32-entry cache, at most 24,576 index bytes.
  Packets own their appended geometry; no textures or scene references are cached.
- `tests/test_room_surface_packet.gd` and `test_moonbay_surface_packets.gd`, paired
  UIDs, `tests/index.json`: buffer ownership/eviction test and native visual/count
  matrix. Explicit native lane corrects the capture-guard heuristic.
- `docs/CURRENT_STATUS.md`: milestone recorded. Existing Moonbay UID preserved.

Evidence: `C:/bs-live-surfaces-20261015/`; drivers: `output/live-surfaces-20261015/`.
Candidate PCK SHA256:
`54de9ab716c2c25c28c6bd6224a857748b3e568ceb636810f346b9b786915e3e`.
Reference PCK: `9dc3459617b35c0936977818a8a1104c572591d5793cff650e56d6f992f8fa49`.
Normal Moonbay file SHA256:
`3aebe4a664a47260fe74b43c4fa7dfa08be907ca50dcb14d86baa8c0b3e6ed43`.
Helper file SHA256:
`012cfd2d56c996155658d990790e8076869ad573f967dc4c94ea388c03e95150`.
Installed Moonbay equals measured source after line-ending normalization; helper
is byte-identical. `production-source.json` records both comparisons.

## Verification

Prior conditional census attributes 490 calls to the live-room surface, including
Moonbay's 244 (base plus retained descendants). Selected runs do not cross shadow
rectangles, AA strokes or texture changes. New native matrix saves 44–46 calls
per complete Moonbay, across all 192 cases: rotations, raised/low walls, mission
phases, fractional bounds, nearest/linear, modulation, custom tint and actual flood
shader. Every image is exact and visible. Missing packet API fails first; green
passes. Buffer ownership, winding, colors, UVs, cache eviction/rebuild: 506 checks.

First prototype rebuilt circle offsets per frame and regressed warm gate CPU.
Bounded immutable offset reuse removes that work. Final warmed, paired animated
gate sweep: 376 exact image pairs; reference -> candidate 399.79 -> 343.17 us and
395.88 -> 338.97 us, about 14% lower in this active filling/draining fixture.
P95 440 -> 373 and 429 -> 375 us. Initial cold art loading is excluded by an
eight-frame warmup. This component result is not the station's steady gate saving.

Installed-source runners:
`output/test-runs/20261015-091511-headless/` (506 checks),
`output/test-runs/20261015-091529-native/` (new 578 checks / 192 exact pairs;
retained-wall 580 exact pairs / lifecycle pass; complete large-room composition
163 checks / 94 exact pairs). No logged errors/warnings/leaks. Full actual-release
station parity adds 12 exact comparisons at fitted/0.25/0.5 zoom and equal frozen
states. Static tail and live gates are explicitly repainted when toggling the
diagnostic flag. Representative native room and station images reviewed.

Actual debug=false benchmark: 3,840 frames, idle/pan/zoom/lighting at 1x/4x in both
orders. All 16 gameplay/camera pairs and loaded source/PCK identities match.
Process guard records no foreign Godot worker or duplicate game.

| Order | Reference mean | Candidate mean | P95 improves | >50 ms frames |
|---|---:|---:|---:|---:|
| Reference first | 22.748 ms | 22.213 ms | 5/8 | 4 -> 3 |
| Candidate first | 22.726 ms | 22.123 ms | 5/8 | 7 -> 3 |

Observed workload means improve 2.35% / 2.65%; some reference lighting/4x phases
also slow outside the changed work, so do not attribute every difference to this
small packet change. Normal idle calls 2313 -> 2269, about 44 fewer (1.9%). Its
delayed render CPU 5.244 -> 5.113 and 5.154 -> 5.100 ms; station gate CPU only
308 -> 300 and 307 -> 299 us. These timing scopes overlap and are not additive.
Normal idle frames 19.794 -> 19.336 and 19.445 -> 19.224 ms: paired reference
50.5–51.4 FPS -> candidate 51.7–52.0 FPS. Compare these contemporaneous controls,
not absolute FPS from earlier runs. All 16 candidate 60 FPS mean/p95 gates fail.
Texture peaks unchanged, 2784.653 MiB. Worst frames 69.292 -> 68.963 and
123.791 -> 73.408 ms; no hitch fix is established. The 123-ms reference outlier
is during lighting, not placement; its sampled drone uploads total only 62 us.

Fifteen completed owner guards preserve all 2,948 non-log files. Independent review
finds no actionable issue. Scoped whitespace checks pass. No task-owned QA process
remains; owner editor PID46624 stays open. Unrelated dirty work is preserved.

## Next action

Requested live-room change and benchmark are complete. No further validation is
pending for this bounded source admission. Floor and environmental submissions
remain larger groups for a new measured batching pass. Full 60 FPS, structural
pacing, endurance and actual Windows/Mac release acceptance remain open.
