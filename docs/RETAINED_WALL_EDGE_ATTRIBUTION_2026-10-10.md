# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: visible wall-cache edge checks

## Objective and acceptance

Finish visual regression checks for private retained wall context before admission.
Preserve the full PC/Mac performance/release scope. Immediate-frame behavior must
have a valid matched normal reference; do not waive an unexplained mismatch.

## Accepted decisions and constraints

Normal source unchanged. Private test-only metadata switch replays original global
wall keys and local keys in one frozen-clock scene. Affected cells are verified
visible before/after mutation. Repeated placements use identical test RNG seeds;
normal game random selection stays unchanged. No runtime/asset copies or quality cuts.
All native tests muted on secondary display in isolated profiles with owner guards.

## Current state

Added `retained-wall-native-edges.gd` and driver under
`output/renderdoc-tools-2026-10-08/`. Small overlay includes current accepted source.
Native cases replay rotation, wall toggle, normal construction-complete corridor
placement and removal, comparing first rendered and settled frames. Actual station
neighbor excluded from structural snapshot correctly invalidates metadata after its
rotation changes. Existing15settled parity cases also run in the fixture.

## Verification

V2:19/19exact pixel pairs (original15 plus rotation/wall first/settled), visible-target
guards and real external-neighbor metadata invalidation pass. V3 extended placement/
removal:21/23exact, completion first/settled differ up to69channels. Difference image
review isolates corridor wall plates; code selects one of12random art variants.
Fixture had different selections between replays. V4 locks/restores RNG for the test:
22/23exact, completion settled now exact; first frame still differs up to28channels.

V5 normal-only control forces global keys for both replays, reproducing precisely
the same completion first-frame difference. Entire signed RGBA difference maps are
equal,4,063changed pixels, same bounding rectangle(344,286)-(1103,874). Reviewed image
shows diffuse particle/background/hand-area differences rather than the previous
wall-plate variant discrepancy. Exact source of this existing settling/replay
difference remains unproven. It is not evidence of a cache-specific defect; it also
does not certify full immediate-frame correctness. Keep helper private for now.

Only V2 is a fully passing pixel run; V3/V4/V5 assert failures are retained diagnostic
evidence. Engine/profile/window guards and capture sequence pass in completed runs.
Initial adapter path-type failure happened before engine launch and was corrected.
All four full owner guards2,938unchanged; all jobs terminal/configs restored.
Normal source/frozen PC/Mac packages unchanged; no new timing reruns or publication.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`retained-wall-native-edges-v2/`, `...-v3/`, `...-v4/`, `...-v5-control/` and their
small staged inputs. V5`baseline-attribution.json` records signed-map equality.
Current turn~3.32MiB evidence plus4scratch profiles175.64MiB containing native image
captures, retained after prior deletion rejection; no retry. C127.18GiB/D80.28GiB free.

## Next action

Resolve immediate-frame reference noise with observable per-frame state and affected
wall/room region comparisons while preserving the full-scene control evidence.
Then prove dynamic crew/light/fog/layering and context/scene-owner release before
admission. Keep prior54matched station states and measured10ms construction savings
as scoped evidence, not global FPS acceptance. Continue drone uploads, loading/memory,
original bug/UI/save/endurance and target-PC/Mac release certification. No release.
