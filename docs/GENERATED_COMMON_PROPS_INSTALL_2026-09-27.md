# Project handoff

Updated: 2026-09-27 · Project: BrineSpace · Task: install generated common props

## Additional 14 installed — later September 27

Owner authorized installing the two omitted packs identified below. Their 14
calibrated PNGs are now registered unchanged: 112 generated additions and 589
station-catalog entries total. All 575 preceding catalog records were preserved;
the additional snapshot is `catalog-before-additional14.json` in the evidence folder.

The repeatable installer now selects 17 packs. The comms panel has explicit
`wall_attachment` metadata, forwarded by `scripts/room_asset_library.gd`;
`scripts/room_layout_store.gd` gives it the existing raised-wall placement envelope,
and `tools/modular_room_geometry.gd` omits floor collision. An empty collision-box
list alone was insufficient because normal geometry falls back to the footprint.
Other furniture and its floor blocking retain their existing behavior.

Expanded native fixture: 6,915 checks, zero failures; all 112 thumbnails, constrained
Studio panel mounting, save/reload into actual gameplay, 448 individual placements
across four room rotations, walking routes and twenty native pilot captures.
Pilots 4/5 show all fourteen additions; panel mounting and source art visually
reviewed. `gameplay-saved-panel.png` proves the saved attachment reaches gameplay.
The current native log/selection/release-coverage files supersede the earlier
98-prop evidence totals. All 112 PNGs are included by read-only release dependency
collection and have LFS attributes. Real-profile fingerprints match under isolated
testing. Owner layouts, source artwork and executable packages were not changed.

No BRINE corner replacements, riser-v4 study or crew animation pilots were promoted.
Those remain separate work. Cards need no rebake because default furnishing was
unchanged. The earlier sections below record the first installation and audit.

## Objective and acceptance

Owner requested installation of the previously generated common furniture, plants,
storage, seating and counters. Install the current revisions in the active Studio
catalog and retain placements in gameplay. This is catalog installation; room
furnishing and executable rebuilding were not requested.

## Accepted decisions and constraints

98 distinct calibrated exports selected across 15 packs. Matte plants replace the
ten older calibrated plants. Refined wood/sink, remaining corner and metal-corner
packs replace their superseded candidates. Earlier rejected seating/corners are
excluded. Existing source PNGs are referenced unchanged by whole resource paths.
The complete pack selection and per-prop registration are reproducible through
`tools/install_generated_common_props.py`; its default mode audits without editing.

New IDs use `sp-generated-` in `rooms/station-props-v2/props.json`, category `common`.
They appear in **Layout Studio → Asset Tray → Common Props** and use the active
station-prop route; the historical `library/common-` route remains filtered out.
All 477 pre-existing catalog records remain unchanged (575 total). Owner layouts,
marks, defaults and room cards were not edited. No new behavior is inferred from
static fridges, charging racks, chairs or dressed equipment.

## Current state

Changed: station-prop catalog; new repeatable installer; native regression fixture
`tests/test_generated_common_props.gd` and its UID/native test-index entry; isolated
runner `tools/check_generated_common_props.py`; current-status entry and this
handoff. Added normalized floor-contact/collision rectangles, two-arm counter
collision and the existing corner draw-depth metadata. Calibrated display widths
are preserved. No production GDScript change was needed.

Evidence: `output/generated-common-install-2026-09-27/` contains the before-catalog
snapshot, 98 source/hash mappings, five source boards, native log, Studio tray,
saved-chair gameplay capture, twelve room pilot captures, release coverage and
before/after real-profile fingerprints. Source images were already untracked in
this concurrent checkout; all 98 are covered by Git LFS attributes. Nothing was
staged, committed or pushed.

## Verification

Native Godot 4.7.2 fixture: 5,502 checks, zero failures. All 98 thumbnails render;
normal Studio add/save/reload reaches the actual gameplay scene. Each prop survives
production layout/retirement filters in all four room rotations (392 placements);
door approaches/routes remain clear at the fixture positions. Counter recesses
stay walkable. Three furnished pilots exercise walking and native rendering in
four rotations beside Bill and an existing accepted furnishing. Source boards and
native captures were visually reviewed. These are fixed-facing sprites in four
room rotations, not four newly authored sprite directions.

Installer is idempotent; all selected hashes and calibrated canvases match their
source manifests. Read-only release dependency collection includes all 98 PNGs.
Every Godot invocation used scratch APPDATA/LOCALAPPDATA; final fingerprints of
the real owner profile match. No executable was rebuilt.
Reproduce with `python tools/check_generated_common_props.py`; the fixture skips
ordinary runs without its isolation marker.

## Next action

Available for owner placement through Common Props after restarting the project.
Future furnishing needs clearance/depth review at the actual chosen positions;
arbitrary placements, seated-character interaction and every flip/scale combination
are not certified by these fixtures. Rebuild through the maintained release workflow
when an updated standalone executable is requested.

## Follow-up missing-assets audit

Owner asked whether other generated assets/animations were missed. Read-only
runtime dependency and byte-hash comparison found two additional uninstalled
prop packs outside the 98-prop selection: `servers-comms-shelves-2026-09-26`
(6 props) and `submarine-utilities-2026-09-26` (8 props). Their calibrated exports
exist; live integration/mounting remains unverified. They were not installed by
this follow-up audit. Evidence: `output/generated-common-install-2026-09-27/remaining-pack-audit.json`.

Also uninstalled: the two corrected BRINE Core corner replacements (native preview
exists; walking and screen overlays still unverified) and the 47-room riser-v4
study (production catalog still uses department/v2/v3 resources). Superseded
plant/corner versions are intentional omissions. The new Veld v2 animation pilot
remains unfinished and uninstalled; current drone/dock, companion and BRINE motion
bindings are already installed per the source consumers and September 27 audit.
