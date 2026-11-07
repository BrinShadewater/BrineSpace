# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: within-pass door port reuse

## Objective and acceptance

Continue the full PC/Mac performance plan. Reduce measured topology work in the door/light validator while preserving exact connectivity and live mutation behavior. Accept only a useful matched-workload improvement.

## Accepted decisions and constraints

The prototype is rejected for normal integration. Reuse is limited to one non-yielding validation call, with records released afterward. No cross-frame topology cache, art, gameplay, owner layouts or normal runtime change this milestone.

## Current state

Private subclass builds a per-room world-port list and cell-side membership masks shared by connection checks. Preserves adjacency, branch ownership, same-room identity and ordinary versus large-room door rules. Calls outside the validation pass retain the original live predicate. Artifacts, fixtures, logs and analysis: `output/door-pass-ports-2026-10-06/`.

## Verification

Headless comparison against actual Main connectivity: 9,172 checks, zero failures. Authored room rotations, branch ownership, cardinal/non-cardinal offsets, pass cleanup, next-pass rotation and immediate outside-pass demolition covered. This is behavioral evidence, not packaged visual acceptance.

Actual-normal native mixed40 comparison: all six full crew/drone/door/light/power/zoom states and texture endpoints equal. Clean completed logs and owner profile fingerprints: 2,936 files unchanged. Candidate first run minimized during the final phase; explicitly invalid, log preserved. Only interrupted candidate rerun. Successful pair shows door validator roughly1.65–1.69ms; differences from control13–217us vary alongside broader CPU/render timing variation. No FPS attribution from noisy full-frame changes.

Alternating same-frame check on the actual candidate Grid, with reuse enabled/disabled:32 pairs,128 calls per backend, identical door/light keys in every pair. Reference mean1,486.30us, candidate1,456.66us; paired mean saving29.64us, median14.38us. Candidate faster16/32 pairs. This diagnostic runs after workload phases with stopped simulation; repeated direct calls are not normal frame acceptance. Extra map construction and lookup largely absorb the avoided port queries. Not a meaningful reliable improvement for normal admission.

All processes terminal. No source renderer patch or new release candidate. Failed/intermediate evidence retained. Full frame/memory/loading gates remain open.

## Next action

Prioritize larger sustained room preparation and rendering costs. Avoid further general port-map work without a substantially cheaper strategy and complete invalidation coverage. Existing private crew/drone provider residency and full-room admission, original nine packaged reports, endurance, refreshed Windows packages and actual Mac certification remain required.
