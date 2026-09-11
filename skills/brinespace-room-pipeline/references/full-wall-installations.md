# Full-wall installations: September 8 production lessons

The owner prefers one connected installation on a sealed wall, with department
color retained and restrained brightness. Preserve better existing compositions:
Pressure Control keeps its original installation. Door masks remain authoritative.

For side-only walls, use newly drawn north–south equipment views with their backing
against the sealed wall. This owner-authorized exception to the default south-facing
contract is limited to the full-wall installation set. Never rotate a horizontal
raster or squeeze it into a narrow strip. Paired source sheets are alternate views
of ONE installation, not two new room assets. Inspect backing direction: the lounge
generator reversed the requested left/right order. Record the selected half.

Use `tools/register_side_wall_props.py` for source polygons. Existing reviewed
registrations are preserved on rerun. Changing a source requires a new revision and
fresh registration/review. Keep the original raster, exact prompt and source hash.
The RGB sheets have white/checkerboard backgrounds; transparency comes from draw
polygons, not from an alpha channel. Do not describe raw sheets as transparent PNGs.

Run `tools/audit_full_wall_cutouts.py` to propose bright-neutral candidates. Bright
trim, glass reflections and pale enamel are not background. Inspect candidates
before choosing seeds. Exterior cleanup does not remove enclosed pipe or gantry
holes. Use `tools/repair_full_wall_gaps.py REGISTRATION --seeds "x,y;x,y"` for
reviewed enclosed holes. It checks source hash, rejects artwork/exterior seeds,
preserves the approved outer bounds and region, and is idempotent. Do not regenerate
the entire outline to fix one hole: even a one-pixel anchor shift affects placement.

Judge brightness in native same-scale rooms and gameplay captures, with the game's
floor underneath. Use source percentiles as diagnostics only. Keep maintenance and
refining dark; clinical cream and controlled blue/green glass can remain lighter.
Do not flatten department contrast with a global tint or remove valid white trim.

Relocate displaced originals only where both visual bounds and ground footprint
fit. Inspect mats, service leads and support props after relocation; a moved blocker
alone does not move a baked wall slice. Leave source art available when no clear
location exists. Keep door approaches clear and validate actual crew routes.

Stateful art needs explicit checks: the side mining cradle is empty while the live
vehicle and hatch remain separate; recovered cryo-pod layouts retain the original
one/two-pod behavior. Run `tools/review_full_wall_rooms.gd` for all 15 rooms, four
rotations and both operating states, plus cryo recovery comparisons and card bakes.
Run `tests/playtest_full_wall_rooms.gd` against all 15 IDs with
`--composition-review` for gameplay-scale evidence and real walking-route checks.
Inspect output, including script errors even when process exit code is zero.

After each accepted pass, update this reference with verified lessons, update the
source/selection ledger, and sync the changed maintained skill files into the
installed snapshot after comparing versions. Keep diagnostic captures in ignored
`output/`; do not ship them accidentally with raw asset exports. Native editor
verification does not establish packaged-build acceptance.

Couch revision lesson: a long side-view silhouette can still contain a slanted
back/picture panel. Inspect its wall-contact edge and interior long axes for
parallel alignment. September 8 v2 straightens these edges; v3 previews a softer
burnt-orange upholstery. Record preview status separately from runtime selection.

Owner palette correction: reducing orange saturation alone did not satisfy the
couch brief. Use fall colors: earthy red-brown rust/chestnut with muted ochre and
dusty burgundy accents. v3 was rejected as still too bright orange; v4 is the
subsequent preview. Do not promote a preview to an accepted style reference.

Approved couch palette: the owner selected v5, a slightly warmer cinnamon-rust
variation on v4. Use assets/side-wall-props-v5/crew_lounge.png as the approved
upholstery reference. The matched horizontal source is
assets/full-wall-props-autumn-v1/crew-lounge-built-in.png. Both are now selected
through current registrations. Keep straight wall-contact edges and restrained
autumn color; earlier brighter previews are not the current reference.

Relocation follow-up: retain a complete saved dressing profile, but derive active
furniture, mats and supported-object definitions from the surviving prop IDs, just
as service routes already follow their endpoints. Otherwise replacements leave
stale host references even if the renderer silently skips them. Verify all live
helpers with audit_room_dressing_hosts.gd --check-mat-bounds and retain the
--negative-missing-host control. Never remove missing-host checks to hide drift.

