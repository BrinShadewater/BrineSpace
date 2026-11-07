# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: current renderer pass attribution

## Objective and acceptance

Locate remaining repeat work during lighting changes and zoom without replaying previously rejected tiny query caches. Diagnose before changing selected pixels, line widths, filtering, animation timing or default effects. Full original PC/Mac release scope stays active.

## Accepted decisions and constraints

Earlier small connection/port caches remain rejected within their recorded scope. Measurements below are instrumented native attribution, not optimization acceptance or packaged certification. Timings overlap parent scopes; draw-call counts and microsecond timings are different units and must not be summed together.

## Current state

`output/compressed-crew-2026-10-06/trace-floor-preparation.py` creates fresh normal Main/Grid/scene copies under `output/floor-preparation-2026-10-07/`; only diagnostic label prefixes change. Main points to private Grid; duplicate Grid class_name and scene UID removed. Room renderers and selected crew/assets use current normal source; no private memory provider. The diagnostic tags `_draw_nursery` setup as floor, shell, content or preview; existing large callback labels remain separate. Original source hashes retained in inputs.json. Normal source/art/UIDs unchanged.

## Verification

- Native Godot4.7.2 Compatibility/RTX4070Ti at1920×1080, deterministic40-room fixture, idle/lighting/zoom at1/2/4×,60 measured frames each:9 phases. Clean engine log/exit, no missing runtime art/warnings/leaked-instance diagnostics. Owner2,936 non-log files unchanged. Probe isolated user dir verified by benchmark. Full report, summary and log retained; process terminal.
- At1× lighting: floor actor setup0.148ms, configure0.376ms, door setup0.262ms, floor rendering0.478ms, light pools0.325ms, equipment shadows0.979ms per measured frame. At2×/4× shadow cost0.956/0.821ms. Floor actor setup0.145/0.129ms. Removing actor setup alone is too small to explain large spikes and may change animation access side effects; no such patch accepted.
- At4×: idle large base callback0.879ms /large Props callback0.490ms /retained prop draw0.963ms; lighting0.916/0.507/0.989ms; zoom2.665/1.242/2.387ms. Source inspection confirms record_draw includes actual drawing callbacks, not solely preparation. Label `setup_large_*` is misleading if treated as exclusive setup cost; do not add these scopes to broader live_rooms budgets.
- Instrumented p95 spans38.409–68.254ms; frame gate still fails. No before/after gain, engine/driver-cause attribution, visual-motion acceptance or hardware/Mac claim.
- Initial preparation failed writing a Unicode Main copy with Windows default encoding before any engine launch. Fixed explicit UTF-8 reads/writes; no native result from that setup failure. Corrected diagnostic completed; no production game fix or changed test expectation.

## Next action

Inspect/test command retention for large static bases during zoom: StaticBase keys currently include screen rect and therefore replay draw commands as scale changes. Prefer a bounded isolated native trial of canonical room-space commands with CanvasItem transforms, preserving original fractional coordinates, line widths, clipping, layering and selected textures. Pixel mismatches reject the trial; no automatic quality change or renderer upgrade. Moonbay's live animation remains distinct from static farm/storage bases. Require measured base-only cost plus matched gameplay comparison before source admission. Continue exact-crew/provider ownership/loading, full original bug/UI/motion, performance/memory/endurance, target PC and native Mac certification gates.
