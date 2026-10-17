# Project handoff

Updated: October 16, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: async reports and longer stall soak

## Objective and acceptance

Reduce report-generated stalls and run a longer guarded large-station soak without
visual or crew-behavior changes. Completed: report worker validated; 20 min 23 s /
63,327 complete frames measured, bounded detail retained, 393 ms stall captured.

## Accepted decisions and constraints

Freeze live scene/GPU state on main; detach lossless PNG/ZIP/folder work to one
worker, maximum two jobs. Keep startup/explicit synchronous API. Preserve reports,
explicit-only Send, pause/UI lifecycle and shutdown joins. No game/crew/art changes.
Use the prior unbatched reference; structural candidate stays private.
Every game run isolated from owner saves. Original rare pre-render cause stays open.

## Current state

Changed `scripts/bug_report.gd`, `scripts/performance_monitor.gd`; added
`tests/test_async_bug_report.gd` with UID and index registration. Other pre-existing
working-tree changes preserved. Helpers in `output/report-soak-20261016/`;
evidence `C:/bs-report-soak-20261016/`. See
[results and limitations](REPORT_SOAK_PERFORMANCE_2026-10-16.md).

## Verification

Report main request 367.708→65.093 ms; automatic trigger 64.510 ms. PNG pixels
match; 18/19 frames continue during writing. Five final diagnostics tests and native
F8/UI test pass; independent review found no remaining blocker. All 26 owner guards
pass; 2,948 protected files match task baseline. Only the two authorized report
scripts differ among 36 installed guards. All 24 frozen game sources and runtime /
native binaries unchanged. WPR stopped, helper exited; owner editor PID 46624
preserved. Earlier profile incident caveat persists.

Normal untraced ten minutes: max 75.643 ms. Traced 4× clean 8 min 23 s: max
393.261 ms, five frames >100 ms. Additional normal two-minute trace: max 70.178 ms.
4× ended early to preserve circular history. Export suffix excluded explicitly;
raw data retained. Clean 4× p95/p99 unavailable. The 393 ms frame has 370.994 ms
inside crew wall scope, 392 exact sample/stacks, no report or texture-upload overlap.
Native complete coverage/function cause is unproven; missing stacks and unknown
raw ownership remain explicit.

## Next action

Profile individual crew/companion updates and path-search/rebuild work around this
new crew-scope stall. Do not infer navigation or renderer cause from module/RVAs.
Live report capture still costs ~62–65 ms on main; PNG/package work moved. Full
current-source Windows release and Mac release validation remain separate work.
