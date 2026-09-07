# Gravity Loom Windows debug evidence

`output/gravity-loom/windows-validation-v1/verification.json` records an exported
build run from an external empty working directory. Selected sources/cards decode
and the current Bill navigation controller completes a controlled tour of all
17 fixture rooms: first production ten, Gravity Loom and six supporting Battery Array cells.
It records 43 reciprocal-door transitions and 3,278 checked movement steps.

This validates the current controller in that layout, not every rotation or
every doorway at native zoom. The legacy crossing fixture failed 12 arrival
assertions because it still drives obsolete progress fields; its 112 frames
are retained as failed diagnostic evidence. Migration is required before any
visual doorway acceptance. Likewise, the earlier 892,032-sample sweep covers
the retained legacy perimeter helper, not Bill's current navigation graph.

Windows debug validation only; no publication or release acceptance.

Follow-up: `crossings-v2` migrates the fixture to Bill's graph and production
update loop, with bounded steps and physical endpoint assertions. All 16
socket/rotation crossings pass; all 112 native crops were reviewed across
three sheets. No Loom apparatus intrudes into the sampled approaches. Shared
horizontal collars partially occlude the lower sprite; full shared-door art
acceptance remains separate. Review: `crossing-review-v2/review.json`.
