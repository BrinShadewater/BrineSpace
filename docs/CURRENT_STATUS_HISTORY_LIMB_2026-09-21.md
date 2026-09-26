# BrineSpace current status

Updated September 21, 2026. This page describes current direction and the latest
bounded evidence. Detailed chronology is preserved unchanged in
[status history](CURRENT_STATUS_HISTORY_2026-09-21.md); older entries are not a task
list or acceptance of later changes.

## Objective and accepted direction

Continue the bought-art migration, natural room furnishing, Bill's pixel-layer walk
repair, other observed animation repairs, bug fixes, polish and measured performance
work. Keep the bible, workflows and asset pipelines aligned with verified findings.
Local script-assisted pixel editing is authorized. **No Higgsfield without a new
explicit request.** No publication or new commit/push is requested in this work.

Use large and medium props in coherent work areas; avoid accessory scatter and
blanket upscaling. Preserve the owner's reference layouts: Research Lab, Mycelium
Nursery, Med Bay, Pressure Control, Crew Lounge, Mining Drone Bay, Ore Refinery,
Cryo Chamber, Listening Post and Xeno Lab. Owner library marks are user data.

The north star remains restoring an underwater station through satisfying placement
and interdependent systems. Normal play has paid building, resource failures and
hidden discoveries. Three functioning cycles stabilize patterns. Doctrines, timed
directives and scenario victory are retired; Conclude Expedition ends the loop.
Preserve these decisions and the prototype save format. See AGENTS.md and
[development notes](DEVELOPMENT_NOTES.md) before gameplay changes.

## Installed work

- **Bill:** enclosed joint pinholes corrected; side-view shoulders/arms now use
  preserved poses [0,1,2,5,2,1] in bare and helmet variants. Existing lower-body
  pixels, timing, stride and head registration retained during that change. A later
  targeted east passing-knee cleanup changes 15 pixels in each bare/helmet phase 2. Canonical builders reproduce
  the repair. West contact-pose ankle cleanup removes a cutout spur in 30 pixels
  per bare/helmet frame, preserving toe, sole and foot registration. Leg contours
  and overall gait quality remain unfinished. East phase 4 now also trims two knee-edge
  teeth (seven pixels each in bare/helmet); three focused tests and 240 native
  reference comparisons pass. See BILL_POSE_CLEANUP_HANDOFF_2026-09-21.md.
- **Salvage/construction drones:** tools articulate below rigid chassis instead of
  shearing the central winch; construction has distinct left/right joints. Both
  16-pose native guards pass and reject old code. Welding beams now share the tool
  transform. Hatch travel now blends scale to eliminate launch/return size jumps
  (six native boundary comparisons pass). One native construction trip completes
  all six phases and restores its dock. Mining/salvage also complete recharge,
  clearance and return. Clearance rendering now prefers exposed work faces and
  blends approach/return; native mining and underwater foundation checks pass. See
  DRONE_MOTION_REVIEW_2026-09-21.md.
- **Maintenance:** revision 05 tool-bench repair bay installed in four default and
  saved layouts. **Bio Lab:** revision 04 grouped work areas installed likewise.
  Both cards refreshed. Crew Hab retains its earlier provisional positive review.
- **Galley:** two adjoining serving counters added only to four saved layouts;
  existing saved arrangements differ from defaults and were preserved. Meal approaches
  now follow the two bought counter types and their copies; a headless gameplay
  fixture completes Bill's core-to-counter meal route in 92 clear steps. Card refreshed
  from those saves. All four effective layouts are now promoted to shipped defaults.
- **Library:** lab-20 registration corrected to remove a neighbouring table edge and
  restore the whole chair. Stable ID retained; source PNG unchanged.
- **Cold Store:** two saved rotations rearranged to expose freezer fronts; blue
  freezer aligns with stock rack and small container moves clear. Card refreshed.
  Inspection targets now follow bought freezer rectangles. Four views/640 walking
  samples, focused station checks and one 50-step gameplay inspection route pass.
  All four effective layouts are now promoted to defaults. See COLD_STORE_SERVICE_HANDOFF_2026-09-21.md.
