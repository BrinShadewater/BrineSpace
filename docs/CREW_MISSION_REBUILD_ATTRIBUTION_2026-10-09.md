# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: reproducible crew mission hitch

## Objective and acceptance

Continue full PC/Mac performance and release readiness. Identify the repeated crew
spike before a remedy. Preserve current mission timing, route safety, navigation
ownership, saves, layouts and selected visuals. These are private actual-release
attribution probes, not a new accepted full current-checkout package.

## Accepted decisions and constraints

No gameplay change or normal-source integration in this pass. Do not defer a crew
exit or simply move the hitch later. Three-worker and transparent upload prototypes
remain private. No public release or broad monolith refactor.

## Current state

Repeated sampled engine3086,4x crew hitch is now attributed to two full graph
rebuilds during mission unload. Private diagnostic main times14 operations only
within frames3078-3094; mission wrapper separately times rebuild and route search.

Artifacts under D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
crew-subpath-attribution/{reference.json,crew-subpath-window.json,main.gd,
reference-main.gd,extracted-main-identity.json,identity-rejection.log,owner-pair.json}
and mission-route-attribution/{reference.json,route-result.json,prepared-identity.json}.
Helpers under output/renderdoc-tools-2026-10-08/: repair-crew-subpath-attribution.py,
analyze-crew-subpath-window.py, prepare-mission-route-attribution.py,
analyze-mission-route-attribution.py. Earlier preparation/correction helpers retain
the audit trail; use the repaired helper for the actual source/overlay order.

The first source-identity guard rejected instrumentation of normal scripts/main.gd:
the fixture uses the crew-storage overlay's frozen candidate main instead. Extraction
was corrected to load the actual fixture scene after its required overlays and save
its instantiated Script.source_code/resource_path. The detail override is mounted
again after crew-storage/badge overlays, before Router/scene compilation. A stopped
intermediate attempt and failed extractions are not accepted timing evidence.
Compiled main SHA d66fab67f6cbe86371b72529b34c97b94c51c4f10ef3099ed957d024c0699f61;
mission timing SHA b609147fafa92675a441be9933151f530e0c20c97b8eb869ed2c7b27b61bd6d9.
Both actual runs enforce compiled-source guards. Normal gameplay files unchanged.

## Verification

Subpath run frame3086:94.800ms, crew62.453ms. Veld mission30.683ms and Marsh
mission30.285ms; ordinary Branforth0.536ms. Flooding0.204ms, companions0.082ms,
passage0.059ms and social0.030ms. Thus the mission branches account for the hitch.
Only17frames collect operation data; counters bounded and unrelated gameplay unmodified.

Finer actual debug=false route run reproduces94.531ms/crew61.425ms:

| Pilot | Phase/leg | Rebuild | Search | Route total | Nodes |
|---|---|---|---|---|---|
| Veld | unload /return_lock | 29.565ms | 0.211ms | 29.789ms | 19677 |
| Marsh | unload /return_lock | 29.847ms | 0.223ms | 30.082ms | 19677 |

Each call rebuilds exactly once: geometry4 scoped cells ->76 occupied cells.
Veld origin/target cell both(22,24), home(21,23); Marsh both(16,26), home(15,25).
Each resulting smoothed route has1point. This is graph reconstruction, not expensive
AStar route search, rendering or PNG decode in this particular hitch. It does not
prove all other stalls have the same cause.

Relevant fixture/source/branch/navigation/mission-return/error/isolation guards pass
in both probes. Texture peak2345.481MiB/crew4074uploads are common; pending drone jobs
are drained on exit/router released. Owner2936 files unchanged in completed probes
and extractions, logs clean for accepted runs, processes terminal/adapters restored.
Timing probes do not prove an FPS improvement; no remedy yet tested. Native behavior
or pixel regressions need not be rerun for diagnostics alone, but are required for
a subsequent optimization that alters navigation preparation or ownership.

## Full-build component attribution

Additional private actual debug=false run separates reconstruction scopes within
same17frame window. Compiled Bill base SHA
c3eefcf5865d9c64e33d17a7b568830b4b7f18c45d922f1ea6ddb4750ce976eb
is validated through all four inherited actor scripts; mission/main identities remain
those above. Artifacts: navigation-build-attribution/reference.json,
build-components.json, owner-pair.json and clean log. Helper:
output/renderdoc-tools-2026-10-08/prepare-navigation-build-attribution.py.

| Component | Veld | Marsh |
|---|---|---|
| Setup/clear | 0.273ms | 0.237ms |
| Geometry | 1.646ms | 1.692ms |
| Template lookup/generation | 0.048ms | 0.061ms |
| Cached link-index setup | 0.049ms | 0.043ms |
| Point insertion/bookkeeping | 9.150ms | 9.250ms |
| Local link assembly | 14.915ms | 15.233ms |
| Cross-cell boundaries | 7.847ms | 7.531ms |
| Signature | 0.467ms | 0.460ms |
| Total | 34.492ms | 34.586ms |

Both76cells/19677nodes/indexed=true and **zero template cache misses**.
Thus another room-geometry/template cache does not address this hitch. Native graph
construction plus point/link bookkeeping and boundary validation dominate. These
scopes have timing overhead and a different run context; don't compare34.5ms to
prior29.6ms as a regression or infer an API's isolated cost from the enclosing loop.
The run preserves existing fixture/source/navigation/mission/isolation guards,
texturepeak2345.481MiB/crew4074uploads/exit cleanup, owner2936 unchanged and terminal
processes/adapter restoration. No optimization integrated.

Official [AStar2D API](https://docs.godotengine.org/en/stable/classes/class_astar2d.html)
reviewed for allocation/point/link controls; no measured reserve_space benefit yet.
Do not infer a performance gain merely from the API's availability.

## Next action

Prototype preserving each actor's independently owned full navigation graph while
using a separate small bay graph. Reuse only when all current inputs agree; otherwise
update changed room nodes/boundaries or use the existing full rebuild. Test physical
point positions/weights/edges, routes, geometry ownership, layout/door/flood/fire
invalidation, staged cancellation and scene exit before actual performance admission.
Retain current mission movement/release timing: skipping the unload rebuild and
paying it at completion merely shifts the hitch. A complete current-input prepared
graph needs a synchronous fallback for stale/unavailable inputs.

Keep independent mutable AStar objects: crew temporarily disable nodes during
searches. Any reuse must validate full topology, layout, door/flood/fire and actor
navigation policy, and restore full station geometry by mission release. Bound parked
resources to their actor/session and release them on reset/exit. Avoid a global graph
cache. Full original release requirements remain open and FPS/stutter gates fail.
