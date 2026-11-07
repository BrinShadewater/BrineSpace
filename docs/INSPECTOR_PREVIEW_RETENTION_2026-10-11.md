# Inspector preview retention

Updated: October 11, 2026 · Project: BrineSpace · Task: performance release readiness

## Objective and acceptance

Remove measured inspector card widget churn while preserving rendered pixels,
presentation updates, gameplay state and bounded resource lifetime. Full release
performance, target hardware, Mac and endurance requirements remain open.

## Accepted decisions and constraints

Keep up to twelve previews as children of the current inspector host, never a
permanent global cache. Compare full `DraftCard.presentation` before reuse;
changed presentation rebuilds the card. Hide other previews and evict oldest
entries. Scene destruction releases nodes and their scene-owned bookkeeping.
No forecast reuse, art, animation, simulation timing or quality change.

## Current state

Installed in `scripts/main.gd`, `_refresh_inspector_card`. The retention body
matches the measured private candidate exactly; installed source/test hashes in
`inspector-preview-retention-trial/installed-identity.json`.
Extended `tests/test_inspector_refresh.gd` with eight checks; existing UID preserved.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`inspector-card-stage-trace/`, `inspector-preview-retention-trial/`,
`inspector-preview-pixels/`, `inspector-preview-native/`.
Corresponding runners/comparator in `output/renderdoc-tools-2026-10-08/`.

## Verification

One instrumented native reference run: card attach ~0.763 ms, build ~0.404 ms,
disposal ~0.241 ms, effects text ~0.037 ms, thumbnail style ~0.013 ms per refresh.
Nested attribution, not exclusive percentages or a release performance gate.

Six actual debug=false native 40-room Windows RTX 4070 Ti 1080p runs, three
alternating pairs, selection at 1x/2x/4x, 1620 measured frames. All 81 UI snapshots
match, including visible card text/size/minimum/filter, inspector text and resource
values/tooltips/colors. All nine paired full phase states and camera endpoints match.

| Metric | Reference | Candidate |
|---|---:|---:|
| Mean frame ms | 24.333 | 23.912 |
| p95 ms | 37.240 | 35.080 |
| p99 ms | 51.000 | 47.402 |
| Maximum ms | 67.381 | 59.499 |
| Frames >50 ms | 9 | 7 |
| Frames >100 ms | 0 | 0 |
| Mean click-handler ms | 7.425 | 6.458 |
| Mean inspector refresh ms | 3.489 | 2.534 |
| Peak texture MiB | 3028.77 | 3028.77 |

Mean frame improves ~1.73%; click handler ~13.02%, inspector ~27.37%. Pair means:
25.163→23.705, 23.678→23.599, 24.157→24.431 ms. Two improve and one worsens;
do not claim universal improvement. These are instrumented selection workloads,
not full gameplay certification or target GPU/M1 acceptance.

Two separate native pixel lanes: all 40 room previews plus eight return visits,
**48/48 crop pixels and rectangles exact**, checking the twelve-entry bound.
Pixel hashes only: no screenshot batch stored. The maintained inspector test also
passes natively with the installed retention body: existing cadence/cryo/final
drainage coverage plus reuse, single visible card, presentation invalidation,
replacement, node/bookkeeping bounds, selection after eviction, and scene release.

Initial native adapter run failed three old cryo assertions because its authored
site is deliberately restricted to `-s`/`--script` launches. Native autoload launch
ignored that metadata and generated a procedural site without the assumed ward.
Failed log preserved. Corrected fixture-only main adapter enables the same explicit
authored-site metadata branch, matching the maintained test's normal script launch;
installed retention code unchanged. Final native-authored log passes with no errors.
This is fixture equivalence, not packaged procedural cryo acceptance.

All sixteen >50 ms workload traces have sampled texture uploads; mean upload cost
15.383 / 16.637 ms. Per-frame paths and grid times retained in
`inspector-preview-retention-trial/tail-investigation.json`; durations overlap and
do not prove uploads alone explain each frame.

All four owner guards: 2938 files unchanged. Jobs terminal; runtime override
restored to guarded empty fixture. Tests muted, secondary-display and isolated.
Evidence ~30.19 MiB; C 123.20 / D 70.11 GiB free at final check. No runtime/art copies.

## Next action

Verify installed preview reuse on reported/current maps and changed presentation
inputs in actual gameplay. Continue the existing lossless/upload scheduling work
without repeating rejected cache-budget or forecast trials. Frame gates still fail;
broader UI/motion, loading, memory endurance, target PC and Mac certification remain.
