# Claude performance evidence and tooling map

Updated October 11, 2026. Companion to the [handoff](CLAUDE_PERFORMANCE_HANDOFF_2026-10-11.md). Performance work is stopped for owner-requested takeover. Read selectively, not as a request to rerun everything.

## How to use the record

Current source establishes implementation; current status and later owner decisions establish intended direction. Dated reports prove only their stated revision, workload and platform. Earlier reports contain jobs that were active then; these are not live-process evidence. Check current process state before attaching or restarting. A private candidate, exact microfixture or headless pass is not broad release acceptance.

Before trying an idea, search this index and the linked report. Record what has materially changed if revisiting a rejected approach. Do not rerun unchanged comparisons to obtain a favorable result. Historical timings used different revisions and workloads: never add their savings or compare them as one cumulative baseline.

## Short reading routes

| Question | Start here |
|---|---|
| What is integrated now? | [Current status](CURRENT_STATUS.md), [topology integration](TOPOLOGY_NORMAL_INTEGRATION_2026-10-11.md), [synergy acceptance](SYNERGY_GEOMETRY_ACCEPTANCE_2026-10-11.md), [door membership](DOOR_MEMBERSHIP_PERFORMANCE_2026-10-11.md), [target sorting](STATION_TARGET_SORT_PERFORMANCE_2026-10-11.md) |
| What storage candidate should be integrated next? | [Immutable effects](IMMUTABLE_EFFECT_STORAGE_2026-10-11.md), [native format/pixel limits](NATIVE_EFFECT_MASK_FEASIBILITY_2026-10-11.md), [original-map adapter results](NATIVE_EFFECT_ADAPTER_REAL_MAP_RESULTS_2026-10-11.md) |
| What foundational research already exists? | [Research](PERFORMANCE_RESEARCH_2026-10-05.md), [coverage research](PERFORMANCE_COVERAGE_RESEARCH_2026-10-05.md), [secondary risks](SECONDARY_PERFORMANCE_RISKS_2026-10-05.md), [prop/animation research](PROP_ANIMATION_RESEARCH_2026-10-05.md) |
| What earlier work was accepted or ruled out? | [Action register](PERFORMANCE_ACTION_REGISTER_2026-10-05.md), then later current-status entries and the searchable index below. Register is dated; it is not today's task list. |
| What remains wrong with pacing? | [Real-map topology limits](TOPOLOGY_REAL_MAP_REGRESSIONS_2026-10-11.md), [actor detail](ACTOR_DETAIL_ATTRIBUTION_2026-10-11.md), [normal drone uploads](NORMAL_DRONE_UPLOAD_ATTRIBUTION_2026-10-06.md), [layer uploads](LAYER_UPLOAD_ATTRIBUTION_2026-10-06.md), [lighting hitch](LIGHTING_HITCH_ATTRIBUTION_2026-10-10.md) |
| What protects saves, disks and comparison fidelity? | [Storage guards](PERFORMANCE_STORAGE_GUARDS_2026-10-10.md), [input isolation](BENCHMARK_INPUT_ISOLATION_2026-10-09.md), [camera acceptance](BENCHMARK_CAMERA_ACCEPTED_2026-10-10.md) |
| What release/bug work remains? | [Bug/performance pass](BUG_AND_PERFORMANCE_PASS_2026-10-04.md), [release workflow](RELEASE_WORKFLOW.md), [Mac plan](MAC_RELEASE_PLAN.md). Historical bug tests do not close current packaged issues. |

## Approaches not to repeat unchanged

| Approach | Decision / evidence |
|---|---|
| Full 21-source indexed palette renderer | Private; all nine matched mean comparisons worsened despite memory savings. [Real-map decision](SHARED_PALETTE_REAL_MAP_RESULTS_2026-10-11.md). |
| Descriptor lease for indexed draw commands | Private, not admitted. [Latest indexed/lease trial](LATEST_INDEXED_PERFORMANCE_AND_LEASE_TRIAL_2026-10-11.md). |
| Effects-only R8 shader provider | Corrected comparison still worsened mean/stall counts; initial lookahead confound documented. [Effects pilot](EFFECTS_ONLY_MIXED_PILOT_2026-10-11.md). Distinct from the native LA8 candidate. |
| First topology-key version | Local CPU savings did not produce repeatable whole-frame acceptance. Lean version superseded it and is integrated. [Version history](TOPOLOGY_KEY_TRIAL_2026-10-11.md). |
| Transparent/cropped atlas, single hot sheet, preparation/prefetch, wall/navigation variants | Consult their specific reports in the index before considering another version; do not infer production admission from a passing fixture. |

The handoff history also records rejected larger global drone caches and conditional material-write retention. These are not blanket prohibitions on new evidence-based designs; unchanged versions do not justify another trial.

## Reuse existing tools and inputs

- Maintained benchmark: `tools/release_benchmark.gd`, `tools/run_release_benchmark.py`. Original reported/current/40-room scenes and mixed-large coverage are distinct. Mixed-large includes Moonbay/Tidal and active crew/drones; it does not cover the full release interaction/endurance matrix. Free-building/failure-disabled flags belong only to dedicated fixtures.
- Maintained subsystem runner: `python tools/run_tests.py --subsystem <name>`. Rendering acceptance requires the appropriate native lane. Preserve test profiles and UIDs.
- Private helper directory: `C:/Users/Alex/Documents/Brine Space/output/renderdoc-tools-2026-10-08/`. Relevant scripts: `prepare-immutable-effect-adapter.py`, `check-effect-loaded-source-immutability.py`, `run-immutable-effects-pilot.py`, `summarize-immutable-effects-mixed.py`, `run-topology-normal-checks.py`. These are experiment tools, not automatically maintained release tooling; inspect before reuse. Do not recursively search output.
- Benchmark evidence parent: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`. Latest `immutable-effects-mixed-repeats/` contains comparison, identity, owner and completion records plus six reports/logs. `topology-normal-integration/` includes pre-edit Bill source and normal-test records. Preserve existing inputs instead of copying entire trees.
- Frozen real-map inputs: `indexed-real-stations-20261010/owner-current-frozen.save` under that parent; reported input `D:/bs-release-20261009/benchmark-input/reported-20261004-015752.save`. Restore scratch copies only, reset autosave destination.
- Existing native diagnostic EXE: see main handoff. Normal-project engine: `C:/Users/Alex/Documents/Brine Space/output/hand-reuse-2026-10-06/steamapps/common/BrineSpaceQA/GodotQA.exe`. Mounting an old PCK after loading a Script does not replace the cached Script; adapted probes must mount first and verify actual source identities.

## Original reports still require current packaged closure

Large-room default prop movement/placement; missing layout-editor characters; Tidal miniature waterline and north-wall pipe overlap; middle hand-card size; salvage prop selection; Hunger/Fatigue/Health/Oxygen meters; compact portrait meters; brighter card/resource accents. Use the existing report/bug notes to find implementation and earlier checks. Do not label these fixed in the release merely because old tests passed.

## Searchable dated evidence index

The companion [dated evidence index](CLAUDE_PERFORMANCE_DATED_INDEX_2026-10-11.md) lists performance-related October 4–11 reports already present in the project. It is a lookup aid, not a claim that every candidate was accepted. No historical logs or benchmarks were rerun to create it.
