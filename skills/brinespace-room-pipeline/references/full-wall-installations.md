> Current owner decision: [top-down and inward-facing contract](top-down-owner-contract.md) supersedes conflicting historical camera guidance below. Read it before production or handoff.

# Full-wall installations: September 8 production lessons

## September 12 owner camera clarification

East/west installations may be flush to their wall; every embedded appliance and
access face must face the room center. North installations are flush and inward,
with slight riser overlap when overheight. South installations face inward but
are viewed top-down, not as tall rear elevations. Use a source as material/subject
reference separately from its camera: a faithful rear repaint can still fail this
contract. Judge the top surfaces and inward access at native room scale.

The owner accepted the Tidal overhead pilot. For subsequent banks, use it as a
camera reference separately from the room's subject/material source. Check each
pump end, tool grip and vise handle; an overhead outline can conceal outward
working faces. Preserve the previous placement-frame ratio when a shallower
silhouette changes collision-driven furnishing fallback (Maintenance, September
12): add blank registration space above the silhouette, not stretched pixels.
Compare the complete room before/after to catch reappearing original props.

For complete-catalog work, keep a room-by-direction ledger reconciled with the
native RoomDatabase catalog. A missing full-wall JSON may be a split/custom host;
inspect that consumer before declaring a missing asset. New library registration,
isolated host preview and default-layout installation are separate stages.
When a directional edit fails, inspect the actual latch/tool before retrying;
never claim that a requested rotation happened because nearby details changed.
An intentional removal must be recorded as a composition change.

Check new default placement in both actual room captures and route fixtures.
Shield's fixture explicitly applied room defaults while its view rebuilt family
art afterward; route success did not prove the selected bank rendered. Catalog
captures now record variant_source, rect and visual_bounds. Inspect those values
and the PNG. Default layouts use catalog room keys, not uncatalogued family keys.
Move floor units clear of actual door lanes, not merely clear of the new bank.

For custom rooms, inspect the fixed_rotation database rule before claiming four
native rotations. Cold Store's side family retains stable fridge/rack IDs and the
powered indicator while replacing source appearance. Register actual new aspect
ratios and set wall contact from the resulting world width; equal lengths do not
imply equal widths. Inspect each crate handle after shelf-facing corrections.
When q0 changes, rebake the card and update every active binding before closeout.

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


Galley overhead lesson (September 12): a correct counter camera can still contain
sideways customer-facing details. Check mug handles, spoon grips and dispensing
taps individually. The first Galley candidate passed the camera gate but failed
those details; a focused second generation corrected them. Preserve source and
prompts for both. For a fixed-orientation custom host, report q0 native evidence
honestly; do not describe four source variants as four playable rotations.


Salvage companion lesson (September 12): distinguish fixed floor totes from carried
versions; a top-down floor source need not replace the carried elevation. A room
with a south doorway cannot adopt a continuous full-width south bank merely
because that source now exists. Keep library-render, valid wall-fit and default
installation stages separate. Enclosed carrying-handle holes require explicit
source-space aperture seeds; dark bores over solid tray bottoms remain opaque.


Observation shelf lesson (September 12): a tall narrow source may still be a
frontal bookshelf stacked down the image. Review book axes, display top planes
and inward handles, not aspect ratio. Opposite side companions can share material
and construction without duplicating display objects. In custom multi-part hosts,
check both prop_visual_bounds and draw_registered_prop library paths; supporting
only the former does not make a registered replacement render correctly. When
moving the retained north section, move its collision footprint with its art and
rejoin side lengths. Recheck native joins and route clearance.


Owner-directed wall replacement: Observation uses its installation upper artwork
in place of the generic riser. Align source top to the wall-top coordinate and
suppress the separate riser in the shared renderer, rather than painting over it
in a card. Preserve the original source; extend adjoining banks at source aspect
and verify native joins, footprint clearance and refreshed card. This exception
is room-specific and supersedes only Observation earlier overlap treatment.


Turbine perspective lesson (September 12): a new overhead housing changes the
visible rotor aperture. Reusing front-view rotation strokes paints motion across
the casing. Derive a compressed ellipse within the intake and relocate the live
lamp to the new control panel. Scope sealed-wall selection by actual orientation;
retain passage-facing layouts and compare their native RGB output for parity.


Current Turbine owner correction (September 12): the machine belongs on the wall
pointed to by the intake arrow, not an arbitrary sealed wall. q0 north, q1 east,
q2 south, q3 west. New side companions face inward; north retains original front
view and south overhead. Keep arrow visible ahead of the machine and relocate
the console clear of the bank. Four native bounds match their target wall and
176 routes pass. This supersedes the prior q0/q2 south selection.


Stateful library lesson (September 12): a custom room draw method can exist yet
never run because nursery_whole_view dispatches library assets directly. Power
machines explicitly opt into custom_library_draw. Verify OFF plus two powered
timestamps, and compare within machine bounds so unrelated console motion cannot
satisfy the check. Preserve the initial failed evidence. A cross-door room needs
an interior machinery footprint; do not force a full bank onto an open wall.


Refrigeration state check: crop or localize powered differences to the intended
indicator, and compare offline output with the retained card. A 2x2 native change
is sufficient for a restrained status lamp when its location and time dependence
are verified; do not enlarge effects just to make a full-room difference obvious.


Airlock storage lesson (September 12): general door-route checks do not validate
functional handoffs. South storage trial passed176 routes but failed the existing
east-facing locker interaction (rect.left-28, rect.bottom+6), which leaves the
room when a bank sits flush south. Restore working placement until a compatible
service anchor and removable helmet rendering are authored. Preserve candidate
source separately; a baked spare helmet cannot satisfy grasp/release visibility.


Research selection lesson (September 12): a replaced directional registration may
produce no native pixel change because authored defaults select a different
library direction and tombstone the family prop. Inspect actual runtime prop IDs
before declaring integration. Correct source orientation and selected placement
separately; preserve the old placement frame and verify unaffected rotations.


Containment overhead review: check each canister catch independently of its round
lid and inspect forceps blunt grip versus pointed ends. Preserve closed sample
state; changing camera does not authorize opening containment or inventing contents.

Anomaly footprint lesson: adding wall_contact changes collision from a shallow
rear strip to the whole overhead bank. Automatic relocation can silently omit an
independent functional prop even when general routes pass. Compare runtime prop
IDs and native pixels before/after; retain the specimen platform explicitly and
verify its clearance. A route pass alone does not prove equipment preservation.

Radio control review: visible screens alone do not establish inward operation.
For the overhead south view, put console pushbutton rows nearest the room edge,
with the tuning surface oriented to an operator above the image. Review clipboard
clip and headset pickup direction separately; cable exits stay on the outer rail.
For rooms with two sealed opposite walls, source existence does not guarantee any
rotation selects that direction. Test the selected south view without applying
the north riser offset, and retain separate live signal equipment.

Use `python tools/compare_room_art.py <before-capture-dir> <after-capture-dir>
--out <report.json>` after native catalog capture. It compares RGB pixels, prop
inventory and placement for each room/quarter. Inspect added props as well as
missing props: a smaller source can free enough space for automatic placement to
restore an unwanted duplicate reservoir. Compare the rejected and final captures
to demonstrate the check catches the actual problem. Native visual review still
decides facing, material quality and whether an inventory change is appropriate.

Isolation state review: preserve whether the observation chamber is closed and
empty independently of its camera angle. Name supply counts in the brief and check
them in the image. Inward service release catches and outward hinges distinguish
operation side without opening the chamber; tube pickup ends face the room too.

Listening console review: a keyboard on the inward edge can still face outward.
Check the spacebar is nearest the operator independently of keyboard placement.
Author dim screen markings and leave room for engine-owned sonar motion. After
changing the display geometry, localize OFF/two-time image differences to the
new disc; unrelated receiver animation cannot prove the sonar anchor is correct.

Gravity Loom split-bank lesson: on a four-door room, author short finished-end
stations beside the entrance rather than a continuous bank across it. A matched
pair can share one source sheet, but each needs independent silhouette, pivot,
display width and collision footprint. Register disconnected pieces separately;
never use the pair's enclosing rectangle as a single blocker. Preserve central
apparatus pixels and compare all rotations; rebake the card when q0 changes.

