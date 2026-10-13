# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: selection/preview loading attribution

## Objective and acceptance

Continue the complete PC/Mac performance/release plan. Establish where remaining
cold room artwork work lands during selection and preview before choosing further
preparation changes. Preserve cold direct-placement stress coverage and all gates.

## Accepted decisions and constraints

No new production optimization in this pass. Existing hand prewarming already
creates room views one per frame. First selected placement hologram renders the
required floor/wall artwork. Measure both stages rather than crediting a moved
hitch as a fix. Muted secondary-display tests, isolated profiles, owner guards,
shared physical QA runtime and bounded evidence. No pointer movement or full copy.

## Current state

New private diagnostic `run-selection-preview-census-v2.py` under
`output/renderdoc-tools-2026-10-08/`. Same accepted galley/library/shadow sources,
original reported save and copied owner layouts. Dedicated fixture puts galley in
the hand before normal warm-up; invokes the normal card-selection callback at
placement frame0, renders the normal hologram at a deterministic legal connected
cell, and retains the direct-placement stress operation at frame30. Clears selection
at frame31. Only private grid probe replaces pointer-derived cell with a fixed
metadata cell; no physical mouse movement or normal input changes.

Scope explicitly recorded in report: scripted callback and native preview renderer;
does not certify physical input or normal construction-queue performance. This
sequence differs from the preceding cold direct-placement fixture and is not a
matched optimization comparison. No source optimization or new packaged delivery.

## Verification

Actual debug=false Windows/1080p RTX4070Ti job69163 terminal0; six phases at1x/2x/4x,
1,080 measured frames, engine/art/input/profile/window guards clean. Owner2,938
files unchanged. Configuration, runtime fixture and loader restored.

| Event |1x|2x, already warm|4x, already warm|
| --- | --- | --- | --- |
| Selection + preview frame0 |86.159ms|21.902ms|30.119ms|
| Placement frame30 |56.440ms|48.023ms|49.550ms|
| Frame after selection |14.733ms|14.441ms|14.638ms|

Cold selection contains17.034ms callback work and57.602ms grid drawing, with52.530ms
in the foreground/preview surface. Placement has20.627ms simulation/navigation and
23.578ms drawing. Entire run maximum86.159ms, five frames over50ms and zero over100ms.
Earlier cold direct-placement stress remains132–137ms. These fixtures cover different
preparation histories; this is attribution evidence, not an additional performance
gain or release-gate certification. Initial preparation now belongs primarily to the
first preview, while placement still has substantial navigation/redraw work.

First driver failed Python fixture preparation before gameplay; preserved logs and
restored configuration. V2 corrected code generation, completed successfully. No
restart of a live native job. Evidence:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/selection-preview-v2-census/selection-analysis.json`,
full trace/log/owner guard in the same folder; private grid source in
`selection-preview-source/`, small overlay in `selection-preview-v2-runtime-pack/`.

## Next action

Prototype bounded CPU preparation for required room floor/wall images when cards
enter the hand, so first preview can consume already-decoded images. Preserve exact
PNG pixels, filtering and complete room presentation; bound workers, decoded memory,
waste and final-owner cleanup. Compare complete hand/selection/preview/placement
sequences, not only the placing frame. Retain cold direct-action stress workload.
Large-map drone upload bursts and all original bug/endurance, target-PC/Mac, memory,
frame/stall and release-packaging/signing gates remain open. No itch publication.
