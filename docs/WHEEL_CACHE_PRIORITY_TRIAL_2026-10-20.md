# Wheel cache priority trial

Updated: October 20, 2026 · Project: BrineSpace · Remaining wheel upload hitches

## Objective and acceptance

Reduce recurring wheel uploads with exact animation timing and original artwork,
within the existing cache budget. **Wheel preference is rejected:** it avoids no
measured wheel uploads and gives no repeatable frame-time improvement.

## Accepted decisions and constraints

The accepted East effect storage, cargo storage and mask retention remain.
No delayed publication, pose holds, enlarged budget or altered sampling/art.
Keep private experimental code out of the production animation script.

## Current state

Only this handoff and `docs/CURRENT_STATUS.md` change in the checkout for this
trial. Private source, runners, logs, identity receipts and analysis live at
`D:/bs-wheel-priority-20261020`.

The candidate changes upload-time and post-draw eviction to prefer stale shared
wheel sheets over other stale sheets, preserving LRU order within each group.
Wheels remain evictable when needed. The same two-frame recent-use protection,
256 MiB budget, canvas ownership and weak restoration apply. It uses the matching
frozen release animation source, not the older checkout script.

## Verification

The isolated cache-policy fixture first fails the wheel-preference check against
the reference, then passes all five checks against the candidate. Other checks
cover budget enforcement, wheel eviction when necessary, recent-sheet protection
and no eviction below budget. This headless bookkeeping fixture is not raster
or animation-readiness acceptance.

Four native, non-debug release-fixture runs, ordered reference/candidate/candidate/
reference, each measure 1,080 frames at 1920×1080 over idle/lighting and 1/2/4×.
Both sides include the accepted East effect, cargo and mask changes; the only
runtime difference is eviction priority. The fixture uses deterministic clocks,
scratch profiles, muted secondary-display windows and disabled automatic reports.
All four runs are valid, with zero automatic reports. Overlay identities are
recorded; both candidates and the final reference also verify loaded animation
source against the intended file before starting the fixture.

| Metric | Reference 1 | Candidate 1 | Reference 2 | Candidate 2 |
|---|---:|---:|---:|---:|
| Sampled wheel uploads | 19 | 19 | 19 | 19 |
| Sampled wheel payload, MiB | 872.813 | 872.813 | 872.813 | 872.813 |
| Wheel upload intervals, ms total | 90.570 | 96.540 | 98.869 | 99.698 |
| All sampled upload intervals, ms total | 448.617 | 460.815 | 484.124 | 459.036 |
| Mean frame, ms | 22.743 | 23.058 | 23.363 | 23.156 |
| p95 frame, ms | 30.623 | 31.011 | 31.970 | 31.882 |
| Maximum frame, ms | 76.478 | 81.781 | 91.217 | 77.739 |
| Frames >50 ms | 3 | 3 | 3 | 3 |
| Sampled texture peak, MiB | 2668.978 | 2668.978 | 2668.978 | 2668.978 |

All 12 paired saved-state/camera checkpoints and 2,160 paired sampled drone poses
match. Pose sampling checks clocks, position, phase, displayed state/heading/frame,
including deposit work-face heading; it does not prove every draw was ready or
pixel-identical. No visual acceptance is claimed for this rejected policy.
All four runs still pass zero of six pacing phases.

Upload accounting deduplicates bounded sampled events; it is not full GPU bus
traffic. Texture peaks are sampled engine accounting, not within-frame driver VRAM.
No production runtime or artwork changes are admitted.

### Eviction attribution

A separate valid instrumented native run records bounded metadata at wheel
eviction. It is diagnostic only, excluded from timing comparisons. It records
24 wheel evictions including setup, 19 in the measured interval: North 4,
South 5, West 6, East 4. **All 19 have zero other stale non-wheel bytes left.**
Recent protected bytes plus the incoming allocation range from 186.060 to
253.204 MiB, leaving insufficient room for every stale 45.938 MiB wheel sheet.
The policy has already exhausted other stale victims when it removes wheels.

Across setup and measurement, the helper builds 66 mixed wheel/non-wheel
candidate lists, reordering 26 relative to plain LRU. These count candidate-list
construction, not necessarily an eviction or avoided upload. They confirm the
preference is exercised, not that it creates space at the wheel eviction point.
See `eviction-analysis.json` and `diagnostic/` in the evidence directory.

Final protection check: all 2,971 owner files hash-identical; signed ZIP size/mtime
unchanged. Temporary release EXE/PCK copies are cleaned, including the diagnostic.
Free space: C 22.01 GiB, D 25.93 GiB. Scoped documentation whitespace check passes.

## Next action

Do not repeat blanket wheel preference or infer a wheel fix from faster individual
frames. A materially different next candidate is choosing among stale wheel
headings using near-future fleet demand, without changing readiness or increasing
residency. Establish whether such a forecast could avoid reloads on the observed
timeline before adding it to gameplay. It is not implemented or validated here.