Reactor short-service lesson: select the free half of a doorway wall from actual
runtime machinery bounds in each rotation. A shared overhead module can stay on
the south wall while moving to its other clear section; do not mirror its controls
or rotate the raster. Preserve existing machinery rather than crowding it into a
symmetrical layout. Compare every rotation and update all card bindings together.

BRINE Core review: default catalog captures can omit the occupied architect pod.
Capture the occupied state and check each rotated pod footprint before adding
south stations. Keep recovery tests separate from generic door routes. Review
reader insertion slots as well as release catches: both must face the operator.
Inventory existing corner registrations before classifying a missing ledger entry
as missing art; recording existing coverage avoids unnecessary duplicate banks.

Split-family inventory: inspect `split-<family>.json` and registrations named
`<family>-<direction>-<section>.json`; a search limited to `side-<family>-south`
misses existing split banks. Record all section sources and leave their review
status pending until checked. Hydroponics service review distinguishes removable
canister caps (inward) from fixed hose fittings (outer backing); preserve crop
growth stages and proportional registration frames independently of the repair.

Life Support overhead review: closed filter cartridges may appear as circular
access lids from above instead of long cylinder elevations. Preserve the count
and service function, place catches inward and fixed hoses outward, and describe
the result as a companion camera design rather than a pixel-identical reconstruction.


Battery south review: distinguish exposed tall access elevations from closed overhead lids. Preserve four cell modules and three distribution units; put release handles and disconnect controls on the inward edge and fixed cable runs outside. A shorter visible silhouette can retain the original proportional registration frame without stretching the source; compare inventory, placement bounds and native pixels independently.


Archive keyboard lesson: inspect asymmetric key layout at source scale as well as keyboard position at game scale. The inward keyboard edge must contain the spacebar. Check reader access separately; an outward protruding release can survive an otherwise overhead design. Keep cartridge counts and original split frames while correcting local service cues.


Retained-art review is a valid catalog outcome: Storage Bay already has overhead closed cargo with inward handles and inventory controls. Verify source hashes, selected native bank, doorway gap and separate equipment, then record reviewed-retained without generating a duplicate. For paired Command consoles, inspect BOTH spacebars and secondary screen button rows independently. A direction repair can worsen material gloss; preserve the rejected candidate and correct bronze/red sheen before integration. Validate powered motion in each changed display crop rather than using unrelated room animation as evidence.


Holographic bank lesson: a static optical bank must not imply an active projection through baked luminous rings or white screen nodes. Preserve faint idle markings and lens counts; engine-owned projector/calibrator supply motion. Check their OFF/two-time differences in separate crops and verify static banks remain invariant. An inward keyboard also requires its top-edge spacebar, and twin-lens device handles need independent access review.


Refinery companion lesson: inspect actual rotation-to-wall selection. A north/south-open layout can select side art while BOTH horizontal rotations reuse north art on sealed walls; adding a south file then changes no pixels. Explicitly select the intended south rotation and update authored positions with preserved equipment IDs/sizes. For ore processing, retain left-to-right hopper/drum/output flow under the new overhead camera; separate live crusher/hopper remain independent. Compare all rotations and distinguish source registration from live selection.


North split-bank seating: a correct inward source can still float below the riser. The optional split specification north_art_offset moves only artwork; split drawing and inherited visual bounds must use the same offset while rect stays on the floor. Battery uses -22, other families default to zero pending individual review. Compare unchanged collision rectangles and side/south RGB, then rebake q0 card and all bindings.


Hydroponics full-direction review: crop channels do not have an obvious operator face, so inspect the companion gauges, service caps and access panel to establish inward orientation. Preserve mature-versus-seedling distinction. North riser seating can use the opt-in art offset after per-room review; compare every collision rectangle and the three unchanged rotations, then verify the refreshed card against the reviewed native image.


Life Support direction review: distinguish fixed pipe ends from filter service ends, and fan controls from symmetric fan blades. Follow registration source paths: this family uses material-polish-v2, not the earlier rollout naming convention. Confirm source hashes before retaining art. Review the north riser offset and refreshed card separately; unchanged collision and other rotations do not alone prove visual fit.


Storage direction review: inspect strap-release buckles as well as crate handles; a closed box alone has ambiguous service direction. Retain directional cargo arrangements that provide inward access rather than flattening every view into an identical stack. North riser seating must preserve the free lift, freestanding crates and their collision footprints, with separate native/card review.


Archive side review: distinguish compact keypads from full keyboards; spacebar orientation applies only to a keyboard that has one. Cartridge pull ends identify access more clearly than symmetric closed panels. Preserve the independent library/terminal while seating north art, and retain existing source designs when their service direction already reads correctly.


Command north seating: material and direction gates are independent. An inward keyboard can coexist with excessive brass/red gloss. Revise materials without changing key arrangement, then preserve proportional source frames and floor rectangles. Powered anchors derived from visual bounds should follow north_art_offset; prove this with separate OFF/two-time crops for each display after moving the art. Keep uncorrected companion material reviews pending.


Four-panel side-sheet registration: group disconnected polygons by both source X and Y quadrant, not just left/right. Each operations/comms panel needs its own preserved proportional frame. Compare q1/q3 inventory and bounds, prove q0/q2 unchanged, and isolate each animated display in both side views. Material-only work can preserve anchors, but source similarity does not prove that automatically.


Holographic north seating can free enough visible floor for automatic relocation of the independent calibrator. Compare ALL prop rectangles after an art-only offset. Preserve the established station in the room view when the family lacks an editor-catalog key; validate layout keys before keeping a draft. Keep rejected relocation evidence and prove final state geometry matches any reused powered capture. Review static idle markings independently from the live projector/calibrator.


Biodome overhead companion: preserve ecosystem zones rather than replacing mixed ferns/tree canopy with uniform crop rows. Keep closed aquatic habitat and nutrient-dispenser count, with inward service caps and outer irrigation. Do not bake falling spray into the static bank. When installing on the opposite sealed wall, retain independent tree/aquatic stations at their original sizes and validate their localized operating effects after relocation.


Run tools/audit_room_facing_coverage.py --out <report.json> at catalog milestones. It checks recorded registration existence, PNG signatures, source hashes, declared-source agreement and direct evidence files. Link capture runtime.json explicitly. For split families, avoid retaining a generic base registration as the north selection after the two section sources change. A clean audit proves ledger consistency only: unregistered directions may be custom architecture, while absent evidence links can refer to work recorded elsewhere. Do not convert either count directly into missing-art or completion totals.


Medical records overhead banks need consistent operator cues: south spacebar and storage catches toward the room, clipboard clip and handset cord away. Remove outer base pulls rather than allowing contradictory access cues. Review exact keyboard geometry after each edit. On switching sealed walls, compare station IDs as well as collision: automatic placement can silently exchange the live exam station for a desk. Preserve exam, consultation and records at original sizes; verify the relocated exam monitor with localized off/on and temporal captures.


North medical desk checks: operator is below the art, so keyboard spacebar belongs on the bottom row and clipboard clip on the far top edge. A keyboard-shaped key grid without a spacebar is not proof of orientation. Keep standby consultation icons free of active-call waves in static art. Preserve proportional registration and compare all bounds to avoid moving stations during this source-only repair. Side banks require their own document and storage access review; inward keypad placement alone does not establish every prop faces inward.


Side records-bank access audit: keypads alone are insufficient. Review clipboard clip, paper ruling, folder grip ends, cabinet pulls and hinges as a coherent operator direction. West means operator right; east means operator left. Outward clips need sideways paper markings, while folder grips and pulls stay inward and hinges outward. Retain counts and closed storage. A source edit that changes the card rotation requires a new card and all three bindings even when floor geometry is unchanged.


Med Center south bank: distinguish inner catches from outer hinges in a closed clear-lid instrument tray; identical latch-like fittings on both edges make access ambiguous. Keep carry handle and release catches inward, continuous hinge outward. Check the small supply case separately. Preserve nine capped sample pots, three cartridge releases and fixed outer hoses. Static diagnostic art stays in quiet standby; validate relocated treatment/imaging effects separately from the decorative bank.


For cartridge banks, review replaceable release ends separately from fixed hose ends. North access releases point down and fixed hoses sit up; west/east cartridges can become horizontal stacked rows so access points inward. Preserve cartridge count. Side keyboards need an explicit vertical spacebar in the inward column. After removing active traces, inspect for residual tiny spikes at native scale; a broad cleanup prompt may leave them. Preserve original proportional frames and verify all prop bounds plus unaffected rotations.


