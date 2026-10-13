# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: loading metadata memory release

## Objective and acceptance

Continue full PC/Mac performance/release readiness. Attribute the first-Continue static-memory increase and release verified obsolete startup data without changing loading order, pixels, worker scheduling or diagnostic totals.

## Accepted decisions and constraints

Do not label the entire ~56 MB step as a leak or solved. Compare equivalent settled states before closing it. Normal cleanup is limited to unused startup path arrays/map after workers join and the manifest is saved. Owner data remains isolated.

## Current state

- `scripts/image_prefetch.gd`: completed_requests scalar preserves post-loading report counts; end releases recorded/previous path arrays and index map after writing the unchanged manifest. begin resets the scalar. Worker/image cleanup, scheduling, source digest and pixels unchanged.
- `tests/test_image_prefetch.gd`: regression checks metadata release, persisted request order, normal inactive decoding and preserved report totals. Existing paired UID retained.
- `output/scene-dependency-warning-2026-10-06/`: three-cycle startup memory trace using a physical private Main copy; two-cycle direct metadata-release attribution; before/after unit checks and installed two-cycle gameplay checks.

## Verification

Three-cycle trace passes 296 checks with zero errors/warnings/anonymous objects. Memory fluctuates substantially within interface/grid/restoration/prewarm stages; worker/image transients must not be equated with settled growth. Normal source unchanged for that diagnostic.

Direct private release after loading is inactive, worker tasks/results empty and image-cache bytes zero: fresh 12,716 recorded paths release 4,637,116 bytes; first Continue (12,723 recorded paths plus 12,644 previous paths/index entries) releases 9,889,100 bytes. Two-cycle probe passes 196 checks, zero errors/warnings. This demonstrates real unused metadata retention and explains only part of the fresh/Continue difference.

Regression before cleanup fails the two new release/inactive-report checks as expected. After cleanup, image-prefetch and crew-progress tests both pass with zero engine errors. Prefetch test has one intentional missing-art warning from its existing bad-path fixture; it is not an exit warning.

Installed cleanup passes 200 native actual New Game/Studio/save/title/Continue checks with zero errors/objects/warnings. All inactive path collections are empty and report request counts remain 12,716/12,723. Existing exact manifest-order/returned-image tests pass. Worker statistics remain available (this warm workload peak 98 pending tasks/87,880,408 decoded bytes); these are observed transients, not a new scheduling acceptance claim.

Installed gameplay static memory: 456,817,188→507,366,406 bytes. Roughly 50.55 MB still separates fresh and first Continue; different stopped actor progression/presentation prevents equivalent-state closure. GPU texture memory is not reduced by this CPU metadata cleanup. Private providers remain unadmitted; normal 12/40-room budgets unverified.

All 2,936 owner non-log files unchanged across every completed lane. Native processes terminal; scoped whitespace checks pass. No art changes, export, commit or publication.

## Next action

Measure the same saved crew/room/playback state immediately before save and immediately after Continue, before additional simulation. Attribute remaining static allocations by actor navigation, presentation, source-bank and UI categories; distinguish stable warm allocations from sustained growth. Keep larger workload, lossless provider admission, refreshed actual release, frame/loading/memory, original bugs, endurance and actual Mac gates open.
