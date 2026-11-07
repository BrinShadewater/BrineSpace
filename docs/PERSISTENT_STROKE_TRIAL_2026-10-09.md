# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: persistent waveform buffers

## Objective and acceptance
Remove recurring mesh allocation from the pixel-equivalent stroke prototype,
preserving drawing, animation playback, resource ownership and complete bounds.
Matched workload and relevant regression checks govern admission; release gates
remain separate and incomplete.

## Accepted decisions and constraints
Private prototype only. Mesh buffers belong to each drawing slot, preventing one
screen's clock from changing another's frozen pixels. Exact numerical geometry can
be shared at the same clock (64-entry bound). Original float32 stroke construction
and color modulation retained. Dynamic vertex updates preserve surface topology;
complete screen bounds padded for joins/feathering. Slots prune unused records after
painting; each slot has a32-record limit with original-painter fallback. Scene exit
clears numerical lookup, node destruction releases owned buffers. No shared image
mutation or production art/layout changes.

## Current state
Final admission decision: reject this version. Full eight-run comparison completes
34,560 samples/96 exact saved-state pairs, zero engine/missing-art errors, owner2,938
unchanged. Small means14.8765->15.2189ms and15.0931->15.2904ms regress; large
28.1916->28.9306ms and28.1643->29.0157ms also regress. Large worst frames
149.492->154.700ms and152.183->158.938ms; candidate over100ms counts6/7, all24
large phase gates fail in both orders. Earlier targeted means are not representative
of the full action workload. workloads-full/analysis.json is final authority.

D:/bs-release-crew-cache-20261009/stroke-persistent-trial/ contains prior allocation
reference, persistent helper, fixtures, exact overlays and workloads/. Verified
physical QA package reused. Normal source, UIDs and delivery remain unchanged.

## Verification
Queued flood-material test completes after the full GPU workload:96 exact native
pixel comparisons plus12 independent active/frozen ownership checks pass with the
bundled flood_submersion shader. No engine errors; owner2,938 unchanged. Geometry
equivalence is supported; performance acceptance is contradicted by full workloads.

Vertex-only hot-path variant is subsequently tested headless:60 geometry cases,
180 exact vertex/color strip comparisons, zero failures/owner unchanged. Three
paired300-build CPU samples reference5833/5688/5690us vs candidate5284/5398/5399us.
Kernel saves~5-9%; this is not a GPU/gameplay frame gain and is too small by itself
to establish a remedy for the broad regression. It remains unadmitted; do not spend
another full benchmark on it without stronger evidence. Both observer jobs exit0.

Contract-first native red reproduces96 correct pixels but fails the new reuse
assertion with24 builds. Persistent native-v1 passes96 pixel pairs with one build,
95 updates,24 tessellations and72 geometry-cache hits. Subsequent ownership run
passes those96 pairs plus12 checks of active/frozen independent slots. Visibility
and modulation checks retained. No engine errors; owner2,938 unchanged.

Matched session63721 exits0: four actual debug=false40-room idle/lighting runs,
all speeds/both orders,4,320 samples. All12 complete state pairs including playback
match; zero engine/missing-art failures; owner2,938 unchanged. Mean frames
30.5445->29.4474ms forward (1.0971ms improvement),29.3451->29.1906ms reverse
(0.1545ms improvement). Content callbacks still cost an additional315.18/385.21us
per frame; total improvement must not be explained as a script-time saving.
Forward candidate finishes with42 mesh builds/45,348 vertex updates, versus15,132
mesh builds in the earlier allocation-heavy trial. Frame gates remain unmet.
workloads/analysis.json preserves paired distributions, state checks and counters.

## Next action
Retire this renderer substitution from production consideration in its current
form. Revisit the separately attributed~4.5ms live-environment cost or measured
room setup work, using the original painter as baseline. Preserve this experiment
as evidence of numerical/pixel equivalence and unfavorable workload economics.
No further GPU jobs remain from this trial. Historical running entries below refer
to earlier progress, not current tasks.

Independent next variant staged, not tested: D:/bs-release-crew-cache-20261009/
stroke-vertex-only-trial/. Current vertex updates consume only positions, yet
make_geometry allocates/fills constant color arrays on every clock. The staged
variant builds those colors only when creating a mesh. Geometry/color parity and
three paired headless CPU samples are staged in test.gd; run-vertex-only-test.py
with lane parity must wait until the ongoing GPU benchmark/material job finishes.
Do not infer performance or equivalence yet. Current measured overlays unchanged.

Both12-room full-workload orders now complete:48 complete state pairs match.
Means14.8765->15.2189ms forward and15.0931->15.2904ms reverse regress. First
order action breakdown shows idle/demolition means improve, but pan/interface/
placement/save/lighting regress; content callbacks add~0.29-0.43ms across actions.
preliminary-12-action-costs.json records it. Candidate counters show nine unique
geometries, with only nine warm-up hits and no subsequent sharing (tessellations
grow1,620 per180-frame phase). Large targeted runs share12 geometries across36
waveforms instead. Sharing/amortization is a measured difference; it is not yet
proof of the complete regression cause. Universal deployment remains unjustified.
Large full-action runs are confirmed live in the existing driver; wait for those
and queued shader checks before selecting a remedy. Do not restart or install.

Full comparison is now confirmed live: driver PID740316/session55795, eight
12/40-room runs,24 actions/speeds,180 samples per phase in workloads-full/.
First forward12-room pair matches24 complete states but mean14.8765->15.2189ms
regresses; candidate worst59.358ms. Do not admit from earlier targeted gains.
Reverse/large results and final owner guard pending. Observer session12169 waits
on that exact process, then analyzes all96 pairs and runs the staged flood-shader
96-pair/ownership fixture only after GPU benchmark termination. No restart needed.
Flood shader fixture uses actual bundled flood_submersion.gdshader; not run yet.

Run the broader12/40-room action comparison with this material change, including
pan/zoom/placement/demolition/UI/save. Test flood materials, layout changes, inactive
screens, topology/fallback cases and resource lifetime before production admission.
Investigate remaining CPU tessellation cost separately; do not claim a1.10ms universal
gain from mixed run magnitudes. Full target hardware, bug closure, endurance and Mac
certification remain open.
