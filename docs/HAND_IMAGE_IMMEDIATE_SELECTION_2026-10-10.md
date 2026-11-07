# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: preparation bounds and immediate selection

## Objective and acceptance

Continue the full PC/Mac performance/release plan. Validate the private hand-image
queue under immediate selection and hand churn, preserving complete fallback art,
simulation and bounded memory. Do not admit it on the earlier delayed-selection
result alone. All full release gates remain open.

## Accepted decisions and constraints

Prototype remains private; normal source and frozen Windows/Mac packages unchanged.
V1 source/evidence retained. V2 bounds encoded PNG buffers as well as decoded image
reservations; unsupported inputs fall back to the original loader. No image quality,
renderer, gameplay or owner layout changes. Native tests muted on secondary display,
scratch profiles and owner fingerprints; reuse the physical QA runtime.

## Current state

Private `hand-image-preparation-v2-source/` adds PNG signature/IHDR, bit-depth,
colour type, compression/filter/interlace and encoded-length checks. Validate each
dimension before multiplication so crafted values cannot overflow the reservation.
Accept only supported <=8bit sources for preparation. At most two tasks,16MiB
decoded reservation,16MiB encoded buffer per task; not a total process-memory cap.
Failed decodes do not count as hits. Original module/consumer/cleanup integrations
and source are retained separately.

Drivers and tests under `output/renderdoc-tools-2026-10-08/`:
`run-hand-image-queue-v2-unit.py`, `run-hand-image-queue-v2-rapid-unit.py`,
`run-hand-image-immediate0-performance.py`, `run-hand-image-immediate1-performance.py`.

## Verification

V2 queue tests19checks pass, then expanded rapid-change fixture220checks pass.
Includes zero/huge dimensions, unsupported16bit input, wrong IHDR/compression,
oversized encoded files and truncated headers, plus exact decoded image bytes,
size/format/mipmap state and consumption/cancellation/scene-end release. One hundred
hand switches maintain <=2jobs and0..16MiB reservation; unused results eventually
discard and reservation returns to zero. Headless storage/queue evidence is separate
from earlier native pixel sampling and actual release rendering comparisons.

Native actual debug=false reported12/owner layouts, 1080p RTX4070Ti job85480:
eight runs/8,640samples across same-frame and next-frame selection, both orders;
placement/demolition at1x/2x/4x. Each delay has twelve equal phase-end gameplay
states. Card arrival is inside the measured interval. No engine/art/input/profile/
window errors; every full owner fingerprint2,938 unchanged.

| Selection delay | Forward original / prepared | Reverse original / prepared |
| --- | --- | --- |
| Same measured frame as arrival |116.874 /100.469ms|120.932 /100.003ms|
| Next measured frame |84.474 /44.598ms|82.680 /44.569ms|

Same-frame preparation consumes one source; the other uses synchronous fallback
and its outstanding result is later pruned. Peak reservation12,575,504bytes
(~11.99MiB), failures zero. One >100ms frame remains in every same-frame run.
Next-frame preparation consumes both sources and has zero pending/reserved after
preview. Those complete run maxima improve84.474->64.040ms and82.680->64.104ms,
with zero >100ms frames in those scoped runs.

Whole-frame means remain mixed: same-frame14.669->14.748 /14.822->14.796ms;
next-frame14.852->14.693 /14.739->14.828ms. Accept no general FPS claim. This
confirms targeted preview benefit and preserves the immediate-selection limitation;
does not certify60FPS, target hardware, all input behavior or the release.

Evidence at `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`hand-image-queue-v2-unit/`, `hand-image-queue-v2-rapid-unit/`,
`hand-image-immediate0-performance/paired-analysis.json`,
`hand-image-immediate1-performance/paired-analysis.json`; full traces/logs/guards
retained. Job85480 terminal0, configurations/fixtures restored, no active native jobs.
No full PCK/source copies or unbounded captures.

## Next action

Resolve actual saved floor/wall preparation paths before admission. Floor meshes
choose finish/material sources per tile; wall context resolves borrowed room/riser
sources. Current prototype records default paths only. `surface_positions(view)`
uses `layout_asset` metadata, which may not be set before the first apply; use the
canonical asset/quarter lookup instead of assuming an unconfigured view has the
correct saved surfaces. Record existing prewarmed views without reconfiguring them
every frame, and invalidate path metadata with layout revision/rotation.

Test earlier request scheduling before card UI rebuilding to reduce the remaining
same-frame fallback competition, measuring the whole arrival/selection sequence.
Then verify saved overrides, final-owner integration, rendered rapid changes and
the40-room workload. Keep cold direct-placement stress. Continue separate drone
upload remedies and full original bug/endurance, PC/Mac hardware, memory/frame/stall,
packaging/signing/notarization gates. No itch publication.