Cryo south machinery: keep control/release ends inward and fixed insulated manifold outward. Distinguish coolant-vessel latches from central caps; remove outward sample-holder pull slots. Preserve blueprint pod count and per-pod authored scale. An opposite-wall bank can resurrect a redundant console; compare IDs and use the valid family/quarter tombstone to preserve the accepted inventory. Update authored positions without changing recovery cache/bypass logic. Compare cached and uncached native blueprint views and run recovery gameplay checks, stating each scope separately.


Cryo side repairs must preserve TWO sample cylinders per side source (north/south have their own counts). A generated access handle can silently replace a cylinder. Check both catch positions on paired vessels rather than accepting bilateral symmetry: every west-bank catch faces right, every east-bank catch faces left. Preserve optional mounting metadata, including its absence; do not add wall_contact just because newer families use it. Failed registration attempts must not make their incidental captures the selected evidence.


Construction south banks need tool shanks/grips facing inward, not merely a relocated storage cabinet. Check each drawer catch after moving the drawer row; a top-row drawer can retain a bottom-facing pull. Preserve six drills, five holders, four drawers, two spools and four-clamp/two-head fixture inventory. For fleet rooms, retain independent drone/cradle and hatch props and test docked/deployed renders: disappearance of the vehicle and opening of the hatch must remain localized while static bank and bench stay unchanged. Pair this visual check with the drone lifecycle suite.


Review mounting and facing separately. Construction CNC access and Salvage control/tool cabinet faces already pointed inward, but absent wall_contact left a10-unit wall gap in both families. Preserve Salvage motor/pipe/plate sorting streams while checking the exposed inward cabinet face. Preserve the valid raster and add explicit mounting only after native evidence establishes the gap. Verify the exact side-only translation, unchanged dimensions, all independent fleet props and unaffected north/south views. This is a geometry correction, not new art; record retained-source acceptance separately from authored companions.


Salvage overhead banks retain three distinct sorting streams: motor parts, pipe couplings and flat plates. Do not homogenize them into generic scrap. Review portable toolbox catches separately from its surface handle; a correct handle does not establish opening direction. Twelve closed parts lids, diagnostic controls and hand-tool grips must all face inward. For relocated fleet rooms, deployment and equipment operation are different checks: verify empty cradle/open hatch and the independent winch control animation locally.


Mining overhead service banks: distinguish the fixed service robot from the independent fleet drone. For south, claws and service eye face up, hoist/reel remain at the outer bottom, and battery releases appear only on inward ends. Remove contradictory outer catches even when the main silhouette is correct. Preserve three packs, four robot cylinders, two claws, three drawers and three drill bits. Keep authored independent equipment scale factors; automatic placement can resurrect a tether, so compare exact inventory and suppress unintended additions. Verify deployed cradle and hatch separately from static bank art.


Mining side review: a blank gantry and downward-facing drawer fronts are not equivalent to the north service station. Side companions must preserve the fixed service mechanism, with claws and cabinet drawer faces pointing inward sideways. Review full source inventory as well as runtime prop IDs: baked equipment cannot be counted by a prop manifest. Preserve proportional frames and compare all four runtime rectangles. Refresh q0 card after changing west art. Existing authored pairs remain supported; follow the owner-approved single-side mirror workflow for genuinely new asset families.


Biomass retained-art review: symmetrical vessel lids do not by themselves establish facing. Check the location of service controls, hopper access and generator interface against the inward wall edge. Existing side controls and overhead south controls can be retained when native fit agrees. Validate operating lamp anchors against each directional source with off/on and temporal crops; preserve the functioning bank replacement rather than restoring a duplicate power_machine. No new raster is required when all these gates pass.


Thermal side banks: count baked subassemblies against the north inventory, not just runtime props. A side silhouette can silently reduce four vent panels to three and two pumps to one. Require visually separate vents and pump covers; reject count-preserving failures before registration. Preserve proportional frames, then check wall seating independently. Source-only bounds parity and subsequent 10-unit wall translation are distinct evidence.


Thermal operating review: the fitted bank is static while the independent thermal_monitor owns live bars. Prove monitor-local off/on and temporal differences in all rotations, and confirm bank/pump crops remain unchanged. Do not add animation to static bank graphics merely because the room operates; preserve the existing division of functional props.


Tidal side filters: rotate cartridge bodies as well as valve access. Three horizontal cartridges stacked vertically put release knobs/taps on the inward end; remove extra bottom spigots introduced during editing. Require three distinguishable coil return bends, not ambiguous overlapping pipes. Keep independent pump and monitor live effects; verify both with localized off/on and temporal crops in every orientation while fitted bank stays static.


Maintenance idle-source review: running wash streams and lit task lamps can survive otherwise correct cabinet facing. Remove these baked active effects without removing the nozzle, lamp or machine parts. Preserve source frame proportions and verify all rotation bounds plus unchanged companion renders. Independent repair/diagnostics effects need a separate state check; an idle-source correction does not prove them.


Maintenance side access: repaint actual cabinet faces and vise geometry toward the interior; merely relocating a downward-facing strip leaves the problem intact. Inventory audit must include both toolbox and cable reel per side, since older paired art can lose different items. Preserve runtime rectangles through proportional registration, inspect the resulting smaller projected silhouette natively, and verify independent diagnostics in every rotation. Existing side pairs need not replace accepted north/south art.


Pressure Control keeps its custom three-piece q0 fitted installation; a generic north registration exists but is not selected. Record the actual source and implementation in coverage rather than crediting the unused registration. Side dial animation must pivot on the painted hub: retained pressure-sides source hubs are approximately (530,443) and (1007,443). Derive normalized anchors from registration frames, then verify local off/on and temporal movement after wall seating.


Quarantine south: a registration filename does not establish matching equipment or runtime selection. The former south source substituted alien terrariums and q2 still selected north. Author the actual six-tube, three-canister, three-case inventory; keyboard spacebar, gauges and case releases go inward/top, hinges/plumbing outward/bottom. Opt into the intended sealed-wall rotation and preserve berth/filter/monitor at original sizes; prove filter and monitor state effects after relocation.


Quarantine keyboard corrections can regress the companion panel. Inspect both keyboards after every edit. When one candidate has the valid west panel and another the valid east panel, select each through separate source registrations; preserve the full originals and exclude invalid panels geometrically instead of repainting pixels. Cases need inward catches and outward hinges, not merely an inward cabinet handle. Keep three gauges with three canisters and remove baked heartbeat/alarm emission from idle banks.


Crew Hab access gate: inward-facing storage is not sufficient if it blocks the berth opening. Require open long-side entry above mattress height and drawers below mattress, with shelf inventory retained. Reject edits that delete drawers or move them into a tall wall beside the sleeper. After repeated structural drift, restart composition from the original open berth rather than chaining edits of the obstruction. Rejected candidates are not integrated or counted as coverage.


Crew Hab fresh-composition recovery: using the horizontal berth only for furnishings/style produced an open side berth after repeated obstructed pair edits. Keep the mattress long edge visible, locate recessed storage access on the thin inward base edge, and give the bedside drawer its own inward pull. Review at native scale before copying the composition to the other side. Preserve old directional bindings until each replacement passes; do not invoke new-family mirroring to retire existing authored pairs.


Crew Hab companion verification: use the reviewed open-entry side as the next reference and preserve shelf counts explicitly. A newly authored opposite side can retain the same runtime frame despite different raster dimensions; validate all prop rectangles and unchanged companion renders. Warm reading light is part of the established hab atmosphere, while the independent desk carries the operating display. Verify the latter without rewriting ambient berth lighting.


## Research inventory correction - September 12, 2026

Pair edits may restore one missing instrument while duplicating a nearby tray.
Count individual tubes, trays and tools in each panel after every edit; a request
for an exact count is not evidence it happened. Research side studies v1/v2
remain rejected for three upper tubes and duplicate west tools. North idle
screen repair was independently integrated after native review with unchanged
rectangles and unchanged other rotations. Preserve tinted glass and sample
material; remove baked operating graphics without erasing instrument detail.


Research side recovery: isolate a single bank after pair edits repeat inventory
drift. Remove a duplicate inset by its exact neighbors and specify the resulting
plain worktop; broad requests to preserve the bank can preserve the defect.
Use a single visible row for counted tubes: overlapping caps are ambiguous.
Selected west/east retain four upper tubes, two lower tubes and one tool tray.
A wall_contact flag does not prove a translation: authored defaults can override
automatic placement. Compare actual rectangles and native art before claiming
a gap was closed. Research rectangles remain unchanged; scanner animation was
verified separately in all four rotations.


