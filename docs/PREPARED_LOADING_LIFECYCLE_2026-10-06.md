# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: dependency preparation through gameplay lifecycle

## Objective and acceptance

Continue responsive loading, lossless memory-provider validation and full PC/Mac performance/release readiness. Test the previous scene-resource preparation result through New Game, dialogue, Studio, save, title and Continue before normal admission.

## Accepted decisions and constraints

Private loader only; normal source, audio, shaders and presets unchanged. Resource paths come from current explicit preload declarations, not a permanent log-derived list. Tests remain isolated from owner saves. Passing this lifecycle fixture does not establish frame-rate, packaged gameplay, Mac, visual or endurance acceptance.

## Current state

Evidence: `output/scene-dependency-warning-2026-10-06/`. Source traversal/provenance, normal-resource and complete-resource loader variants, native lifecycle controls and JSON/log/owner results. Actual gameplay fixture remains the existing current-Main copy with experimental crew and indexed exterior drone providers.

## Verification

- Traversal of normal Main's explicit preload graph: 299 scripts, exactly the 36 observed audio/shader resources. Normal-resource preparation through the private gameplay fixture passes 194 checks/two cycles, but still leaves four anonymous warning objects; original control passes 194 and leaves three. The initial scene-only success therefore did not justify gameplay admission.
- The prepared fixture log identifies four additional shaders loaded on its background thread: private `rg8`, `r8`, `r8-flood` and `rg8-flood` shaders. Traversal of that fixture's actual declarations finds 315 scripts/40 resources, including precisely those four additional shaders.
- Complete preparation passes 398 checks/four cycles with zero failures, script/engine errors, anonymous objects or exit warnings. Actual dialogue/Continue handling, Studio open/close, recovery, seeded selected drone presentations, crew/fleet save restoration and old scene/provider/cache releases retain existing assertions. This is not natural mining job assignment or general motion acceptance.
- Skip between-frame waits for dependencies already in ResourceLoader's cache. Preparation elapsed 67.086 ms on first load, then 185/179/189 us on Continue; maximum individual resource load 2.422 ms first, 9/10/11 us warm. Background scene-resource loading remains ~2.051 s cold, 40.984/51.369/41.086 ms warm. These are resource-stage observations on this PC, not total readiness benchmarks or target-hardware certification.
- The first complete-run cached-count logging field erroneously assigns 1 instead of incrementing, due to generator string replacement. That field is excluded from conclusions. Corrected the generator for future runs; its cache-skip branch and measured timings are unaffected. Existing measured loader/log remain intact.
- Settled title textures 191,674,855→197,588,501 bytes (+3.09%), static memory 237,820,593→245,273,623 (+3.13%) across four cycles; ownership count zero at every title. This short fixture stays within 5%; it is not ten-transition/two-hour acceptance. All 2,936 owner non-log files unchanged; completed native processes terminal.

## Next action

Build a minimal preparation stage using maintained declarations, with explicit failure/cancellation cleanup and no cached-resource delay. Verify it in the actual normal loading path, then repeat experimental-provider lifecycle coverage and actual release gameplay separately. Do not install a fixture-wide generated resource list or claim the engine defect is repaired. Larger steady frame costs, normal memory budgets, loading targets, packaged bug closure, endurance and actual Mac certification remain open.
