# Native performance measurements

Apple M4 MacBook Air,24GB, macOS27.2, Godot4.7.2 Compatibility OpenGL/Metal; actual1600×900 benchmark drawable. Muted, VSync off, uncapped FPS, deterministic driver. Same frozen three-room startup checkpoint/layouts, then deterministic40-room fixture with powered rooms/actors ready. Seeded resources/freebuild are confined to this performance fixture. 1×/2×/4× mean **simulation speed**, not absolute camera zoom. Camera fitted all40rooms; zoom phases oscillated near0.85/1.1 of fitted zoom. Ordinary release journeys rendered at2940×1652 and are separate from this cohort.

## Balanced source/editor comparison

Six visits ABBAAB,180 frames per action/speed per visit; three visits per build. A=7e3029a4, B=585111ca3. Identical36,679 runtime inputs verified against the parent manifest. No competing Godot/export processes during accepted visits. First profile startup followed by learned order; no certified OS cold cache. Parent is a fresh isolated **editor/source** run; storage did not permit a separate parent release export.

| Metric | Mac parent A | Integration B |
|---|---:|---:|
| Ready ms, visits |8151 /5092 /5056|5692 /4649 /4679|
| Median ready ms |5092|4679|
| 4× placement average FPS |38.97|38.99|
| 4× placement p99 ms |50.13|47.50|
| 4× placement worst ms |55.49|85.97|
| Peak RSS range, decimal GB |4.00–4.19|3.78–4.36|
| Peak physical footprint, decimal GB |5.09–5.24|4.98–5.42|

Median ready was8.1% lower in this small warm-cache/order-confounded cohort. No broad speedup or memory reduction claim follows. All nine phase cells/raw samples are in balanced-analysis.json and balanced/*.

## Actual release candidate, three fresh processes

Same audited PCK, debug=false, external QA benchmark autoload/empty scene; script call-stack tracking and automatic capture/breadcrumbs off during measurement, as with source `-s` fixtures. This is an instrumented release-template workload, separate from normal title→New/Continue. Ready4427/3513/3523ms; scene-request→ready5025/4125/4142ms. RSS2.73/3.97/4.18GB; whole-process physical footprint **4.93/5.15/5.27GB** (`time -l`). Different processes do not measure within-process growth/leaks.

Each cell pools540 frames (180×3), retaining valid outliers:

| Action/speed | Average FPS | p95 ms | p99 ms | Worst ms |
|---|---:|---:|---:|---:|
| Idle1× |45.29|26.75|35.28|77.49|
| Idle2× |43.60|29.22|41.59|68.03|
| Idle4× |43.05|29.22|32.74|35.65|
| Zoom1× |39.98|35.48|39.94|48.87|
| Zoom2× |39.11|37.03|41.70|45.09|
| Zoom4× |37.29|36.72|41.22|45.53|
| Placement1× |45.26|26.30|33.12|44.40|
| Placement2× |42.07|29.84|36.67|47.55|
| Placement4× |40.91|31.40|40.04|69.47|

No accepted measured release phase exceeded100ms. Windows863ms placement,241ms frame and27.3s startup were not reproduced here and remain unexplained; short cohorts cannot clear rare stalls. Ordinary final New/Continue loading was5459/4670ms, with separate title automatic hitch captures556–643ms. No60FPS, long-soak, cold-cache or physical-iPad memory acceptance claim. Prior iPad EXC_RESOURCE2867MB remains open.
