# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: navigation reuse lifecycle verification

## Objective and acceptance

Continue PC/Mac release performance work by reducing the navigation rebuild cost
identified in real-station construction spikes. Close remaining private prefix-reuse
behavior checks before final matched timing or production admission.

## Accepted decisions and constraints

Keep independent crew graphs, exact point IDs/positions/weights/disabled flags,
ordered connections, room maps and deterministic routes. Staged loading must clear
old graph/reuse keys immediately and allow synchronous supersession. No gameplay,
animation or visual-quality changes; muted secondary-display isolated profiles only.

## Current state

Production navigation remains unchanged. Existing private V2 candidate matches the
current original navigation script as its reference and retains the staged-clear fix.
Added `output/renderdoc-tools-2026-10-08/prefix-lifecycle-checks.gd` and
`run-prefix-current-lifecycle.py` with retained generated adapter. Current accepted
preparation/shadow/galley source overlays are included; older per-layer grid profiling
is excluded. Small overlay only; no full package or source copies.

## Verification

Successful actual debug=false large-station run: 58 additional lifecycle operations;
87 fresh-reference graph comparisons, 1,044,474 point records and 10,821 selected
cross-station routes equal. Includes actual detached galley placement/removal,
saved prop move/deletion/restore, zero reuse after geometry revision, and subsequent
reuse. Moved geometry really changes; deleted prop is absent; original scratch
layout contents restore exactly. Detached Moonbay tests six phases at all four
rotations with repeat builds, internal multi-cell boundaries, removal, staged clear
and yielded synchronous supersession. Subsequent connected station placement and
demolition at 1x/2x/4x also compare against fresh rebuilds.

Verification is deliberately expensive. Its frame timings are invalid performance
acceptance evidence. Prior V1 timing (~32% rebuild CPU reduction, mixed whole-frame
means) does not certify this final V2 integration. No new FPS improvement claim.

Failure evidence retained: initial adapter redeclared prefix census locals, causing
dependency compile failure; removed that unnecessary census. Second fixture mistook
Moonbay internal cells for external station connections; corrected only the fixture
precondition. Galley edits matched before that failure. Only V3 is accepted.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`prefix-current-lifecycle-v3/verification-summary.json`, successful log/trace/fixture,
`prefix-current-lifecycle-v3-runtime-pack/`, and prior failed sibling folders.
Current reference SHA256 `1e0a5bfea9fc4a4ac9a6042ad2a1bb5ccf709efadcc2e6131c9f2001c424df4d`;
private candidate `9250068ab59e2d77e5a1be11bf91c3ddae9f7e742be99b24c1d1b266e8698ad9`.

All three full owner guards: 2,938 unchanged. All jobs terminal; fixture/configs
restored. Evidence ~9MiB plus six new scratch profiles ~7.32MiB. Automatic approval
review rejected profile deletion with “blocked by policy”, no detailed reason;
profiles remain and deletion was not retried. C124.28GiB / D80.76GiB free. No main
display/sound use, export, upload, art deletion or accepted-package changes.

## Next action

Run final V2 matched flag-off/on timing against current accepted preparation baseline
with verification disabled. Compare rebuild CPU, affected frame tails and overall
means on reported12/large40 before deciding admission. Then address broad redraws
and independent drone-upload spikes. The complete loading/memory/bugs/UI/endurance,
target-PC/Mac native certification, signing and release-readiness gates remain open.
