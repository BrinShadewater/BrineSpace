# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: environment rendering CPU

## Objective and acceptance

Improve environment rendering without changing appearance, then benchmark the
large station against the accepted floor-batched baseline. Installed shared-edge
frond geometry for a consistent 0.15–0.17 ms seabed CPU saving. Frame-time gains
are small; smooth 60 FPS and pacing remain open.

## Accepted decisions and constraints

Keep original animated vertices, UVs, indices, colors, draw order, textures,
filtering, clocks, reduced-motion/Low behavior and live gameplay. Native work
serial, muted secondary display, scratch APPDATA with copied layouts, owner
fingerprints. No export, commit, art or shader change. Normal Grid/private LOD
and Windows delivery unchanged. Do not repeat rejected wave rectangle conversion.

## Current state

- `scripts/ambient_fronds.gd`: compute the unchanged height-independent sine
  amplitude once (24 sine evaluations become two), reuse seven row edges instead
  of calculating twelve, and preallocate the original 24 ordered vertices. Fixed
  UV/index topology uses 336 packed bytes. Each returned buffer belongs to the
  caller; no animated geometry or scene/texture references are cached. Original
  `offset()` and rectangle fallback remain; `reuse_strip_geometry=false` preserves
  original geometry for comparison. Existing module UID retained.
- `tests/test_frond_geometry.gd` + UID: independent original formula, byte-exact
  buffers and mutation isolation; headless `render-perf` index entry. Initial
  private ownership test caught shared-array mutation; returning UV/index copies
  fixed it. Do not remove those copies without revisiting the ownership contract.
- Upright kelp is unchanged: fresh profiling found zero draws in this fixture.
  Fronds have 20 draws/frame, costing 300–312 us before the change.

Evidence: `C:/bs-environment-render-20261015/`, final candidate under `plants/`.
Drivers: `output/environment-render-20261015/`. Final source SHA256:
`0b23003f2615a962f18168d723048d385d9ef57fd4a59e3c760bd5602ab7c1cc`.
Reference PCK: `e6c8e6f0b99509f28d726467e23033ede9df851897aee55844054e79e2f87c85`.
Candidate PCK: `fa65dc5329ad6e93436e15d448581afd8f341980dfe9e2b9669bffa84df41939`.
`plants/final-verification.json` pins installed bytes and measured PCK identities.

## Verification

Normal headless `output/test-runs/20261015-103714-headless/`: **1,517 checks / 504
cases**, exact position/UV/index bytes across settings, clocks, seeds, fractional
and negative rectangles, independent plant buffers and caller mutations.
Normal native `20261015-103725-native`: **288 exact nonblank comparisons**; another
**288 reflected/flooded pairs** via `normal-wet`. Together cover 288 frond pairs
and 288 unchanged kelp controls, three selected sources each, both filters,
fractional widths, clocks and reduced motion. Successful logs clean.

Private continuous CPU diagnostic: **240 exact animated pairs**, 20 fronds/frame,
both viewport orders. Original 324.73/326.23 us -> candidate 115.94/116.83 us.
Final complete-station `plants/station-parity1`: **12 exact adjacent image pairs**,
fitted/.25/.5 zoom, both directions/repeats, frozen gameplay snapshots equal.
Fitted capture visually reviewed. Independent source review found no actionable issue.

Actual debug=false `plants/compare1`: **3,840 frames / 16 exact phase gameplay-camera
pairs**, idle/pan/zoom/lighting at 1x/4x, both orders, no foreign Godot. Overall means
22.066->21.892 and 22.069->21.702 ms (0.8–1.7%). Seabed CPU saves 145–169 us in
every paired phase. Normal idle 18.962->18.946 and 19.165->18.688 ms:
**52.2–52.7->52.8–53.5 FPS**; the first comparison is essentially flat, so no
uniform idle-FPS saving is established. Idle p95 worsens 20.975->21.108 and
20.581->21.045 ms. Overall p95 improves 9/16 phases. Maxima 68.525->74.389 and
70.630->69.170 ms; >50 ms frames 3->3 and 4->3. No general pacing/hitch claim.
Draw calls (~2131) and texture peak (2784.653 MiB) unchanged. All 16 candidate
60 FPS mean/p95 gates fail. Broader whole-frame deltas are not solely attributed
to the smaller consistent seabed CPU saving.

**21 recorded owner guards preserve all 2,948 files.** Runtime override restored;
only pre-existing editor PID46624 remains. No test/game job left running.

## Next action

Current frozen census: nine environment passes contribute 436 conditional calls;
foundations 143, terrain 156, derelicts 57, exterior actors 56. These masks overlap
and exclude the Grid's direct live seabed drawing; static seabed alone is 11 calls.
Reference/restored totals both 2114. Timings are attribution, not additive savings.

Seek an exact ordered submission or CPU reduction in those remaining groups.
General foundation occlusion was rejected at source review: fascia and shadows
spill north of southern terrain, blockers do not imply opaque pixels, exposed
rock boundaries vary, and visibility/connectivity must invalidate retained keys.
Do not install a blocks-only skip or merge cliff/ridge drawing across their order.
Mac, target hardware, broader pacing and early-access release gates remain open.
