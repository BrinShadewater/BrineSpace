# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: sustained rendering attribution

## Objective and acceptance
Locate continuing rendering costs in the40-room scene after local wall/floor
trials fail to resolve sustained performance. Rendering exclusions are diagnostic
only, never a quality setting change or accepted optimization.

## Accepted decisions and constraints
Frozen accepted crew-cache Grid source, actual debug=false package, isolated
profiles and owner guards. Same deterministic simulation continues in every lane.
Compare forward/reverse orders and phase-end gameplay states. Known idle editor
is recorded; these runs do not certify target hardware. Keep source/packages intact.

## Current state
One-file private Grid overlay at D:/bs-release-crew-cache-20261009/live-layer-diagnostic/.
Modes: none; live_env suppresses LIVE_LINES/LIVE_ABOVE/EXTERIOR_ACTORS/FOG/LIFE
environment pass painting; rooms suppresses the LIVE surface and its child content.
Rendering targets are hidden, without skipping simulation. Other renderer layers
continue. Driver run-live-layer-diagnostic.py runs three idle speeds,180 samples
each, both lane orders. Existing completed preparation-diagnostic physical QA copy
is hash-verified and reused; previous fixture preserved alongside new fixture and
identity. No additional multi-gigabyte package duplication.

## Verification
Final session15450 exits0: six packaged runs/3,240 measured frames; no engine or
missing-art errors and owner2,938 unchanged. Exclusion counters confirm the five
live environment callbacks disappear; room exclusion removes live-room callbacks
and content draw time. Normal source and delivery remain unchanged.

All-visible averages27.2011/28.1998ms forward/reverse. Live environment exclusion
saves4.4407/4.6483ms; room exclusion saves7.2155/8.5356ms. These separate changes
are diagnostic bounds, not additive independent costs or production improvements.

Exact state analysis passes all six environment comparisons but fails all six
room comparisons. Recursive investigation finds128 differences, all exclusively
animation playback for Margot, River and Branforth (keys/phases/motion/last sample).
No other captured state differences. Rendering drives that playback; bypassing
room painting freezes its saved history. Keep the exact-check failure and detailed
state-differences.json, never remove fields to claim compatibility. Actual fixes
must preserve playback advancement and historical save bindings.

Room-exclusion screenshot reviewed: floors/walls remain, room props disappear;
cards, inspector and a synergy modal remain. This confirms the intended exclusion
but does not establish normal motion/room visual acceptance. analysis.json records
timing, callback counts and exact mismatches. Owner guard records unchanged2,938.

Isolated overlay packaging passes, owner unchanged. Native session15450 is running.
First all-visible forward lane completes: mean27.2011ms; zero engine/missing-art
failures. Complete exclusion/state comparisons and final owner fingerprint pending.
Inspect resulting draw counters and screenshots to confirm what each exclusion
actually removes before interpreting timing differences. Unrelated simulations,
loading, original bugs, endurance and Mac acceptance remain open.

## Next action
Prioritize attribution inside live-room setup/slot drawing and exterior drone
rendering, retaining animation sampling. Existing _room_setup_skippable rejects
special rooms and actor-containing rooms; ordinary static props already retain
commands. Measure those specific paths before changing their invariants. Environment
exclusions preserve full captured state and are another verified cost target.

Wait on15450, compare all measured states and frame distributions, inspect excluded
layers' draw profiles/counts. Choose a quality-preserving change from observed
attribution; do not interpret hidden-layer FPS as production improvement.
