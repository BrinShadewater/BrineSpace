# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: bounded lossless crew preparation trial

## Objective and acceptance
Reduce the exact compressed crew provider's measured startup compression/bounds
cost while preserving selected pixels, wrapper identity/metadata, readiness and
resource release. Full original PC/Mac release scope stays open.

## Accepted decisions and constraints
Private trial only. PNG/prefetch calls remain main-thread; at most8 independent
images enter worker compression/bounds preparation. No worker GPU calls or
non-thread-safe global cache access. Finish waits for all required work. No
permanent decoded cache or art changes. Reject if broader fidelity/loading fails.

## Current state
`output/crew-worker-compression-2026-10-07/batch.gd` extends the existing private
CPU batch. Selected surviving weak records feed a bounded compression/bounds
queue; main thread adopts packed immutable frames and uses existing wrapper
metadata/counters. Early materialization retains existing synchronous fallback.
Physical player adapters select this batch only during private measurements.
Drivers under `output/compressed-crew-2026-10-06/`:
`test-crew-worker-batch.py`, `measure-crew-worker-startup.py`,
`summarize-crew-worker-startup.py`. Normal runtime/art remain unchanged.

## Verification
Small native selected six-source/24-wrapper probe94 checks/zero failures/errors/
warnings/leaks: exact original/reference pixels, dimensions/filter/alpha metadata,
repeated-path source sharing, consumer mutation isolation, discarded source not
prepared, bounded jobs and all tasks/results consumed. Six jobs/peak6/wait99us.
This is not full selected-roster raster or consumer regression acceptance.

Three matched native initial-new-game startup pairs (first fresh profiles, then
two learned-order launches; second pair reversed) all full crew state, loaded/
discarded/requested/source counts, private storage and reported ready/exit texture
endpoints equal. Six clean exits/logs; no missing art; routers released.

Request-to-ready serial -> worker:
- Initial17,560.076 ->14,999.324ms (OS caches uncontrolled; no certified cold gain).
- Learned pair1:7,873.864 ->7,309.802ms.
- Learned pair2:7,881.451 ->7,763.948ms.
Learned median7,877.658 ->7,536.875ms (~340.783ms less); variability remains and
warm6s gate still fails. Scene load included. Ready texture1,082.994MiB/exit80.055MiB
equal in all six runs; these are few-room initial-game loads, not40-room acceptance.

Worker runs6,622 jobs/peak8/zero unused/jobs left. Learned summed worker compression
~1,853ms, bounds739–806ms; main waits551–654ms, PNG530–559ms vs serial259–268ms.
These overlapping CPU work totals must not be added to wall readiness. Worker
preparation helps, but extra same-pixel jobs and shared-pool contention remain
plausible measured tuning targets. Existing unique source counts remain5,834;
job count exceeds sources by788. Deduplication currently operates by pending path,
then pixel digest only after result consumption, so pending identical-content paths
can compress twice. Prefetch requests12,717 in both lanes, zero unused prefetch.
All owner fingerprints2,936 files unchanged; Slots/Router/flood/player original
bytes restored; all processes terminal.

## Next action
Deduplicate pending compression work by existing PNG content digest while retaining
separate wrappers/path registration. Test alias-first/canonical-first consumption,
early materialization, worker draining and exact source/metadata before comparing
loading. Then selected Veld/James/Marsh consumer/raster coverage and large-station
lifetime/endurance. No normal provider admission or FPS/packaged/Mac claim yet.
