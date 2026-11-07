# Project handoff

Updated: September 20, 2026 Â· Project: BrineSpace Â· Task: three-room composition pilot

## Revision 02 â€” owner feedback and current selection

The owner called Crew Hab okay and Maintenance/Bio Lab lackluster. Crew Hab stays
as the provisional reference, unchanged. The other two rooms now use larger,
more complete work areas instead of the sparse first-pilot arrangement below.

- Maintenance: enclosed CNC machine, component rack, electronics diagnostic desk,
  twin-arm assembly station, instrument bench with nearby drawers and parts bins.
- Bio Lab: biosafety cabinet with supply locker, distillation rack with secured
  storage, paired analysis benches, incubator and specimen tank, and an operator
  console. Only the console/diagnostic desk moves to the closed wall when rotation
  opens the north approach; the main equipment groups stay together.
- Eight keys updated in defaults and local Studio layouts; all other keys,
  including Crew Hab, compared equal. Two room cards refreshed.
- Candidate and installed native review each pass 8 views and 1,280 clear walking
  samples, with no overlapping bounds or blocked door approaches. Native rotation
  contact reviewed. All 188 authored layouts pass the layout-key checker.
- No source raster edits or generation services. Existing composite assemblies
  provide a stronger focal point and more useful detail at the same room scale.
- Evidence and rollback inputs: `output/room-composition-pilot-2026-09-20/revision-02/`.
  `owner-before.json` and `defaults-before.json` preserve the first pilot;
  `selected-art.json` records source hashes and registry IDs. Only restore these
  eight keys after checking for newer edits. The root review page shows revision
  02; first-pilot captures remain preserved under the original `installed/`.

Owner review of this revision is pending. The following sections retain the first
pilot's scope and dated evidence; revision 02 above is the current selection.

## Objective and acceptance

Replace scattered furnishing with logical groups of large/medium bought props.
Crew Hab, Maintenance Bay and Bio Lab are installed for the owner's visual review,
not accepted for a station-wide rollout. Research was used as an untouched
composition reference. The owner has not yet answered which rooms they personally
positioned, so the entire original local save is backed up.

## Accepted decisions and constraints

- Preserve the hybrid visual style and character identities. No blanket upscale.
- Use large/medium equipment first; no scatter of pipes, extinguishers or tiny filler.
- Preserve original functional furniture and its approaches when gameplay uses it.
- No Higgsfield unless explicitly requested. No generation service was used.
- Bill's body-motion repair remains next; Mac release work follows a stable build.

## Current state

| Room | Composition |
| --- | --- |
| Crew Hab | Original usable berth, bought bunks and personal lockers along the rear; a separate sofa/table/plant corner. |
| Maintenance Bay | Original precision repair station, tool drawers, bench and screened welding bay; a separate robot cell beside parts bins. |
| Bio Lab | Preparation bench, incubator and microscope bench grouped along the rear; a separate specimen tank. |

When north opens in quarters 1â€“3, only the obstructing equipment moves aside.
Small standalone accessories and overlapping old/new furniture were removed from
these layouts, not from the asset library. No source raster repair was needed for
the selected props; the older bed/machinery still show the hybrid detail contrast.

Changed: `rooms/full-wall-v1/default-layouts.json` (12 keys),
`assets/room-cards-v2/{crew_hab,maintenance_bay,bio_lab}.png`,
`tools/review_room_composition.gd` and its paired UID,
`tests/test_layout_keys.py`, CURRENT_STATUS, the visual bible and room skill.
The installed room skill is synchronized from the maintained repository source.
The same 12 keys are installed in the owner's local `room_layouts.json`.
All non-pilot layouts were compared and preserved.

Local review evidence: `output/room-composition-pilot-2026-09-20/index.html`.
The directory also holds native before/final/installed images, all four rotations,
composition spec, candidate layouts and logs.

## Verification

- Candidate and installed-default native reviews: 12 views, 1,920 walking samples,
  zero failures each; prop bounds, door routes and original berth access checked.
- `python tests/test_layout_keys.py`: 188 authored layouts, zero problems.
  Self-test detects all eight planted faults. The checker now reads tileset IDs and
  valid aliases; null suppression entries need no surviving asset.
- `python tools/run_tests.py --only test_crew_room_activity,test_tileset_registry`:
  both pass, including 36 activity/rotation/actor cases and 10,507 props.
  Logs: `output/test-runs/20260920-222908-headless/`.
