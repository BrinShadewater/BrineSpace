# Project handoff

Updated: October 6, 2026 · BrineSpace · Loading progress between PNG requests

## Objective and acceptance
Keep startup responsive during non-image work without changing selected art,
crew timing, frame selection or gameplay. Full release performance remains open.

## Accepted decisions and constraints
Small source changes only; compressed crew backend stays private. Isolated
profiles verified before writes, owner files fingerprinted before/after.

## Current state
`scripts/image_prefetch.gd` adds `service_loading()`, gated by active loading and
the existing 120 ms pump limit. `scripts/crew_texture_batch.gd` services after a
complete weak frame registration. No PNG request is invented; gameplay does not
pump. `tests/test_crew_loading_progress.gd` and paired UID added to render-perf
native lane in `tests/index.json`.

Diagnostic generator `output/compressed-crew-2026-10-06/prepare-loading-progress.py`
instruments a runtime copy of Prefetch; normal diagnostics overhead is unchanged.
Evidence in the private single-buffer `loading-progress`,
`loading-progress-attribution`, and `loading-progress-serviced` directories.
Regression evidence: `output/compressed-crew-2026-10-06/crew-progress-regression/`.

## Verification
Before: native regression 5 checks / 3 failures. After: 7 checks / zero failures,
complete pending entry visible to callback, requests/bookkeeping unchanged,
rate-limited and inactive calls covered. Existing image-prefetch test passes;
registry parses and new UID unique in scripts/tests/rooms.

Native actual title/New Game/transmission/Studio/save/title/Continue diagnostics:
154 behavioral checks each run, zero failures/engine errors. Old resources release;
all 2,936 owner non-log files unchanged. Instrumented processes warn about one
exit ObjectDB instance; this remains unresolved and is not waived as harmless.

Before service: fresh 100 callbacks over 13.438 s, max update gap 912 ms, three
gaps >250 ms; Continue 33 callbacks over 5.316 s, max 800 ms, three >250 ms.
Repeat attributes ~865/802 ms gaps to entry into crew materialization and
~316/322 ms to Bill supplemental loading. After service: fresh 103 callbacks over
13.320 s, max 783 ms, one >250 ms; Continue 37 over 5.332 s, max 656 ms, two
>250 ms. All callbacks valid. Separate random sites and single runs: not a
matched speed comparison, frame certification or visual acceptance.

Remaining longest gap is now before the first batch registration. The intervening
Grid setup includes door finish creation and shared card source-region readbacks/
GDScript pixel scans. This is a narrowed interval, not proof of the exclusive cause.
Continue also has a ~320 ms nursery-view gap. Actual warm whole-scene prefetch
submitted 12,644 workers, peak pending 98, peak decoded ~96.7 MiB, eight unused
results; narrower three-bank counts do not represent full startup.

## Next action
Time door finish creation, card readbacks and region scans separately, then accept
only an exact-output optimization with matched measurements. Loading progress still
has long gaps. Worker alias work, rendering/upload stalls, longer warning/endurance,
12-room memory, original bugs and packaged Windows/Mac gates remain open.
