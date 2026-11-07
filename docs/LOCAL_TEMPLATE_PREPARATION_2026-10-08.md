# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: scoped rebuild census and private local-template collision preparation

## Objective and acceptance
Continue entire performance/bug/PC-Mac readiness plan. Reduce measured navigation CPU work while preserving exact graph IDs/weights/connectivity/routes, selected pixels/clocks and owner data. No publication. Single matched pair is not release certification.

## Accepted decisions and constraints
New local-template shortcut stays private. Only authored/large cell-local point/link generation can use it; corridor/legacy and explicit sample-all mode retain old path. Padded/clipped global collision rectangles computed once with the same operations/coordinates as original sweep; candidate preserves can_stand point checks, original half-open segment_hits_rect, immutable template points/links and native emission order. No approximation or changed clearance.

## Current state
Private D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/{bay-build-census,local-template-fast,local-template-runtime}/. Normal source unchanged this turn. Fast candidate integrates prior private bay scope; actual reference/candidate identical patch pack, --fast-local-template alone selects shortcut, both use --bay-scope. Guard compiled base script/mission SHA and actual helper build counts. Existing UIDs/art/layouts untouched.

## Verification
Actual full natural mission census3,000frames1/2/4x:12 build events, all retained below256 bound. Boarding has three1,319-node graphs: Veld45.781ms (cold4 keys38.200ms), Branforth19.732ms (one cold12.137ms), Marsh19.543ms (one cold11.517ms). Roughly62ms of template construction. Unload frame653: one full19,659-node graph88.312ms, cold5 keys44.815ms; native points7.369ms/links21.790ms/cross links11.833ms. Later frame905: Veld41.888 and Marsh42.442ms full graphs in same frame, zero cold keys. This is two mission graphs, not one ordinary crew graph; don't falsely attribute to normal stagger budget. Native assembly remains independently expensive. Instrumented timing is diagnostic, not FPS acceptance. All missions complete, logs clean, owners unchanged.

Private reference/candidate geometry test152,400 checks/zero failures over cold/warm phases/locks. Broad proof with scratch owner room_layouts copy:316 current room/rotation configurations,307,046 checks/zero failures. Complete point-ID maps, positions, weights, every native adjacency and selected exact paths identical. Initial broad fixture had no tree current_scene for layered companion lookup: invalid run retained, not accepted despite zero comparison failures; private fixture Grid getter now supplies actual fixture Main, final logs clean. No production change for fixture setup. These are graph proofs, not rendered pixel reviews.

Actual matched same-pack native debug=false40rooms/four crew, complete natural three-mission lifecycle3,000idle frames1/2/4x each lane. Fast template build count reference0/candidate62; all pilots two scoped crossings/no fallback and full graph recovery. All compared per-phase mission/resource/crew/drone/door/light/power/zoom/prop endpoints and final mission history identical. Means45.471/47.278/48.306 to42.749/44.247/44.193ms; p9551.929/56.930/63.147 to46.648/51.033/56.662. All3 improve in this one pair; unresolved run-order/host variation, no three-run certificate.

Matched boarding2x frame75:125.326 to88.948ms; crew79,175 to45,028us. Unload4x frame653:190.106 to144.626ms; crew93,815 to57,364us, engine wait95,458 to85,560us. Later4x frame905129.307 to123.153ms; crew90,338 to86,197us, template change cannot eliminate zero-cold-key graph emission. Candidate maximum144.626ms still fails stall/FPS gates; separate2x142.935ms frame also open. Renderer timing disabled/unavailable. Peak2,346.502MiB/uploads4,074/exit228.259MiB identical; no memory saving claim. Logs clean; owners2,936same; adapters restored; all jobs terminal. comparison.json contains exact state equality and hitches.

## Next action
Investigate/retest faster native point/link assembly in combination with proven template shortcut and scope, preserving full graph parity and matched complete lifecycle. Earlier indexed-link trial saved CPU but worse overall means; don't admit without fresh matched evidence. Actual moved-prop/native visuals/repeated reversed-order performance and title pause ownership remain before scope admission. Fresh staged checkpoint/recall passed earlier, full release loading/memory/endurance/original nine reports/target hardware/PC-Mac packages/signing remain open.
