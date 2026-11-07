# Early non-wheel eviction trial

Updated: October 20, 2026 · BrineSpace · Wheel upload hitches

## Objective and acceptance

Test whether retiring a non-wheel sheet earlier can retain wheels until reuse,
counting displaced uploads while preserving timing, artwork and the memory budget.
The private candidate reserves room for one 48,168,960-byte wheel allocation by
retiring stale non-wheel sheets after drawing. It protects the same two-frame
recent-use window and retains the existing normal pressure eviction afterward.

**Rejected:** wheel reloads are unchanged, displaced non-wheel work varies by
order, and equivalent availability is not established. No runtime change retained.

## Accepted decisions and constraints

No enlarged cache, changed animation clocks, pose holds, delayed publication,
changed artwork or sampling coordinates. Accepted East effect, cargo storage and
mask retention are included on both sides. The candidate adds no texture owners.

## Current state

Private scripts and evidence: `D:/bs-wheel-reserve-20261020`. Both runtime variants
derive from the matching frozen Windows release animation source. The reference
adds only the same availability counter used by the candidate. All loaded overlay
animation sources are verified against their intended files before the fixture.

Only this handoff and `docs/CURRENT_STATUS.md` change in the checkout. The trial
is not installed in production; the existing dirty checkout is preserved.

## Verification

The isolated bookkeeping fixture fails two intended checks on the reference,
then passes all five on the candidate. It verifies early non-wheel removal,
one-wheel headroom when eligible, recent-use protection, no reservation without
a wheel and no removal when sufficient headroom exists. It is not raster testing.

The native comparison uses the existing isolated packaged-release fixture:
1920×1080, 1,080 samples per run, idle/lighting at 1/2/4×, deterministic clocks,
muted secondary-display windows, automatic reports disabled. Order is reference,
candidate, candidate, reference. No normal production reporting code changes.

Availability instrumentation counts false results from the existing `ready()`
method in both lanes. The delta spans the first to last recorded sample, including
inter-phase work. It is not a count of unique missing frames or proof of complete
visible drones. Sampled poses likewise do not establish raster/readiness equality.
No visual acceptance is claimed for this experimental policy.

All four native runs are valid/non-debug with zero automatic reports. All 12
paired saved-state/camera checkpoints and 2,160 paired sampled drone poses match.
All four runs still pass zero of six pacing phases.

| Metric | Reference 1 | Candidate 1 | Reference 2 | Candidate 2 |
|---|---:|---:|---:|---:|
| Sampled wheel uploads | 19 | 19 | 19 | 19 |
| Wheel payload, MiB | 872.813 | 872.813 | 872.813 | 872.813 |
| Other sampled payload, MiB | 3455.027 | 3595.067 | 3684.715 | 3503.192 |
| All sampled upload intervals, ms | 583.985 | 631.023 | 790.487 | 572.965 |
| Mean frame, ms | 25.440 | 25.483 | 28.494 | 24.789 |
| p95 frame, ms | 36.557 | 35.728 | 46.521 | 34.242 |
| Maximum frame, ms | 94.800 | 96.604 | 106.206 | 77.100 |
| Frames >50 ms | 12 | 7 | 35 | 6 |
| Unavailable ready calls, first-to-last sample | 298 | 292 | 278 | 301 |
| Sampled texture peak, MiB | 2668.978 | 2668.978 | 2668.978 | 2668.978 |

Displaced work from deduplicated sampled upload events:

- Pair 1: candidate adds 140.039 MiB. West stop, East stop and South charging
  each upload one extra 45.938 MiB full sheet; cargo storage reuploads add 2.198
  MiB and contact foam adds 0.028 MiB.
- Pair 2: candidate removes 181.523 MiB net. It uploads South carry, West stop,
  East stop, South left steering and East right steering once less each, but
  again uploads South charging once more, plus the same cargo/foam additions.
- Thus the repeated extra full-sheet cost is South charging; the first pair's
  stop-sheet displacement does not repeat. Neither pair saves a wheel upload.

The reference runs themselves vary in non-wheel upload counts and wall time.
Matched simulation snapshots/poses do not imply identical asynchronous decode
completion or ready-call histories. No repeatable whole-station speedup or general
non-wheel regression is established. The candidate's lower final texture endpoint
(1907.198 versus 1968.448 MiB) does not lower the sampled peak.

Readiness failures change by -6 in pair 1 and +23 in pair 2. These are calls, not
unique missing frames, and cannot certify unchanged visual availability. Given
zero wheel savings, no extra visual-acceptance testing or production integration
is warranted. Original artwork and animation-selection code were untouched.

Evidence files include `analysis.json`, per-run `*-paths.json` and
`displaced-analysis.json`. Upload events are bounded sampled CPU API intervals,
not exhaustive GPU bus traffic; engine texture samples are not within-frame VRAM
peaks. Scratch profiles isolate all Godot tests from player data.

Final protection receipt: all 2,971 player files hash-identical, signed ZIP
size/mtime unchanged, temporary release EXE/PCK copies cleaned. Free disk space
is C 20.80 GiB and D 25.90 GiB. Delivery binaries remain unchanged.

## Next action

Do not retain or repeat this fixed one-wheel headroom policy. It changes residency
without bridging wheel reuse. Any different earlier-eviction proposal needs an
identified non-wheel sheet that can stay absent through the target wheel's next
use, with its next request and draw-readiness accounted for. Current evidence
does not identify such a safe interval; wheel hitches remain unresolved.
