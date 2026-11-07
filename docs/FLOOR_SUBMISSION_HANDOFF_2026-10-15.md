# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: floor rendering submission

## Objective and acceptance

Optimize floor rendering without changing appearance; compare the large station
against its current frozen baseline. Installed the combined threshold/border
packet after exact pixels and paired Windows timing. Smooth 60 FPS remains open.

## Accepted decisions and constraints

Preserve tile art, clipping, UVs, float colors, room order, retained floor behavior
and live actors/doors/warnings. No new raster LOD, art, gameplay or layout changes.
Native jobs serial on the secondary display, isolated APPDATA, copied owner layouts
and real-profile fingerprints. No export/commit/publication. Existing private LOD
remains confined to the frozen benchmark overlays; normal Grid is unchanged.

## Current state

- `rooms/floor-profiles-v1/modern_details.gd`: eligible adjacent doorway threshold
  polygons share one textured packet, retaining each original triangulation,
  arithmetic, UVs and edge order. Zero/one thresholds keep the original stamp path.
  Packet finishes before other floor drawing; no cross-room batching or new cache.
- `rooms/whole-room/room_lighting.gd`: on Windows, its four fixed floor-edge shadow
  outlines share one packet. Existing equipment-shadow cache, palette, budget and
  conservative fallbacks are unchanged. Other platforms keep original outlines.
- `scripts/floor_border_packet.gd` + UID: fixed native closed-strip geometry,
  40 vertices / 96 indices; one shared 1,344-byte packed buffer set, no texture or
  canvas references. Pinned Godot geometry attribution and MIT notice included.
- `tests/test_floor_threshold_packets.gd`, `tests/test_floor_border_packets.gd` +
  UIDs; native `render-perf` index entries. Existing unrelated index edits preserved.

Evidence: `C:/bs-floor-render-20261015/`; final combined evidence in `combined/`.
Drivers: `output/floor-render-20261015/`. `final-verification.json` records installed
source hashes, exact measured bytes, UID pairs, unchanged Grid and owner guards.
Reference PCK: `9bbb318a36c6bea20d2dd4f87a7114b417e4c19378ff921cc398653341f50e60`.
Candidate PCK: `3624917b7b26f2004249c992b6174f2ead86b346c7def0ecd594ee581f75e743`.
Windows delivery remains unchanged.

## Verification

Normal-source native run `output/test-runs/20261015-093800-native/`: all four pass,
logs clean. Thresholds: **1,082 checks / 360 exact visible image pairs**, zero/one/
multiple/duplicate and rejected ports, rotations, fractional scale, nearest/linear,
inherited tint and flood shader; up to four calls saved. Borders: **676 checks /
192 exact pairs**, rotations/scales/oversampling/materials, exactly three calls
saved, immutable buffers and canvas release. Local floor retention: **23 checks**.
Equipment shadows: **128 exact pairs**, including original conservative fallbacks.
Independent source review found no remaining actionable issue; its platform-test
finding was corrected before the normal native run.

Final actual debug=false complete-station `combined/station-parity2`: **12 exact
adjacent image comparisons** at fitted/.25/.5 zoom, repeats and both directions;
gameplay snapshots equal. Conditional calls: 2252->2114, 1909->1772, 1301->1226.
Final capture visually reviewed. Final PCK identities verified after this check.

Combined `compare1`: **3,840 frames / 16 exact phase gameplay-camera pairs**,
idle/pan/zoom/lighting at 1x/4x, both orders, no foreign Godot. Mean frames:
22.885->21.995 and 22.316->21.985 ms (about 1.5–3.9%); p95 improves in 13/16 phases.
Normal idle: 19.573->19.042 and 19.238->18.986 ms, **51.1–52.0->52.5–52.7 FPS**.
Calls ~2269->2131; delayed render CPU 5.126->4.830 and 5.044->4.804 ms. GPU samples
disagree between orders; no GPU-time saving claim. Texture peak unchanged at
2784.653 MiB. Frames >50 ms: 5->3 and 4->3; maxima 116.599->70.056 and
66.365->67.557 ms. This does not establish a general hitch fix. All 16 candidate
60 FPS mean/p95 gates fail.

Earlier threshold-only `compare1` in the parent evidence directory also covers
3,840 frames. Its small idle saving and lower calls were consistent, but a first
candidate 4x slowdown made aggregate timing inconclusive; final acceptance uses
the combined comparison, not a claimed threshold-only FPS improvement. Preliminary
combined parity1 predates a header/license constant edit; parity2 pins final bytes.

**21 recorded owner guards preserve all 2,948 files.** Runtime override restored;
only the pre-existing owner editor PID46624 remains. No test/game job left running.

## Next action

Re-profile the remaining environment and render-submission groups against this
baseline. Idle is still roughly 2.3–2.4 ms over the 16.67 ms budget; broader pacing,
Mac/native target hardware and early-access release gates remain outstanding.
Do not repeat already-batched floor tiles or loosen the exact-pixel gate.
