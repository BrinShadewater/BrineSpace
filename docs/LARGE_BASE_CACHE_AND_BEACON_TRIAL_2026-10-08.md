# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: retained-base invalidation census and beacon batching

## Objective and acceptance
Continue full PC/Mac performance readiness, preserving exact art, timings and gameplay. Require executed candidate evidence and three matched runs before admission; one pair does not certify a gain. No publication.

## Accepted decisions and constraints
Do not rewrite base cache invalidation on this evidence: existing static/Moonbay caches already hit more than 99% of submissions. Keep beacon batching private; its zoom results currently worsen despite fewer calls. No normal room/art changes this turn. Existing normal seabed admission is documented separately.

## Current state
New private work/evidence under D:/BrineSpace-performance/2026-10-08/large-base-key-census and moon-beacon-batch. Base census wraps current MoonBase and StaticBase submit methods without changing decision/state, counting changed fields and snapshot time. Beacon prototype preserves ordered native colours/geometry, combines rectangles, Godot-style circle fans and original polygon triangulation; native antialiased lines remain original and flush batches. circle implementation/licence notice reused from prior inspected engine-derived proof. No texture mutation, reduced frames, lossy art or renderer upgrade.

New diagnostic runtimes are independent physical EXE/bootstrap copies on D. Canonical release remains on C and is loaded read-only. Existing generated C bootstrap EXE relocated with size/SHA verification to D:/BrineSpace-performance/2026-10-08/retained-bootstrap/BrineSpace.exe; relocation.json is recovery authority. Restore that exact EXE before running old C-bootstrap controllers. No canonical packages, art, player data or previous evidence moved.

## Verification
Actual debug=false 40-room/four-crew diagnostic: three 60-frame idle phases at 1/2/4x. Nine retained bases submit 3,250 times, miss 23 (99.29% hits); changes are initial water_level/idle mission initialization and one bounds update. Snapshot/key construction accumulated 25,913 us, approximately 71.58 us per common submission frame, including instrumentation. This rules out frequent base invalidation as the reported idle bottleneck; not complete pan/zoom or active mission evidence. Peak 1,734.531 MiB and exit 228.259 MiB reflect shorter fixture chronology, not a memory improvement. Owner 2,936 files unchanged, clean terminal job.

Beacon native 96 exact image comparisons, zero failures, across scale/rotation/active state/angles with fractional position and modulation. Visible two-beacon cases reduce 34 or 40 calls to 12; some offscreen cases are 0/0, so 96 is comparison count, not 96 visible draw reductions. Native test is ordinary canvas shader scope, not full room motion/layer acceptance.

First actual pair did not execute prototype (both metadata counters zero): exclude ALL its timings from candidate evaluation. Original cached Moon module survived normal-path override. Corrected PCK uses a unique Moon script binding through MoonBase, candidate first then original. Execution assertions pass: 1,124 candidate calls vs 1,124 reference calls, opposite counters zero. Same immutable PCK and original art in both lanes, actual release debug=false, uncapped/focused 1080p, 40 rooms/four crew, 9 x 180 idle/pan/zoom phases, 1/2/4x.

Corrected candidate saves roughly 64.4–66 draw calls per frame. Idle/pan means improve in all six phases by 0.232–0.885 ms, zoom means worsen in all three by 0.783–1.043 ms; p95 improves five of nine. This single pair is mixed, not admitted. Detailed render profiling disabled, so recorded render_cpu_ms zero is unavailable measurement, not zero render cost. All compared crew/drone/door/light/power/zoom AND large-prop counters equal in all nine phases; does not close historical cross-run zoom differences or every animation invariant. Both peak 2,348.739 MiB, exit 228.259 MiB, uploads 4,297; no memory gain. No errors/warnings/leaks/missing art, owners 2,936 files unchanged, runtime adapters restored, all processes terminal. Corrected evidence actual-bound/{identity,comparison,control,candidate,owner}.json; retain unbound failure separately.

## Next action
Investigate prototype geometry construction during zoom: retained bases must redraw at changed bounds, and this prototype rebuilds circle/polygon arrays in script on each redraw. Test bounded current-state geometry retention against identical native pixels and timing before further admission runs; do not rerun solely for favourable noise. Prioritize larger live-room preparation/submission work. Full combined source export, nine original packaged reports, save/UI/endurance/loading/memory/stutter gates, target PC/M1, signing/notarization/Gatekeeper remain open. Current public release has not been changed.
