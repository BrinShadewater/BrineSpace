# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: current-station performance

## Objective and acceptance

Reduce the reproduced construction-completion stutter without changing navigation,
gameplay timing or visuals. Matched real-station workloads establish the scope;
this milestone does not certify the full PC/Mac release.

## Accepted decisions and constraints

Muted secondary-display native tests, isolated profiles and owner fingerprints.
Reuse the physical release runtime with small script overlays; no art copies or
screenshot batches. Preserve route ordering, shared graph caches and live collision
policy. No navigation deferral or broad refactor. Indexed provider remains private.

## Current state

Changed `scripts/bill_npc.gd`: `_template_segment_clear` rejects disjoint rectangle
bounds before the existing half-open segment sweep; stationary points use Rect2
membership. Other collision routines remain unchanged. Extended
`tests/test_navigation_segment_parity.gd` with 12,000 template-link cases.

Attribution locates River's template cache misses at 8.731 ms of a 13.512 ms rebuild;
Margot's same-frame rebuild has no template misses. This motivates the narrow fix.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`companion-point-link-attribution`, `template-bounds-trial`,
`template-bounds-workloads`. Runners/comparator in
`output/renderdoc-tools-2026-10-08/` use the maintained release benchmark machinery.

## Verification

Three alternating debug=false native pairs on the frozen current 10-room station,
idle/pan/selection/zoom-selection at 1x/2x/4x, 90 frames per phase: 6480 frames.
36 full phase states/cameras and 162 paired UI snapshots exact.

| Metric | Reference | Candidate |
|---|---:|---:|
| Mean frame ms | 12.147 | 12.187 |
| p95 ms | 20.082 | 19.921 |
| p99 ms | 30.952 | 31.158 |
| Maximum ms | 52.881 | 44.928 |
| Frames >50 / >100 ms | 1 / 0 | 0 / 0 |
| Texture peak MiB | 1945.262 | 1945.262 |

Construction-completion crew time improves in all three pairs:
25.915→19.399, 24.220→19.372, 24.026→19.901 ms. Mean reduction ~21%.
Whole-run averages are mixed (+0.33% pooled); accept as a targeted stutter fix,
not broad FPS gain. Texture/upload counts unchanged.

120,000 original/candidate GDScript template comparisons exact, including stationary
points, short grid links and half-open edges. Installed maintained test: 38,624
comparisons, zero failures, no engine errors. Installed function body matches the
measured candidate; source hashes retained in `installed-verification.json`.
Paired UIDs unchanged. All owner guards: 2938 files unchanged. No native jobs remain;
runtime override restored. New evidence 21.22 MiB; C 122.98 / D 69.74 GiB free.

## Next action

Run the same matched bounded comparison on reported 12-room and deterministic
40-room maps before claiming benefit across stations. Investigate the separate
~9 ms Margot passage update without rebuilding, and remaining rendering tails.
Large-map frame gates, target hardware, loading/endurance, broader gameplay/visual
checks and actual Windows/Mac release certification remain open.
