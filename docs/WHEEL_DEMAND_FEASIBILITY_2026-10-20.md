# Wheel demand eviction feasibility

Updated: October 20, 2026 · BrineSpace · Upcoming fleet demand

## Objective and acceptance

Test whether choosing a stale wheel heading by upcoming demand can avoid reloads
with the same memory budget, exact animation timing and original artwork.
The recorded local opportunity saves **zero reloads even with perfect future
heading knowledge**. No runtime forecast is added on this evidence.

## Accepted decisions and constraints

Keep the existing budget and two-frame recent-use protection. No changed texture
coordinates, art, delayed publication or pose holds. The accepted East effect
storage remains. This feasibility test reuses existing evidence rather than
running another native benchmark without a plausible improvement.

## Current state

Only this handoff and `docs/CURRENT_STATUS.md` change in the checkout.
Private replay, five tests and machine-readable analysis are at
`D:/bs-wheel-demand-20261020`.

Input is the completed native wheel-priority diagnostic at
`D:/bs-wheel-priority-20261020/diagnostic/mixed_large-1920x1080-1.json`.
Its SHA-256 is recorded in the analysis receipt. No Godot process or player
profile is opened in this task; runtime, art and delivery files are untouched.

## Verification

The diagnostic's per-eviction bookkeeping gives stale wheel bytes as cached bytes
minus recent bytes minus other stale bytes. Every measured result divides exactly
by the known 48,168,960-byte wheel-sheet allocation. Of 19 measured wheel evictions,
18 have only one stale wheel sheet available and one has two. None has other
stale non-wheel bytes left.

The single choice is between West and North at process frame 866. One sheet must
be removed to satisfy the budget. Frame 867 requires another allocation and forces
removal of the remaining stale wheel. Both removals are necessary under the
recorded pressure; either heading has the same allocation size.

| Choice | Frame 866 victim | Frame 867 victim | Next sampled heading needs |
|---|---|---|---|
| Recorded LRU within wheels | West | North | West 869; North 894 |
| Perfect future demand | North | West | West 869; North 894 |

Neither heading appears in any sampled actor pose between the two eviction points.
The local replay therefore misses both later demands under either ordering.
Native uploads were recorded later, at frames 872 and 896; sampled pose demand
must not be confused with upload completion or visible readiness.

`python D:/bs-wheel-demand-20261020/test_replay.py`: **5 tests pass**. They cover
selection of the later-needed heading, earlier LRU misses, loss of the advantage
under a second forced eviction, a single eligible victim and the recorded interval.
The synthetic one-eviction case demonstrates that the replay can distinguish
the policies when there is an actual retention opportunity.

This is a bounded counterfactual with fixed recorded non-wheel pressure, not a
full cache simulation, actual route predictor, new native A/B run or visual
acceptance. Sampled poses omit full draw, request and prefetch history. It rules
out a gain from swapping this local wheel victim choice, not every predictive
cache policy on every station. No new performance claim is made.

## Next action

Do not add fleet forecasting solely to reorder this wheel pair. A new candidate
needs evidence of a longer retention opportunity: for example, a demand trace
showing a different earlier, non-wheel victim can safely free enough space until
reuse. Treat that as a separate hypothesis and account for displaced uploads.
The wheel hitch remains unresolved under current constraints.
