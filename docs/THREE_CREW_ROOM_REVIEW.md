# Three-crew room-review fixture

The station fixture accepts `--controlled-tour --three-crew-review` with the
batch-two manifest. This is an authored post-repair art/navigation scenario,
not a paid construction or full rescue-progression test.

Bill uses production emergency core recovery. The fixture moves the two seeded
architect pods into its existing Cryo Chamber and explicitly marks the ward
paid/repaired. It adds a real Crew Hab at (17,20) for two more berths, then calls
production `CryoRecovery.advance` twice. Power, food, oxygen, capacity and clear
spawn checks remain active. No fake roster or forced actor visibility is used.
All changes are fixture-local; isolated meta paths protect player unlocks.

The extra habitat makes this a 31-room itinerary. Production navigation is
updated after adding it and before retaining graph IDs or assigning a route.
Bill's destinations are scripted; Veld and Branforth use production updates.
The existing movement checks cover Bill's speed, swept room collision and
reciprocal door crossings. They do not certify every peer's swept trajectory or
all possible traffic situations. Pixel-depth approval remains a separate review.

## Retained development evidence

- `output/three-recovered-tour-v1` and v2 fail three recovery assertions. V2
  identifies the unmet berth prerequisite: population 2/2 after the mixed
  economy produced a clone, despite only Bill being a recovered architect.
- Adding Crew Hab provides capacity 4. V3 wakes all three actors but fails its
  first destination because the topology change invalidates the scheduled route
  on the next update. This is fixture sequencing, not a demonstrated prop defect.
- `output/three-recovered-no-power-v2` exits 1 with three recovery assertions.
  Both thaw steps explicitly report waiting for power with population 2/4 and
  food/oxygen available. Thus the powered setup does not bypass the power gate.
- V4 updates production navigation before scheduling. Its start sidecar records
  all three `crew_active` and `crew_present` flags true at actual 1600x900.
  It exits 0 without engine/script errors: 31 arrivals, 31 rooms visited,
  88 reciprocal transitions and 6686 Bill collision/speed samples. All three
  crew are active during this native run; the assertions retain the scope above.

The generated Node export bridge passes all six consistency checks after these
fixture changes.
The low-wall, south-facing equipment and 72-unit doorway contracts are unchanged.

## Windows export entry point

`tools/export_room_validation.ps1` now accepts `-ControlledTour -ThreeCrewReview`
and optional `-CompositionReview`, together with the batch-two additional
manifest. It expects the extra habitat in traversal and focused-capture counts,
and rejects missing/nonboolean/false active or present flags in the tour-start
sidecar. The complete start sidecar is retained in `verification.json`.

The helper rejects `-ThreeCrewReview` without `-ControlledTour` before creating
the output directory. Focused images retain crew positions from the completed
tour; they do not arrange crew behind every prop. A set of 21 focused captures
therefore proves capture availability, not 21 room-depth approvals.

## Packaged result and inspected views

`output/batch-two/three-crew-review-package-v1/verification.json` passes import,
host preflight, export and external-directory runtime with no engine/script
errors. PCK SHA-256:
`DA29E5A86F8CE966F18EC44AB9795EB1627B2C0532EE6534D0C4D24325669AFF`.
The tour records 31 arrivals, 88 transitions and 6683 Bill collision/speed samples;
all three active/present flags are true in retained tour-start metadata. The
native result's 6686 samples are a separate run, not a required exact count.
All 21 focused captures exist at the recorded 0.52 zoom.

Visually inspected the exported Anomaly Lab, Holographic Core and Med Office
full frames at actual 1600x900. Anomaly's receiver fascia reads consistently with
its machinery and adjacent lab trim. Holo's department floor/material change is
readable beside the brighter laboratories. Med Office is unpowered, with dimmed
equipment and a crew member visible in the clear central aisle; furniture remains
south-facing and inside the low hull. That clear-floor pose is not an overlap
test. No actor is present in Anomaly's focused cell, despite all three actors
being active elsewhere. These three images do not approve the remaining 18.

Next visual evidence should capture crew near registered props during room visits,
not merely refocus the camera after everyone has moved elsewhere. Keep reachable
poses and forced depth probes distinct. The current package remains a passing
three-crew scheduled tour, not complete character/prop depth certification.

## Captures during visits

The native fixture now accepts `--crew-visit-review` with the controlled tour.
It captures one actual pose per destination at 52 percent zoom: the first sample
within 32 world units of a registered prop footprint, or an explicitly labelled
arrival fallback. The sidecar records prop identity/distance, world-space feet
for all crew and the trigger. No actor is repositioned. Assertions check that
camera capture leaves all feet unchanged and restores tour zoom.

