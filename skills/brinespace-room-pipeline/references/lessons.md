# Lessons and attribution



For BrineSpace work, also read the active checkout's

`skills/brinespace-room-pipeline/references/lessons.md`. Installed copies are

snapshots; newer project observations take precedence. Preserve attribution

when synchronizing this reference.



## Ten-room source batch, September 6



- Keep the source ledger synchronized with later integration work. Batch two had

  three rooms still marked source-only after live integration. The read-only

  audit_batch_two_integration.py now checks immutable source hashes, complete

  identity coverage, both selected card mappings, native card sizes and required

  records. These consistency checks explicitly do not approve visuals or packages.

- Extend resource-UID coverage as new fixtures are added. The batch audit now

  covers 32 script/UID pairs, not only the initial room subset; it never rewrites IDs.



- Respect the surface actually visible in source art. Medical Office's desktop

  monitor shows its rear; put activity on its separate front-facing diagnostic

  console rather than painting a screen on the monitor back. Static furniture

  remains a valid host even when the room itself functions.



- Carry static-host expectations into economy-driven pixel tests, not only the

  isolated preview. Medical Center's supplied/restored cases animate diagnostics

  while its supply furniture stays still; room operation does not animate everything.



- Empty medical equipment should show readiness, not invented patient vitals.

  Medical Center keeps supplies static and uses three localized diagnostic

  readouts. Its trolley/cabinet render as separate pieces while collision reserves

  their whole group: document that distinction rather than implying a walkable gap.



- Report the actual room ID and world foot coordinates in shared route failures.

  Holographic Core passed full bounds but clipped two rotated perimeter turns;

  moving its projector eight units outward cleared the same expanded test without

  shrinking equipment or changing walking rules. Preserve failed route evidence.



- A luminous annulus needs a ring-shaped replacement, not a solid dark disk.

  Holographic Core uses shared source-space quads so the renderer and tests agree;

  assert the lens centre remains uncovered and all quads stay on the host.

  Correcting one ring does not certify the remaining source indicators offline.



- A projected volume can be a local wireframe effect registered to its emitter,

  independent of the room bitmap. Holographic Core's pilot verifies motion per

  host, but direct renderer-state checks do not establish economy or pause

  behavior. Painted cyan lens details still require offline cleanup separately.



- Include restoration after shortage/suspension in economy-driven visual tests.

  Bio's five-state sequence checks that all hosts restart, not merely that they

  stop correctly. Missing consumables may leave normal room lighting available.



- Bio Lab's twin tanks share one machinery host but require two disjoint fluid

  effect surfaces. A single enclosing rectangle also includes the dry controller.

  Check each sample against the union of actual working surfaces, not only the

  host silhouette or broad effect envelope. Closed centrifuge lids stay static;

  use visible readouts for operation until internal motion is actually exposed.



- Anomaly's read-only indicator-region helper suggests connected colour clusters,

  not accepted emissive masks. Semantically separate painted material/glass from

  lights. A stricter per-prop coverage audit caught 25 tiny violet pixels omitted

  by the helper's minimum cluster size; retain failed bakes and verify corrections.

- Reuse verified department hull materials independently from candidate machinery.

  Anomaly's dark equipment does not require its entire Science floor and walls

  to become dark. Preserve canonical sockets and upright prop registration.



- Refinery tests now check sampled effect envelopes against reserved center aisles,

  in addition to effect containment within source silhouettes. A conveyor can be

  internally valid yet cross a route after registration; test both coordinate spaces.

- Scrolling belt lines over static ore are operating cues, not literal material

  transfer. Keep this limitation explicit until moving ore pieces and occlusion

  are authored. Passing motion pixels alone does not prove conveyor realism.



- Storage has no automatic machinery cycle in its gameplay contract. All four

  registered hosts intentionally stay still while the room functions. Assert

  this expectation explicitly instead of adding ornamental movement to satisfy

  a generic animation check. Lighting remains independently testable.

- Departmental art does not require a gameplay-category migration. Storage uses

  Logistics grey/yellow while retaining the existing Engineering category and

  capacity rules; record the distinction rather than changing doctrine balance.



- Maintenance distinguishes two animated hosts from static tooling and storage.

  Explicit per-host motion expectations catch both missing activity and accidental

  animation of stored materials. The repair-part overlay does not prove an arm

  articulates; describe that distinction in the integration record.

- Tall racks need full-silhouette rotation checks in addition to ground footprints.

  Maintenance's panel rack passes containment in every layout; that evidence still

  does not replace production-actor occlusion or neighbor-crossing review.



- Research's scanner aperture uses separate textured frame/head/base polygons.

  An outer silhouette alone would preserve pale source floor inside the arch.

  Open spaces in props need internal masks or deliberately separated pieces;

  neither exterior cleanup nor outer-bounds tests detect that defect. Inspect

  piece boundaries at native scale and keep their source coordinates reviewable.

- Research is south-only although its inherited base renderer is a cross. Set

  topology before embedded configuration and test all four rotated masks against

  the database. A generous cross aisle in the source is not a four-port blueprint.



- Battery's station integration required updating the separate draft aspect-fit

  allowlist as well as both texture maps and variant selection. A correct baked

  card does not prevent a consumer from cover-cropping it. The native 2560 frame

  confirms the complete draft silhouette after that change.

- Source-polygon registration can retain floor in concave service loops. Record

  this separately from full-bounds containment: passing bounds does not prove a

  clean silhouette. Keep exact source UVs and inspect native room crops.



- Persist each built-in result in the project immediately, before issuing another

  generation. Interruption after a successful generation otherwise leaves the

  manifest at briefed with the only source outside the checkout.

- `tools/audit_room_source_batch.py` checks source hashes, real dimensions and

  alpha counts and builds a labelled same-canvas-scale sheet. It never changes

  acceptance status. Use a new audit directory to preserve prior evidence.

- Ten 1280 requests again returned 1254 square. Nine initial sources were RGB;

  painted checkerboards occurred in Research and Refinery. Alpha must be inspected

  per asset, including after revisions; don't infer it from a tool preview.

