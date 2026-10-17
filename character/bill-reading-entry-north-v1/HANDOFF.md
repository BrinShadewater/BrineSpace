# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill north tablet transitions

## Objective and acceptance
Continue the full master-consistent Bill animation set, then cross-animation
consistency and polish. This milestone authors north take-out and put-away in
both gear states. They are staged candidates; owner acceptance remains separate.

## Accepted decisions and constraints
Right-hand take-out must stay on Bill's anatomical right (viewer's right in this
rear view). The tablet moves forward and becomes naturally occluded by the torso.
Both boots remain planted and hips seated. Reuse exact selected north seated and
new reading endpoint pixels. Matte master grade and selected native rear helmet
remain the authorities. Put-away is the exact reversed take-out sequence.

## Current state and changed files
Four gear states/24 references, six poses per transition, 480ms finite timelines
and 256px plane with pivot128,224 and standing height148. Entry durations are
60,80,100,100,80,60ms; exit is reversed. Sources and exact prompts are retained:
primary exec-a6999412-1ee7-47c1-a98e-41476adfece3, corrected arm atlas
exec-e66eb374-e924-4be9-8f4f-a905d3b27743. Only primary interiors2/3/4 and corrected
interior1 are selected. Primary0/5 are replaced by exact seat/reading endpoints.

`build.py` performs deterministic extraction/grade/native helmet fitting.
`correction.py` uses near-opaque segmentation for the edited source and the frozen
primary grade. Primary ruler is .214/.251; edited source uses its separately
measured .214/.2455 ruler. No per-pose height normalization or anatomy synthesis.
`registration.json` and hashes record selected sources and protected body regions.
No runtime actor logic, normal loader or selection registry changed this milestone.

## Verification
43 package checks pass: both raw sources, selected corrected cell, fixed rulers,
frame bindings, exact endpoint joins, reversed exit, boot contact and protected
body pixels. Candidate player fixture passes103 native checks in11.03seconds:
loaded pixels, plane/density, dry seated depth, finite clocks and endpoint hold.
Fresh native82px paired entry/exit board visually reviewed. All2,914 real non-log
profile files unchanged under scratch APPDATA. Preview chains entry/read/exit.

Rejected intervals: primary pose1 reached the left belt then switched hands;
the local generated edit corrects that anatomy. Its soft alpha fringe inflated
contact measurements, producing a visibly taller frame despite103 technical
checks passing. Near-opaque component segmentation, separately frozen source
ruler and primary material curve correct the extraction. Earlier outputs/logs
remain historical evidence; current final source and native reports are bound
in candidate-evidence.json. Passing pixel/timing checks alone did not certify fit.

## Remaining work and next action
Extend the selected north sitting family with reading and tool transitions;
generalize Bill's north reading clocks/cache/interruptions without changing room
art or turning lounge resting into reading. Prove normal-loader bindings and
saved/interrupted stages; current selected observation sofa faces south, so a
rotated room does not provide a north reading service. Other directional life/rest
families, world journeys and full-set consistency/polish remain. Full goal active.


## Later selection authority — September30,2026

Now selected by bill-seated-north-family-v1; read that family handoff and
selected-reading-evidence.json for current normal-loader/stage/checkpoint scope.
Candidate reports above remain historical source evidence.
