# Report generation and longer stall soak

Keep game rendering and crew logic unchanged. Preserve existing synchronous
report API for explicit fixtures/startup recovery; use an async runtime path for
automatic captures and manual Save/Send. Main-thread GPU/live snapshot access
stays main-thread; detached PNG/ZIP/fallback work goes to one bounded worker.

1. Freeze current report sources, previous benchmark reference and owner baseline.
2. Demonstrate a failing real PNG/ZIP nonblocking/snapshot test before production
   changes. Implement frozen requests, bounded jobs, paused completion, UI tokens,
   explicit-only upload and shutdown joins; exercise success/failure paths.
3. Validate diagnostics subsystem and native report UI/pixel/content behavior with
   isolated saves. Compare the actual release runtime's report main-frame cost.
4. Run a longer visible large-station soak with bounded stacks/IRQ/I/O capture,
   respecting the20GiB storage reserve and preserving primary/follow-up evidence.
   Plan two10-minute normal / 4× blocks; refine capture storage method before running.
5. Audit sources/save fingerprints and record measured results/remaining limits in
   CURRENT_STATUS, report and maintenance-template handoff. No release promotion.

Completed October 16: async report path and diagnostics/native validation pass.
Accepted soak evidence totals20m 23 s/63,327frames:10min normal untraced,2min normal
Memory trace,8m23s clean4× Memory trace. Windows prompt minimized the initial4×
attempt; rejected. Authorized helper retry succeeded. External near400ms trigger
ended4× early to preserve393 ms frame; full raw/export suffix retained separately,
clean prefix independently checked. Crew wall scope370.994 ms; function cause open.
See docs/REPORT_SOAK_PERFORMANCE_2026-10-16.md and matching handoff.
