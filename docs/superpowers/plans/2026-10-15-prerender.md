# Pre-render stalls: stacks, interrupts and diagnostic I/O

Keep both frozen structural lanes and normal game/crew/visual code unchanged.
Investigate before choosing a runtime fix; retain every valid benchmark row.

1. Restore safe disk headroom by verifying/deduplicating two explicitly named
   immutable old QA EXE/base-PCK copies to existing identical hard links. Preserve
   all contents, paths and evidence; record before/after hashes and free space.
2. Freeze the previous cohort and owner baseline. Extract actual base diagnostic
   sources; create private diagnostic-only wrappers for monitor, error polling,
   breadcrumbs, screenshots/PNG and report I/O. Keep inclusive nested timestamps
   in memory with a checked cap; no per-event file writes.
3. Four serial post-warm captures: SampledProfile stacks, CSwitch, ISR/DPC and image
   metadata, 600 idle frames at normal/4×. Bounded elevated WPR helper only, game
   unelevated; no persistent rights/priority/affinity/power changes. Check stack
   association, event loss/schema, interrupt overlap and clock/ownership coverage.
4. Correlate long pre-render samples with diagnostic spans and stacks. Distinguish
   primary stalls, automatic-report follow-up and texture calls. Preserve limits
   (no PDB/source attribution without evidence; CSwitch V5 auxiliary fields unknown).
5. With diagnostics/traces/parsers off, run two preselected original four-process
   unmodified-lane FPS/4× placement comparisons, 120 frames/phase. Verify source,
   state/camera, save/native and window guards. Record all outcomes and caveats in
   results, CURRENT_STATUS and the maintenance handoff template. No release claim.

Completed October16: user-authorized helper retry succeeded after one Windows
elevation cancellation. Two benchmark series, four I/O-only runs while waiting,
four stack/IRQ captures and one separate forced-report calibration completed.
Zero reported event loss; one missing stack retained. No game edits or promotion.
See `docs/PRERENDER_PERFORMANCE_2026-10-16.md` and its matching handoff for results.
