# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: native effect adapter repeated station validation

## Objective and acceptance

Reduce texture retention/upload stalls while preserving selected visuals, resource
identity and gameplay. Full PC/Mac performance and release gates remain open.

## Accepted decisions and constraints

Candidate remains private. Preserve the original rendering pipeline, PNG sources,
nearest-only mask selection and original-art fallbacks. No quality reduction or
engine change. Muted secondary monitor, isolated user directory, bounded outputs,
20 GiB free-space floor; no runtime/source copies or screenshot batches.

## Current state

Six alternating native debug=false mixed-station runs completed: 6,480 frames,
36 full gameplay states/camera paths/action-speed labels exactly matched. All
candidate phases report three mask sources, original fallback draws zero, and
actual native mask draws. No missing runtime art or engine errors.

| Pooled metric | Reference | Candidate |
| --- | ---: | ---: |
| Mean ms | 31.516 | 30.211 |
| p95 ms | 47.177 | 45.238 |
| p99 ms | 58.741 | 53.163 |
| Maximum ms | 130.850 | 77.134 |
| Frames >50 ms | 96 | 61 |
| Frames >100 ms | 4 | 0 |
| Peak engine texture MiB, every run | 2928.086 | 2744.336 |
| Settled end texture MiB, every run | 1939.219 | 1939.219 |

Peak reported memory reduction is repeatable: 183.750 MiB. Mean change per pair
is -0.019%, -0.544%, -11.263%. The third reference is materially slower; pooled
4.14% improvement is not a stable general FPS claim. The first two pairs have
slightly more >50 ms candidate frames (21→22 and 20→24); do not imply uniform
stutter improvement. All three candidate runs avoid >100 ms stalls. Still fails
the overall frame-time release gates. Engine texture accounting is not a direct
physical GPU residency measurement; existing memory gates are not relaxed.

## Verification

Original and extended adapter rendering checks: 576 and 2,304 exact whole-image
pairs, with native/fallback contexts and four flood states. Earlier native mask
representation proof covers all 180 frames in 8,640 nearest/white pairs.
Missing/invalid derived-file fallback and explicit lifetime: 20 checks pass.

New scene ownership probe: 33 checks pass using current SessionArtCache release
code and two real Node tree_exited callbacks. First exit preserves all nine weak
references; last exit releases descriptors/masks/lazy originals and drains an
outstanding worker without upload. This tests actual ownership callbacks, not
full title/game/Continue transitions or the two-hour soak. First probe exposed a
missing hand-preparation helper in the older reusable runtime; fixture now loads
the current helper explicitly. Corrected native run has zero engine errors.

Owner 2,938 files unchanged after repeated runs and both lifetime attempts;
runtime override restored by each terminal runner. Production source/art unchanged.
Artifacts: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/native-adapter-mixed-repeats/`
and `native-effect-adapter-scene-lifetime/` in the same parent.
Tools added: `check-native-adapter-scene-lifetime.py` and
`run-native-adapter-original-maps.py` under `output/renderdoc-tools-2026-10-08/`.

## Next action

Eighteen alternating native runs on reported/current/original-large stations are
running in `native-adapter-original-maps/` (session 11816). Finish that same job,
verify source identities, complete states and owner fingerprints, then judge
admission. A separate revision in `native-effect-adapter-source-guard/` now
validates the original PNG hash before selecting derived storage, so replacing
selected art at the same path cannot silently draw stale effects. Native pixel,
invalid/missing/stale-source fallback and lifetime validation of that revision
remain pending; running benchmarks retain their original frozen inputs. Builder:
`output/renderdoc-tools-2026-10-08/prepare-native-adapter-source-guard.py`.

Prepared `bill-update-attribution/runner.py` measures unchanged topology signature
construction and fire-cell refresh inside real actor updates; not executed yet.
Only measured hotspots justify a navigation optimization. Keep original and mixed
large workloads separate. Actual gameplay
transition endurance and Mac native visual/performance acceptance remain pending.
