# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: remaining drawing CPU

## Objective and acceptance

Continue performance work toward 60 FPS with identical appearance, live animation,
crew, doors and warnings. Admit a contained CPU saving after exact geometry and
native pixels; distinguish component savings from whole-frame improvements.

## Accepted decisions and constraints

Install direct packet vertex assembly. Keep all original float/vector arithmetic,
stroke acceptance, triangle order, antialiasing and bounded index-cache ownership.
The independent-strip path remains the oracle. Private room LOD stays private;
Windows delivery and Mac acceptance are unchanged. No export or commit requested.

## Current state

- `scripts/water_stroke_triangles.gd`: 61 added lines route packet strokes through
  one ordered vertex allocation/append, replacing three temporary vertex strips.
  Reuse identical rounded endpoint calculations; retain native color fills and
  existing index/key snapshots. No shader, texture, clock or draw-order change.
- `tests/test_water_packet_assembly.gd` and paired UID: 3,000 packet stress cases
  compare acceptance, every vertex/color byte, strip order and independent ownership
  against the unchanged nonpacket path. Includes short/closed/duplicate segments,
  tiny/large coordinates, varied colors and width thresholds. Registered in
  `tests/index.json` render-perf; runs headless.
- `docs/CURRENT_STATUS.md`: acceptance milestone recorded.

Evidence: `C:/bs-moon-prefix-20261015/`; drivers:
`output/moon-prefix-20261015/`. Frozen candidate PCK SHA256:
`b6a8c044702dc41c700e03ddf39d905d86e3a7114abfb94fceff25f8015f56ea`.
Reference PCK: `293947cf8939b09611abc7b5d761abb65d24ff8df571a00740c4336bb922a7ff`.
Normal helper file SHA256:
`87cec1d37e2847aa9f023251b5f033fda6cd07b0f3a907795a0f014543224aa9`.
Normal executable source equals the measured candidate after excluding comments
and normalizing line endings; three existing normal comments are preserved.
`production-source.json` records the normalized source identities.

## Verification

Fresh attribution rejects the proposed Moonbay retained prefix: `Common.begin`
costs only 134–138 us; the whole fixed prefix costs 176–183 us, versus about
1.6 ms for the base. No prefix caching or Moonbay renderer change was installed.

New geometry test fails first for the missing assembler, then passes all 21,001
checks with the private and installed candidates. Installed-source runner evidence:
`output/test-runs/20261015-035254-headless/` and
`output/test-runs/20261015-035304-native/`. Native stroke cache/scalar checks 7,960,
180 exact visible image pairs; water 493 checks, 244 exact image pairs; complete
large-room composition 163 checks. All pass, no logged errors/warnings/leaks.

Final installed-source continuous sweep: 720 exact animated pixel pairs across
full water and filling/pumping, both drawing orders. Representative image reviewed.
Reference -> candidate mean water CPU (us):

| Order | Full water | Filling/pumping |
|---|---:|---:|
| Forward | 1571.29 -> 1388.24 | 992.87 -> 852.68 |
| Reverse | 1567.52 -> 1375.41 | 990.07 -> 850.08 |

This is an 11.65–14.14% local saving (0.14–0.19 ms). All four p95 values improve;
forward full-water maximum worsens 2287 -> 2442 us, so no universal hitch reduction
is claimed. Index storage unchanged: 92,400 bytes for full water; 22 pumping
layouts / 975,000 bytes. Cache caps unchanged, no additional textures or retained
buffers. `production-sweep.json` and `production-sweep-sample.png` preserve evidence.

Actual debug=false release comparison: 6,720 frames, idle/pan/zoom/lighting/
placement/demolition/interface at 1x/4x in both orders. All 28 phase gameplay and
camera pairs match; all loaded-source and immutable PCK checks pass. Native process
guard observes only the pre-existing idle editor, no foreign Godot worker.

| Order | Reference mean | Candidate mean | P95 improves | >50 ms frames |
|---|---:|---:|---:|---:|
| Reference first | 23.607 ms | 22.094 ms | 10/14 | 15 -> 12 |
| Candidate first | 22.166 ms | 22.029 ms | 8/14 | 9 -> 10 |

Do not attribute the broad first-reference slowdown to this small geometry change.
Normal-speed idle 19.698 -> 19.658 ms and 19.818 -> 19.488 ms; candidate about
50.9/51.3 FPS. Idle large-base CPU saves 157/142 us; reverse-order all-phase savings
117–150 us are consistent with the scoped saving. Draw calls and delayed render
CPU remain essentially flat. All 28 candidate 60 FPS mean/p95 phase gates fail.
Texture peaks identical, 2784.653 MiB. Worst frames 121.173 -> 73.762 ms and
71.494 -> 71.046 ms. The 121-ms reference demolition frame includes about 25 ms
action, 25 ms station step and 50 ms grid drawing, with no drone upload; this is
not evidence that the previous structural-change outlier is solved.

Fourteen completed guards here and two earlier red/green preflight guards in
`C:/bs-local-floor-20261015/` preserve all 2,948 owner non-log files. Scoped whitespace
checks pass. Independent source review finds no actionable issue. No task-owned
QA process remains; owner editor PID46624 stays open. Unrelated dirty work preserved.

## Next action

No further validation is pending for this bounded change. Larger remaining costs
include approximately 5.3 ms delayed render submission and 4.4 ms live-room drawing
in the idle profile (overlapping scopes, not additive). Attribute remaining draw
calls/material breaks before choosing another batching change. Structural-change
pacing, actual Windows/Mac release play, endurance and 60 FPS acceptance remain open.