Clone Lab side repair: verify workstation geometry as well as the chamber
release. A moved handle does not turn a downward-facing cabinet or monitor.
Require the monitor plane, keyboard approach and cabinet doors along the inward
long side. Check transport-case catches and centrifuge releases separately.
Restore both microscope and monitor in each companion; preserve sample storage.
A plain end may retain a viewing window while service doors open inward.
Native scale review must judge the broader workstation end after proportional
registration. Clone defaults preserve all rectangles, and console/nutrient
effects were checked independently in all four rotations.


Ore Refinery review: a white exterior request can incorrectly whiten machine
frames and piping. Reject palette drift; keep the original dark charcoal/orange
reference as the material authority while cleaning the exterior. Specify idle
lamps and ingots separately from orange paint and hazard-yellow markings.
Process flow can remain along the wall while loading gates, service releases
and collection access face inward. Audit outer drawers after central controls
are corrected. Read actual rotation mapping: Refinery west is q0, north q1,
east q2, south q3. Its q0 card therefore follows the west repair.


Biodome side review: preserve living inventory and foliage density while turning
aquarium viewing/service glass toward the inward long edge. Nutrient canister
caps alone do not establish access; retain three caps and visible inward valve
controls. Remove baked irrigation spray without deleting nozzles or aquarium
water. Check tiny cyan remnants after edits. Proportional registration preserves
size; explicit wall contact closed the side banks' 10-unit gap. Verify tree and
aquatic/processor effects independently, rather than treating static planted
wall art as evidence of functioning-room animation.


Xeno Lab review: retain already-correct inward glove and microscope geometry.
Idle-screen cleanup must distinguish powered graphics from painted warning
emblems; restore static markings if generation erases them. Preserve translucent
fluid, specimen color and fine coral branches while reducing device emission.
Check fitted-bank static state separately from scanner, workbench, vessel and
sample effects. A mount flag can change without moving saved rectangles; Xeno
keeps all placements and independent visual bounds unchanged.


Bio Lab repair: count culture trays in each view; side banks had three against
the four-tray north reference. Restore four visibly separated trays and put
controls beside the inward access handle, away from outer pipes. For persistent
down-facing drawers, explicitly permit the lower cabinet outline to expose an
inward side face; otherwise an edit may move pulls without changing perspective.
Review autoclave lid catches and microscope eyepieces separately. Preserve
bench tools and blue storage bottles, then verify native size and independent
centrifuge/cold-storage state effects. Bio placements remain unchanged.


Anomaly Lab review: a correctly inward-facing bank can still omit a specimen
tube. Compare discrete rack inventory with the north reference; restore three
tubes without covering the dish or microscope. Keep valid containment geometry
and avoid unnecessary source repainting. Native review retained north, side
wall contact closed a 10-unit gap, and the unchanged q0 needed no new card.
Verify diagnostics, capacitors, receiver and platform state effects separately
from the static fitted bank.


Owner side-view feedback (September 12): correct wall placement and inward access do not establish a satisfying side silhouette. Review focal machinery recognition at gameplay scale, including whether the identifying rotor or working face remains readable. The owner reported disliking side views; exact affected asset and reason remain unconfirmed. Do not silently treat a technical pass as owner acceptance or propagate the questioned design across the catalog. Preserve directional placement while developing a reviewable art correction after the target is established.


Med Bay mounting regression: adding west wall_contact changed pre-default auto-placement and swapped the independent console for a second bed, even though the saved bank rectangle stayed unchanged. Removing that flag restored the original inventory without moving any final rectangle. Compare actual IDs in every rotation before claiming placement preservation; invalidate operating evidence when its prop inventory differs from the corrected revision.


Cold Store directional scope: fixed north-south doors prevent continuous end-wall banks. Create missing equipment companions separately while preserving the live through-aisle. For a south-wall refrigerator, the roof and rear casing dominate; front food windows are legitimately occluded and should not be invented on the back. Source-facing correctness still requires native footprint and projected-depth review. Uninstalled studies are not completed directional coverage.


Cold Store north/south companion review: a steeper lid angle alone does not make a rear overhead view if every shelf remains exposed. Require the opaque upper shelf to occlude lower tiers and use a compact footprint; hidden inventory is not missing inventory. Preserve separate north front sources with alpha registration and register generated south sources without raster edits. Review all companions at the same intended world width. Fixed-rotation rooms can gain reusable library companions while their playable layout and card remain pixel-identical; describe that scope explicitly.


Radio north idle repair: identify glass-covered physical mechanisms separately from electronic screen graphics. Remove the left waveform but preserve the right tuning reel, painted dial ticks, red plastic buttons and small owner-sized headset. Count the four patch sockets/cables after editing. Verify separate receiver/listener operating effects and untouched rotation parity; do not claim hull-riser screens were changed when only the fitted bank source was repaired.


Mycelium idle repair: generation may reinterpret removed water streams as solid plumbing. Require dry nozzle air gaps and compare against the original geometry before selecting. Keep calm trough water and mushroom species groups. A fitted layout may remove the original rack/reservoir targeted by irrigation code; zero state differences are an unresolved effect-wiring finding, not proof of successful operating verification. Record that remaining work explicitly.


Mycelium effect wiring: target surviving bench/filter props and explicitly classify them as animated for retained rendering. Split static base and effects so cached source art does not freeze operating cues; preserve original rack/reservoir effects for alternate layouts. North nozzle positions are tied to the selected source registration, not generalized to other facing art. Check inactive RGB parity separately from retained state/temporal captures. A subpixel scan can disappear at particular placements; use a visible one-world-unit line inside the screen and sample distinct scan phases.


Crew Lounge side audit: source-panel order is not wall direction; existing left panel is runtime east and right panel west. Verify registration before changing seating. West lacked the coffee station present in north/east; restoring it also requires the brewing cavity and pot access to face inward, not merely adding a mug. Preserve warm ambient lamps as habitation identity. When a restored lamp extends above the old silhouette, expand the proportional frame width so the full lamp fits; do not crop it to preserve old height. Check unchanged rotations and all prop metadata.


Lounge east follow-up: cup corrections can fail literally even when appliance facing is fixed. Inspect and record the actual selected geometry rather than repeating prompt claims; reject duplicated handles. Register only the repaired panel from its source, preserving the opposite runtime registration. Compare all prop metadata and retained north/south pixels; independently verify the galley display supplies operating feedback while seating stays static.


Isolation north review: preserve analog gauge artwork and hazard paint while quieting emissive lenses. Operating checks must follow actual per-rotation prop IDs: q0 flush_left/flush_right replacements can be static even when q1/q2/q3 battery props animate. A passing family-level state check cannot cover an unchanging orientation; record the missing cue and investigate its own draw path.


Isolation operating follow-up: a static replacement need not inherit unrelated battery animations. Add a small cue to its own authored lamp apertures, classify only the affected bank/orientation as animated, and gate on operating. Keep source-space anchors tied to the selected registration. Verify retained drawing as well as direct preview, with temporal deltas confined to instrument faces and off/untouched-orientation RGB parity.


Turbine side readability study: strict narrow intake prompts can hide the defining rotor at gameplay scale. A broader foreshortened inward-facing opening can reveal blades without putting a frontal fan disk on the roof. Compare a candidate in the same machine rectangle and preserve arrow-wall routing; new source framing can alter apparent silhouette length even when the rectangle is unchanged. Keep aesthetic candidates separate from live registrations until selected, and recheck operating anchors after silhouette changes.


Shield review: quarter number is not a wall name. This room maps q0 west, q1 selected south, q2 east and q3 north; saved variants can override the nominal full-wall direction. Derive coverage from actual runtime side_view/variant_source and inspect the matching image. Retain already-correct art when native fit/material review supports it, and verify independent monitor/injector effects without treating every pass as a repaint requirement.


Heat Recovery north companion: compare material changes at the same world width as the retained south view. Reduce continuous copper highlight stripes while preserving fin density and insulation texture. Pure white source exteriors still need enclosed-loop registration; inspect the native draw because an aperture seed placed on the cable itself leaves a white patch. Add reusable companions without blocking four-door room geometry or implying they replaced its default installation.


