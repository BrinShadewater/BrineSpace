# Companion and placement CPU pass

Updated: October 20, 2026 · Project: BrineSpace · Task: targeted optimization pass

## Objective and acceptance

Reduce recurring work in current source without changing gameplay, artwork,
animation timing or the existing texture budget. Retain only measured local
improvements with behavior checks. This pass does not revisit rejected wheel
eviction policies or certify large-station frame pacing.

## Accepted decisions and constraints

No persistent cache, stale-state window, reduced update frequency or deferred
animation. Existing physical assistance, recovery, discovery and safety rules stay.
Owner save folder and signed delivery are protected. No export/publication.

## Current state

- `scripts/companion_repair.gd`: check the four architects before allocating and
  scanning the station's room keys for hull work. If nobody can be welding a hull,
  proceed directly to the existing ward check. When a hull worker exists, retain
  the original room ordering and eligibility checks unchanged.
- `scripts/main.gd`: placement experiment naming now fetches a room definition
  only if the live neighbor lacks `display_name`. Dictionary.get's eager fallback
  previously deep-copied a definition even when unused.
- `tests/test_companion_target_cost.gd` and paired UID: preserved old target oracle,
  500 varied-state comparisons, four naming controls and diagnostic local timings.
- `tests/index.json`: focused subsystem; `docs/CURRENT_STATUS.md`: milestone.

## Verification

Godot headless local microbenchmarks, both invocation orders, microseconds/call:

| Case | Before | After |
| --- | ---: | ---: |
| 40 rooms, no hull worker | 16.98–16.99 | 1.79–1.82 |
| 200 rooms, no hull worker | 79.62–79.99 | 1.81–1.82 |
| 40 rooms, active hull worker, no eligible job | 16.93–17.02 | 17.96–18.07 |
| 200 rooms, active hull worker, no eligible job | 79.87–80.24 | 80.23–80.75 |
| Existing neighbor display name | 3.07–3.13 | 0.267 |

The extra actor check costs roughly one microsecond when a hull worker is present;
the common no-hull-work case avoids the room scan entirely. Name figures measure
the expression, not an entire UI refresh. Target timings use synthetic 40/200-room
fixtures and 4,000 calls per sample; name timing uses 20,000. No FPS, native hitch,
memory or full-station performance improvement is claimed.

504 oracle/name checks pass. Existing hull-assistance regression plus updated ward
(35 checks), Margot company (26) and placement experiments (59) pass, including
existing Save/Continue and physical state controls. Initial benchmark attempt had
mixed indentation in the new fixture; corrected before successful measurements.
No render/art changes; no fresh native visual review required for these equivalent
query paths. Existing large-station upload hitches remain unresolved.

Evidence: `D:/bs-optimization-20261020` source baselines, logs and protection receipts;
runner logs `output/test-runs/20261020-225440-headless` and
`output/test-runs/20261020-225509-headless`. All tests used isolated APPDATA.
All 2,971 owner files hash-equal and signed ZIP stat unchanged.

## Next action

Use a native profile of a representative current-source station before choosing
another broad frame-cost target. Preserve prior rejected upload-policy evidence;
these local savings do not close that separate performance gate.
