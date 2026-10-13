# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: responsive scene-dependency preparation

## Objective and acceptance

Remove the anonymous background-loading exit warning while preserving responsive loading, selected resources and the full PC/Mac performance/release scope. This is diagnostic evidence, not normal loader admission or release certification.

## Accepted decisions and constraints

Private probes only. Keep normal loading and export presets unchanged. Use scratch profiles, resolved-directory guards and owner fingerprints. Preserve the earlier release executable/PCK and restore its original diagnostic adapter after each experiment. Do not attribute GPU texture memory or gameplay frame costs to these small anonymous objects without measurement.

## Current state

Evidence: `output/scene-dependency-warning-2026-10-06/`. Normal-script dependency probes, observed-resource inventory, preparation controls, two minimal resource-preload scripts, actual debug=false release adapters, identities, logs and JSON results. The inventory contains 4 shaders and 32 audio resources observed in the normal Main background-load log; it is a diagnostic list, not a new production registry.

## Verification

- Native background script loads: Grid 1 zero-reference warning object; Main 23; RoomDatabase/CrewLife/Studio editor 0. RoomDatabase/CrewLife complete in microseconds and may already be cached by startup; these are not cold-load claims.
- Minimal valid scripts, never instantiated: empty RefCounted script 0 warnings; one shader preload 1 object; one audio preload 1 object. Initial constant named Resource shadows a native class and failed parsing; renamed to SelectedAsset and rerun successfully. Failed log retained and excluded from evidence.
- Native normal scene, never instantiated: no preparation 18 warning objects; shaders first 24; audio first 1; all 36 dependencies first 0. Counts vary between cold runs and are not memory deltas. Synchronous preparation is spread across frames; measured per-resource maximum 13.995 ms, cumulative resource-load work 158.183 ms. The scene still loads in the background (~2.585 s).
- Same previously audited actual Windows release executable/PCK, explicitly debug=false: two original controls each 34 warning objects; two all-dependency controls each 0. Synchronous resource-load maxima 11.915/12.443 ms; cumulative work 95.354/105.150 ms; subsequent background scene-resource load 1.234/1.184 s. These exclude per-frame yields and do not establish total startup improvement or target-hardware stall budgets.
- Sequential background preparation of all 36 dependencies also exits cleanly: native 0 objects; two actual release runs 0. Release summed dependency waiting 557.219/557.778 ms, then background scene 1.168/1.184 s. Waiting includes yielded frames and is not main-thread blocking time; additional explicit between-resource yields are outside that sum. This proves a fully background-loading alternative but has a loading-time tradeoff. No throughput claim.
- Every successful lane has zero script/engine errors and exit 0. All 2,936 owner non-log files remain identical. Both release adapter restorations verified; original executable/PCK unchanged. Processes terminal.

The evidence narrows the trigger to nested resource preloads during background GDScript loading; normal scene execution, Studio and new animation providers are unnecessary. Preparing and holding those resources beforehand avoids the symptom in the tested resource-only lanes. Exact engine object identity and C++ defect remain unproven. The related [Godot LoadToken proposal](https://github.com/godotengine/godot/pull/121025) remains open as inspected; it documents ignored unreference results but its original reproduction uses a different sub-thread option. No engine patch or upgrade applied.

## Next action

Test a bounded private dependency-preparation stage through actual New Game/dialogue/Studio/save/title/Continue, including cancellation and failed resources. Derive required whole paths from maintained resource declarations instead of installing this log-derived duplicate list. Measure total readiness and progress gaps, compare retained resources after exit, and tune background scheduling only if measured. Then consider normal admission. Memory-provider acceptance, demanding frame-time gates, packaged bug closure, endurance, actual Mac and release certification remain open.