Heat Recovery new side family: use one authored east registration with direction=east and the -side suffix, then verify the existing full-wall loader produces a mirrored west registration. Native review must show controls pointing inward on BOTH copies at the same world length. Keep north/south authored separately. Reusable family availability does not authorize wall-spanning placement across the four live doorways; keep the current south skid default.


### Library companions and overridden north views

Listening Post q0 retains a U-shaped source even though a north full-wall registration exists. Resolve actual rendered prop IDs before claiming a north replacement. Review library companions independently at equal world scale, and prove live parity. A quiet library console does not remove baked activity from the retained live source. Printed paper waveforms are ink; preserve them when suppressing electronic emission.


### U-shaped sources split across movable props

A true-alpha reference can return an opaque checkerboard. Verify mode and center-aisle pixels before integration. If a generated neutral-background correction is selected, keep raster bytes and register vector silhouettes; intersect those with each original source region before mapping to movable prop bounds. Preserve the original source frame, including its nonzero origin, to avoid stretching the three sections or closing the aisle. Verify native seams, clear floor and independent movement bounds; compare metadata separately from regenerated art pixels.


### Elevated camera is not sufficient for side-view readability

The turbine elevated-camera study added a large top hatch but retained a tower-like stack. Check construction and floor footprint, not merely visible top faces or inward direction. A wider candidate fit into the unchanged prop aspect can occupy substantially less wall length and lose intake readability. Record actual occupied silhouette at native scale; reject before propagating a weak camera solution to other rooms. See docs/TURBINE_SIDE_REVISION_2026-09-12.md.


### Fixed-room missing directions

Observation has a fixed south doorway, so its south shelf fills library coverage without replacing the entrance. For a south low cabinet, review the far/north access handles, near/south closed backing and top display recesses at native scale. Record actual contents when the generated companion changes counts; do not call a redesigned display an exact rotated reconstruction.


### Low serving-counter side companions

Use the existing serving length as the native-scale reference: Galley side study is 152 units long, not enlarged to make meals readable. Check pot, each tray and every mug independently; inward handles are a useful asymmetric mirror check. Record one authored library item plus a horizontal flip honestly when no full-wall family selects the mirrored view automatically.


### Inspect lower cabinet access separately

Mycelium side repair moved hanging tools inward on the first attempt but left lower cabinet handles facing image-bottom. A focused second edit corrected the access faces. Review each actionable surface rather than approving an inward-looking strip as a whole. Include projecting tools in contain registration, check native scale after the fit, and report floating-point visual-bound differences separately from unchanged placement rectangles.


### Workbench side access

Check the vise screw and T-handle projection as a functional facing cue, independent of the tool rack. Keep operator-side projection inside the registered silhouette. For a narrow enclosed carrying-handle gap, verify the aperture seed's actual pixel: a seed on amber hardware does nothing. Re-render after correction and preserve the source raster.


### Airlock service art is modular

Trace composition texture regions and per-quarter service centers before proposing a continuous wall bank. The pressure chamber rotates independently while frontal furniture may merely relocate. New directional locker art must retain an explicit removable helmet attachment and pass actual approach/handoff checks, not just a screenshot. Distinguish static helmets painted in the source from the runtime removable shelf helmet.


### Check the host drawing branch before library substitution

Airlock's dressing renderer rejects registrations without its dressing flag. A newly registered library bench can render in Studio yet disappear if substituted directly into that host. Inventory the actual draw branch and preserve semantic IDs before integration; isolated library review must remain labeled host-pending until rendering, clearance and crew service checks pass.


### Distinguish furniture containment from hull contact

Airlock's service fixture uses a 180-unit furniture envelope even though hull art reaches 184. Check the host-specific envelope before selecting a side placement. When service checks fail, run the unchanged baseline and compare exact failure classes; record pre-existing failures explicitly and repair any additional failure introduced by the art. A clean delta is not a green end-to-end service result.


### Standable fitting points also need connected routes

Airlock q1/q2 service points fell in wall collision bands; q3 was standable but unreachable through the navigation network. Probe the actual local point, intersecting blockers and route endpoints before changing placement. Keep the source-local handoff attachment and actor scale; move the whole service fixture when necessary. Inspect test loops as well as summary labels: the current Airlock suite covers Bill four rotations and the other two humans q0, not a full actor-by-rotation matrix.


### Upright cylinder side companions

Use visible circular shoulders and foreshortened bodies to establish the overhead camera; count cylinders explicitly and keep manifold against the wall. Check service buckles and hose outlet on the inward edge. Distinguish an authored library direction from its mirrored installed direction, and compare unaffected rotations after host substitution.


### South pressure-bank review

For a south bank, put the manifold on the near/south edge and the securing buckles and hose outlet on the far/north operator edge. Review at existing world width even when the overhead silhouette is shallower than frontal art; do not enlarge it merely to expose detail. Confirm semantic inventory, unaffected rotations and the host's service checks.


South Airlock check benches use an overhead empty slatted seat with access handles along the north/inward edge. Keep the existing service-bay width and verify chamber circulation after replacing a taller frontal sprite; shorter projected depth is expected, not a reason to stretch the source.


Radio side banks: preserve room-scale width and original placement when changing the camera. Show worktop around adjacent low console bays and put service handles on the inward long edge. Dark static screens avoid painted operation signals. Correct facing and unchanged collision bounds do not establish owner acceptance of the camera.


Listening Post side companions separate paper information from electronic operation. Keep chart ink in static art, darken electronic glass, and remeasure sonar hubs against the final registered frame after camera changes. Verify each mirrored-looking authored direction independently: registration padding and hub coordinates can differ. Inward keyboard spacebars and cup handles provide concrete facing cues.

Listening Post owner standardization (September 12): use one Deepwater wall family across all four directions. An exact 180-degree rotation can derive the opposite horizontal wall only after the source passes a strict overhead and inward-control review. If inherited floor machinery clashes through accent color alone, bind a room-specific palette derivative rather than repainting the shared donor atlas. Retain geometry, activity anchors and operating effects, and render all four orientations because removing a baked q0 installation can expose a different underlying prop set.

Xeno containment lesson (September 12): attractive front-elevation containment art can become an impassable-looking floor mass when rotated to side walls. Preserve the functional story in a shallow overhead lid, hatch and work edge, then derive all four registrations from exact quarter turns of one canonical source. Use glove ports and controls as facing evidence. Reject camera failures before spending effort on alpha cleanup; after selection, retain only the reviewed connected silhouette and record removed component counts.

Maintenance wall lesson (September 12): when an accepted south source is already overhead, promote it to the canonical four-direction source rather than generating unrelated companions. Exact rotations keep tool grips, vise access and drawer handles as concrete inward-facing evidence. Mute orange with an HSV material mask that preserves luminance structure and separate yellow/steel materials. Convert white fields with border-connected neutral removal, never a global pale-pixel key, and record both removed-background and recolored-pixel counts.

Crew Hab berth lesson (September 12): directional consistency includes capacity and furniture program, not only palette. A matte side repair still fails when three low pods become one oversized bed with a wardrobe and canopy. Promote the accepted overhead construction across all walls with exact turns, use mattress/pillow access as inward-facing evidence, and remove obsolete effect metadata when the replacement has no corresponding physical fixture.

Clone Growth Wall lesson (September 12): an accepted directional bank can be embedded in a larger paired source sheet. Use the accepted registration's source geometry to isolate that bank, clean only its border-connected neutral exterior, and rotate the isolated bank exactly. Do not rotate the whole paired sheet or substitute a different wall's equipment program. Define wall contact with the outer service rail and verify inward access with the tissue window, microscope, keyboard and consumables in all four native views.

Emergency Isolation lesson (September 12): trace every visible layer before interpreting an owner name. A reported “full wall” may be a baked perimeter loaded by the base room while the retained service bank is a separate registered prop. Inheritance can also import a different room's complete furnishing program. Remove those layers at their owners, update stale floor-profile hosts and manifest claims, then rotate the accepted bank. Sparse floor space is valid when it makes containment legible. Apply matte correction to a displaced shared prop at its canonical source and keep geometry and alpha unchanged.

Biomass material lesson (September 12): preserve accepted wall geometry while correcting the semantic accent family. Mask the old hardware hue and map it into the room's feedstock/process color at restrained value; do not tint cream vessels or charcoal pipework globally. Trace dark companions to renderer multiplication before repainting them, and use a room-specific tint when the shared source is otherwise sound. Give an opaque multi-prop service sheet a true-alpha room copy even when polygon clipping hides most of its white field, then verify pale interior objects survived.

