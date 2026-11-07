# UI forecast trial and inspector attribution

Updated: October 11, 2026 · Project: BrineSpace · Task: performance release readiness

## Objective and acceptance

Reduce measured UI refresh overhead without stale forecasts, changed visuals or
gameplay. Admit optimizations only with relevant behavioral checks and a matched
workload comparison. Keep full release performance/platform gates open.

## Accepted decisions and constraints

No persistent economy forecast cache. Direct panel updates must observe current
inputs. Tests stay muted, secondary-display, scratch-profile and storage-bounded;
reuse the existing physical debug=false release runtime with small overlays.

## Current state

No production edits this pass. Private scoped forecast reuse is **not admitted**:
resource refresh returns its local forecast, and only its synchronous `_refresh_all`
caller passes that dictionary through inspector refresh/content. Independent
inspector calls still calculate a fresh forecast. The existing projection helper
duplicates delta before crew upkeep, and audited intermediate UI paths do not
change economy inputs. No gameplay timing or simulation changes.

Evidence directories under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`ui-refresh-inner-trace/`, `ui-scoped-forecast-trial/`,
`ui-scoped-forecast-direct-check/`, `inspector-component-trace/`.
Matching runners and trial comparator are in `output/renderdoc-tools-2026-10-08/`.
Candidates/instrumentation remain private files; preserve existing production work.

## Verification

Nested diagnostic: one 40-room release selection run, 270 measured frames and
28 refresh calls. Resource forecast ~0.511 ms, inspector forecast ~0.550 ms,
resource-chip updates ~0.500 ms. This establishes duplicated forecast cost.

Scoped candidate: six native debug=false 40-room runs, three alternating pairs,
selection at 1x/2x/4x, 1620 measured frames. All 81 selection UI snapshots match
(inspector text, resource labels, tooltips and colors); all nine paired full phase
states/cameras match. Separate candidate native run passes 44 comparisons: all
40 placed rooms plus resource Power=0, master power off, pumps off and next-cycle
inputs, comparing direct fresh updates with shared-refresh output.

| Metric | Reference | Candidate |
|---|---:|---:|
| Mean frame ms | 24.367 | 24.840 |
| p95 ms | 36.878 | 37.558 |
| p99 ms | 52.512 | 56.380 |
| Maximum ms | 69.894 | 88.637 |
| Frames >50 ms | 11 | 12 |
| Frames >100 ms | 0 | 0 |
| Mean click-handler ms | 7.409 | 7.051 |
| Mean inspector refresh ms | 3.485 | 3.053 |
| Peak texture MiB | 3028.77 | 3028.77 |

Handler mean improves ~4.83%, but frame mean worsens ~1.94%; all three pair
frame means worsen. Do not install on this evidence. Instrumented runs support
attribution, not uninstrumented release certification.

Every >50 ms trace examined: all 11 reference and 12 candidate tail frames have
sampled texture uploads. Mean sampled upload cost 18.387 / 20.841 ms; largest
individual decoded texture 137.81 MiB. Mean grid draw 35.231 / 39.704 ms;
simulation step 4.415 / 4.438 ms. Scope overlaps: do not add these durations or
claim uploads alone explain every stall. Per-frame paths/times retained in
`ui-scoped-forecast-trial/tail-investigation.json`.

Follow-up reference diagnostic: one 40-room selection run / 28 refresh calls.
Inspector content ~1.840 ms, identity ~1.750 ms, nested inspector card path
~1.499 ms, card construction ~0.406 ms, forecast ~0.542 ms. Totals include nested
and independently invoked sections, so they cannot be summed or read as exclusive
percentages of `_refresh_all`. This directs the next investigation toward card
refresh/disposal/theme work, rather than assuming construction is the whole cost.

All four completed owner guards: 2938 files unchanged. Native jobs terminal;
runtime override restored to guarded empty fixture. New evidence ~29.76 MiB;
C 123.17 / D 70.17 GiB free at final check. No runtime/art copies or owner writes.

## Next action

Separate inspector-card disposal, style invalidation and text work before a new
candidate. Keep upload scheduling and decoded-atlas residency high priority;
use matched tail traces and the existing private lossless-provider evidence.
Do not rerun the unchanged forecast candidate. Full frame gates, target hardware,
Mac, motion/visual acceptance and endurance remain incomplete.
