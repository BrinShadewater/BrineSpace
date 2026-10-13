# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: current-source real-station comparison

## Objective and acceptance

Verify the accepted hand-image preparation on the saved reported station and its
deterministic large extension. The complete PC/Mac performance/release plan remains
open; this comparison does not certify a new packaged release.

## Accepted decisions and constraints

Retain the cold-preview improvement, but do not claim a general FPS improvement.
The new large-map comparison shows a small consistent mean regression requiring
follow-up. Preserve selected art, simulation, owner layouts and saves. Native tests
remain muted on the secondary landscape display, in isolated copied profiles.
Reuse the existing physical QA executable/PCK; no full asset/package copies.

## Current state

Production source unchanged this turn. Added focused disposable benchmark drivers,
analysis and profile cleanup under `output/renderdoc-tools-2026-10-08/`.
Small captured current-source overlay retains only the scripted preview-cell hook
in grid; excludes earlier per-layer/wall-reason profiling. All other preparation
files match current normal source. Existing Bill timing instrumentation is identical
between lanes. Reference disables preparation with the existing diagnostic flag.

## Verification

Actual debug=false Windows executable, RTX 4070 Ti, 1920x1080, saved 12-room station
and its 40-room extension with copied owner layouts. Three matched pairs each,
alternating order; 12 runs / 12,960 measured frames. Selection, connected direct
placement and demolition at 1x/2x/4x. All 36 paired phase-end gameplay states equal.

| Aggregate metric | 12-room reference / prepared | 40-room reference / prepared |
| --- | --- | --- |
| Mean frame time | 14.863 / 14.749 ms | 27.525 / 27.797 ms |
| P95 | 16.418 / 16.442 ms | 37.451 / 38.000 ms |
| P99 | 22.793 / 22.161 ms | 55.525 / 56.570 ms |
| Maximum | 121.479 / 81.951 ms | 135.423 / 135.568 ms |
| Frames over 50 ms | 20 / 16 | 49 / 44 |
| Frames over 100 ms | 3 / 0 | 18 / 19 |
| Mean first preview | 116.964 / 80.451 ms | 49.224 / 48.781 ms |

Cold preview improves 31.2%; 12-room mean improves 0.77%. Large mean is 0.99% worse
(all three pairs), so the queue is not a remedy for large-station FPS. Loaded large
surfaces have little preview preparation opportunity. Candidate phase texture peaks
are 1,586.306 MiB / 2,784.533 MiB, unchanged from references; phase values do not certify
per-frame or driver peak memory.

18 of 19 large candidate >100ms frames occur at construction/demolition frame30.
Representative demolition: crew system 51.699ms, grid draw 46.718ms, no same-frame
or sampled drone upload. Timings overlap and must not be added as separate totals.
The additional 104.485ms frame has 275.625MiB sampled drone uploads taking 62.946ms.
Every >50ms frame is retained with overlapping action/step/draw/render/upload data.
These observations support separate navigation/redraw and drone-upload remedies.

Engine/art/input/window/profile guards pass; all 2,938 owner files unchanged in both
full comparisons. Source hashes unchanged; runtime fixture restored and jobs terminal.
Removed all 12 new disposable scratch profiles (33.86MiB); report ZIPs retained with
verified hashes. Evidence directories total about 106MiB, plus small source/overlays.
C:124.29GiB / D:80.77GiB free. Shared QA and accepted rollback packages preserved.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`real-station-preparation-reported-20261010/`,
`real-station-preparation-large-20261010/`, and
`real-station-preparation-source-20261010/` contain paired analysis, traces, slow-frame
census, owner guards, inputs/source hashes, retained reports and cleanup manifest.

This uses current source overlays in a real release executable. It does not certify
a plain new package, physical mouse/construction-queue interaction, sustained
endurance, full workload matrix, GTX1650 target or native Mac gameplay.

## Next action

Address the measured construction navigation rebuild and broad redraw costs; inspect
the existing private prefix-reuse trial's remaining lifecycle/integration checks
before admission. Separately reduce clustered drone uploads without pixel changes.
Investigate preparation's ~1% large-map regression before claiming broader benefit.
Continue all loading, bug/UI/save/endurance, target-PC/Mac and signing/release gates.
No export/upload/itch visibility change this turn.
