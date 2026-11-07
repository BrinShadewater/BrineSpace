# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: remaining full graph rebuilds

## Objective and acceptance

Reduce the remaining navigation stall while preserving routes, ordered graph
semantics, geometry, doors/fire, mission timing and actor ownership. Full original
PC/Mac release-performance scope stays open. This pass establishes changed inputs;
no new gameplay optimization is retained and no FPS acceptance is claimed.

## Accepted decisions and constraints

Normal cold-template/point/link optimizations remain retained. Do not skip rebuilds
using room count, total node count or the existing topology string alone. The
signature refresh also updates locked_room_cells and misses some geometry-cache
inputs (recovery furniture etc). Graphs stay independently mutable per actor.
No timing deferral, graph sharing, art/quality changes or broad refactor.

## Current state

Bounded debug=false frame1256 probe compares previous/current ordered local-template
keys, per-cell counts and signatures on three actors. Small previous-key/count maps
are replaced each rebuild and belong to the actor; no permanent visited-state cache.
Private inherited Bill SHA
7c5c16eb62c0c2312f4ab592bacc040e72aabacbbaf1542ecba605a42b2eef12
passes compiled-source guards. Normal Bill SHA93e31c... remains unchanged.
Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/navigation-delta-probe/:
candidate.json,delta-components.json,accepted-delta-proof.json,owner-pair.json,
owner-local-templates.json,default-local-templates.json,local-template-owner.json.
Helpers output/renderdoc-tools-2026-10-08/prepare-navigation-delta-probe.py and
test-navigation-delta-templates.py. No live jobs.

## Verification

- Actual same40-room idle1x/2x/4x workload completes cleanly. Frame1256 all three
  actors change12of76cells:four components for each of three Moonbays. Signature
  differs; same occupied cell order and same19695nodes. Other64cell keys unchanged.
  First changed cell is index20; unchanged leading prefix is only4894nodes (~25%).
  A prefix-only strategy would retain much less than the total unaffected geometry.
- Changed keys move from station_open=true /not boarding to station_open=false /
  boarding-or-exit-bay=true with sub_present=true. Changed geometry is real;
  whole-graph reuse would require a stronger proof and is not admitted.
- Headless current normal geometry reproduces these12actual cell/socket states,
  before/after,with copied owner Studio layouts and separately defaults. In BOTH:
  six cells have identical ordered local points/links/blockers; six differ in all
  three. Every changed cell retains its own point and link counts. Equal counts
  therefore do NOT prove identical nodes or edges. Owner-layout cell counts match
  actual release328/359/316/316; defaults differ370/421/346/397 as expected.
  These are local-template comparisons, not full graph-update/route acceptance.
- Probe final missions and all phase crew/drone/mission endpoints match prior
  cold-template candidate. Texturepeak2345.481MiB/exit228.259MiB,crewuploads4074,
  existing branch/cleanup guards pass. All2936ownerfiles unchanged for both native
  and headless runs; logsclean/adaptersrestored/processesterminal. Normal hash same.

## Next action

Prototype updating only changed local graph sections when ordered cell ownership
and per-cell node counts permit preserving exact IDs. Disconnect/rebuild boundary
edges in original order; update changed positions/weights/local connections and
global lookup while retaining unaffected local graph work. Fall back to full
reconstruction for changed counts/order/layouts or unproven state. Prove exact
ordered adjacency/routes,temporary disabled-state reset,invalidation and lifecycle
before matched release measurements. Equal counts alone must never authorize reuse.
Boundary checks also remain costly (~12ms/actor) and need their own measured remedy.
Full-source packages,broad workloads,original bugs,loading/memory/endurance and
Windows/Mac certification gates remain open.
