# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: minimal provider shader preparation, ten transitions

## Objective and acceptance

Continue full PC/Mac performance/release readiness. Test lossless crew/indexed-drone providers across ten actual native save/title/Continue transitions without the generated all-resource preparation list or recurring frame waits. Provider normal admission and larger-station/endurance acceptance remain open.

## Accepted decisions and constraints

Private shader helper/loader only, using four whole indexed-provider shader paths in addition to the newly accepted normal shader declarations. The normal game has no references to these private resources. No shader/source pixel, material, animation, worker or gameplay changes. Dedicated fixtures retain free-building reserves; ordinary runs remain unchanged.

## Current state

`output/scene-dependency-warning-2026-10-06/`: provider-render-shaders.gd, minimal-provider-loading.gd, minimal-provider-probe.gd, preparation/runner, minimal-provider-ten results/log/lifecycle/owner JSON. Current normal loading copy changes only the additional helper preload and resource-stage timing print. Existing current-Main private crew/drone lifecycle fixture retained.

## Verification

- Ten native New Game/title/Continue cycles pass 1,010 checks, zero failures, script/engine errors, leaked-object diagnostics or shutdown warnings. Includes dialogue acknowledgement, initial Studio open/close, normal recovery into roster, selected seeded drone presentations, crew/fleet restoration, weak old-scene/player/bank/group/image release, and empty session/cache/factory ownership at title. Seeded presentation is not natural assigned mining acceptance.
- Background scene-resource load: 2,101,749 us initially, then 49,973–50,168 us. No generated 36/40-item preparation loop or cached-resource frame delay remains. These measurements are not total gameplay readiness or FPS certification.
- Settled title texture memory 191,674,855→197,809,541 bytes (+3.20%); static memory 237,821,395→245,732,353 (+3.33%). Owners zero at every title. These ten small-fixture transitions meet the 5% settled-title growth threshold; two-hour/large-station endurance remains open.
- Gameplay static memory jumps 462,012,849→518,026,307 bytes at the first Continue (+12.12%), then only +0.13% through game_9. This is not closed as a leak or harmless warm-up: fresh and restored actor progression/presentation differ. Recorded crew-bank raw estimate (1,066,970,976), compressed bytes (98,326,303) and zero spill slots stay constant; library image count falls 39→26. These counters do not explain the ~56 MB step. Follow-up attribution required before equivalent-state memory acceptance.
- Gameplay textures observed ~2.11–2.17 GiB in this small private fixture. Neither the normal 12-room ≤2 GiB gate nor normal large-station ≤3 GiB gate is certified. Normal memory backend remains unchanged.
- First/last native station screenshots inspected: current room/UI/crew art present in these views. Frozen screenshots do not close motion/layering, every drone phase or original packaged bug coverage.
- Scratch profile confirmed. All 2,936 owner non-log files unchanged. Native process terminal; no normal source/art edits, export, commit or publication this turn.

## Next action

Attribute the first-Continue static-memory step using equivalent stopped actor/renderer states and resource-category counts; do not rerun identical lifecycle coverage just to accumulate passes. Extend the maintained deterministic larger-station workload for memory/presentation pressure and actual crew/drone/production behavior. Refresh the frozen actual release for the admitted normal shader fix. Complete provider source/consumer/composition/admission work and tackle larger steady frame costs; all original release targets, packaged bug/endurance and actual Mac gates remain open.
