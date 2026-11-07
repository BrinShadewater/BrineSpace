# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: hydroponics/storage base retention normal admission

## Objective and acceptance

Reduce repeated complete large-room base drawing with unchanged selected output, material/filtering/layout behavior and scoped lifetime. Full PC/Mac release/performance scope remains active.

## Accepted decisions and constraints

Normal large_room_canvas now uses StaticBase for hydroponics_farm/storage_depot. Deep snapshot/bounds/reduced-motion/Studio revision keys retain commands; only generic machine_clock omitted after renderer/common/door/wall read audit. Original Moon retention unchanged; Tidal remains immediate. Original prop/wet order, inherited materials and child diagnostic accounting preserved. Internal --immediate-static-large-bases retains comparison path. No new textures/global cache/quality changes.

## Current state

Changed scripts/large_room_canvas.gd, existing UID preserved. New tests/test_static_large_base_retention.gd with paired unique UID/native render-perf index. Evidence output/large-base-retention-2026-10-06/{composition,normal,normal-existing,normal-station} receipts/logs/JSON. Performance comparisons still use private compressed-crew/six-sheet drone fixture; those asset providers remain unadmitted.

## Verification

Two-type private shared LIVE composition12exactpairs(all40bounds/248ordinaryslots/activeBRINE/3scales×idle/flood/launch/return) pass with nonblank captures; scene floor/wall/foreground/UI passes not included. Actual normal focused8retention/invalidation checks pass; existing normal135large-roomchecks/80exactpairs pass with materials, nearest/linear, room states, layout/hide/replacement/owner cleanup. Unique pairedUID/index/whitespace pass. No normal permanent broad raster duplication added.

Actual normal matched physical40room six60sample phases, internalflag control/current same normal helper. Hydro3slots9redrawsconstant/hits717→1617; storage3slots7redrawsconstant/hits715→1615. Tidal not instrumented by retained counters (reported0redraws means no retained counter, not no rendering); actual immediate callbacks continue. BaseCPU1.74–1.94→.72–.92ms (~1.0–1.03ms saved), total liveCPU7.54–8.17→6.51–7.10ms (.86–1.06ms saved including children). All6fullcrew/drone/door/light/power/zoom snapshots and texture endpoints equal, no engine/missingart errors.

p95reference→candidate46.774→43.812,46.957→45.705,44.569→44.367,47.708→45.858,49.269→49.258,52.874→54.946ms. Wholeframe results mixed (4xpan worse); no universalFPS or release acceptance. Private finaltexture2776.236MiB equal/no memorysavingclaim. Every owner2936non-log fingerprint unchanged; all processes terminal.

## Next action

Profile next measured preparation areas (seabed~1.6ms and underwater wave lines~1.5ms) with exact output/state controls, and remaining renderer/backend work (~14ms). Preserve selected effects and effective filtering; avoid approximate GPU animation without exact proof. Six-sheet drone Main title/save/Continue lifetime still needed before normal admission. Full normal memory/loading budgets, original packaged bug reports, long endurance and actual Windows/Mac hardware/signing/package certification remain open.