For natural-layout revisions, author per-room activity briefs and target positions
in activity-layouts.json. Clearance resolution is subordinate to those intentions,
not a substitute for them. Reserve pending furniture while settling larger objects
so an unsuccessful later move can safely keep its original position. Review every
rotation, host-relative mat, route and stateful layout after regrouping.

Color consistency means shared construction and highlight restraint with distinct
department finishes. Review all selected source registrations on native floors and
record decisions; do not normalize unrelated departments to one numeric brightness.
Crew Hab autumn sources now match the approved lounge fabric reference.

Room Layout Studio authoring: local user://room_layouts.json overrides are applied
after authored full-wall placement. Preserve the owner's layout file. Tests must
redirect the store to isolated output. Verify drag/save/reload against actual
runtime footprints, reset and independent rotations; previews alone are not
persistence evidence. Fixed baked slices remain locked and local edits do not
silently rewrite source art or static cards.

### Room studio surface edits

The studio exposes actual rotated door bays and approach lanes, and separate
prop, floor-panel and floor-decoration layers. Floor drags swap panels to retain
coverage. Namespaced tile/ and decor/ overrides share the existing local layout
save and undo history. Include these overrides in floor-decoration cache signatures;
otherwise preview and runtime can reuse stale placements. Test drag, undo, disk
reload and runtime resolution with an isolated save path. Baked wall art and
host-attached mats remain fixed/host-driven; do not imply all pixels are objects.

Saved draft review: read the absolute user layout path reported by
`tools/review_saved_room_layouts.gd`. Save alone is not approval to adopt a draft.
After the owner chooses adoption, use `--promote=asset/quarter` to validate and
write one entry to `rooms/full-wall-v1/default-layouts.json`; inspect the native
result and source diff. Preserve local drafts and unrelated default entries.
Studio Reset must restore adopted defaults; local changes take precedence.

North-wall preview lesson: include the existing raised rear wall and foundation when judging height; interior-only cards omit this context. The owner removed the extra bright Listening Post installation in favor of its original U-console. Sealed-north full-wall sprites now lift 22 units visually into the low crown, independently of ground footprints. Validate the extended visual envelope and door lanes separately. See docs/ROOM_ARCHITECTURE_2026-09-08.md.

Studio unused-art library: discover the registered full-wall JSON sources, preserve
polygon cutouts and texture registration in runtime props, and identify additions
with stable library/ keys. Unused means absent from the selected room/rotation.
Insertion, removal (including null tombstones for adopted additions), undo, reload,
and repeated runtime application must preserve identity without duplicating props.
Never test against owner saves. Raw source images do not belong in the placement
library until they have renderable registration and clear footprint bounds.

Riser end treatment: determine adjacency from actual exposed raised-wall eligibility, not just side occupancy. Continue the room�s own vertical wall material up exposed ends; omit the return beside an adjoining riser. Use registered hull and fitting sprites for the raised face. Native fixtures must explicitly enable raised walls after scene settings load; defaults currently hide them.

Riser composition follow-up: use department-specific mount layouts rather than repeating one panoramic window and paired accessories everywhere. Fit windows without stretching; secure spaces can use panels instead of glazing. Review all non-corridor consumers, including rooms outside the full-wall installation manifest.

Corner seam lesson: room-specific wall and cap sprites can have transparent bevels and different vertical offsets. Back exposed returns continuously and overlap the low corner; checking rectangle endpoints alone misses visible holes. Compare background pixels in native corner strips, retaining the previous gapped images as a negative control.

Catalog audits: inspect all four room orientations, not only q0 cards. Pressure Control and Listening Post retain accepted baked installations at q0 but use inherited registered equipment elsewhere. Record this directional identity gap without restoring rejected bright replacements. See docs/ROOM_WALL_ASSET_AUDIT_2026-09-08.md and its native capture tools.


Vertical completion follow-up (September 8): all fifteen catalog installations now have west/east registrations. The six new pairs are in assets/side-wall-completion-v1; Pressure and Listening references come from the retained originals. Research checkerboard registration uses reviewed neutral minimum 210. Record threshold and source hash; polygon exclusion is not alpha transparency. Isolate RoomLayoutStore.path before adding native fixture views. Preserve personal files and distinguish draft acceptance from authored layout checks. See docs/SIDE_WALL_COMPLETION_2026-09-08.md for twelve-variant, full-wall and production-route evidence.

