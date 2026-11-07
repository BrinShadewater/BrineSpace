# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: door-style lookup performance

## Objective and acceptance

Reduce measured door validation work without changing owner styles, layout freshness,
poses, lighting or simulation. Full PC/Mac release acceptance remains open.

## Accepted decisions and constraints

Normal painted-door style lookup now preloads the layout-store script rather than
calling the runtime resource loader on every lookup. It still calls the same live
`shared_positions` method. No new style/layout cache, source/art change, downscaling,
quality change or export. Existing script UID unchanged.

## Current state

`rooms/doors/painted_door.gd`: one resource-call substitution in `style_override`.
`tests/test_door_style_lookup.gd`, paired unique UID, render-perf index: independent
original lookup oracle, every catalog style and room mapping, quarter normalization,
invalid inputs, layout reuse on/off and wholesale data replacement without revision.
Private evidence under `output/door-style-preload-2026-10-06/`; finer profiler under
`output/door-depth-2026-10-06/`.

## Verification

Finer native attribution on the accepted connectivity implementation: style selection
~356–359 us/frame, depth masks ~92–94 us, pose lookup/narrow classification ~73–84 us.
Do not treat the earlier ~0.59 ms grouped measurement as depth-mask cost alone.
Diagnostic instrumentation adds overhead; no profiled FPS acceptance.

Direct private lookup comparison: 4562 checks pass. Three alternating 5000-call
pairs: original 14026/14093/14024 us versus candidate 7314/7412/7357 us (~48% lower).
Actual normal source expanded permanent oracle: **11858 checks pass**, zero errors.
Resource preload parses successfully through current dependencies; no cycle error.
Existing same-resource layout reads remain live in the tested mutation scenarios.

Matched native 40-room 1080p idle/pan at 1/2/4x, 60 samples per phase. Both branches
use accepted connectivity reuse and identical private style-call counters. Candidate
department lookup execution required in every phase. Door/light preparation:

| Phase | Before ms | After ms |
|---|---:|---:|
| Idle 1x | 1.587 | 1.475 |
| Pan 1x | 1.578 | 1.460 |
| Idle 2x | 1.596 | 1.496 |
| Pan 2x | 1.584 | 1.473 |
| Idle 4x | 1.601 | 1.460 |
| Pan 4x | 1.597 | 1.461 |

All six full crew/drone snapshots, 30 door entries (including style/frame/depth
masks), full lighting keys, powered-room counts and zoom equal. Source representation
does not change drawn geometry. Whole-frame results mixed and still fail, candidate
p95 36.426–46.934 ms; no aggregate FPS or loading improvement claim. Fixture uses
private compressed crew, distinct from normal release gameplay.

**Texture counters differ:** candidate lower by 0.151–0.185 MiB, final
3168.333 versus reference 3168.518 MiB. Cause unassigned; startup/warm-up presentation
and upload counters also differ slightly. Do not claim memory savings or identical
allocation histories. Both remain above the large-scene budget. Gameplay and door/
light state comparisons remain exact; repeated release-candidate runs still required.

All successful logs clean; all 2936 owner non-log files unchanged. UID uniqueness
and test-index JSON checked. All processes terminal.

## Next action

Continue larger measured costs (connectivity/room-port preparation and renderer
submission boundaries). Depth masks are a smaller lead than previously grouped
timing suggested. Resolve allocation-history variance when certifying repeated
memory/loading runs. Original bugs, lifecycle, endurance and actual packaged
Windows/Mac performance/signing/Gatekeeper gates remain open.
