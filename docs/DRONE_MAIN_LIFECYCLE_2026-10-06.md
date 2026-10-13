# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: indexed-drone Main lifecycle and release assertion repair

## Objective and acceptance

Continue the complete PC/Mac performance/release plan. Before normal admission of the six-sheet lossless drone provider, verify actual Main/title/save/Continue integration, texture/job ownership, selected composition and release-safe execution. Full release gates remain open.

## Accepted decisions and constraints

Private fixture/provider only; normal gameplay, selected art and owner saves unchanged. Preserve the original frozen six-source provider. Do not suppress exit warnings or infer their cause from a low reference count. Assertions must not perform required PNG loads.

## Current state

`output/drone-main-lifecycle-2026-10-06/` contains a physical fixture using current Main with explicit private Grid/type/title bindings, the current compressed crew and six-source exterior renderer, isolated profiles, native/verbose logs and results. `provider/` is a physical copy of the previously frozen six-source provider and its PNG sidecars. Frozen original provider hashes all match.

The copied bank now performs index/palette `load_png_from_buffer` calls outside assertions. Previously, the palette load and null-source index load were inside assertions and would be omitted when assertions are stripped. The assertions now check already-computed return values. No palette pixels, sampling, shader, frame count, resource identity or cache policy changed.

## Verification

- Two native actual Main cycles: New Game/transmission → recovery/crew → Studio → indexed South/West mining and North startup/wheels → save/title → Continue. Complete drone-fleet and crew snapshots restore; old scene, private crew resources, drone session/bank/group and sampled wrappers release. Title indexed factory/jobs/textures/byte bookkeeping empty. 194 checks, zero failures or engine errors.
- Fixture explicitly registers a mining bay and seeds valid animation states for rendering; this is controlled integration coverage, not naturally assigned mining or packaged gameplay certification. It requests South effects before scene exit to exercise pending-job cleanup.
- First fixture failed checkpoint validation because its fixed bay coordinate overlapped an unopened Margot recovery site. The corrected fixture chooses ground with no room, blocking wreck or deposit; before/after wreck validation passes. Normal save validation correctly rejected the invalid scratch station; no production save-loss bug claimed. The initial inferred-type parse error was also corrected in the private fixture.
- Corrected provider/current Main repeat: 194 checks, zero failures/errors. Source-assertion audit proves both required PNG loads remain after assertions are removed. A native assertion-erased bank probe passes 168 checks and 120 complete-drone image comparisons, including all six independent source wrappers, actual payload accounting, fallback and weak/session release. Its log has no exit warning.
- Full-scene exit warning remains: five anonymous RefCounted objects in first corrected run, four in verbose repeat, three in corrected-bank repeat, all reported reference count zero. Resource release checks do not explain these objects. Do not treat count changes as a causal fix or claim the indexed provider causes the warning. Earlier crew/Studio warning investigation remains relevant.
- Corrected-bank small-scene title textures 191,674,855→197,514,821 bytes (~3.05%). Indexed bytes at each title zero. This is only two transitions in a small station; neither ten-transition nor two-hour/large-scene memory acceptance. No performance/loading or normal memory-budget claim.
- Every completed lane uses verified scratch user data; all 2,936 owner non-log files unchanged. All native processes terminal. No normal provider admission, normal source edits, export, commit or upload this turn.

## Next action

Compare the current full-scene lifecycle with indexed rendering disabled, preserving crew/Studio stages, to separate the exit warning from the new provider. Finish surrounding dock/exterior/material composition and source-sidecar integrity/release checks before normal admission. Actual debug=false packaged execution is still required; assertion-erased debug-native evidence is narrower. Then pursue normal memory/loading budgets and larger steady renderer/system costs while retaining original packaged bug/endurance/Windows/Mac gates.
