# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: shared-state station composition coverage

## Objective and acceptance

Check private retained large-room composition against original LIVE drawing with actual mixed-station data and ordinary retained contents. The measured ~7-ms private CPU saving remains promising; normal admission and release acceptance are still pending.

## Accepted decisions and constraints

Both renderer copies draw the same paused native fixture state in simultaneous SubViewports, avoiding cross-run animation/time differences. Simplified Grid subclasses disable their normal ready/process behavior, share already loaded crew players, and invoke the actual `_paint_surface(LIVE)` implementation. These are native LIVE-layer comparisons, not complete gameplay screenshots, floor/wall/foreground acceptance or benchmarks.

## Current state

Private probe/preparation and isolated runners: `output/moonbay-station-composition-2026-10-06`. Final coverage under `neighbors/`; reference/candidate captures retained there and visually inspected. No normal runtime changes this turn.

## Verification

Initial 12 equality pairs had no explicit room visibility guard; do not use them as neighbor coverage. Second probe fits every room bound and guards nonblank output, but visual review found ordinary props were culled against the original Main camera. It is insufficient for ordinary-room coverage.

Final probe overrides comparison view bounds, disables prop culling explicitly, fits all 40 room bounds, checks >10,000 nontransparent pixels and asserts at least 100 visible ordinary slots with equal counts. All 12 comparisons pass exactly: 3 distinct zoom sizes × idle/flood/launch/return mission states. Both sides show 248 visible ordinary slots; nontransparent pixels 117,279–300,866. All 12 multi-cell rooms, including three Moonbays, are on screen. Captures show large-room bases alongside ordinary props (ordinary floor/shell passes intentionally omitted). Each native process exited cleanly; each owner's 2,936 files unchanged. No FPS measurement or memory claim from this check.

The actual LIVE implementation includes the conditional BRINE north-wall signal path, but this probe does not instrument whether the fixture activated it. Do not close that specific active-signal coverage from code presence alone. Scope also excludes continuous zoom, owner layout imports, full scene materials, removal/culling/return lifecycle and foreground effects.

## Next action

Instrument active BRINE signal execution and add lifecycle checks for demolition/replacement, visibility recovery and complete owner release. Cover live layout/style mutations and filter/material inheritance. Then install the retained renderer with permanent relevant tests and accurate child-callback diagnostics, followed by a justified matched mixed-station run. Keep full release frame/memory/PC/Mac gates open.
