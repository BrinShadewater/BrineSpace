# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: scheduler tracing / idle burst

## Objective and acceptance

Get tracing working, investigate without appearance/crew changes, repeat FPS and
4× placement hitches. Capture and benchmarks complete; primary stall causes remain
open. Keep structural candidate private; no game-code fix applied.

## Accepted decisions and constraints

Frozen prior 24-source/PCK lanes; retain all valid rows. Serial scratch profiles,
muted visible secondary QA, owner editor 46624 preserved, 20 GiB reserve. Standard
Windows elevation used only for bounded WPR helper; no persistent rights/service,
priority/affinity/power change. Broker exited; WPR stopped. Prior profile caveat
persists. No export/Mac/long-soak acceptance.

## Current state

Normal game sources/UID/tests unchanged. New helper/parser code under
`output/scheduler-20261015/`; fixed compiled helper and evidence under
`C:/bs-scheduler-20261015/`. New results and this handoff, plan at
`docs/superpowers/plans/2026-10-15-scheduler.md`; CURRENT_STATUS updated.
No commit or release. Existing dirty work preserved.

Four successful bounded captures: 4,800 diagnostic frames / four exact phase pairs.
Known measured ownership, zero reported loss/overlap; one initial boundary orphan
each. Main scheduled residency ~99.7%; lower CPU class <0.5%. Includes potential
ISR/DPC/spin time. All captured >50 ms frames overlap texture creation. Original
~30.8 ms sustained upload-free window absent. V5 state/wait/priority decode is
unverified: legacy decoder, TDH1168/MOFV1–V4. Raw evidence retained; timing-only joins.

## Verification

3,840 fresh untraced frames / 16 exact state-camera pairs. Fresh normal idle
53.17→48.82 FPS, 4× idle 45.84→28.93, placement 44.05→44.46; 0/16 60 FPS gates.
Retain 5.24 s / 435 ms primary pre-render stalls and following 603 / 445 ms frames
that include automatic reports. Reports amplify following frames; primary cause
unresolved and not explained by sampled uploads/grid work. Second comparison has
no >100 ms sample. Action mean 58.426→58.037 ms, mixed orders; following >50 ms 5→3.

All 13 owner / 12+12 binary guards pass; 2,948 protected files equal initial/prior.
Prior exact raster/cache evidence reused for identical game bytes. Parser model 25
checks, topology/serialization/compile checks and independent frame-join/report
ordering review pass. Full limits and tables: SCHEDULER_PERFORMANCE_2026-10-15.md.

## Next action

Trace recurrence of unscoped primary pre-render stalls with sampled stacks,
ISR/DPC accounting and narrow periodic diagnostic-I/O timings. Resolve V5 decoder
before wait/priority classification. Treat texture creation as a measured repeated
hitch contributor, not an explanation of every stall. Do not hide bad benchmark
rows or disable automatic capture solely to improve results.

Final free space ~20.28 GiB, just above 20 GiB reserve. Own shader caches total
13.55 MiB and were retained with all traces/results. Plan storage headroom before
further large QA writes; no unrelated evidence was removed.
