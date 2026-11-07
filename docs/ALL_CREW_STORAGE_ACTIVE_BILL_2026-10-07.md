# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: shared four-crew storage and active Bill restoration

## Objective and acceptance
Continue full PC/Mac readiness. Memory/behavior gains must preserve exact art/bindings and pass actual packages before admission.60FPS/p95/p99/stalls/loading/12room/memory lifetime/bug/UI/endurance/platform gates remain open.

## Accepted decisions and constraints
Keep prototype isolated. Shared existing router/bank includes Bill; no second singleton, no quality/art/filter/source-selection changes, no bigger drone cache yet. Current main/renderer selection copied from authoritative normal source; frozen three-crew helper primitives reused without altering frozen inputs.

## Current state
`output/all-crew-storage-2026-10-07/` contains shared worker/frame/slots/router/display, Bill subclass, generic bank with conditional carry_banks adoption, current-source physical control/candidate Grid/Main/scenes. Both use compressed Veld/James/Marsh; candidate adds Bill into existing bank, preserves all four historical dictionaries. Only constructor/source-storage routing changed; no normal runtime edits. Preparation source hashes/selection scope in selection.json.

## Verification
Native few-room startup control3crew vs candidate4crew:1751.229->1060.765MiB, exact690.464MiB saving. Both settled exits128.863MiB/router released. Candidate raw-equivalent1,610,154,592bytes/compressed139,203,414(~132.755MiB), zero missing. Readiness14.347/13.763s, single native pair/OS cache uncontrolled/not packaged loading. Do not transfer native values to earlier PCK: startup setup/scope differs.

Actual Bill scratch save/fresh-main restores: four bindings×bare/helmet North carry entry,8cases/692checks, clean. Real workshop dispatch and collision-clear lane; exact disk actor/source/clock roundtrip, paused root/clock/needs, matching physical trajectory/needs/art/entry/stow plans for30future ticks per case. Both source and room captures retained. Viewed Master helmet post-restore room: Bill/body/equipment/props visible; cardhand occludes lower room. Covers actual entry restore, not full arrival/rise/all-room natural route chooser/endurance. Original fixture's historical two-case scope string retained in records.json; records-scoped.json adds correct eight-case scope. Native normal actor unchanged; private player execution guarded by its actual script path.

Active native40room fixture explicitly activates walkable legacy Bill in addition to Veld/James/Marsh, normal drones/production; idle/pan/zoom1/2/4x9phases×60frames each lane. First fixture failed because newly forced Bill had nil decision_rng; stopped owned process, retained invalid-bill-rng-fixture.log, initialized RNG only in fixture, then reran. Successful pair clean/error-free; all full crew/drone snapshots, door/light/power/zoom/large-prop states match. Candidate presenter actually shows73Bill/215James/63Marsh/138Veld distinct frames,0missing. GPU uploads1259control/1727candidate; extra Bill presentation uploads are expected and not treated as counter parity.

Every phase exact690.464MiB lower reported textures; candidate endpoints1672.527–2346.686MiB (~1.63–2.29GiB), end2102.737MiB (~2.05GiB), control2793.201MiB. Phase endpoints only/no transient peak or large-memory certification. Whole-frame p95 improves7phases/regresses2; one pair is insufficient for FPS gain. Candidate p9538.065–66.205ms fails16.7ms gate. Worst100.879ms zoom has65841us aggregate draw/269callbacks; latest ordinary drone upload662 vs sampler674, so no coincident atlas upload (sample673). Preserve worst-frame.json/profile scopes; overlaps must not be summed and callback count is not whole-grid redraw count. No clean-stall gate. Full candidate screenshot viewed: station/art/cards/portrait meters present, synergy toast+hand obscure part of station; not full motion/visual acceptance.

All native processes terminal; every fingerprint preserves2936owner non-log files. Normal source/art/layouts/archives unchanged this interval. No combined PCK built/audited or Mac validation.

## Next action
Freeze and test actual combined debug=false source/package or a rigorously identified diagnostic source overlay, verify actual bank/Bill execution and correct fixture identity. Compare loading plus active12/40room memory/frame workloads; track peaks/lifetime and remaining Bill arrival/rise/gear/cargo/UI paths. Native endpoints show headroom, but do not enlarge GPU cache until relevant measured memory bounds and repeated-upload comparison support it. Redraw-only100ms zoom burst remains alongside atlas-upload stalls. Original full release issue register/endurance/targetPC/Mac signing/testing gates stay open.
