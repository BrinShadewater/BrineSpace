# iPad staged navigation geometry — October 20, 2026

Installed **brinespace-d651c889f9aa83a8**, unchanged VM1 sampler, on the physical
A14 iPad13,18 (4 GB). Source HEAD remains
`81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted dirty work.
Scoped validation only; initial loading and memory headroom remain open.

## Diagnosis and change

New bounded scalar timings split checkpoint copy/apply, crew preparation, finish
and total restoration, plus each navigation build's total/yield time and yield count.
The native 56-room/four-crew probe measured copy/apply ~8ms versus crew ~1.6s;
physical-device stage timings are recorded below. The measured restoration span
is dominated by crew preparation rather than copying/applying the checkpoint.
Reading the save before restoration is outside this subspan.

Staged graph assembly now uses the existing owner-clipped boundary sweep after
its geometry is complete. The fixed authored +/-176 point lattice also skips a
redundant can_stand scan: its grown/clipped blocker point sweep already proves
that predicate inside the convex cell/closed-socket domain. Corridor/legacy shapes,
all general live route/fire/door policy checks and synchronous assembly retain their
existing behavior. Yield budgets, cancellation checks, independent actor graphs,
point/link ordering and save state remain unchanged. Temporary boundary lists are
local to one build. `--reference-staged-navigation-geometry` retains former staged
geometry work for same-package comparison. No raster/source quality changes.

Meaningful isolated-cache red: 108 checks / 4 expected work-reduction failures.
Expanded actual-pack regression: 324 checks / 0 failures; 29,152 ordered graph records
and 312 exact routes across four rotations, ordinary/large rooms, corridors/corners
and hardware locks. Additional boundary 24,054 and segment 153,824 comparisons pass,
along with staged restoration and the existing navigation-prefix suite. All 14
actual-PCK suites, raster/source audits and strict signing pass. Native actual-display
runs use isolated profiles/final owner fingerprints; export configs restored exact.
The first expanded fixture lacked its owning-game context and logged script errors;
the runner rejected it. The fixture was corrected and all suites rerun successfully;
this was not a production failure or grounds to remove coverage.

## Physical measurements

Same package, fresh-process staged shortcuts disabled → enabled, same paused
56-room/four-crew fixture with seeded reserves and normal gameplay rules:

| Measure | Reference | Candidate |
|---|---:|---:|
| Station build ms | 8692 | 8649 |
| Restore total ms | 3553.416 | 3239.471 |
| Crew preparation ms | 3491.247 | 3156.421 |
| Sum graph build total ms | 2871.642 | 2487.482 |
| Sum graph yield wait ms | 1639.187 | 1349.505 |
| Graph yields | 148 | 125 |
| Engine texture MiB | 893.462 | 893.462 |
| Latest sampled process MB (decimal) | 2076.037 | 2078.199 |

Installed baseline station build 9766ms;
candidate first 8483ms;
same-process repeat 6297ms.
The device disconnected during the first baseline attempt; the helper
was reconnected and the baseline captured without overwriting owner backups.
Baseline-after-reconnection versus warmed candidate is not a controlled speed claim.
Deliberate harness process stops can show the existing unclean-session notice;
those are separate from spontaneous crashes. Build timing excludes later first redraw.
Ordered measurements do not establish a fixed loading gain or process-RAM saving.
GPU-region pages may alias and are not additive to process footprint.

Normal 1× 56-room/four-crew run: 10.147
endpoint-counted active minutes, cycle 70→104,
all four active/alive, errors 0. Sampled process peak 2188.431MB,
end 2153.877MB; first/last-minute medians differ
5.259MB. Sparse active median 17.14FPS,
maximum sampled frame 151.819ms. Observed pauses excluded;
endpoint accounting is not continuous frame capture and warming is not a leak rate.

Actual card-return clearing passed. Save/title/Continue/Save passed complete-state
and exact-timer comparison (only `_path`, `event_history`, `saved_at` differed).
All five original owner files are SHA-exact after final launch; cycle 64/seven rooms
paused 4×, menu closed, no selected room. No new physical multitouch, completed paid
construction, long-duration leak clearance or release clearance is claimed.
Continue profiling crew preparation/initial redraw and texture residency before
attempting broader ownership or scheduling changes.

## Identity and recovery

- Source SHA-256: `d651c889f9aa83a816da9d5da5c88b2bd8693ff15cc512e4778521950d03b1cb`
- Export/app PCK SHA-256: `cdd9627718b8416776f00d7e49cfe9c8d414e326eba9c0e93e1d44168b693741`
- Signed executable SHA-256: `a01c8ea77e80514a99b9b1d215d03e36e55665a397dafc99ef6b3fc1a9c08cb1`
- Sampler SHA-256: `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66`
- Complete candidate: `/Users/Shared/BrineSpace-ipad-optimization-20261020/staged-navigation-boundaries/candidate`
- Full immediate rollback **87a7**: `/Users/Shared/BrineSpace-ipad-optimization-20261020/door-source-sharing/candidate`.
  Strict signature and executable/PCK hashes rechecked at final acceptance.
- Five-file original backup: `/Users/Shared/BrineSpace-ipad-optimization-20261020/staged-navigation-boundaries/candidate/immediately-before-install`
- Portable evidence: `docs/ipad-memory-placement-evidence-2026-10-20/staged-navigation-geometry`.

Frozen Mac/Windows deliveries and all protected earlier rollback/recovery donors unchanged.
