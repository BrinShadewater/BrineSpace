# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: four measured mining-drone storage hotspots

## Objective and acceptance

Reduce large uploads and memory without changing selected pixels, original atlas dimensions, clocks, filtering or default quality. Full original PC/Mac release gates remain open.

## Accepted decisions and constraints

Only a private twenty-source candidate; accepted production crew storage and original art/delivery untouched. Reuse validated indexed storage with ordinary fallback. No cropped-frame substitution or speculative global cache increase.

## Current state

Private candidate `D:/bs-release-crew-cache-20261009/indexed-drone-hotspots/` adds North mining body/effects, East mining effects and East collection to the prior sixteen-source provider. Current source PNG hashes match frozen accepted inputs. Exact written PNG reconstruction checks cover every RGBA pixel, including transparent RGB. Aggregate decoded payload: 529,858,560 → 192,773,120 bytes (about 505.31 → 183.84 MiB). This is resource payload, not whole-scene memory or performance acceptance.

Stage/encoding, pixel validation, pack and run tools under `output/renderdoc-tools-2026-10-08/`, with `indexed-hotspot`, `indexed-drone-hotspots` or `indexed-drone-hotspot` in their filenames. All resource identities retained; overlay has 53 members.

## Verification

Native Compatibility/RTX 4070 Ti source probes: all 660 animation cells × three scales × mirrored/unmirrored = 3,960 exact rendered pairs. Nonempty cells require visible output at native scale. All four processes clean, zero failures/engine errors, owner 2,938 unchanged. Selected North body and East particle captures inspected; faint particles remain faint. Original source hashes, generated PNG hashes, per-source probes/results/logs and captures retained in `native-pixels/`. No Mac/other GPU, full-scene composition or motion acceptance from these per-sheet checks.

## Next action

Actual debug=false 40-room idle 1×/2×/4× backend diagnostic completes, session 45436 terminal 0. Six full states match both controls; source count 20/active factory, zero selected duplicates/fallback draws, errors/missing art 0, owner 2,938 unchanged. Means 26.748/27.420/30.255 ms; p95 28.939/35.229/41.713 ms; texture endpoints 1845.620/2351.111/1954.336 MiB. Three >50 ms frames remain, worst 61.315 ms. One candidate is not optimization acceptance; higher-speed means remain above the original controls.

Four-run sixteen-source control versus twenty-source candidate comparison completes, both orders, 180 frames per speed (2,160 samples total), session 83010 terminal 0. Six full states exact, runtime source counts/active factory correct, selected duplicates/fallbacks zero, owner 2,938 unchanged. 2× p95 improves 39.488→35.915 /39.877→36.692 ms; 4× p95 improves 43.237→40.904 forward but regresses 40.313→42.223 reverse. All six candidate FPS gates fail. Candidate >50 ms counts total 4/6 versus control 9/5; neither lane samples >100 ms. Means and tails mixed: no production admission or repeatable overall FPS gain. Evidence in `paired-idle/analysis.json`.

Native flood checks add 846 exact pairs across twelve selected cell entries (eleven for East collection), three flood configurations, three scales and mirroring. All four clean, owner unchanged. Duplicate last-cell entries are counted as performed comparisons, not unique frame coverage; ordinary per-cell coverage remains separately 3,960 pairs. This establishes sampled flood pixels, not full-scene lighting/motion/fallback/lifecycle acceptance.

Remaining candidate hitches include indexed South collection body/cargo uploaded together, plus ordinary East mining, carrying and steering sheets. One 50.264 ms frame has only a four-byte/0.073 ms upload, so uploads do not explain every stall. Next bounded transition preparation investigation is separate from adding more source encodings; see [collection preparation](INDEXED_COLLECTION_PREPARATION_2026-10-09.md). No production source or delivery changes.