Bio wall lesson (September 12): small operator-facing details can prove rotation more reliably than the outer cabinet silhouette. For an overhead microscope bench, check eyepieces first, then jar access and case latch orientation. Promote one accepted source through exact turns only when those cues remain inward. Border-connected neutral cleanup is required when white dishes and pale laboratory paint must survive unchanged.


Isolation side revision: recount repeated machinery after every camera edit. A plausible three-bay bank can silently become two; reject that study and repair the exact missing inventory before registration. Quiet static lenses need source-local operating cues and animated-prop classification in both direct and retained rendering. Check every lamp, not one representative pixel.


Shield side valves must be checked from pivot to grip: controls can sit on the inward half of a bank yet point toward the wall. Review every repeated grip and preserve the two-tank/three-compartment inventory. Card refresh follows the actual q0 bank (west here), not the compass direction changed. Wait for the native card file before validating its consumers; GUI process dispatch is not bake completion.


Reactor service companions: compare every pickup, valve, cartridge pull and case latch against the inward operator edge. A correctly placed pipe rail does not establish access direction. Keep the two-filter/three-cartridge inventory and a clear work surface; review at intended 120-unit length. A single authored east registration with a mirrored west fixture proves library availability, not live host fit or two authored entries.


Reactor side host fitting uses the unoccupied upper side bay, switching to mirrored west when the cooler occupies east. Keep the station at its reviewed length, clear the side doorway, and compare prop inventories to prove central machinery stayed intact. Validate every quarter even when three share coordinates.


North Reactor service companions put the rear pipe rail north and every access cue south. When fitting a new compass companion into a furnished room, replace the equivalent service station where appropriate instead of duplicating its function and narrowing circulation. Record the actual per-quarter selections, not only source availability.


Gravity calibration side art preserves five graduated weights and two empty scale pans. Adjustment knob and case latch establish inward access. A calibration-bench companion does not cover the separate control-console direction; keep coverage stages per functional asset. Replace the south weights station when installing its side companion so the calibration inventory is not duplicated.


Gravity side control modules place both pickup grips and adjustment knobs inward. Keep the screen quiet in static art and distinguish any future operating cue from source review. Fit the paired calibration/control stations on opposite upper side bays without duplicating their south counterparts; verify central-apparatus metadata and the unchanged default card view.


Gravity north pairs retain the functional split and doorway gap: weights/balance on one side, control modules on the other, every access cue south. Register each silhouette independently from the shared source sheet. Source availability across compass directions and per-quarter live selection are separate facts; record both without inferring owner camera acceptance.


BRINE corner repair: an edit restricted to one arm can still repaint the other and replace instruments with blank cabinet covers. Check each functional bay and the preserved arm before registration. Reject unintended inventory changes even when the new inward controls look plausible. Keep the source study separate from installed geometry.


Explicit per-bay screen counts preserved BRINE corner inventory where a generic side-camera edit replaced instruments with covers. Treat a selected inward-access correction separately from unresolved painted operating traces and owner camera acceptance. Compare the entire corner because the supposedly preserved arm may also be repainted.


BRINE northeast repairs preserve two four-roll cassettes and separate angled/lower consoles; place all catches and control rows on the left inward edge. Recheck source proportions and complete corner fit even when the intended change is only access direction. Preserve world collision bounds and report source-arm length changes rather than claiming identical artwork.


Facing coverage audit: tools/audit_room_facing_coverage.py reconciles a fresh RoomDatabase export with the ledger. All47 identities and four entries each establish inventory coverage only. Text flags are review candidates, not defect counts: negation/history can produce false positives, and unflagged stages do not prove acceptance. Inspect nested library/live records and preserve latest owner feedback in any completion audit.


Airlock directional lockers must reserve an empty pickup tray for the removable runtime helmet. Distinguish stored spare helmets from the interactive one. Verify carrying-handle apertures at native scale, and align both service approach and rendered helmet to the new tray before selecting a locker source.


Directional Airlock lockers share one helmet anchor between rendering and crew fitting; preserve the legacy offset for existing lockers. A library prop with a dynamic attachment needs custom_library_draw honored by both direct and retained paths. State-only tests can pass while that attachment is invisible: inspect actual before-grasp, after-grasp and returned screenshots. Keep sidebar viewport failures separate from verified handoff behavior.


North suit-storage companions need a rear mounting rail and inward front access latches, with the removable helmet tray empty. Recount two stored helmets separately from the runtime helmet. Native library registration proves source loading and silhouette at intended width; it does not prove furnished-room fit, crew handoff, or matte material quality. Small brass edges can remain too busy at gameplay scale even with correct inventory.


A material-only generation can shift the silhouette by a pixel even when the camera and inventory are preserved. Re-register the actual revision and review its native-size rendering. Reduced large metal highlights need not resolve fine brass-detail density; evaluate the furnished room before accepting material consistency.


Airlock north wall mounting must coordinate the existing upper fittings with the locker. Raising the whole fixture into the riser can overlap wall instruments and violate floor-prop containment. Keep projected wall art, collision footprint and the crew handoff anchor explicit; a passing floor-edge candidate is not completed wall mounting.


Native room-service fixtures that manually advance simulation must also control independently processing dialogue nodes. A screenshot yield can open the greeting and acquire a pause even when the main node has processing disabled. Probe pause, readiness and dialogue ownership before modifying interlock logic. Disable automatic dialogue in the fixture; retain production pause behavior.


A wall-mounted service cabinet may use separate wall_art_rect and floor footprint while retaining a tested handoff anchor. Omit only architectural fittings intersecting its projected art. Review isolated room and adjacent-room station captures: top-aligned art can be correct in isolation but occluded by neighboring station content. Footprint parity cannot prove shared-wall visibility.


Before diagnosing occlusion, inspect the full viewport and capture the same state with the camera shifted. Airlock north review exposed a second issue: omitted shared risers require BASE_Y mounting, while exposed north walls use TOP. Never project a cabinet into the neighboring room simply because its isolated raised-wall preview passes.


Set per-room raised-wall visibility before configuring wall-mounted props. Shared renderers otherwise risk inheriting the previous room setting. Check raised, low, shared and raised-again on the same view with invariant floor geometry and correct projected mounting height.


A side bank can have inward latches yet still fail the camera contract when its contents remain stacked front elevations. For shallow kit trays, show helmet crowns with inward side visors, sideways boots with inward toes, and compact folded cloth bundles. Recount inventory after reprojection and review mirrored library variants at intended length before live service fitting.


Side locker kit facing and crew handoff facing are separate constraints. Preserve authored inward visors/toes while placing a reachable service shelf for the existing action clip. Verify both mirrored installations independently. A collision-free long cantilever can still look crude; record support polish separately from native service success.


When a continuous south bank conflicts with the entrance, author finished independent sections rather than cropping a doorway through machinery. Preserve functional inventory while relocating it between bays. Recheck bin pulls and vise access after splitting; a correct doorway gap does not establish inward access. Native library spacing still requires host-specific tote and route review.


Single-door layout tests can pass without proving a workbench is reachable. For fitted service candidates, check paths from the entrance to each operator edge using production crew collision and segment rules. Fixed-rotation views repeated by a four-quarter harness remain one distinct orientation. Preserve the live default separately from candidate host evidence.


A semantic prop variant can lose its room-specific animated drawing when replacement occurs at render time. Mark the original semantic prop for custom_library_draw and preserve that flag through apply_variants. Compare off/on and two operating times in both direct and retained renderers; successful source loading alone can hide a missing indicator.


When quieting a multi-screen corner bank, count glass apertures separately from displayed signals. Preserve dark glass and bezels rather than replacing screens with blank cabinet covers. Colored fluid is not automatically powered emission; retain material identity while removing screen traces and illuminated buttons. Repainted bottle details require explicit review rather than a geometry-preservation claim.


Quiet corner-screen bases can carry source-local operating_screens rectangles in their registration. Keep traces within glass, transform them with the registration, and mark the owning prop animated for retained drawing. Validate every screen independently in both renderers; twenty checks here mean ten screens times two renderers, not twenty assets or pause-transition proof. Refresh the actual q0 card after idle source selection.