Current floor replacement: live details use rooms/floor-profiles-v1/modern_details.gd and modern-details.json to map stable legacy placement IDs to style-v2 art. Preserve saved IDs and aspect-fit mount bounds. Run audit_floor_detail_anchors.gd with owner drafts excluded; September 8 replacement passes 320 placements with zero missing hosts. Keep accepted pressure/listening installations and resolve their floor hosts against actual native props.


Inward-facing correction: a vertical backing is not evidence that its appliances face inward. Inspect every screen, hatch, drawer, eyepiece, glove and handwheel. Operator faces belong along the inner long edge; short ends can be closed caps. Foreshorten side-facing panels and use top housings/skylights rather than keeping south-facing front rectangles. Preserve functional details during targeted edits: an eyepiece correction accidentally changed a glove into a tube and required repair. Judge darker source revisions on actual native floors. Selected sources: assets/side-wall-inward-v2; evidence: docs/SIDE_WALL_INWARD_2026-09-08.md.

South-bank completion: retain accepted q0 U-shaped artwork independently from q2 registrations. Load optional side-<asset>-south.json for q2 without applying the narrow west/east footprint rule. Check all four orientations and idle/working states. Neutral registration must seed actual image corners; generated dimensions can differ from requested dimensions. Capture cards natively with enough margin for raised walls AND foundation feet; isolate owner drafts. See docs/RARE_DIRECTIONAL_COMPLETION_2026-09-08.md.

Station operating-effects lesson: review catalog adjacency at normal zoom separately from reciprocal crew routes. Wait for zoom/layout settlement before focusing captures. Use visual-bounds-relative instrument anchors for each authored directional view, with the existing operating flag and owning game clock. Test rendered offline stability and actual pause/resume pixels. Only split base/effect drawing when the inherited view supports those methods; registered-only views must retain their registered draw path. See docs/STATION_COMPOSITION_PASS_2026-09-08.md.

Observation-library lesson (September 8): owner rejected rounded U-installation corners in favor of straight backing and small square bevels. Keep the porthole round while squaring the furniture silhouette. Register the unchanged RGB source as north/west/east polygon pieces with separate ground footprints; native rendering removes the checkerboard without repainting glass. Observation V2 passes south-entry collision and a 168-sample production-controller return route. Its current blueprint is fixed north-facing; this is not directional-art acceptance for four rotations. See rooms/underwater/observation-room-v1/README.md.

September 8 Studio correction supersedes the earlier q2-only south-bank rule: select optional south registrations from the actual mounting wall, not quarter number alone. Preserve stable prop IDs and owner files when making baked regions movable; test visible bounds as well as saved positions. Repeated runtime library application must retain directional replacements of native props. Repainted crane apertures need seeds selected on the new source; old seed positions can land on artwork and silently retain white openings. Native review caught this after a source-only material pass. See docs/STUDIO_OWNER_NOTES_2026-09-08.md.

Corner furniture pilot: a flush northwest asset uses the west inner wall x=-184 but the north riser base y=-192; equal x/y offsets leave a visible north gap. Preserve the deep transparent inner notch and short arms clear of both door approaches. The first BRINE console is a 128-unit-wide NW library asset, with source/export and static Studio clearance evidence in assets/brine-corner-service-v1. Keep corner orientation and conservative rectangular collision limitations explicit; do not count static fit as crew-route acceptance.

BRINE NE companion, September 8: use distinct machinery rather than mirrored equipment. The 128-unit bank fits at (56,-192) only after replacing the old dual workstation in the review fixture. Tray availability does not imply automatic safe placement. The riser samples the upper service face separately from the cap; exclude tall lower cabinetry. The stray tube projection was a floor alignment decal: remove its owning layer.

Door polish, September 8: register separate low and raised pressure-door skins; clip rigid leaves at pocket mouths rather than scaling details during travel. Share finishes with BRINE default sockets and both airlock hatches. Cosmetic wet-closing history follows actual aperture, clears on restart/Continue, and holds on pause; no crossing foam remains at zero aperture. Skip dry pairs before added door lookups. Review normal-size station captures as well as enlarged atlas frames.
