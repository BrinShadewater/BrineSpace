# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: antialiased waveform geometry reuse

## Objective and acceptance
Reduce waveform submission work without altering antialiasing, joins, colors,
clock math, animation playback or layering. Require native pixel parity and
matched packaged performance; full release gates remain open.

## Accepted decisions and constraints
Private prototype only. Geometry adapted from the executable's Godot commit
ed1daf0bf001b61586d9930840f2f1394092c079; downloaded source and MIT notice retained.
Original width compensation, center/feather strips and float32 rounding preserved
in the tested cases. Three ArrayMesh surfaces use white/transparent vertex colors
with the original color modulation. Exact points/width/clock reuse, bound64 entries.
Slots retain mesh leases until repaint; Grid exit clears the lookup. No shared
image mutation, selected-art edit, normal-source change or delivery replacement.

## Current state
D:/bs-release-crew-cache-20261009/stroke-mesh-trial/: stroke.gd, original renderer
source, pixel fixture, control/candidate overlays and workloads/. Open positive-width
waveforms only; closed/thin unsupported cases use the original painter. Candidate
PreparedScreens swaps only waveform submission; remaining formulas/calls unchanged.

## Verification
Native contract-first red test fails only for absent reuse API. Actual debug=false
native-v1 passes64 exact pixel pairs. Extended native-v2 passes96 pairs across six
clocks, four zooms and four widths, alternating color modulation. Reference visibility
assertions pass for zoom>=0.5; tiny-zoom image and a full-size waveform reviewed.
96-case cache stats24 builds/72 hits; no engine errors or owner changes. This does
not prove flood-material, all animation joins or full packaged visual acceptance.

Matched session94403 exits0: four40-room idle/lighting runs at all speeds/both orders,
4,320 samples. Twelve exact saved-state pairs match including playback; no engine/
missing-art errors; owner2,938 unchanged. Frame means29.1989->29.2333ms forward and
29.2136->29.2855ms reverse slightly regress. Content painting regresses415.39/418.91us
per frame. Twelve distinct meshes build per frame,24 additional requests hit;
final forward counters15,132 builds/30,288 hits. Full frame gates still fail.
workloads/analysis.json retains all comparisons. Do not install this version.

## Next action
Investigate persistent mesh buffers keyed by stable screen geometry, with exact
vertex updates instead of allocating new meshes/surfaces every clock. Preserve
resource leases, complete conservative bounds and concurrent clock semantics.
Test native pixels and matched performance again only after that material change.
Current geometry equivalence is useful evidence; performance acceptance remains
unproven. Other sustained draw paths, original bugs, endurance and Mac gates open.