- **Isolation Vault:** control cabinet grouped beside the battery rack in all four
  saved rotations, with concurrent-edit guards and a backup. Card refreshed and
  visually inspected. Four native views/640 walking samples pass. Defaults were
  promoted in a later parity-checked pass; owner visual acceptance remains separate.
  A subsequent live-game review found repeated view setup removed its saved props.
  Cleanup now runs only on geometry rebuild; 15 repeated/rotated setups pass and
  native station captures show the furniture retained. Cards alone missed this bug.
- **Runtime art:** migrated room/environment PNG roots repaired, including five
  foundation bindings. Export guards reject mismatched templates/unselected raw art.
- **Rendering:** projected equipment shadows batched per prop; nine native pixel
  comparisons match exactly. 100-room overview draw calls fall from 12,502 to 11,052.
  Rounded contact bands are unchanged; see performance notes for timing limits.
- **Diagnostics:** soak reports now count every slow frame and distinguish completed
  from requested cycles. No runtime optimization was justified by the latest small
  station budget result.
- **Layout cache:** application stamps now also check the last applied prop count.
  Partial/empty prop removal no longer masquerades as an unchanged saved layout.
  Focused removal, unchanged-fast-path and explicit-deletion checks pass, alongside
  the 15-setup Isolation Vault regression. No frame-rate improvement is claimed.

## Staged work and remaining priorities

1. Finish Bill's leg-contour and natural-motion review. Do not revive rejected
   whole-limb/warped-ankle studies merely because their mechanical checks passed.
   Higher-clearance and generic kneepad-overlay studies were also visually rejected;
   those studies were not installed. A targeted east phase-2 contour cleanup is now
   installed; continue individual knee review before raising the step.
   Other crew base walks have changing upper poses; supplemental/equipped/action
   and drone motion remain outside that audit. Review observed defects individually.
2. Continue native gameplay review of installed room pilots and their art at normal
   zoom. Technical checks and agent still review are not owner visual acceptance.
   Cold Store/Clone Lab looked coherent in the recent bounded review; no changes.
   Native 52% zoom review of Maintenance/Bio/Hab/Isolation supports keeping large
   prop scales; small desk items read mainly as texture. Evidence and unscaled
   room crops: output/room-gameplay-scale-2026-09-21/visual-review.json.
   This is agent review, not owner acceptance. Galley counters also remain visible
   in live captures; review exposed and corrected stale fixed meal locations.
   Observation Room now reads at the bought sofa, with matched sit/read/rise
   offsets and south-facing pose. Four-rotation checks and one 149-step curiosity
   route pass; native transition poses inspected. Veld/Branforth seated poses also
   inspected. Marsh needed a south-facing seated depth-metadata repair to prevent
   sofa occlusion; native preview and focused metadata guard pass. Modified sofa
   variants remain outside this visual check. See OBSERVATION_SEATING_HANDOFF_2026-09-21.md.
3. Research q2 has a confirmed disconnected route in the production Bill graph.
   A one-prop move restores it in the staged candidate; **owner layout unchanged**.
   Candidate: output/owner-room-references-2026-09-21/research-door-candidate.json.
   Pressure Control's gs-14 machine visibly extended beyond the room; a separate
   four-rotation candidate moves it 24 units inward and passes four views/640 samples.
   Saved owner layouts remain unchanged. Listening Post's warning concerns its fitted
   east-wall console; leave it for visual review rather than an automatic floor-bound
   correction. Evidence: output/owner-room-references-2026-09-21/pressure-correction/.
