# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Veld coordinated cargo

## Objective and acceptance
Full master-matched Veld set, followed by cross-library polish. Full goal active.

## Accepted decisions and constraints
Original identity/anatomy/proportions/matte grade; preserve room geometry and
normal selections until visual/world lifecycle acceptance. Scratch APPDATA only.

## Current state
workshop_motion_preview.gd + UID is fixture-only Veld subclass. Holds real route
through master East-West and West-North turns, aliases exact held East before
first turn, delays unload until arrival turn completes. Original speed/waypoints.
New test_veld_workshop_coordinated_joins_v1.gd + UID, matching tools runner,
review_coordinated_workshop.py, build_workshop_motion_review.py and review folder.
Normal production actor/manifests unchanged. Arrival hold bypasses normal update;
it is authoring evidence, not a safe/restore-compatible runtime controller.

## Verification
Output coordinated-joins-v1 retains first2assertion failures with exact scripts;
v2:5053checks0failures,2102ticks316captures,189frozen inputs stable,2931owner files
unchanged,102.67s. Shared CrewLife/main included. Candidate turns41/48shown ticks
with0physical travel, baselinehalfturn30.659units. Sixboards76unique pairs and2
nativefull scenes inspected. Two89frame/9983ms APNG snapshot comparisons exact
decoded178frames; not uninterrupted motion or all316visual capture acceptance.

## Next action
Author whole master-matched North unload/pickup interiors to canonical North held
turn endpoint and original master idle, without body strips/per-pose fitting.
Inspect North old final idle versus true original master before endpoint choice.
Author real first-step/stop joins; do not force held legs into walking frames.
Then safely coordinate controller travel/arrival turns with service loss, safety,
medium, equipment, death and fresh Continue checkpoints before normal adoption.
South/cardinal remaining master actions, dormant furniture sources and full-library
consistency remain. Existing normal lifecycle and cargo ownership not certified
by this authoring-only subclass. Stale player.motion during finite actions is
not the displayed source; use actual row membership/clock for interval evidence.

North action milestone now exists: see character/veld-cargo-north-master-family-v1/HANDOFF.md. Terminal idle/prop lifecycle and true first-step/stop remain.
