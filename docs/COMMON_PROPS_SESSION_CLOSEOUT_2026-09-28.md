# Common hallway props session closeout

Updated: September 28, 2026 · Project: BrineSpace

## Objective and acceptance
Make the session's non-drone floor props available as organized Common props in Layout Studio, review their visual consistency and preserve production lessons. The owner accepted the polished set before requesting this library closeout.

## Accepted decisions and constraints
19 props: 3 equipment, 6 crates/cases, 2 barrels and 8 plants. Muted matte surfaces, readable overhead forms and small-to-medium footprints remain the direction. Drone/probe machinery, collars and outlets are excluded; their accepted connection remains locked. Floor finishes and riser artwork remain in their dedicated selectors. No automatic room furnishing or changes to owner layouts/marks.

## Current state
`rooms/station-props-v2/props.json` and `assets/hallway-props-v1/manifest.json` agree on stable sp-hall IDs and common category. Studio labels use Hallway / Equipment, Crates, Barrels or Plants / name; search Hallway or a family name in Common. Registry order groups the new batch without moving unrelated records. Display widths remain 30–50 world units. Selected polished rubber-plant and asparagus-fern sources and pot-contact footprints are retained.

Visual board: `assets/hallway-props-v1/polish-review/all-props-native.png`. Registration and mark fingerprints: `assets/hallway-props-v1/polish-review/common-closeout.json`. Earlier comprehensive audit: `docs/ART_CONSISTENCY_POLISH_2026-09-28.md`.

## Verification
Shared-scale native board reviewed for relative size, apparent pixel density, silhouette/readability and muted color. Plants retain intentional differences in height and leaf shape; source image resolution is not a density target. The 19 registrations feed the station catalog and Common tray predicate; no owner category/name overrides affect these IDs. Native corridor/corner/tee checks cover four rotations and crew-clearance routes. Latest rerun passed all 228 placements with the owner profile unchanged; all 19 selected source hashes and registry mappings match. Owner marks are unchanged. The updated skill reference matches its installed copy; pre-existing differences in SKILL.md and room-decorating.md were preserved. Exact rerun result lives in `assets/corridor-risers-v2/evidence/hallway-props-summary.json` and its review log. This is bounded native placement evidence, not a mixed-prop traffic or release playtest.

## Next action
Session closed out locally. Use Layout Studio Common and search Hallway to place these props. No further generation or automatic decoration is pending for this batch. Other concurrent character work is outside this closeout. No commit, export or release was performed.