4. Optimize overview rendering from the verified 100-room native baseline: roughly
   12,500 draw calls, 23.93 ms render CPU/21.71 ms GPU versus 2.04 ms simulation.
   Layer isolation identifies the two floor passes as the largest initial target
   (roughly 2,700-2,800 calls each), followed by walls. A native component probe
   narrows the floor cost to equipment shadows: Research/Med Bay each use roughly
   88 shadow calls out of 93 incremental floor calls. Target equivalent shadow
   batching/caching for the remaining contact bands. Projected polygons now batch
   with bounded pixel parity. Profile camera now targets an occupied cell and checks
   visible coverage: 100/100 overview and 3/3 close room centers. See
   [native baseline](PERFORMANCE_BASELINE_2026-09-21.md).
   The fixture forces drawing and enables profiling, so total loop time is not
   normal gameplay FPS. Latest paid-operation fixture records 90/90 active-drone
   frames in each scenario (launch/outbound/work/return); docking and close drone
   articulation still need review. It grows to 101 rooms during the final close sample.
   The headless small station result below does not establish FPS. Normal paid-run pacing, opening
   power feedback and audio mix still need human review.
5. Refresh release packages after a stable milestone, then test on the owner's
   Apple Silicon Mac. Current packages predate the latest sprite/layout changes.
   Native Mac launch/gameplay/signature acceptance and notarization remain open.
6. Older unresolved owner notes remain traceable in the history: dialogue note 17
   needs a real-session trace; blurry-UI note 14 involves viewport/stretch direction;
   removing dead doctrine scaffolding is optional, not a reason to restore doctrines.

## Verification and limits

- Bill complete pack: **11,773 checks, zero failures**. Native bare/equipped
  candidate and post-integration equipped playback captured. Three focused Python
  surface tests pass; the standalone review command now reproduces all 24 selected
  side-view body/helmet frames instead of presenting stale frozen upper bodies; an injected frozen-torso mutation is rejected.
- Maintenance and Bio: four views/640 walking samples each pass. Galley candidate:
  four views/640 samples, plus eight reachable production meal-service points.
- Library: **10,507 props on 269 sheets** pass registration validation after lab-20.
- Other crew audit: **96 bare base-walk frames**, no canvas-edge contact; no exact
  frozen upper region in non-Bill rows. Still inventory is not temporal acceptance.
- Native large-station fixture now requires its requested room count; the old
  "100" case only reached 78. Corrected run reaches 50/100, zero fixture failures;
  Historical overview/close loop means were 79.91/12.69 ms under forced-draw profiling.
  Those close timings were invalid (empty view). The corrected native capture shows
  three room centers, 5.21/4.27 ms render CPU/GPU and 2,699 draw calls.
  Evidence: output/game-pass/2026-09-21-count-verified/large-render-profile.json.
- Modest station: **40 completed cycles, 800 frames**, 0.90 ms mean/12.9 ms worst
  simulation time, 137 route searches. Rendering excluded. Normal-run reporting
  check correctly records seven completed cycles/140 frames and zero logged errors.
- Windows package `brinespace-66abbef9bc1a8278`: scoped actual-release startup,
  simulation/F8 and exact-PCK checks passed for that older build.
- Mac Universal candidate `brinespace-97c09d09887b0d5b`: both architectures and
  executable permissions verified; exact PCK has 15,085 matching files. Ad-hoc local
  candidate only, not a native-tested or notarized release.

## Evidence and maintained workflow

[Art/release handoff](ART_AND_RELEASE_HANDOFF_2026-09-21.md),
[Bill review](BILL_WALK_REVIEW_2026-09-20.md),
[room pilot](ROOM_COMPOSITION_PILOT_2026-09-20.md),
[visual bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md),
[release workflow](RELEASE_WORKFLOW.md), [Mac plan](MAC_RELEASE_PLAN.md).

Use maintained skills/brinespace-room-pipeline and skills/brinespace-character-pipeline;
verified changes are synced to installed copies. Scope file searches away from output/.
Preserve existing owner edits; verify current keys before any saved-layout write.
Update the relevant section here at milestones; put experiment chronology in dated
reports instead of prepending repeated, conflicting status sections.

Focused Bill guard:
`python -m unittest discover -s tests -p test_bill_walk_surface.py`.
Godot subsystem routing: `python tools/run_tests.py --subsystem <name>`; use native
lanes for rendering. Python tests are invoked directly, not through the GD runner.