For mixed analysis banks, separate electronic displays from pale physical filter media and sample racks. Quieting emission should preserve filter-roll counts and sample inventory. Angled screen traces need conservative interior bounds; verify each aperture at native scale rather than using a whole-bank difference.


Raised-wall electronic displays belong to two rendering lifetimes: quiet architectural texture in the cached wall pass, powered signals in a dynamic pass. Verify the host cache path before adding time-dependent drawing to north_wall; a direct preview alone can animate while the station remains frozen.


Retained-content screenshots do not automatically exercise cached architectural surfaces. Record which pass owns the tested pixels. For BRINE riser signals, separate fixture animation proof from full station WALL/LIVE cache and visibility validation, including low/shared walls and pause.


### Cached architecture and operating displays (September 12 verification)

A retained room-content capture does not verify cached station walls when its fixture still calls NorthWall directly. Keep quiet wall textures in the cached architecture pass and powered signals in the live pass. Verify in the actual station renderer: power-off versus power-on pixels, two operating times, an explicit paused process step, and stable wall-rebuild counts while only signal time changes. BRINE evidence: output/brine-station-wall-2026-09-12/checks.json and runtime.json; both screen apertures pass, with rebuild count 5 throughout powered animation and pause. Review visibility separately for low walls, disabled wall hardware and a north neighbor. These technical checks do not imply owner acceptance of camera, materials or side silhouettes.


### Turbine camera reconstruction study

A subject-only reference can still dominate the camera despite explicit overhead/floor-mounted instructions. September 12 east-low-study added a skid and readable inward rotor but retained much of the reference elevation and glossy generator edges. Keep it as a study, not a selected improvement. Next camera repair should supply an actual camera/layout reference or reconstruct without the misleading source; stronger angle adjectives alone have repeated the same geometry. Evidence: assets/turbine-directional-v3/east-low-review.json.


### Fresh turbine reconstruction and intake repair

Removing the old elevation reference produced a clearer overhead floor skid (east-overhead-fresh-study.png). It also moved the exposed rotor upward, so the next edit explicitly closed the top aperture and placed blades inside the inward side intake. Review both camera and functional opening independently: satisfying one can break the other. The repair still needs background/alpha and native material checks; it is not installed. Evidence: assets/turbine-directional-v3/east-intake-review.json.


### Clean overhead turbine native study

Imagegen replaced the baked checkerboard with white and subdued orange highlights. Read-only vector registration excludes the exterior without changing source pixels. The fresh source is wider than the old elevation, so preserving its world rectangle via contain registration shortens the occupied wall length. Native q1 now reads as an overhead skid with inward left intake on the east arrow wall, but scale/finish, west companion and functioning anchors remain before selection. Evidence: assets/turbine-directional-v3/east-clean-review.json and output/turbine-fresh-2026-09-12/native/current_turbine-q1.png. Native capture exits 0; this is candidate review, not owner acceptance.


### Wider replacement artwork and saved positions

A candidate rect changed before render can still receive the saved default position during rendering. Turbine fresh fitted preview preserved 270 wall length and mirrored west correctly, but east crossed the hull because the old narrow-source position was reapplied. Validate final rendered geometry, and revise the candidate layout position with the source aspect rather than trusting pre-render rect values. Existing bounds-based rotor/lamp UVs also require remapping after a camera reconstruction. Evidence: output/turbine-fresh-2026-09-12/fitted and assets/turbine-directional-v3/east-clean-review.json. No live selection yet.


## Overhead turbine side assets installed

East clean source now supplies both side registrations, with mirror_horizontal metadata for west. Source-local effect points mirror through the same transform as art. Default east position updates with the wider footprint; all176layout routes and20side-variant checks pass20260912-135713-headless. Native installed captures at two clocks exit0; four effect crops change with time and west installed view reviewed. q0 card unchanged. Retained station pause/state and owner aesthetic acceptance remain. Evidence assets/turbine-directional-v3/east-clean-review.json.


### Galley cooking-bank side companion

Serving furniture does not establish directional coverage of cooking/washing machinery. Added a separate overhead galley kitchen: dry jars, two-ring cooktop, prep board and sink; every hand-access edge faces inward. East and mirrored west native library preview reviewed at55.68x300. Host placement and operating effects remain separate gates. Evidence assets/galley-directional-v1/kitchen-side-review.json; fixed north kitchen unchanged.


## Galley side kitchen host study

Added kitchen-side-host-layout.json replacing semantic kitchen only in isolated candidate. East bank x128.32133,y-176 at55.67867x300 leaves existing south serving counter and entrance clear. Native host reviewed; production crew graph reaches three inward work points from entrance. Fixed q0 repeats four times in the adapted route fixture, not four directional hosts. Sparse composition and operating detail remain; fixed live north kitchen unchanged. Evidence output/galley-kitchen-host-2026-09-12.


## Galley cooktop state verified

Added optional cooktop_ring registration metadata and source-local ring drawing in galley_view. Original semantic kitchen carries custom_library_draw before variant application, so retained library rendering keeps the room effect. Six native direct/retained captures exit0; both ring crops pass active and temporal checks, retained on-a reviewed.20side variants pass20260912-140448-headless. Evidence output/galley-kitchen-state-2026-09-12/checks.json. This does not prove pause behavior; alternate host composition/live selection remain.


## Galley south kitchen companion

Created kitchen-south.png with inward north handles, outward south faucet root and broad overhead worktops. Registered continuous300x59.63library asset and reviewed native preview. Current galley south entrance requires a separately authored split bank; do not place the continuous strip over the door or crop through equipment. Source cooktop anchor supplied but south operating state remains unverified. Evidence assets/galley-directional-v1/kitchen-south-review.json.


## Split south kitchen prepared

Created two independently finished120-wide cooking and prep/washing sections from a new imagegen source, not a raster crop through machinery. Native pair reviewed across116-unit gap. All four functional bays retained with north access. Current host still needs its existing south serving counter relocated and access/state checks; split source is candidate only. Evidence assets/galley-directional-v1/kitchen-south-split-review.json.


## Split galley host access verified

Installed cooking/washing registrations in library and added isolated kitchen-split-host-layout.json.120-wide south sections flank116-unit gap; existing serving identity uses its east-wall companion. Native host reviewed; entrance routes reach cooking, washing and serving points with production collision/segment checks. Adapted test repeats fixedq0four times. Composition remains sparse and split cooktop state is unverified; current live north kitchen remains selected. Evidence output/galley-split-host-2026-09-12.


## North galley idle repair prepared

New kitchen-north-idle.png removes painted orange emission while retaining pantry/cooking/prep/washing inventory. Read-only vector registration prepared; live source unchanged. Pot/faucet highlights remain strong, so idle-state success is not full matte-material acceptance. Native fitted review and effect alignment remain. Evidence assets/galley-directional-v1/kitchen-north-idle-review.json.


## North kitchen material revision prepared

Targeted metal-only imagegen repair reduced the pot/faucet/utensil highlights while preserving quiet diffusers and cream cabinet brightness. This is a material change rather than global dimming. New kitchen-north-matte source and vector registration are ready for native fitting; floor collision/mount and powered effect/card integration remain. Evidence assets/galley-directional-v1/kitchen-north-matte-review.json; live source unchanged.


## Live north kitchen matte source installed

Galley draws registered matte north art into the existing kitchen visual bounds while retaining semantic prop and collision rectangle. Native q0 and refreshed north-matte card reviewed.176layouts pass20260912-141751-headless;47card parity passes. Current code had two card-path consumers; both updated rather than assuming the historical three. Old source retained for geometry/provenance. Explicit north state/pause and owner aesthetic checks remain. Evidence assets/galley-directional-v1/kitchen-north-matte-review.json.


## Installed north galley state verified

Six native direct/retained captures completed exit0. The existing small operating indicator changes with power and time in both paths while new quiet source remains selected. Retained on-a visually reviewed. Evidence output/galley-north-state-2026-09-12/checks.json. Fixed clock sampling establishes animation, not station pause behavior; explicit pause and owner aesthetic acceptance remain.


## Cold Store low-compartment side study

Created fridge-west-overhead.png without the misleading elevation reference: three closed low compartments, nine food groups, inward right handles and outer hinges. Source review finds broader flat lid planes and quieter materials; native comparison must still establish camera readability. Actual alpha/source metadata is in assets/cold-store-directional-v1/fridge-west-overhead-review.json. Registration, operating marker and host review remain; current live bank unchanged.