`output/crew-visit-review-v1` passes movement but its proximity selector included
wall blockers. The inspected Research Lab frame caught a doorway pose; retain
it as evidence of the selection defect, not a machinery-depth review.

V2 uses `geometry.props`, excluding walls. `output/crew-visit-review-v2` exits 0
without engine/script errors: 31 arrivals, 88 transitions, 6699 movement samples.
Its 31 visit records contain four near-prop samples and 27 arrival fallbacks:
Maintenance repair table, Crew Hab chair, Holo calibration cart and Medical Center
care trolley. Maintenance and Crew Hab full frames were inspected at 1600x900;
these are useful scale/clearance views but do not establish overlapping-pixel
draw order. Inspector connection overlays remain visible as diagnostic UI.

Six generated bridge consistency tests pass. This visit-capture revision is
native-tested, not yet exported. Next, distinguish a reachable overlap pose from
mere proximity before calling any room depth-approved; do not inflate props or
move crew through collision simply to obtain overlap evidence.

## Four-prop static overlap follow-up

Reviewed the remaining V2 Holo and Medical Center visit frames: neither contains
enough actor/cart overlap to approve depth. Ran the existing native depth oracle
against the exact four selected props instead:

- `output/holo-cart-depth-v1`: `holo_calibration_cart`.
- `output/medical-trolley-depth-v1`: `medical_care_trolley`.
- `output/maintenance-table-depth-v1`: `repair_table`.
- `output/hab-chair-depth-v2`: `hab_chair` from `rooms/whole-room/crew_hab_view.gd`.

Each exits 0 with no engine/script errors, twelve static poses and zero ordering
failures. Across the four props, all 32 ordinary front/rear poses are standable
in their complete layouts, and reversed ordering changes pixels. The 16 additional
forced-overlap poses are non-walkable and recorded separately. Normal sorted
rendering matches the explicit expected order in all 48 comparisons.

Visually inspected q0 full-room diagnostics behind all four props and in front
of the medical trolley. The table and chair correctly cover Bill's lower body
when he stands behind them; the carts layer correctly at their lower height.
These 2x diagnostic canvases are centered on the prop and can crop distant room
edges. They are static current-Bill checks, not all-character animations, walking
reachability from a doorway, or full-room framing approval. Other rotations have
pixel-order checks but have not all been visually inspected.

The first Crew Hab attempt used an incorrect production-ten path and stalled on
a null script load. Its uniquely identified process was stopped; logs remain at
`output/hab-chair-depth-v1.*`. The tool now rejects missing custom view paths before
creating output. `depth-invalid-view-v1` exits 1 promptly and creates no image
directory. This is a diagnostic robustness fix, not an art change.

## Interactive local review page

[Crew / prop depth review](crew-prop-depth-review.html) provides prop, rotation
and pose controls; normal and reversed isolated renders use the same framing.
A separate room-context image avoids presenting a background change as an
ordering difference. Original images and JSON records are directly linked.
Forced non-walkable poses carry a distinct warning, and image-load errors are
shown instead of silently leaving an apparently valid review.

`node --test tests/test_crew_prop_depth_review.cjs` passes two tests: all 48
selections agree with their underlying ordering/standability records, all 144
PNG links have 800x800 headers, and rotation wrapping/error-state controls work
in a DOM stub. This is not a real-browser rendering or accessibility audit.
The page is local and depends on retained output folders; it is not published.

## Remaining rear-pose rotation review

Visually inspected the q1/q2/q3 full-room behind-prop images for all four props
(twelve additional images). Upright prop silhouettes are retained; none of these
selected props visually overflows its adjacent hull. Maintenance's table and
both carts retain the expected foreground relationship to Bill. This extends
visual coverage of rear poses only, not every front/forced pose or animation.

Crew Hab q3 exposes a separate open finding: Bill's valid rear-chair pose projects
his upper body above the north hull. This is the already documented low-wall
projection class, now identified at an exact review pose. The gallery displays
this finding for chair/270°/behind separately from its passing prop-order result.
All three gallery tests pass, including warning visibility and clearing.

The bible already requires low walls and forbids clipping heads or shrinking
crew as a workaround, so no contradictory aesthetic amendment was added.
Any proposed furniture setback or rear-access adjustment must preserve real
circulation and receive its own rotated composition review; it is not implemented
or approved by this finding.
