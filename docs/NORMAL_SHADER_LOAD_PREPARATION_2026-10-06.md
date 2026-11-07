# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: normal render-shader preparation

## Objective and acceptance

Continue the full PC/Mac performance/release plan. Remove the reproduced normal loading-path exit warning while retaining background scene loading, existing transition behavior and original shader output. Overall memory/frame/loading/release gates remain open.

## Accepted decisions and constraints

Prepare only the two normal render shaders through shared declarations already used by the renderer. No generated dependency list, background preparation jobs, cached-resource delays, global asset cache, renderer upgrade or quality change. Preserve existing source UIDs and unrelated dirty work.

## Current state

- New `scripts/station_render_shaders.gd` and paired source UID declare the original derelict/fog shaders at whole paths.
- `scripts/loading_transition.gd` preloads that small declaration script when the title prepares its loading interface, before background Main parsing.
- Grid derelict material and UnderwaterVisibility fog material use the same declarations. Shader source, parameters, separate material instances and draw behavior unchanged.
- Existing native `tests/test_loading_transition.gd` additionally checks that both shaders are cached before background Main loading.
- Private before/candidate/installed evidence: `output/scene-dependency-warning-2026-10-06/` normal-loading and installed-derelict logs/results/owner records. Earlier 36/40-resource experiments remain intact and experimental.

## Verification

- Actual normal title/Main/crew/renderer control passes 24 loading checks but leaves one anonymous zero-reference warning object. Private two-shader preparation passes the same 24 checks, with zero objects/warnings/errors. Unlike earlier full fixtures, these runs use normal rendering and selected crew providers.
- Installed change passes 26 native loading checks, zero errors/objects/warnings. Coverage includes New Game, checkpoint restoration, exact reserves, transmission pause/input blocking, explicit mouse/key Continue, reduced motion and archive replay. Scratch directory verified by adapter.
- Existing native derelict rendering test passes: 48,992 changed pixels, zero alpha changes, stable paused wear, camera translation, lights-off darkening and exact original restoration after material removal. This is relevant shader behavior evidence, not full release visual acceptance.
- Maintained release selection includes the helper and both shader resources, with no additional raster/audio assets versus the previous frozen inventory. Paired UID exists in source; raw runtime selection deliberately excludes .uid files. The first audit wrongly required runtime UID selection and was corrected to distinguish source pairing from runtime resources; no exporter change made.
- All completed native lanes fingerprint all 2,936 owner non-log files unchanged. Scoped whitespace checks pass; native processes terminal. No assertion-only side effects, art edits, physical candidate export, commit or publication this turn.

The normal loading method itself is unchanged; this fix adds no async preparation/cancellation work or permanent lookup tables. Existing cancellation/failure acceptance remains part of the broader release plan. The exact C++ identity of anonymous objects is unproven; do not call this an engine repair or claim it lowers GPU texture memory/FPS costs.

## Next action

Verify this accepted source change in a refreshed frozen actual release candidate. Apply equivalent minimal preparation to the four experimental indexed-drone shaders before longer provider lifecycle admission; the normal helper intentionally does not depend on private output resources. Continue larger steady rendering/actor costs, normal memory budgets, total loading targets, packaged bug closure, endurance and actual Mac certification.