- Command's targeted edit removed screen traces but sealed only one of four gaps.

  A successful local correction is not whole-image compliance. Keep the useful

  equipment separately and retain authoritative engine-owned hulls and sockets.

- The Lounge edit corrected two sideways chairs while preserving broad surrounding

  composition. That does not certify pixel equality outside the target, nor the

  orientation of other furniture groups. Review those separately.

- Quadrant-separated sources simplify registration but risk making every room's

  composition alike. Keep varied focal shapes and author final prop layouts around

  canonical topology; do not mistake the source-sheet arrangement for final design.



See `docs/PRODUCTION_TEN_SOURCE_REVIEW.md` for pending gates and known defects.



These are adapted workflow ideas, not imported external instructions or copied

engine code. Reviewed 2026-09-05; external projects may change.



## Sprite-maker / Sprite Studio



[Asset-pack harness](https://github.com/JohnKinyanjui/sprite-maker/blob/main/src-tauri/resources/skills/sprite-director/references/asset-pack-harness.md):

coordinated projection, scale, palette and complete pack manifests. Use contact

sheets to review our separate room assets; do not inherit its generation-sheet

strategy automatically when individual high-resolution rooms are needed.



[Polish script](https://github.com/JohnKinyanjui/sprite-maker/blob/main/src-tauri/resources/sprite_polish.py):

local repair regions, source hashes, reversible versions and geometric comparisons.

Adapt the principle of preserving outside-region pixels. Its corner-color keying

and 64-color remapping are not defaults for dark, detailed BrineSpace rooms.



[Quality gates](https://github.com/JohnKinyanjui/sprite-maker/blob/main/src-tauri/resources/skills/sprite-director/references/quality-gates.md):

separate technical diagnostics from visual acceptance. Its documentation contains

different animation approaches; do not combine them into one purported guarantee.

For BrineSpace machinery prefer deterministic local overlays. For generated

character strips follow the available sprite-pipeline skill and the user's brief.



## Capybara 2.5D engine



[Asset integration](https://github.com/d-liya/capybara_2d_engine/blob/main/.agents/skills/capybara-game-developer/ASSET_INTEGRATION.md):

preserve proportions, register assets in their real consumers and separate static

art from stateful overlays. Generation alone does not finish gameplay integration.



[Placement data](https://github.com/d-liya/capybara_2d_engine/blob/main/docs/recipes/map-placement.md):

named bounds provide stable placement anchors. Translate this to Godot room-local

regions; do not import its coordinate ordering, engine API, cloud keys or web stack.



## BrineSpace observed failures



- Never invent human-readable Godot UID strings. Hand-written batch-two IDs

  failed ResourceUID text/id round-trip even though path-based preloads worked.

  Generate new IDs through ResourceUID.create_id()/id_to_text(), keep script pairs,

  and validate canonical form/uniqueness. Check references before correcting IDs;

  this is not permission to regenerate established user resource identities.

- Full-host/actor detail crops make all-prop depth review practical. Capture the

  union of the complete silhouette and actual production sprite, not just ground

  bounds. Include an adequate outer gutter: Xeno's first detail pass clipped a

  north-side actor's review margin. More canvas space preserves native scale;

  shrinking sprites to fit would conceal the problem.

- Single-door neighbor fixtures may need a different rotation for the supporting

  room. Xeno's south-only socket required a facing Nursery, not two identical room

  rotations. Preserve actual masks and test return traversal too.



- Biodome uses effect envelopes for specific beds and contained tanks. Staying

  inside a large assembly outline is insufficient: an irrigation effect could

  otherwise run over a cabinet or dry floor. Test the relevant surface too.

- Plants remain visible without power; operating irrigation is not plant growth

  or acquisition. Preserve those distinctions in room acceptance records rather

  than claiming that lively source art implements future content-state systems.

- Fine foliage/concave pipe gaps can retain source floor even when the full

  silhouette fits the walls. Review at native close-up and record cleanup debt;

  containment and standability tests cannot certify a clean visual cutout.



- Data Archive's rotated rack clipped the actual perimeter walker despite valid

  wall containment. Test reverse entry routes as well as centre/socket lines;

  move ground registrations rather than changing gameplay paths to excuse art.

- Shared-wall pixel tests must account for department materials. Ivory brightness

  rejected a visible charcoal Archive wall. Keep existing bright-wall checks and

  constrain dark-material exceptions; visually inspect the seam, since a colour

  heuristic alone cannot certify that structure was drawn correctly.

- Baked cyan indicators can be covered by registered dark apertures, with active

  traces drawn separately. A source-pixel coverage audit found 42 then four missed

  pixels before passing. This is a colour-specific diagnostic, not a complete

  emissive mask; retain source art and failed bakes as evidence.



- Concurrent art sessions exposed a shared fixture-save filename. Visual harnesses

  now include process ID; each process removes only its own fixture. New capture

  directories alone do not isolate user:// save data.

- Clone Lab has three distinct powered-but-idle causes: missing biomass, missing

  data and full habitats. Its native tests exercise the actual economy for each,

  plus missing power and suspension; all-machine animation must stop without

  confusing normal light availability with working-cell membership.

- Full visible vessel height is not ground depth. Register both, rotate centres,

  and test source-top clearance, supported socket routes and character depth.

  The reusable capture_registered_room_poses.gd fixture uses production actor

  geometry; captures and standability alone do not prove pixel-correct occlusion.



- A restyled whole-room image can preserve broad composition but move its wall

  strips. Reusing old wall UVs sampled background into Life Support's first card.

  Register material regions anew, inspect a native card, and preserve the failed

  bake. Isolate a redesigned room in its own subclass when older departments

  inherit from its original renderer, so a local art change cannot restyle them.

- Use docs/ROOM_ROLLOUT_LEDGER.md for the current full-set queue; earlier candidate

  counts are not integration or underwater-bible acceptance counts.



- After testing a visual flag directly, verify how the simulation supplies it.

  Nursery v4 drives the actual economy with adequate inputs, missing biomass and

  missing power. The latter two both stop machinery, but only power shortage

  darkens the room. Never infer electrical availability from a map named

  `powered_room_cells`: this legacy map actually contains working cells.



- Machine-specific animation tests need machine-specific crops. Existing tank

  bubbles can make a whole-room motion test pass even if a new rack effect is

  absent. Nursery irrigation uses registered source anchors, rack-only pixel

  comparisons, all four layouts, inactive stillness and paused pairs. Effects

  follow the host translation rather than quarter-rotating upright machinery.



### Underwater corridor follow-up



- Author shallow structural fittings once as room-local geometry shared by the

  renderer and containment tests. Bands and flush grates rotate with their surface;

  they do not need upright directional sprites. Keep them outside tapered door

  approaches and rebake both card consumers when the shared surface art changes.

  Station v6/cards v3 verify this approach for the narrow corridor kit only.



- Test asset dependencies outside the checkout. The first station PCK rendered

  rooms but lost RichTextLabel cost icons: raw images alone did not satisfy

  imported-resource consumers. Include raw bytes and required import remaps/data.

  V2 passed with 1,544 packaged files. This is a dependency smoke, not a release

  export; actual export templates/presets remain a separate gate.

- A fixture can print PASS while the engine reports resource failures. Require

  clean ERROR/SCRIPT ERROR logs and inspect the actual packed render as well.



- Production integration requires checking canonical mask orientation separately

  from art orientation: straight cards are north/south, the guide was east/west.

- A narrow layered neighbor cannot replace a full room's boundary wall. Retain

  the full boundary and let a single shared collar own only the doorway span.

- Transparent space around a narrow hull must reveal one continuous environment;

  per-card water rectangles exposed the placement footprint in the first station capture.

- Fit complete narrow silhouettes in draft thumbnails. Cover-cropping cut off the

  sealed ends despite correctly baked card PNGs. Test the actual TextureRect mode.



- V6's close-up cycle revealed the fixture was using a smaller legacy actor even

  though it checked the correct foot radius. V7 uses the production 40x56 source

  crop, 46.08x65.28 world size and y68 foot baseline. Verify visual scale and

  collision independently; use native 2x seam crops without rescaling for review.

- Wall fixtures need their flat housing orientation rotated with their anchor.

  Rotating only the centre left horizontal lamps on vertical corridor walls.



- A second, straight-corridor style image coincided with recentering and widening

  the generated elbow. Retrying with only the exact guide improved the outline,

  but still produced tall wall faces. These trials do not prove either strategy

  locks geometry or produces rotatable art.

- The native follow-up uses selected wall/deck surface regions and a flush hatch

  on authoritative polygons, not a rotated whole corridor painting. Surface-scale

  changes are recorded in code; upright equipment would need separate handling.

- Narrow collars require the shallow cutaway in both orientations. Reusing a

  tall front room arch made the downward corridor connection look freestanding.

- Preserve generation failures, source prompts and sample registration separately

  from native review evidence. Passing traversal does not approve the art finish.



- Requested transparent PNGs returned opaque white/checkerboard backgrounds.

- Requested 1280 output returned 1254 square images.

- Cross-room style references leaked extra door trim into straight corridors.

- A corner had convincing trim but no actual openings.

- A refinery conveyor visually blocked a required path.

- Deep lounge doorway cutouts and independent crop margins changed seam geometry.



Cryo and second-batch lessons:



- The same style reference produced both pale and dark Medical floors, and Xeno

  copied its unwanted tee gaps. Explicit negative prompts still do not lock

  department surfaces or sockets. Register useful props onto shared geometry and

  authoritative departmental flooring; keep painted-shell failures recorded.

- Check small supporting details too: Cryo tests include floor service inlays,

  not just the machinery silhouette, in the wall-containment gate.

- Derive room-specific animation meaning from actual contents. Empty Cryo pods

  can show equipment pressure gauges, not a patient heartbeat. Occupied/damaged

  variants need real presentation state; don't claim that empty artwork implements

  recovery or resolves legacy damaged-pod descriptions.

- Source, registered consumer and owner approval stages can differ within a batch.

  Keep per-identity evidence rather than labelling ten sources as ten finished rooms.



Crew Hab integration lessons:



- A reused renderer can silently inherit the wrong port mask. Assert the actual

  database room topology, not merely the base class's geometry, in neighbor tests.

- Animation tests need per-prop expectations: a powered desk may animate while

  empty beds and chairs remain still. Do not add meaningless movement to pass tests.

- Warm habitation lighting belongs in independent fixture/pool parameters, not

  baked into the illustration or applied globally to every department.

- Test the actual draft-card aspect mode as well as the exported card image.



Therefore: inspect alpha pixels, bind art to canonical geometry, record transformations,

review whole sets at gameplay scale and keep acceptance stages separate. Neither a

successful tool call nor a passing cleanup test is proof of production readiness.



### Mining bay registration



- Audit legacy scene-level effects when replacing room art: the previous drone flight ignored hull crossings and underwater deployment. Suppress incompatible flight for the registered room while preserving production behavior. A closed hatch is not a deployment animation.

- Sample effect positions in world space at every rotation. Source-host containment alone missed a tall servicing indicator entering an aisle. Narrower assembly scale and symmetric quadrant centers passed the actual clearance check.

- Re-bake a new card version after registration changes and retest its consumer. Keep failed evidence separate from passing evidence; never reuse capture directories.



### Salvage bay and fixture evidence



- Preserve complete articulated claws in the registered outline, including tips below the cradle footprint. Test full visual bounds separately from floor collision.

- Powered diagnostics do not authorize idle winch, crane or hatch motion; do not invent activity purely to satisfy per-host pixel tests.

- Shared fixture output must name the actual subject. The nursery-derived room fixture now calls `evidence_subject()` so its final banner identifies the tested room; custom fixtures should override this hook when they change the subject.



### Lounge furniture groups



- Use several rendered polygon pieces for separated furniture within one registered group, so source floor does not become a rectangular patch around chairs. Preserve intentional rugs as art. Collision may still reserve the complete group; document that difference.

- For multi-piece hosts, test effects against the union of rendered pieces as well as the outer assembly bounds. An enclosing rectangle alone can incorrectly accept an effect drawn in a transparent gap.



### Command displays



- Register the physical screen rectangle separately from the equipment outline. Test every sampled display effect against that smaller surface and world-space aisle clearance; host containment alone permits traces over bezels and controls.

- Keep card masters offline and make operating displays additive engine effects. A corrected dark-screen source can be usable even when generated hull gaps remain wrong, provided no generated gap enters the authoritative wall renderer.



### Quarantine topology



- East/west straight rooms need a structural rotation offset relative to the shared north/south mask. Apply that offset to layout geometry only, preserving the registered equipment orientation. Verify canonical sockets against the room definition for all four rotations; a generic straight-route pass is insufficient.



### Batch connection sweep



- Derive expected socket compatibility from RoomDatabase, independently of the renderer geometry. Sweep ordered room pairs, both rotations and all four sides using actual registered footprints. The ten-room sweep covers 6,400 cases and 294,516 compatible route samples.

- Keep geometric connection evidence separate from pixel seams and production-actor evidence. Passing a centerline collision query cannot certify the drawn doorway or the walker animation.



### Ten-room package smoke



- Dynamic manifest paths need explicit packaging roots: the `--production-ten` option includes each view, card and fixture, rather than assuming a quoted-path scan discovers constructed paths. Verify selected source files against the package inventory too.

- Run every new room fixture through the PCK from an external empty working directory. Check subject-specific PASS output, process exit and all stderr; one representative scene cannot prove that every room source is present.

- Explicit PCK dependency coverage is not a standalone export. Preserve that distinction even when all packaged fixtures pass.



### Economy-driven room visuals



- Test supplied, depleted, suspended and restored states through `_apply_room_economy()` before comparing pixels. Injecting working-cell flags proves renderer gating but cannot prove the economy supplies those flags correctly.

- Depletion does not imply every room stops: derive expectations from real consumption, and keep passive zero-input rooms functional. Preserve static-prop expectations independently of functional state.

- Report the orientation and state scope actually covered by the batch body; inherited fixture preamble captures are not evidence for a different subject.



### Production walker paths



- Sample `get_test_walker_position()` with the rendered foot offset when verifying movement against registered collision. Ideal centerlines miss perimeter anchors and door offsets. Check production neighbor selection as well as geometry compatibility.

- Record previous-cell state: initial departures do not cover all ingress-to-egress turns. Path samples also do not certify autonomous state transitions or sprite occlusion.



### Ingress turns caught a real collision



- Initial departures passed while Command Center ingress turns collided 1,964 times with quadrant consoles. Cover each available previous door in path tests. Match the room walking layout to the art circulation; the four-socket central-cross layout fixed the conflict without changing sockets.

- Preserve failed evidence and rerun the same expanded sweep: 1,199,880 samples passed after the layout correction. Do not call unreviewed screenshot sets visual acceptance.



### Seam review scale



- Auto-fit changes scale with pair orientation: the 1600 fixture uses 31% for vertical pairs and 50% for horizontal pairs. Record actual zoom and do not claim equal-detail visual comparison. Supplement gameplay-scale evidence with consistent-scale doorway captures when judging small seams.

- Record exactly which frames were visually reviewed separately from the capture inventory. Forty generated frames do not equal forty inspected frames.



### Crossing sequences



- Advance the production walker update function and assert arrival, then capture before/at/after the doorway. Record actual cell and zoom per frame in a sidecar index.

- Use one zoom across horizontal and vertical pairs for comparison. Keep controlled state-machine stepping distinct from autonomous long-run simulation, and captured sequences distinct from reviewed sequences.



### Mixed-station walker exercise



- Place the full batch in one connected layout and let production neighbor selection choose destinations. Assert every transition and record visited-room coverage, rather than repeatedly forcing a single neighbor.

- Distinguish simulated walker seconds from elapsed runtime and economy cycles. The fifteen-room fixture covers 303 autonomous destination transitions, but does not certify performance or long-run resource balance.



### Incompatible neighbors



- Include an adjacent room with its only socket facing away. Verify both production neighbor rejection and walker updates remaining in the source room, then inspect the rendered flush wall. Adjacency alone must never imply a door.

- A blocked-neighbor capture is distinct from an isolated room: shared-wall ownership and omitted-side rendering are exercised only when a neighbor exists.



### Review native doorway sequences efficiently



- Arrange unscaled diagnostic screenshot regions in progress order for all room/rotation sequences. Record crop bounds and sheet hashes, and preserve full source frames. This enables complete sampled doorway review without repeatedly inspecting mostly empty full-window captures.

- A doorway crop can establish local threshold appearance and sampled actor overlap, not full-room containment or unsampled animation frames. Keep the review claim tied to those pixels.



### Standalone export exposed missing sources



- Editor/PCK success did not prove template export. The real executable lost raw room PNGs while imported cards survived. Retain runtime source bytes through an EditorExportPlugin alongside imported textures; include_filter alone was insufficient for these imported PNG resources.

- Official templates disable scene overrides. Use an export-only feature-selected validation scene with isolated saves; mechanically adapt fixture plumbing and preserve assertions. Set the actual game as current_scene so renderer lookups do not resolve to the wrapper.

- Always inspect executable stderr and pixels. The fixture printed PASS despite missing interiors, and the exporter returned zero with plugin parse errors. Neither exit status nor a PASS banner alone certifies exported art.



### Checked export command



- Use `tools/export_room_validation.ps1` with explicit engine and new output paths. It fails on logged errors even when Godot exits zero, requires runtime result markers and station coverage, and records artifact hashes. Do not call a manually observed PASS banner the automation success condition.



### Extending batch verification to a new room



- Reuse the production walker fixture with `--additional-manifest=` and `--focus=`

  to exercise both ordered directions against the existing pack plus the new room.

  Assert that the focus exists so a typo cannot produce an empty successful sweep.

- The economy fixture supports `--manifest=` and prints tested identities and

  actual state count. Preserve zero-input producer semantics: depleted reserves

  need not stop operation. Keep inherited banner claims subordinate to the body

  scope (the economy body currently tests base rotation only).



- Native seam verification also accepts `--manifest=` and `--all-ports`.

  Rotating only the first port does not exercise a second port beside different

  furniture. Record canonical port alongside rotation in frame names/index and

  review each sequence; Thermal Control covers eight distinct departure setups.



### Extend real export coverage with room manifests



- `tools/export_room_validation.ps1 -AdditionalManifest @(...)` forwards explicit

  `res://` manifests to the exported mixed-station fixture. Its dynamic trunk

  includes every subject; validation checks source hashes, raw PNG decoding and

  all-room visitation. Do not assume newly mapped art is covered by the old batch.

- Minimal source manifests may omit `selected_source`; use `source` as fallback.

Reject duplicate room identities rather than silently counting them twice.



### Combined-batch clearance and export records



- A single reference neighbor is insufficient: Holographic Core passed its

  Nursery route but the twenty-room ingress sweep found 110 projector contacts.

  A four-unit registration correction cleared 4,162,008 sampled route positions.

  Preserve full-silhouette containment and rerun cards, all rotations and states

  after placement changes; do not fix collision by hiding or shrinking the actor.

- Export manifests duplicate selected source/card references for a runtime fixture.

  Audit them against provenance and both live consumers before export so a stale

  card cannot pass as current artwork. Keep this check distinct from PNG decoding,

  runtime visitation, native visual review and release acceptance.



### Native crossing sheets and progression fixtures



- `tools/build_crossing_review_sheet.py` takes the capture index, a new output

  directory and explicit native crop bounds. It never resizes frames or marks

  sheets reviewed. Keep actual inspection findings separate from generation.

- A zero Power reserve does not necessarily interrupt a discovery pair: a live

  Reactor supplies Power through the existing economy. Use real suspension to

  test interrupted streaks rather than changing power behavior to fit a fixture.

- Native expansion tests should buy foundations and the earned prototype with

normal costs and failures enabled. Isolate metadata and manual loop-save paths.



### Individual exported room fixtures



- Reuse source fixture assertions through a mechanical Node bridge when the

  export template disables SceneTree overrides. Test the generated bodies against

  the originals and record source hashes; a copied fixture can otherwise drift.

- Keep a whitelisted runtime fixture selector in the validation build only, with

  unknown names failing explicitly and the existing station test as default.

  Run every room at supported viewport sizes with isolated saves and clean logs.

- Include generated scripts in UID audits. Successful path-based exports can

  conceal malformed historical UID strings. Check references, correct only the

  invalid pair with Godot-generated identity, and preserve the failed evidence.



### Contrast-background edge inspection



- Similar source and target floors can conceal retained background pixels. Render

  each actual registered prop offline on both dark and light diagnostic backgrounds

  before declaring its silhouette clean. The native prop-edge tool changes no

  source art; background variants are evidence, not newly generated assets.

- Biodome's fern contour included three vertices over empty source floor, producing

  a grey spike. Removing those vertices fixed the spike without moving the prop.

  Keep a known-background exclusion point and a neighboring retained-art point

  in regression tests, but do not call two points a complete alpha-mask audit.

- Re-bake the card and update station/card/export consumers after contour changes.

  Scope selective exported reruns to the repaired identities explicitly; the full

  batch remains the runner default. Keep finer fringe defects in the review queue.



### Material edits still require registration review



- A source edit that preserves composition can still enlarge pipework, bases

  and controls. Compare every silhouette and pivot before reusing cutouts.

- Bake the card through the same offline renderer after registration changes,

  and inspect both the card and station scale. Update legacy variant fallbacks

  as well as the central catalog so old imagery cannot reappear randomly.

- Keep material color distinct from active emission: amber inspection glass

  can remain amber offline, while moving diagnostic cues belong to the engine.



### Offline display surfaces and scaled diagnostic marks



- A static readout in a donor screen remains visible when animation stops.

  Cover the display interior in every state, then draw operating marks above it.

- Transform both endpoints from source coordinates. Adding a fixed world-space

  length after transforming only the start makes diagnostics escape small hosts.

- Re-bake offline cards after changing display surfaces; preserve the donor and

  document any separate source LEDs that have not yet been reviewed.



### Unoccupied medical equipment



- Empty treatment beds should show equipment readiness, not invented patient

  waveforms. Occupancy-driven diagnostics require an actual occupancy state.

- Check each assembly's powered/offline pixels independently; a central console

can otherwise conceal a stalled bedside monitor in whole-room comparisons.



### Whole-batch prop review



- Review every registered assembly on both contrast backgrounds, with captured

  pixel hashes and crop bounds. Preserve native scale; a thumbnail can conceal

  the source-floor corners exposed on Clone Lab's incubator.

- Separate silhouette contamination from offline material damage. An opaque

  rectangle may suppress a painted light while also erasing panel construction.

  Passing motion/offline gating does not approve those replacement materials.

- Prioritize clear source-background islands before ambiguous contact shadows.

  After a contour repair, inspect actor overlap again without changing collision

or scale merely to make the diagnostic prettier.



### Offline hardware is not a blank display



- Classify the surface before suppressing painted activity. Holographic Core's

  computing bays contain slots and recessed hardware, not four empty monitors.

  Redrawing their source texture with restrained modulation preserves detail

  beneath independent operating traces; it is not full emissive extraction.

- Inspect offline materials and add a local interior-detail regression. Keep

  bezels outside the sampled crop, and prove the test rejects a deliberately flat

  negative control. Pixel variation alone is not aesthetic acceptance.

- Shared-checkout controller changes can invalidate old movement fixtures while

  room state checks still pass. Preserve the failed coverage gate and report

  reachable versus actually visited rooms before changing a simulation horizon.



### Expansion resource identities and discovery fixtures



- Validate cost/input/output keys against the game's canonical resource catalog.

  A test that repeats an invented alias can pass while the real resource is bypassed.

- Derive partner rotations from actual door masks; north/south straight modules

  need a quarter turn to connect east/west. Four-port rooms cannot be sealed by

  rotation, so use suspension or a disconnected neighbor for negative cases.

- Compare persistent research against the starting balance, not an assumed zero.



### Broad perimeter machinery and batch preflight



- A perimeter path made of diagonal chords can cross broad central machinery.

  Verify the production walker's route before selecting corner waypoints; do

  not shrink collision footprints to make an apparatus pass.

- Missing or malformed fixture manifests must quit with an error. A SceneTree

  assertion can leave a headless process alive; test the negative exit path.



### Controller migrations invalidate movement fixtures



- Inspect the current update method before trusting old movement evidence. A

  legacy position helper can still return plausible paths after production

  movement has moved to another controller.

- Crossing fixtures should schedule graph destinations and then advance the real

  controller in bounded steps, checking clearance, speed and physical arrival.

- Spawn close to the threshold for doorway review; whole-room route fractions

can miss the crossing itself. Record actual controller foot positions.



### Controlled traversal versus destination choice



- For needs-driven NPCs, distinguish all-room physical traversal from autonomous

  visitation within a fixed period. Preserve failed behavioral evidence; do not

  alter gameplay priorities or count mere graph reachability as physical arrival.

- A controlled test may schedule destinations while using the production graph,

  smoothing and movement. Check every step for clearance, valid boundary crossing

  and speed; record continuous feet and actual arrivals. Label that mode explicitly.

- Keep both test modes available and make exported verification require the mode

  it requested. A disabled-target negative control should fail, while ordinary

  room movement stays untouched. Camera-scale review remains a separate gate.



### Contrast-sheet integrity



- Hash checking alone does not make two backgrounds comparable: require identical

  integer crop bounds for each prop, offline state and valid recorded world scale.

  Label the recorded scale rather than hard-coding it. Reject duplicate/missing

  backgrounds and capture paths outside the evidence directory.

- Test sheet assembly pixel-for-pixel, plus deliberately invalid manifests. These

  checks protect review evidence, not visual acceptance. Old captures remain

  historical evidence; their file hashes do not prove the renderer is current.



### Classify offline repairs by construction



- Preserve grouped indicator topology when reconstructing unlit lenses.

  Anomaly's first small-indicator pass made three lamps read as a blank panel;

  the revised bounded slots retain their grouping without source glow. Review

  enlarged native surfaces and the offline card separately. Static lens shading

  is not a new animation, and highlight coverage alone cannot approve its design.



- Xeno's source comparison separates optical glass, curved strip lamps, sloping

  indicator faces and surrounding metal. A rectangle covering their combined

  bounds removes construction as well as emission. Fit the actual aperture and

  retain housing detail; preserve glass depth separately from active points.

- Do not generalize a successful hardware texture modulation to every surface:

  it can restore painted activity inside a lens. Capture the current renderer,

  record source-coordinate repair targets and keep before/after evidence scoped

  to the frames actually inspected.



- Xeno's material follow-up uses separate dark lens layers and local housing

  texture modulation. This restores construction but shifts indicator glass to

  muted olive; inspect and disclose that tradeoff. Do not call textured rectangles

  exact aperture masks. Six interior-detail checks across four rotations reject

  a deliberately flat fixture, while source coverage remains a separate test.



- Anomaly's broader hardware-modulation trial was visually rejected: dim violet

  strip lamps still read as powered. Preserve that failed render and keep only

  independently validated changes (here, the three optical lens interiors).

  Geometric coverage of source highlights does not prove their rendered emission

  is suppressed when the replacement draws the source texture again.



- Fit slanted lamps with source-space polygons, not enclosing rectangles.

  Anomaly's two platform corner lamps retain covered violet pixels while exposing

  surrounding metal again. Pair positive lamp points with negative housing points

  and the full source-highlight audit; none alone proves the complete contour.



- Holo's calibrator silhouette bridged empty space above a thin crossbar with

  diagonal floor wedges. Trace the component's stepped silhouette and retain

  its beam/optical plate; do not shrink the entire assembly. Check excluded floor

  points and retained hardware points alongside full effect containment.



- An enclosed pipe gap needs an actual omission, not a floor-colored overlay.

  Biodome partitions its source silhouette around a verified small opening,

  caches the resulting source polygons and draws them with the same registration.

  Preserve the whole assembly's collision reservation and test pipe/tank retention

  independently of background exclusion; a visual hole is not a new walking path.



### Intermittent graphical evidence



- Anomaly's 2560 exported fixture failed motion/pause comparisons while other

  graphical fixtures overlapped, then passed alone with identical PCK and checks.

  Preserve both runs. Prefer serial timing-sensitive captures while investigating;

  one isolated pass does not prove concurrency caused the earlier failure.



- Inspect full failed frames: Anomaly's paused pair contained the game menu in

  only one frame. Reject obstructing menus explicitly and preserve per-capture

  state (pause, clock, viewport, scroll, zoom). A real-menu negative control checks

  that diagnostic. Remaining motion failures without the menu still need separate

  investigation; do not attribute every mismatch to the first cause found.



- Scripted art-state fixtures now isolate Main's automatic/input callbacks and

  viewport GUI input; their economy, clocks and walker steps remain explicit.

  Inject Escape/W/Space to test isolation, and report that interactive controls

  and automatic time progression are outside this fixture's coverage. Do not

  change normal gameplay controls to stabilize diagnostic screenshots.



- Verify PNG dimensions, not requested CLI widths. Xeno/Anomaly material exports

  labelled 1280 and 1600 actually captured 2560x1440. Preserve their state evidence

  but retract multi-resolution coverage until exact-size reruns pass. Room crops

  and caller-written verification metadata cannot independently establish size.



- Isolate display preferences as well as saves before initializing Main. A

  windowed-mode assignment alone did not undo inherited fullscreen-size behavior;

  fixture-local unsaved settings plus clearing borderless mode produced actual

  1280x720 frames. Verify PNG IHDR independently in the export runner and preserve

  the original player preferences. Recheck all sizes, not only the default one.



### Composite room export assets



- A source/card decode does not verify separately composited characters. List

  extra PNG components with hashes and validate each inside the exported build.

- Keep original character pixels when replacing their environment. Register a

  silhouette independently instead of embedding the old background rectangle.

- Whole-assembly motion verifies aggregate animation only; it cannot establish

  every overlay independently. Keep component decoding and visual review distinct.



### Requested viewport is not captured viewport



- Put fixture windows in windowed mode before assigning their size. A retained

  window mode can defeat resizing while every gameplay assertion still passes.

- Assert each captured image's actual pixel dimensions against the request, and

  keep both values in evidence. Folder names and CLI arguments are not proof.

- Build review crops from actual frame geometry; a fixed crop from another

  viewport can contain only background even when the crossing itself passed.



## Preserve platforms when removing loop backgrounds



Trace source-space openings explicitly and partition the remaining render polygon

into simple pieces. This exposes the live room floor without changing immutable

raster donors, cable colors, platforms or collision footprints. Compare native

room and card consumers; never remove every dark region as presumed background.

Record reviewed openings and distinguish them from mechanical decks and shadows.



## Organic room composition — owner-directed revision



Room furnishing must describe activities and relationships, not an inventory arranged in four quadrants. The repeated two-small-props-in-front-of-each-host pilot is rejected even though its geometry tests passed. Do not use equal accessory counts, mirrored spacing, uniform host resizing or automatic front offsets as an acceptance shortcut.



Before production, author a room-specific composition with a focal activity, secondary work or rest area, circulation and deliberately quiet space. Assign every object a physical support: floor, shelf, tabletop, wall mount or equipment attachment. Small tabletop objects inherit the supporting surface's position, elevation and depth ordering; they are not independent floor obstacles. Tables, carts and lamps need their own grounded footprints. Never depict mugs, sample handling or tools as routinely placed on the floor to avoid implementing supports.



Layer the composition: architecture and utilities; floor paint, rugs, grates and cable covers; grounded furniture and equipment; supported working objects; restrained stateful lighting or equipment motion. Cables and hoses connect believable endpoints and avoid open doorways. Floor decoration is not collision geometry. Upright equipment remains south-facing; allow authored variation only where the asset and function support it.



Use unequal cluster sizes and function-specific spacing. Place a lamp where light is needed, a bin where waste is produced, a cart where someone can access it. Keep narrow corridors sparse and BRINE's chamber serene; natural composition does not mean filling every room to the same density. Preserve department materials and maintained condition.



Acceptance requires native visual review of relationships and hierarchy, not a prop-count threshold. Verify supported-object registration, four rotations, room/card agreement, actor access and occlusion, operating/offline lighting, and packaged asset availability. Technical success cannot override an owner rejection of composition.





### Supported furniture pilot: measured geometry and source provenance



The owner-rejected pairing scheme is replaced in the first three rooms by authored activity areas. Use `rooms/whole-room/room_dressing.gd` and room-specific JSON where suitable; the helper supports grounded furniture, host-drawn tabletop objects, source pivots/ground widths and floor-only service routing. Do not turn it into automatic scattering. A lamp overhang is visual geometry, not the full floor obstacle. Quarter-specific clearance adjustments need native review.



Confirm the canonical door topology before reserving aisles: Research Lab has one south port, so an offset preparation island can occupy space that a tee room needs for transit. Maintaining an unnecessary cross-shaped empty floor is not fidelity to this room.



After an image-generation edit, re-read native dimensions and alpha before reusing registrations. The Research island changed to 1312x1199 during its successful alpha edit. Maintenance alpha requests repeatedly retained painted checkerboards; its RGB atlas is sampled with explicit source silhouettes, including furniture gaps, and is not labeled alpha-cleaned. Validate those rendered edges visually. Keep raw failures and exact prompts; avoid repeating equivalent alpha requests indefinitely.



Record composition JSON hashes in `composition_assets` and raster hashes in `component_assets`. The packaged station fixture verifies both. `tools/audit_room_composition.gd` reports rotation bounds and floor overlaps, but cannot judge whether a room feels natural. See `docs/ORGANIC_ROOM_COMPOSITION.md` for implemented scope, evidence and remaining work.





### Supported furniture and alpha registration (2026-09-06)

Use tools/register_alpha_silhouette.py for read-only alpha-to-vector registration

when appropriate. It preserves the source raster and splits interior holes into

hole-free draw polygons. Reject painted checkerboards/opaque images; alpha channel

presence alone proves nothing. Thresholding is not suitable for all glass or haze.

Keep rejected generations and exact edit prompts. Bench-top objects should inherit

the host position and depth. Flush covers and drains belong on the floor layer,

without furniture collision. A successful route test or a new workbench does not

prove organic composition: inspect whether the old four-corner layout still dominates.



Layout lesson: audit footprints AFTER wall-containment adjustment in every quarter. Tall south-facing shelving can shift inward and collide with adjacent furniture even when canonical floor rectangles are separate. Storage v3 exposed this; v4 corrects the rack spacing/size and passes four-quarter checks.



Reuse lesson: mining turnaround can reuse registered workshop tools and furniture when their actual task matches; author the room placement, service endpoints and floor details independently. Keep donor RGB silhouette restrictions and provenance attached to the reuse.



Shared-furniture lesson: a recovery intake bench can use logistics scanning, manifest and containment equipment. Describe its actual contents accurately; do not call a reused closed case an open scrap bin. Under-surface storage adds detail without independent floor obstacles.



Command furnishing lesson: preserve finished charcoal/grey metal with restrained red trim and information-handling accessories. A chart cabinet is useful supported detail but does not satisfy a central operations composition; track those as separate work.



Topology lesson: Quarantine has east/west circulation, so the sealed north wall can hold preparation furniture between the berth and filters. Do not copy the north/south drone bay aisle assumption. Keep instruments supported and distinguish a sealed cooler from open specimen storage.



Habitation reuse lesson: book storage belongs between sleeping spaces and a reading lamp should serve a seat. Group shared furniture by use and check quarter-specific wall clamping; source integrity hashes alone do not prove packaged rendering.



Medical fixture lesson: original equipment may animate while added preparation furniture stays static. Check both contracts explicitly. A non-overlapping floor footprint can still produce overlapping visual capture bounds; adjust placement and preserve the failure instead of weakening the image-state check.



Service placement lesson: a technically valid cart positioned in front of a machine can repeat the rejected accessory staging. Prefer a working position alongside its equipment; drains belong to fluid-handling hosts, not every new furnishing.





Composition dependency audit: run `python tools/audit_composition_dependencies.py

rooms/production-ten/manifest.json rooms/whole-room/export-manifest.json` from the

checkout. It validates every profile texture against the declared source/components

and checks their hashes, normalizing Windows separators. The focused test exercises

undeclared textures and stale profile/texture hashes. It does not decode images,

prove packaged loading or establish composition quality. Custom drawing without a

profile (currently Lounge) remains separately covered by its asset manifest.



Reproduction evidence: compare recorded controller hashes before calling a later tour a regression reproduction. If the controller changed, a clean native tour proves only the current run; it does not explain an earlier packaged collision or replace fresh packaged verification.



Agriculture asset lesson: preserve seedlings, pruning tools and irrigation storage on real supports; inspect their gameplay scale after registration. A detailed source trolley can read too small when squeezed beside a large harvest unit. Record that limitation rather than calling a route pass visual acceptance.



Scale correction: Hydroponics trolley v2 increases world width 28 to 42 units without modifying or upscaling the source raster. Review the new native card and recheck circulation in every rotation when enlarging support furniture.



Renderer extension lesson: when an older room adapter is a shared superclass, add room-specific furnishings in a leaf view instead of injecting them into every inheriting room. Preserve its source-pixel transform for old machinery and use registered transforms only for new furniture.



Central-machine lesson: Reactor routes circulate around its core, so a contained north-side table can still obstruct the real walking path. Validate perimeter traversal before selecting the layout; preserve rejected placement evidence and use unoccupied service-corner space.



Medical Office lesson: its straight north/south sockets differ from Med Bay. Read the actual room topology before borrowing clinical furniture placement; side-wall reference storage can serve consultation while leaving the central route clear.



Cryo variant lesson: ordinary built-room furnishings must not silently populate discovered recovery wards. Keep that variant explicit and retain recovery tests. Static transfer supplies should stay static in economy-state comparisons while original machinery retains its effects.



Visual-gap lesson: compare full artwork bounds as well as floor footprints around tall vessels. The composition audit now reports visual_overlaps explicitly. Clone preparation required narrower furniture and quarter-specific positions to avoid both neighboring silhouettes; floor nonoverlap alone was insufficient.



Archive furniture lesson: removable data caddies and patch leads belong on protected work surfaces and storage trays. Use purpose-specific contents and quiet dark finishes; do not substitute workshop tools or general books for data-service equipment.



Composition review: a supported cart alone does not repair four isolated corner displays. Review the whole-room silhouette, stagger related activity areas, and connect real equipment endpoints with restrained services. Floor dressing must actually be called by the room floor renderer; a populated profile alone is insufficient. Keep technical route passes separate from natural-layout acceptance. When resizing a support assembly, review the size of its attached objects as well as their anchors; a fixed-size case can become oversized on a smaller lift. Marked staging space can stay partly open while a small case explains its purpose. Discover live furnishing helpers by their script identity, not a single variable name. Validate registered furniture IDs as well as mat, supported-object and cable endpoints; exercise a deliberately missing clinical host to prove alternate helper names are covered. Keep one authored footprint per equipment registration; post-registration overrides can silently undo a layout change. Inspect resolved native geometry before trusting a source-coordinate edit. During layout revisions, distinguish invariants from old composition assumptions in tests. Keep actual route and source-effect checks; replace fixed screen-position bands with registered-equipment containment when justified by the new arrangement, documenting the failed prior check. When reusing a furniture registration, replace donor quarter-position overrides along with the canonical footprint. Distinguish intentional lamp-over-table artwork overlap from overlapping floor obstacles. Reconcile the furnishing ledger against the current RoomDatabase identities before reporting coverage; concurrent additions must receive their own brief and evidence rather than disappear behind a historical room count. In narrow routing rooms, put service cabinets within the wall band and stagger lights along travel; preserve the passage silhouette and test actual connected traversal. Keep card export revisions selectable without overwriting prior evidence. For central apparatus rooms, add an explicit perimeter clearance check; a generic motion fixture does not prove that newly placed service furniture preserves circulation. Resolve room fiction from its current equipment and production brief before selecting decorations; legacy database names can differ from the implemented underwater function. For specialized servicing areas, generate a supported workbench assembly with recognizable discipline-specific tools and lower-shelf storage; preserve a complete silhouette and verify alpha before registration. Judge its contents at gameplay scale, not only in the large source. Service routes should take a plausible short path between their endpoints; inspect the resulting line at room scale and remove arbitrary zigzags before selecting a card. Inherited room views must explicitly replace parent furnishing profiles when they replace the equipment list; otherwise floor services can reference equipment that no longer exists. Quarter-specific positions should preserve the activity relationship as well as clearance: review the cart beside its serviced host in all four views, rather than treating any empty gap as an equivalent placement.



Underwater hull fitting lesson: see references/underwater-hull-fittings.md for the airlock study, separate wall/deck registration, actual-alpha cleanup and wall-bay validation.

Studio-versus-live lesson: the Studio deliberately shows more than the running game, so a failing layout or Studio test is usually enforcement working rather than a regression. Three owner decisions cause it — dressing and `library/common-` decorations are filtered out of live rooms by `RoomLayoutStore.is_common_decoration()`; free placement is the Studio default, so `issues()` reports nothing until the toolbar toggle is turned off; and wall decorations are paused wholesale in `decoration_props.gd`, which empties every riser fitting. Check those three before changing code, and when coverage exercises a paused feature, guard it behind the same flag instead of deleting it so it returns when the pause lifts. Placement envelopes are no longer duplicated: Studio and the live game both call `RoomLayoutStore.envelope_for()` and `door_lane()`, with the live values as the truth, so a placement accepted in Studio survives in game.

Fixture timing lesson: prefer waiting for observable state over a fixed delay. A fixed wait after a scene swap flaked under load, and the first replacement failed three times because it compared against a node the swap had already freed — poll the live scene for the state it should have reached, with a generous ceiling so a genuine failure still reports through the existing checks. When a test fails in a way you cannot explain, print the actual per-frame state with a temporary probe before editing it; two blind attempts cost more than one measurement.

Skill file encoding lesson: three reference files were Windows-1252, and one of those was mixed Windows-1252 and UTF-8. Converting a mixed file wholesale mangles the parts that were already correct, so decode per byte-run — UTF-8 first, Windows-1252 only for the bytes that fail — and confirm afterwards that no `Ã`/`â€` markers appeared. Garbled arrows and stray escape sequences in these files came from the same source.