- Native four-quarter contact sheet visually reviewed; three cards freshly baked.
- Broad Grid initialization during the older capture/card tools logs missing
  legacy-art paths (including Tidal and Command Center). Direct pilot-view review
  is clean. Investigate those warnings before stable-build or Mac acceptance.
- No normal paid expedition, Mac export, release acceptance or owner approval
  is implied by this bounded pilot.

## Next action and rollback

Review the three rooms with the owner. Refine density, grouping or scale before
decorating more rooms. Identify their hand-authored reference rooms first.
The visible old/new detail contrast remains an art-direction decision.

Backups under `output/room-composition-pilot-2026-09-20/`:
`owner-layouts-before.json`, `owner-layouts-pre-install.json`,
`defaults-before.json`. To roll back after later Studio edits, restore only the
12 pilot keys from those files into freshly read documents, after inspecting any
new edits to those keys. Never overwrite the whole current owner file.
Do not reset unrelated working-tree art captures or the owner's library marks.


## September 21 review direction

Reinspected revision-02/rotation-review.jpg. Larger equipment now reads clearly,
but both rooms still arrange many stations as separated perimeter groups around
a broad empty central aisle. Further work should test a connected working area,
not add small filler: an L-shaped diagnostic/parts cluster in Maintenance and a
clear preparation-to-analysis progression in Bio. Preserve door-to-door routes,
original functional furniture and untouched Crew Hab/owner rooms. Stage alternate
layouts for comparison before overwriting installed revision 02. This is an agent
critique and next experiment, not owner acceptance or a newly installed revision.


## Revision 03 staged comparison â€” September 21

Candidate only: output/room-composition-pilot-2026-09-20/revision-03/pilot-layouts.json.
Maintenance groups the robot, diagnostic desk, drawers and bins in the lower-left;
Bio groups preparation/analysis benches along the left and culture equipment right.
No owner/default layouts or cards were overwritten. First render revealed overlaps;
refinement separated them and corrected one drawer's room-edge overflow.

Final native check: 8 views, 1,280 walking samples, zero failures (final.log).
Q0 images inspected: grouping is more explicit in Maintenance, but the lower-left
now feels crowded and the right half vacant. Bio remains too perimeter-driven.
Do not promote this merely because geometry passes. Revision 02 remains installed.
Next composition needs an intentional working aisle between related equipment,
rather than packing an entire work cell against one boundary. Keep this alternative
as comparison evidence and adjust the spatial structure before adding more props.


## Revision 04 staged alternative â€” September 21

Candidate: output/room-composition-pilot-2026-09-20/revision-04/pilot-layouts.json.
Maintenance separates a larger diagnostic desk and drawers on the left from the
robot work area on the right; removes the loose parts-bin prop. Bio enlarges and
aligns the preparation/analysis benches and culture equipment across the lower
work area. Revision 03's one-sided cluster was not promoted.

Final native review: eight views and 1,280 walking samples, zero failures, final.log.
Q0 and q2 inspected, including the relocated support console beside the robot in
q2. Readability improves over revision 03; q2's console remains closely packed and
needs owner review. Installed defaults, local owner layouts and cards remain at
revision 02. Asked which hand-positioned rooms should serve as visual references;
answer pending. Avoid repeated speculative rearrangement until that reference
information or feedback on the staged alternatives arrives.


Scale correction to revision 04: removed the optional drawer that had been shrunk
to 0.45 merely to fit below the diagnostic desk. That workaround contradicted the
pipeline's crew-relative scale rule. Pre-correction candidate retained as
before-scale-review.json; current pilot-layouts.json omits it. scale-reviewed.log:
8 views, 1,280 walking samples, zero failures; Maintenance q0 inspected. No live
layout writes. The room skill's historical two-addition cap is now explicitly
superseded by the current activity-led bought-prop workflow; installed skill synced.
The bible now distinguishes gait support timing from joint-art quality and records
composition crowding/scale lessons without claiming owner acceptance.


## Selected-prop quality inventory â€” September 21