Fresh-profile furnishing parity: Galley, Isolation Vault and Cold Store now use
their reviewed effective layouts in defaults (12 entries). Native local-vs-fresh
comparison matches all 12 PNGs exactly; both runs pass 1,920 walking samples.
Player saved layouts and named owner reference defaults were unchanged. Evidence:
output/furnished-defaults-2026-09-21/. Existing release archives still predate this.

Cold Store near-counter service regression fixed: station destinations are exempt
from the wandering minimum distance. Native paid-build test passes all three crew,
stock-check completion/save/pause/suspension and 612 continuous walking samples.
Evidence: output/furnished-defaults-2026-09-21/test-cold-store-fixed.log.

Projected shadow geometry now uses a bounded footprint/rise cache. Nine native
parity cases with moved props and varied heights pass; isolated geometry work
drops from 191.6 ms to 7.6 ms per 20,000 calls. This is not an FPS measurement.
See SHADOW_CACHE_HANDOFF_2026-09-21.md.

Full-station shadow-cache comparison shows no clear render-time gain: 100-fit
CPU 22.122 vs 22.085 ms, identical draw calls; loop timings vary in both directions.
Both populated native fixtures pass. Keep the cache benefit scoped to geometry
construction; retained room rendering already avoids much repeated work.

Split-wall layout selection repaired for Storage Bay, Battery Array, Hydroponics,
Life Support, Data Archive, Command Center and Holographic Core: renderers now read
the canonical Studio room keys. 70 repeated/rotated setups, 28 native views and
4,480 walking samples pass. Seven cards refreshed; owner layout file unchanged.
Earlier station screenshots/performance fixtures predate this furnishing correction.
See SPLIT_LAYOUT_KEYS_HANDOFF_2026-09-21.md.

Storage Bay now has a consistent bought-prop layout in all four saved/default
rotations: left-side shelving and a grouped northeast crate/hand-truck area. Small
drum removed; clear circulation retained. Local and fresh renders match exactly,
640 walking samples each; native live view inspected and card refreshed. Only four
Storage owner entries changed, with backups. Owner visual acceptance remains open.
See STORAGE_COMPOSITION_HANDOFF_2026-09-21.md.

Single-wall helpers now resolve Studio catalog keys too. Anomaly/Radio rotation
restoration and Medical Office/Center saved-deletion handling repaired. Expanded
34-room/340-setup guard passes; native affected-room checks pass after medical
corrections. Twelve cards refreshed, no owner layout edits. See
WALL_LAYOUT_KEYS_HANDOFF_2026-09-21.md for scoped native results and initial failures.

Cast review board now reads selected crew catalogs, respects frame registration,
and labels unauthored actions. Focused native walk/carry capture completed with
zero coverage/join failures; this is not gait acceptance. See
SELECTED_CAST_REVIEW_HANDOFF_2026-09-21.md.

Carry-turn exit now resumes on its authored destination pose without stale gait
phase/travel. Actual Bill/Veld/Branforth bare/helmet endpoints and subsequent
distance phase pass 12 cases; Marsh lacks these turn clips. No new sprite pixels.
See CARRY_TURN_HANDOFF_2026-09-21.md. Ordinary Bill gait remains unfinished.

Ordinary swim-turn exits now also reset to the authored endpoint. Expanded
carry/swim/swim-carry playback regression passes 36 cases, with endpoint images
compared after pivot registration. No art changes or broad gait acceptance.

Newest Windows candidate 4035ce07d72e861f is not accepted: New Game reports two
empty-image errors. Traced to Storage prop sheets omitted by JSON quote scanning.
Manifest collector now parses JSON; six tests pass and all registered sources are
covered (61 additional assets). Repaired export and actual-release validation remain
pending. See RELEASE_JSON_REPAIR_HANDOFF_2026-09-21.md.

