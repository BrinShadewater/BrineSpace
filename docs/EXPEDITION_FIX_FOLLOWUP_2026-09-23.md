# Expedition and routing follow-up

Updated: September 23, 2026 · Project: BrineSpace

## Objective and acceptance

Exercise a fresh paid expedition, recheck the reported repair/charging fixes,
investigate remaining routing stalls, and present the scenery choices for owner review.

## Accepted decisions and constraints

Normal costs, failures, collision and oxygen rules remain enabled. Owner saves,
layouts and art marks are untouched. No commit, push or release package.
Automated native play establishes mechanics, not human pacing acceptance.

## Current state

`scripts/flood_safety.gd` skips the duplicate crew-avoidance escape pass when no
peers exist. It also avoids unnecessary per-edge peer checks. With peers present,
both avoidance modes remain available. `tests/test_owner_report_regressions.gd`
covers the search bound and retained peer fallback alongside physical doorway
escape and repair-route checks. No persistent navigation cache was added.

## Verification

- Fresh native seed 32, normal dealt hands/costs/failures, 4x speed: Veld recovered,
  disk Continue preserved map/resources, explicit conclusion alive at cycle 16,
  zero failures. Evidence: `output/procedural-sites-2026-09-23/expedition-32-bugfix-followup/`.
  The 6,892 controller samples averaged 0.96 ms, worst 59.35 ms; drawing/GPU is excluded.
  This run preceded the small escape-search optimization.
- Native replay of the copied 18:53 report: Bill reaches and welds the Reactor,
  seals its hull, remains alive, and restores the sealed state through disk Continue.
  `output/owner-bugs-2026-09-23/native-repair-followup.log` passes. Welding and
  fresh-expedition conclusion captures were visually inspected.
- Owner regression and battery suites pass; navigation segment parity passes
  26,624 comparisons. Logs use the `-followup` suffix in that evidence directory.
- Native charging fixture also passes with zero failures: 16 stored Power charges
  an empty battery, 3 holds, and 4 automatically resumes while preserving 3.
  `native-drone-followup.log` records the result; the reserve inspector capture
  was visually reviewed. This is controlled fixture evidence, separate from the
  fresh paid expedition.
- Isolated 05:00 doorway-report escape probe, same copied profile: before 243.54 ms
  first/198.70 ms warm; after 206.60/124.73 ms. These are individual diagnostic
  samples, not an FPS guarantee. Subsequent timings varied. The remaining stall
  largely involves valid graph paths rejected by final movement smoothing:
  seven of eight joins returned 31–42 raw points but no usable smoothed path.
  A trial of shared failed-search results did not improve this and was removed.
- Existing light/dark and native fog scenery comparisons were re-inspected;
  provisional low-rock/timber choices remain unchanged. See
  [owner review](PROCEDURAL_SITES_OWNER_REVIEW.md).

## Next action

Owner review of rock/timber materials and scale, then human recovery-site pacing.
Routing work should next explain why graph-valid swim paths fail final smoothing,
using `output/owner-bugs-2026-09-23/probe_escape_parts.gd` and the copied 05:00
report. Preserve body clearance and test actual movement; do not relax collisions
merely to accept a route. Occasional stalls remain unresolved.