Current owner fix queue is empty: favourites.json is [] and names.json is {}.
The dated library handoff's two outstanding stars are historical, not current work.
Revision 04's 14 selected props have no entries in the existing hole report.
Source regions range from 43-pixel-wide lockers to 190/191-pixel-wide machinery;
placement ratios are 0.52â€“0.92 world units per source pixel. This does NOT measure
screen pixels at a particular camera zoom, prove defect-free art, or establish
stylistic acceptance. It does show that this layout is not enlarging those source
regions beyond one world unit per pixel. Preserve the inventory and source hashes
in revision-04/selected-prop-quality.json before any targeted art repair.

No blanket upscale is supported by this evidence. Compare specific props at normal
station zoom with the detailed crew/environment before choosing local cleanup,
redrawing or a different library item. No marks, source PNGs or library entries were
changed by this inventory.


## Owner reference evidence â€” September 21

Captured all 40 views of the ten named owner rooms from the preserved fresh save:
output/owner-room-references-2026-09-21/native. Research and Crew Lounge q0 inspected.
Their intentional assemblies/layered furniture invalidate a blanket visual-bounds
non-overlap requirement. The review tool now records visual overlaps as notes;
--strict-visual-overlap retains the old gate for deliberately disjoint layouts.
Native follow-up on Research/Lounge: 8 views, 1,280 samples, 16 overlap notes,
with the Research q2 center-to-north straight approach still flagged. Check actual
alternate navigation before declaring that a blocked door. The full initial capture
also flags Pressure/Listening art extents; preserve owner layouts while inspecting
whether those are intended wall-mounted bounds. No owner/default layouts changed.

### Research doorway attribution and live geometry — September 21

The review now searches the Studio actor graph for a door approach route and lists
collision props at blocked endpoints. Research q2 fails at (0,-168):
`library/tileset-lab-36`, rectangle (-33.1875,-218.7392,66.37499,69.39204), with
10-unit actor clearance. Native preview: four views, 640 walking samples, one access
failure. A separate native probe calls `Grid.bill_room_geometry` with the saved
owner layouts and each rotation's connected side. That prop remains in gameplay
geometry and blocks the same point; all other rotation approaches are clear.
Evidence: output/owner-room-references-2026-09-21/live-geometry.json and
navigation-attribution/. No owner layout changed. Full doorway traversal remains
unverified; blocked center approach alone does not prove an actor cannot enter.

## Maintenance repair-bay pilot installed — September 21, 2026

Revision 05 replaces the isolated diagnostic desk with two adjoining medium tool
benches, forming a manual repair bay opposite the robot assembly station. CNC and
parts storage remain across the upper work area. Native four-view/640-sample review
passes; q0/q2 visually inspected. Installed only four Maintenance keys in defaults
and owner saves, after verifying the owner keys still matched previous defaults;
all other keys preserved. Backups and evidence: output/room-composition-pilot-2026-09-20/revision-05.
The single Maintenance card was rebaked and visually inspected. Bio remains at
installed revision 02, with revision 04 staged; ten owner reference rooms unchanged.
This is an installed pilot for owner review, not owner visual acceptance.


## Bio Lab pilot and console registration repaired — September 21, 2026

Installed the previously staged revision 04 Bio layout: aligned preparation and
analysis benches, separate culture equipment, and rotation-specific console placement.
Four native views/640 walking samples pass after correcting lab-20's source region:
[144,389,144,91] included a neighbouring table edge and clipped the chair;
[180,389,108,115] contains the complete workstation. Region, absolute pieces,
display width and footprint were rebuilt together using the maintained helper;
source PNG unchanged, stable ID retained. Registry validation passes 10,507 props.
Only four Bio layout keys changed in defaults and owner saves after matching the
prior defaults; all other keys preserved. The single Bio card was rebaked.
Evidence/backups: output/room-composition-pilot-2026-09-20/bio-final.
Installed for owner review; no owner visual acceptance claimed.


### Pressure/Listening extent review - September 21

Pressure gs-14's visual extent reached x213.24 beyond the room's x192 outer bound;
q0 showed the lower-right machine cut at the edge. Staged a single x114 -> x90 move
in each quarter, with size and every other placement preserved. Four native views
and 640 walking samples pass; q0 reviewed and the full machine is visible. Owner
saves unchanged. Candidate and captures: output/owner-room-references-2026-09-21/
pressure-correction/. Listening q0's separate warning is the fitted east-wall
console, whose declared bounds reach x195.56; preserve its placement pending
wall-specific visual judgment, not an automatic free-standing floor correction.