Repaired Windows candidate brinespace-e7c1ea935b573fd2 now passes maintained export,
exact-PCK audit (15,146 checked; zero discrepancies), actual release New Game,
simulation and F8 with zero engine errors. Gameplay/report captures inspected.
Location: builds/BrineSpace-layout-turns-fixed-2026-09-21. The external smoke now
fails on engine errors; the old faulty package is a verified negative control.
Matching Mac export remains pending; broader visual/gait acceptance remains open.
See RELEASE_JSON_REPAIR_HANDOFF_2026-09-21.md.

Matching Mac candidate brinespace-e7c1ea935b573fd2 is prepared in
builds/BrineSpace-mac-layout-turns-2026-09-21. Maintained wrapper fully exercised;
Universal 2 structure/permissions pass and exact PCK checks 15,146 assets with zero
discrepancies. README/checklist and hashes included. Native Mac launch, signing
acceptance and gameplay remain untested. See MAC_LAYOUT_TURNS_HANDOFF_2026-09-21.md.

Bill cadence diagnosis: all 12 selected side poses match the prior reviewed pixels.
An uninstalled 12-pose source-layer study preserves the six original endpoints per
side, but inspected midpoints retain the bulky knee silhouette. No production
change or motion acceptance. Next repair should target a representative passing-leg
pose before clip expansion. See BILL_GAIT_DIAGNOSIS_2026-09-21.md.

Bill passing-pose candidate: one built-in image edit plus deterministic registration
improves the inspected east phase2 knee silhouette, preserving original upper body
and boots exactly. Raw source/prompt and60native diagnostic captures retained in
output/bill-passing-pose-2026-09-21. Uninstalled: neighboring poses still need coherent
treatment and temporal review. See BILL_PASSING_POSE_HANDOFF_2026-09-21.md.

Bill source study now covers east phases1/2/3 with cleaner knee/shin treatment.
Articulated foot masks correct the earlier band-only boot-preservation limitation;
protected source pixels match exactly. Native partial-clip captures completed with
bare/helmet variants, no engine errors. Still uninstalled; phases0/4/5 and whole-loop
review remain. See BILL_ADJACENT_POSES_HANDOFF_2026-09-21.md.

Bill east candidate now covers all six knee/shin poses, retaining original upper
body and articulated feet with matching palette. Bare/helmet native captures and
loop GIF generated. Uninstalled: whole-loop/leg-order review (especially phase4)
and independent west repair remain. See BILL_EAST_LOOP_HANDOFF_2026-09-21.md.

East candidate foot-bounds-v2 now preserves original transparency as well as boot
pixels, closing the opaque-mask-only limitation. 24preview frames pass scoped
alpha/palette/protected-region checks;60native captures regenerated. Still no
production change or full gait acceptance. Owner treatment feedback requested.
See the latest section of BILL_EAST_LOOP_HANDOFF_2026-09-21.md.

Current restored-layout performance fixture passes native50/100room, visible-center
and active-drone checks with no engine errors. 100-close render CPU/GPU5.28/4.16ms;
100-overview20.04/17.89ms (instrumented, not FPS). Load shows365msCPU/398msfirstframe,
zoom-fit190msfirstframe. These are current baselines, not claimed improvements.
An isolated adjacency optimization remains uninstalled; load breakdown is the next
performance target. See PERFORMANCE_BASELINE_2026-09-21.md latest section.

Companion checkpoint restore now reuses loaded textures while creating fresh actor
and playback state.812texture/isolation checks, companion save/legacy tests and
native staged restore pass. Same100-room synchronous restore probe drops374->75ms;
normal Continue is staged, so this is not a claimed Continue latency or FPS metric.
Existing Windows/Mac packages predate this code change. See
COMPANION_RESTORE_ART_HANDOFF_2026-09-21.md. Bill/room polish remains unfinished.

Human clearance loaders now read selected-revision profiles directly, removing
three redundant legacy-source reads without changing collision envelopes.336scoped
clear/blocked checks and the existing doorway/smoothing regression pass. Evidence:
output/selected-clearance-2026-09-21/. No new art installation or build export.