## Cold Store side candidate native fit

Alpha-derived vector registration preserves source pixels. Centered aspect containment left visible casing away from west wall; align the contain frame to the authored backing edge instead. Flush q0 native candidate reviewed and capture exits0, existing prop bounds/aspect retained. Source marker/state and route checks remain before live selection. Evidence assets/cold-store-directional-v1/fridge-west-overhead-review.json.


## West Cold Store bank installed

New overhead source selected in existing west registration with left-aligned contain and original aspect. Optional source status_point556,996 maps indicator through the registration transform. Native q0/q2 power/time crop checks pass;176layouts/20variants pass20260912-142729-headless. Refreshed overhead card reviewed and two consumers updated;47card parity passes. Retained/pause and east rack consistency remain; no owner acceptance or export claim. Evidence assets/cold-store-directional-v1/fridge-west-overhead-review.json.


## East Cold Store rack material candidate

Six-container inventory and inward latches retained while tub/frame highlights were reduced. Right-aligned contain fits prior aspect and keeps backing flush. Native q0 reviewed alongside selected west fridge; capture exits0. Candidate only pending registration selection, layout regression and card refresh. Passive rack needs no invented operating emission. Evidence assets/cold-store-directional-v1/rack-east-matte-review.json.


## Cold Store side pair selected

East rack matte source installed after native review; original registration preserved in assets.176layout routes and20side variants pass20260912-143238-headless. Refreshed matte-pair card reviewed and both current bindings updated;47card parity passes. West fridge and east rack now use quieter side materials while preserving inward access and inventory. Owner aesthetic and retained/pause verification remain.


## Salvage north bench matte idle candidate

Created bench-north-matte.png preserving used teardown inventory while removing baked task-lamp emission and reducing metallic sparkle. Wear remains dense; source review does not settle native noise. Vector registration excludes exterior and left rail handle aperture without rewriting pixels. Existing live bench unchanged pending native fitting, operating light and card checks. Evidence assets/salvage-directional-v1/bench-north-matte-review.json.


## Matte north salvage bench installed

Registered matte bench now draws in original visual bounds, leaving semantic collision/placement intact. Task lamp receives a small source-aligned powered diffuser overlay; explicit state checks remain. Native room and refreshed card reviewed;176layouts pass20260912-143731-headless,47card parity pass. Concurrent underwater_visibility parse failure interrupted initial card bake; current source was already corrected externally, failed process stopped, retry exits0. Evidence assets/salvage-directional-v1/bench-north-matte-review.json.


## North salvage lamp and indicator verified

Six native direct/retained captures exit0. Separate lamp and indicator crops each change with power and time in both renderers; retained on-a visually reviewed. Separate effect crops prevent a surviving indicator from concealing a missing task lamp. Evidence output/salvage-north-state-2026-09-12/checks.json. Explicit station pause and owner aesthetic acceptance remain.


## Salvage tote matte source prepared

Targeted accessory finish separately from bench: retained bearing/hose/rotor/flange inventory while reducing gold and white sparkle. Both handle apertures use explicit exterior seeds; dark part recesses remain opaque. Candidate registration preserves prior aspect; native comparison/card selection remain. Evidence assets/salvage-directional-v1/tote-south-matte-review.json.


Salvage matte tote selection (2026-09-12): review accessory finish in the furnished native card after changing the main bench; small brass parts can retain distracting glare independently. Preserve inventory and handle apertures, then refresh both current card bindings. Evidence: assets/salvage-directional-v1/tote-south-matte-review.json.


BRINE south service lesson (2026-09-12): quiet the complete idle source, including small teal tabs and buttons, while preserving the overhead functional layout. One source-local operating_screens rectangle restores restrained live telemetry through the existing library renderer. Verify an isolated screen crop in direct and retained off/on/time frames, then review the idle card separately; those frames do not establish station pause behavior. Evidence: assets/brine-core-directional-v1/service-south-idle-review.json.


Battery overhead companions (2026-09-12): state control inventory across the complete section, not ambiguously per unit. First source repeated three gauges/four switches on every transformer; corrective edit restored the total before installation. Split-wall consumers must explicitly decode mirror_horizontal; UV reflection alone cannot mirror an unreflected registration. Preserve the prior collision aspect with an outer-edge-aligned contain frame, then inspect both native walls. Evidence: assets/battery-directional-v1/side-overhead-review.json.


Archive split-screen lesson (2026-09-12): blank overhead display sources need operating-only telemetry carried through both split registration decoding and retained animation classification. Reuse the existing source-local screen drawer for library and split assets, including mirrored UV projection. Inspect separate screen crops on each wall in both renderers; a passing east display cannot prove its west reflection. Eight isolated native cases passed; station pause remains a separate check. Evidence: assets/archive-directional-v1/side-overhead-review.json.


Storage overhead lesson (2026-09-12): preserve departmental display color when moving baked emission into runtime. Optional operating_screen_color is carried by both library and split registrations, leaving the established cyan default intact while Storage uses muted amber. Review the mirrored console separately from geometry; four isolated east/west direct/retained power/time cases pass. Maintain counts for small cases and console controls as well as large crates. Evidence: assets/storage-directional-v1/side-overhead-review.json.


Crew Hab reading-light lesson (2026-09-12): material repairs can preserve an already-correct overhead camera. Quiet the painted lamp and its pillow spill, then register a small source-local diffuser polygon in the animation pass. Test power changes and steady pixel parity across times; a reading light should not acquire machine flicker merely to pass a temporal-change test. Preserve personal belongings and inspect thermos, trim, wood and ceramic separately. Evidence: assets/crew-hab-directional-v1/east-matte-idle-review.json.


Crew Hab authored-pair lesson (2026-09-12): when east and west already have separately authored contents and access, repair each source in place rather than replacing the pair with a convenient flip. Give each reading lamp its own source polygon; preserve outer-edge registration and compare unchanged orientations and placement metadata. West source and native fit reviewed in assets/crew-hab-directional-v1/west-matte-idle-review.json.


Med Office full-wall lesson (2026-09-12): continuous full-wall consumers need the same explicit mirror and operating-screen metadata handling as split/library consumers. Copying a mirrored JSON alone does not alter a decoder that ignores the flag. Validate both walls, both screens and both rendering paths; eight cases passed. When the default quarter is a side wall, refresh the room card after a side-camera change. Evidence: assets/med-office-directional-v1/side-overhead-review.json.


Med Center instrument-facing lesson (2026-09-12): an overhead tray does not establish inward tool access. Inspect finger loops independently of tray catches and machine controls. Correct scissors and each clamp before mirroring the counterpart; three clamps and the large scissors now have room-facing grips. Separate the small status screen from the large diagnostic display in native power/time checks. Evidence: assets/med-center-directional-v1/side-overhead-review.json.


Strict-overhead family lesson (2026-09-12): when the owner names one south bank as
the camera/style exemplar, exact raster and registration quarter turns give every
wall the same inventory, material and viewing angle. Preserve the prior directional
registrations as provenance, transform polygon boundaries with the raster, and keep
the existing placement/collision frames. Review the native room rather than the
rotated source alone: independent furniture, doors and route clearance decide
whether the derived bank actually fits. Refresh q0 cards after selection.


Corner alignment lesson (2026-09-12): a fitted L-shaped corner bank can be correct
in scale and source geometry yet sit too high against the room panels. Apply the
smallest shared translation to both banks in all room quarters, compare native
before/after images, and rerun real door-entry routes. Do not resize the source or
move the central equipment to disguise a wall-contact error.


Final-route lesson (2026-09-12): rerun the complete preferred-layout suite after
the last visual integration, even when the changed renderer cannot affect the room
named by a failure. In a shared moving worktree, reproduce the failure before
editing. Here three Med Center stations formed a barrier between two side doors;
moving the group against the closed wall restored the route and improved the native
composition. Keep the production view's forced arrangement and saved default in
sync so the visual capture proves the same geometry the route test checks.


Current-catalog closeout lesson (2026-09-12): finish a broad room-art pass with a
fresh native export from current source, not a count of generated candidates or old
per-room reports. Reconcile its identities against the coverage ledger, capture all
applicable rotations, and inspect quarter contact sheets as one visual system. Keep
historical direction stages for provenance, but add a separate current-contract
review gate with exact manifest evidence so stale “pending” text cannot be mistaken
for an active defect or silently rewritten as owner acceptance.
