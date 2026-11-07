# Station visuals, lossless audit and query trial decision

Updated: October 11, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Finish corrected real-station visual checks for the hardened private renderer,
audit selected encoded pixels, and measure a narrow room-preparation optimization.
Preserve the full release plan, visual quality, saves and owner layouts.

## Accepted decisions and constraints

Keep indexed provider private pending remaining gameplay/renderer/endurance gates.
Reject the source-port query candidate as a performance optimization: correctness
and a local saving do not override mixed frame results and worse tails.
No production source changes this pass. Reuse existing packs; isolated profiles,
muted secondary display and owner fingerprints remain mandatory.

## Current state and verification

Corrected station-only native replay completed: reported 12-room 28/28, owner-current
10-room 24/24, deterministic 40-room 28/28 captured pixels and complete contexts
exact. All 36 end-phase checkpoints/cameras exact. HUD visibility assertions pass;
reviewed large witness is unobscured. Workshop case changes are visible and remove
exactly in reported/large; current has no actor-free workshop for this fixture.

Fixture-only deterministic survey, lighting and notification clocks plus frozen
portrait processing preserve exact replay comparisons. Gameplay source unchanged.
This is stabilized station-crop acceptance, not full motion/UI or FPS certification.
Evidence: `hardened-indexed-station-pixels/station-comparison.json`,
`station-owner.json`, `station-identity.json`, `station-pair*.json` and witnesses.
Earlier obscured and failed hide-only comparisons remain preserved separately.

All 21 encoded sources reconstruct exact original RGBA pixels read directly from the
actual base release PCK (SHA256 e9d3f8460270b78b8eba5d29300349f1639ebd405965223e2b88f1be1ba6d297).
Original packaged PNG data streams in memory to the CPU audit; no extraction copies.
Source/index/palette/reconstructed hashes retained in
`indexed-packaged-pixel-audit/result.json`; owner guard unchanged. This covers every
selected atlas cell's decoded pixels, not every rendered join/filter/platform state.
Runner: `output/renderdoc-tools-2026-10-08/audit-indexed-packaged-pixels.py`.

Private source-port query candidate hoists a room's port list within one synchronous
preparation call and uses the existing known-port helper. It preserves sentinel,
branch ownership, internal alias and multi-cell behavior. No cross-frame cache.
Actual source engine: 2,401,600 comparisons over 316 room/rotation variants, zero
failures. Evidence: `nursery-port-query-trial/geometry.json` and owner guard.

Six actual debug=false 40-room runs / three alternating pairs / 6480 frames:
mean 25.970→25.914 ms (-0.217%), p95 42.610→43.034, p99 54.480→57.254,
frames >50 ms 57→61, none >100. Peak textures unchanged 3028.007 MiB.
All 36 complete phase checkpoint/camera comparisons exact. One pair worsens,
two improve; no robust whole-frame gain accepted. Reject; do not install or rerun
unchanged merely to seek a better result. Nested door preparation saves approximately
189–245 us/frame depending on action, but that does not close the frame budget.
Both lanes use fixture-only deterministic survey/notification clocks.
Evidence: `nursery-port-query-workloads/{comparison.json,door-setup-attribution.json,owner.json}`.

## Next action

A separate source inspection finds selected_room_cell in the floor/wall surface key,
while actual selection/hover/terrain visuals have their own layers and keys. Existing
`test_live_surface_retention.gd` intentionally uses selection to force immediate
repainting during zoom settling. Preserve that contract.

Prepared, NOT TESTED private candidate:
`selection-surface-key-trial/candidate-grid.gd` and `source-identity.json`.
During ordinary settled rendering it retains the prior selection-only key component;
during zoom preparation/reuse/settling it tracks actual selection as before. Other
structural/layout/power dependencies are unchanged. First verify native pixel parity
and immediate zoom-settle interaction, then measure a matched repeated selection
workload. Do not edit tests to waive the existing interaction guarantee or claim
the dependency unused in every situation.

## Handoff and storage

All jobs terminal; QA runtime override restored. Completed owner guards: 2938 files,
zero changes. No real save writes, art deletion, package upload or release certification.
Visual directory now 201.43 MiB including all preserved attempts (grew ~45.69 MiB
since prior handoff); new query/audit/prepared-candidate directories total ~31.31 MiB.
C: 123.24 / D: 70.39 GiB free. Main/source/PCK images reused; no new runtime copies.
Full original bug/UI/save/workload, endurance, target-hardware, Windows packaging,
Mac gameplay/signing and release gates remain open. No FPS improvement installed.