Battery Array r3 installed in four saved/default entries, with backups and all other
layouts preserved. Larger primary racks and grouped service equipment replace scatter.
Saved/fresh four-view renders match; each passes640walking samples. Live52-percent
view and refreshed card inspected. Owner visual acceptance remains open; no export.
See BATTERY_COMPOSITION_HANDOFF_2026-09-21.md.

Bill candidate review found apparent knee-pad leg switching at crossings. A shared
phase0 layer study fails joint continuity due to missing occluded source fabric.
Both remain uninstalled; complete limb-source coverage is the next repair target.
See BILL_EAST_LOOP_HANDOFF_2026-09-21.md latest section.

Bill now has an uninstalled complete near/far limb-source study from built-in
imagegen. Continuous fabric addresses missing occluded patches; source registration
and full-cycle verification remain. Raw source/prompt preserved; no Higgsfield.
See BILL_EAST_LOOP_HANDOFF_2026-09-21.md latest section.

Complete-limb Bill candidate now has all six east poses registered to existing
joints, with original upper/boots protected.24preview frame checks and60native
captures pass; source board/frame033 inspected. Uninstalled; full motion/west and
canonical integration remain. See BILL_EAST_LOOP_HANDOFF_2026-09-21.md.

Bill independent west limbs now join the east candidate:24bare/helmet frames pass
protected-band/palette/alpha checks and60native captures complete. Both directions
remain uninstalled pending motion/style review and canonical integration. Evidence:
output/bill-bidirectional-limbs-2026-09-21. No Higgsfield.

Bill limb candidate now has retained project sources and a deterministic builder
(tools/build_bill_limb_candidate.py). All24rebuilt frames match reviewed candidates
exactly; production bindings remain unchanged. Motion/style acceptance and actual
integration remain open. See BILL_LIMB_BUILD_HANDOFF_2026-09-21.md.

Bill limb surfaces are now INTEGRATED for playtesting, superseding the uninstalled
candidate entries above. Exactly24walk PNGs changed; all other generated assets
and metadata unchanged. Full rebuild,3surface tests, complete2214frame validator
and60native captures pass. Archived construction-source lookup repaired without
changing frozen hashes. Owner motion/expedition review remains open; no export.
See BILL_LIMB_INTEGRATION_2026-09-21.md.

Installed Bill station fixture captures walk/idle/kneel/repair/stand without errors;
four-rotation doorway/smoothing regression passes. Apparent open-floor repair traced
to a valid current shelf target26units away, not a removed prop. Visual relationship
could be clearer; no behavior change. See BILL_LIMB_INTEGRATION_2026-09-21.md.

Windows playtest brinespace-1e25ea27901c0eae is ready in
builds/BrineSpace-limb-polish-2026-09-21. Export/exactPCK15149assets/actualrelease
NewGame+simulation+F8 pass with zero errors; screenshots inspected. Includes Bill,
Battery and restore updates. Matching Mac refresh next; broader visual/gameplay
acceptance remains open. See LIMB_POLISH_RELEASE_HANDOFF_2026-09-21.md.

Matching Mac limb-polish candidate1e25ea27901c0eae is ready in
builds/BrineSpace-mac-limb-polish-2026-09-21. Maintained exporter, Universal2/permissions
and exactPCK15149assets pass. README/hashes included. Native Apple Silicon gameplay
and signing acceptance remain untested. See MAC_LIMB_RELEASE_HANDOFF_2026-09-21.md.

Data Archive composition installed in four saved/default entries: matched server
pairs and grouped terminal/filing station. Other layouts preserved; saved/fresh
views match and each passes640walking samples. Live scale and refreshed card
reviewed. Owner acceptance open; current packaged builds predate this change.
See DATA_ARCHIVE_COMPOSITION_HANDOFF_2026-09-21.md.

Life Support composition installed in four saved/default keys: matched tanks,
larger air handler, compressor and monitoring desk. Other owner data preserved.
Saved/fresh renders match; each passes640walking samples; live scale/card reviewed.
Owner acceptance open. Windows/Mac packages predate this and Data Archive updates.
See LIFE_SUPPORT_COMPOSITION_HANDOFF_2026-09-21.md.
