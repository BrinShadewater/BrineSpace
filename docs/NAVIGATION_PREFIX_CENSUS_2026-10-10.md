# Project handoff

Updated: October 10, 2026 · Project: BrineSpace · Task: navigation rebuild reuse inputs

## Objective and acceptance
Reduce synchronous graph rebuilding while preserving independent actor graphs,
ordered navigation behavior, locks/fire, geometry ownership and simulation timing.
Full PC/Mac performance and release scope remains open. Census is not optimization.

## Accepted decisions and constraints
Native tests muted on secondary display, isolated profiles and owner fingerprints.
No graph sharing/staggering, asset or normal gameplay changes in this pass.
Keys/counts alone do not prove identical points, weights, adjacency or routes.

## Current state
Drivers output/renderdoc-tools-2026-10-08/check-navigation-capacity.py,
prepare/run-navigation-prefix-census.py, prepare/run-connected-navigation-census.py,
analyze-navigation-prefix-census.py. Private current Bill adds bounded before/after
ordered template keys/counts, revision and capacity metadata; current activity helper
included. Original audited installed-cache PCK/art unchanged, debug=false.
Temporary runtime overrides restored after every terminal job.

## Verification
Isolated headless native-engine capacity probe: clear retains16,384/32,768 capacity
across repeated11,454-12,309point fills. Raw point insertion1.35-1.94ms; this is a
synthetic loop, not complete gameplay rebuild time. No reserve-space optimization
justified as a remedy for retained-capacity rebuilds. Owner2,938 unchanged.
Evidence benchmark-input-isolation/navigation-capacity/{result,owner}.json under
D:/bs-release-crew-cache-20261009/.

Original action census58912 terminal0:1,080samples, placement/demolition at1x/2x/4x,
clean engine/art/input/mute/display guards and owner2,938 unchanged. All18 observed
actor rebuilds retain an11,454-node prefix by ordered key/count/revision. Original
benchmark places detached solar_array at(17,23), keysolar_array:0:[], adding285nodes.
It does not exercise connected interior-room placement. Treat original placement
evidence within that scope. This adds coverage; it does not replace that workload.

Connected galley census12632 terminal0:1,080samples, same guards/owner unchanged.
Selection uses legal footprint and reciprocal _ports_connect checks; actual placed
room must have connected neighbors. All18rebuild observations retain7,376prefix
nodes,64.397% of smaller graph. At index26 storage_bay(18,17) changes open socket
key[3]->[0,3] and326->329nodes; appended galley(18,16) has299nodes and south socket.
Graphs11,454->11,756->11,454. Stalls126-136ms persist. No performance gain claimed.
First connected attempt15377 exited1 before gameplay: restricting find_space also
restricted the initial40room assembly. Failed evidence/clean owner guard retained;
v2 applies connection selection only during the measured placement action.

Evidence navigation-prefix-census/ and connected-navigation-prefix-census-v2/
{diagnostic-none,completed,owner,prefix-analysis}.json beside capacity outputs.
No broad behavior or pixel acceptance claimed by metadata collection.

## Next action
Private partial-prefix prototype only after exact graph comparison. Preserve each
actor's graph; remove/rebuild changed suffix and rebuild cross-room boundaries in
original order. Reset disabled-node state, verify available IDs, and fall back for
staged builds, changed layout revision, policy/locks or unsupported state. Compare
complete IDs/positions/weights/ordered adjacency/selected paths against full rebuild
with owner/default layouts, connected/detached placement, demolition, door/fire,
Moonbay phases and cancellation. Metadata equality is insufficient for admission.
Measure matched native workloads only after that correctness proof. Keep current
station reuse retained; no additional production optimization in this pass.
All jobs58912/15377/12632 terminal; no active GPU job at this handoff.
