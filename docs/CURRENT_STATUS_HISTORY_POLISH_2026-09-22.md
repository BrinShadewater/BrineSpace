# BrineSpace current status

Updated September 22, 2026. This is the current entry point, not an experiment log.
Prior notes are preserved verbatim in [earlier history](CURRENT_STATUS_HISTORY_2026-09-21.md)
and [limb/room/release history](CURRENT_STATUS_HISTORY_LIMB_2026-09-21.md).

## Objective and constraints

Continue natural bought-art furnishing, Bill's pixel-layer and motion repair,
other observed animation fixes, bug fixes and measured performance work. Maintain
the bible, skills and pipelines. The broad goal is unfinished.

Use large and medium props in coherent work areas. Avoid accessory scatter and
blanket upscaling. Preserve owner layouts: Research Lab, Mycelium Nursery, Med Bay,
Pressure Control, Crew Lounge, Mining Drone Bay, Ore Refinery, Cryo Chamber,
Listening Post and Xeno Lab. Library marks are owner data. Local deterministic
pixel editing is authorized. **No Higgsfield without a fresh explicit request.**
No commit, push or publication is requested.

Normal play retains paid building, resource failures, hidden discoveries, three-cycle
pattern stabilization and Conclude Expedition. Doctrines, timed directives and
scenario victory stay retired. Preserve prototype saves; avoid broad refactoring.
See AGENTS.md and [development notes](DEVELOPMENT_NOTES.md) before gameplay changes.

## Installed animation and runtime work

Life Support's reviewed desk now has an exact keyboard-side approach and standing
console action. Bill's native chooser/arrival view is reviewed; 48 shared room
activity cases pass, including all human crew/four Life Support rotations and
focused save/interruption checks. A 28-second normal-process observation now
captures approach, three completed work cycles and curiosity-driven departure:
239 samples, stable contact and connected limbs in the inspected room-scale
sequence. Owner and broader autonomous acceptance remain open. No furniture or
source art changed.
Follow-up fixes curiosity-driven console work continuing after power loss:
regression reproduced before the fix; all 48 activity cases pass afterward.
Moved-furniture service-point geometry is checked. Restore now cancels an active
console action whose saved contact no longer matches current furniture, preserving
safe position and needs. Stale/current contact checks pass all 12 human/quarter
console cases within the 48-case suite; other historical actions remain separate.
[Console integration](LIFE_SUPPORT_CONSOLE_CONTACT_2026-09-22.md),
[original contact diagnosis](BILL_MAINTENANCE_CONTACT_REVIEW_2026-09-22.md).

Paid native observation now spans a midpoint disk restore: exact idle position,
state, resources and cycle preserved; normal Resume then advances through cycles
7-9 with autonomous movement. The station survives cycles 4-9 under paid rules.
1110 crops include a self-selected south kneel/work/stand/departure, reviewed at
native scale. This is bounded fixture evidence, not human/owner acceptance.
The export collector also omits Branforth's specific new authoring study from
broad scans; eight collector tests pass and all runtime locker frames remain.
[Observation and packaging scope](EXPEDITION_RESUME_REVIEW_2026-09-22.md).

Airlock shelf helmets now match each human's fitted visible dimensions and keep
that fit through the return handoff. Native continuous actions pass all 12
actor/quarter combinations (2217 travel samples); ten source-dimension/selection
checks pass, including no geometry lookup in empty airlocks. The airlock card is
refreshed. No owner layouts or character art changed in this pass. Included in the
current test packages; owner visual acceptance remains open. [Shelf fit evidence](AIRLOCK_SHELF_FIT_2026-09-22.md).

Branforth's locker identity repair is installed: 20 interior frames replaced;
four exact standing endpoints and 2181 other runtime files unchanged. Native
four-quarter actions pass 739 travel samples, 360 captures and selected-pixel
checks. Independent canonical repeat reproduces all 2201 runtime files exactly.
Archived-source resolution and atomic writes repair two rebuild failures; validators
now explicitly cover existing bunk/berth supplements. Veld's reviewed art remains
unchanged. Current packages include these repairs; owner acceptance remains open.
[Integration and evidence](BRANFORTH_LOCKER_IDENTITY_INTEGRATION_2026-09-22.md).

Bill locker identity repair is installed: 24 frames now use one coherent source
with exact current standing endpoints and unchanged handoff timing. The other
2233 runtime PNG/JSON files remain byte-identical. Native four-quarter actions pass
739 travel samples, 360 captures and exact selected-texture checks. Full validation
passes 2244 frame references, including explicit bunk contracts. Independent full
rebuild reproduces all 2257 runtime files exactly. Current packaged builds include
this repair; owner motion acceptance remains open.
[Integration and evidence](BILL_LOCKER_IDENTITY_INTEGRATION_2026-09-22.md).

Current Windows and Mac test packages are **brinespace-b0d1640cfe18c6fc**. See
Current test builds below for paths, verification scope and native Mac limitations.

Four-crew autonomous process review now passes 3600 updates / 180 simulated seconds:
every crew sleeps and rises, maximum one occupant. Fixed a rested actor repeatedly
reusing the bed while nearby colleagues remained at maximum fatigue. Fifteen
centered native phase captures support contact review. Controlled power and stopped
economy timer mean this is not full expedition acceptance.
[Sharing review](BUNK_MULTI_CREW_REVIEW_2026-09-22.md).
Priority now also requires a reachable bed; disconnected peers cannot hold it.
Twelve eligibility checks and the repeated four-crew scenario pass. Priority
queries are cached within each synchronous choice, with no persistent queue.
[Eligibility fix](BUNK_ELIGIBILITY_FIX_2026-09-22.md).

Marsh's bought-bunk profile is installed alongside his working legacy berth.
Normal arrival, seven disk restores, exact rendered frames, interruption, shared
claims and low-battery rise-before-charging checks pass. Legacy berth, battery
routes and 507 generic sleep checks pass. All four cast now have profiles for the
reviewed unmirrored bought bunk; other sizes/orientations and broader autonomous
acceptance remain separate. [Marsh integration](MARSH_BOUGHT_BUNK_INTEGRATION_2026-09-22.md).


Bill's bare/equipped bought-bunk profile is installed with the reduced helmet fit.
Normal arrival, shared claims, fourteen disk restores, interruption and completion
pass. Native review also fixed cached standing-state rendering after a paused
restore. Full canonical rebuild reproduces all 2431 inventoried files exactly;
movement clearance is unchanged. [Bill integration](BILL_BUNK_INTEGRATION_2026-09-22.md).


Installed September 22: bought-bunk destination claims prevent Veld/Branforth
selecting the same empty bed while another crew member is en route. Claims derive
from live routes/rest stages, disappear on abandonment/death and add no save data.
The native Branforth controller regression, including two-crew choice and release,
passes. [Shared bunk routing](BUNK_CLAIM_FIX_2026-09-22.md).

Installed September 22: Bill, Veld and Branforth reverse only completed lie-down
motion when service is interrupted, preventing a fully reclined pose jump. The
507-check regression still passes after Veld's integration.
[Interruption fix](SLEEP_INTERRUPTION_FIX_2026-09-22.md).

Installed: Marsh's legacy berth profile and compound cabinet collision preserve
close approach, seated contact, entry/rise and interruption. Native arrival, five
disk restores, pause, low-battery exit and invalid-save checks pass again after
Veld's save integration. Earlier seeded travel evidence remains in the
[Marsh handoff](MARSH_BERTH_INTEGRATION_2026-09-21.md).

Installed September 22: Veld uses the reviewed bought orange bunk at its authored,
unmirrored size. Her seven-frame 1.84s entry/reverse exit and sleeping hold have
bare and helmeted runtime catalogs, phase-specific foreground depth and preserved
contact on save/restore. Normal chooser/arrival, fourteen disk restores, pause,
partial interruption, completion, invalid saves and unsuitable bunk rejection pass.
Rebuilding the supplement and finalizing clearance changes none of 18 inventoried
files. Native entry and resting captures were inspected. This is a controlled
station fixture, not a full expedition or packaged-build acceptance.
[Veld integration](VELD_BUNK_INTEGRATION_2026-09-22.md).

Bought-bunk foreground rendering is installed in direct and retained queues,
including sideways-move cache invalidation. Earlier exact parity, 17 layer checks
and 36 activity cases remain recorded in the
[layer handoff](BOUGHT_BUNK_LAYER_INTEGRATION_2026-09-22.md).
Branforth now also has installed bare/equipped entry, sleep and exit. Normal
chooser/arrival, fourteen disk restores, pause, interruption, completion and invalid
saves pass; rendered contact frames match his exact source pixels. Veld's regression
and 507 generic sleep checks pass after integration. The 18-file supplement rebuild
is identical and leaves movement clearance unchanged. Marsh is also integrated as recorded above; this does not imply coverage of other
bunk sizes/orientations.
[Branforth integration](BRANFORTH_BUNK_INTEGRATION_2026-09-22.md). Owner layouts were
not changed. Source studies and earlier rejected contact candidates remain in the
[contact history](BOUGHT_BUNK_CONTACT_2026-09-21.md). Release packages predate this work.

Observation Room saved/default reconciliation is installed: four effective keys,
every other room preserved, both four-view/640-sample native runs pass and eight
RGBA comparisons match the reviewed saved layout. Card refreshed and reviewed.
The q3 watch interaction now selects a clear nearby point; eight read/watch route
checks and sofa regression tests pass. Autonomous activity and release acceptance
remain separate. See the saved/default audit below for evidence.

Saved/default audit (September 21): eight unprotected room types retain substantive
overrides; two additional raw differences are numeric rounding only. Fixed review
catalog identity and incorrect corner/tee door masks. Corrected default corridors
pass 12 views/1920 samples. Saved straight-corridor failures are now traced to a
six-pixel clear band missed by the Studio's 16px graph; a 4px probe finds routes.
Production corridor geometry excludes these props from crew collision. Keep the
cramped furnishing as a visual/Studio issue, not a proven live navigation bug.
Earlier 29/32 image comparisons included misidentified corner/tee views.
No bulk promotion was performed. Ten owner rooms remain untouched.
[Audit and next steps](LAYOUT_DEFAULT_AUDIT_2026-09-21.md).

Airlock R2 is installed: restore the functional chamber/hatch removed by saved
null overrides and move bought supplies out of the wet area. Four native views and
640 walking samples pass; R1's blocked east approach was rejected. R2's four-quarter
static cycle poses, dry exclusion, production locker-point clearance and shelf
visibility checks pass. Four complete effective Airlock keys promoted to saved and
default layouts; every other key preserved. Both installed four-view/640-sample
runs pass and all eight native comparisons match R2 exactly. Card rebaked and
visually reviewed. The subsequent native Bill review passes four rotations, 743
travel samples, ten interlock phases, pause/power interruption and disk restores.
Eight continuous equip/remove traces (360 samples) exposed a visual identity
mismatch between removal, equip and standing. The replacement is now installed
as described above; other humans and packaged handoff verification remain
separate. [Live review and visual finding](AIRLOCK_LIVE_REVIEW_2026-09-22.md).

**Historical checkpoint: brinespace-867eac6b1b17b4fc.** Windows and Mac
now include the later Bill endpoints/north-west work repairs, both power-room
layouts/cards and door-edge reuse. Both exact PCK audits pass (15151 assets, zero
missing/changed/remapped/unexpected); actual Windows EXE passes with debug=false,
zero failures and empty stderr. Mac Universal2 structure passes; native Mac remains
unverified. Packages below describing f2ec as current are historical checkpoints.
[Historical release evidence](WORK_POLISH_RELEASE_2026-09-21.md).

Power-room grouping R4 is installed: Turbine supports are grouped by quarter;
Heat Recovery's process module and controls form a pair with a clear service aisle.
Eight saved/default keys changed; every other key is preserved. Both cards refreshed.
Each native composition run passes eight views/1280 walking samples; sixteen
installed saved/default image comparisons match the candidate exactly. Both machines
pass four-quarter operating/offline/held-clock checks; gameplay-scale views reviewed
in an isolated funded fixture. Owner visual acceptance remains
open. R2's blocked west approach was rejected. Release refresh is now complete above.
[Integration handoff](POWER_ROOM_GROUPING_2026-09-21.md).

**West moving work identity is now revised too:** canonical-reference lowering
poses preserve slimmer suit proportions and a planted front boot; wrench work
changes only arms/tool over fixed anatomy. Exact idle endpoints and smaller helmet
remain selected.32west-action PNGs changed;4427other runtime files unchanged.
Ten focused tests,full2214-frame validation and11773consumer checks pass. Native
171-sample sequence matches the reviewed candidate. Paid west capture covers71
images at an explicitly selected available service point through kneel/work/stand
and departure, with normal costs/failures. Both north/west work repairs are now
installed; owner visual and ordinary-expedition acceptance remain open. Three
built-in image calls; no Higgsfield. Current packages predate these repairs.
[West identity handoff](BILL_WEST_WORK_IDENTITY_2026-09-21.md).

**North moving work identity is now revised:** canonical-reference lowering poses
retain the small backpack and strap layout; the tool loop moves only arms while
body/legs stay fixed. Exact idle endpoints and smaller helmet remain selected.
32 north-action PNGs changed; 4427 other inventoried runtime files unchanged.
Nine focused tests, full 2214-frame validation and 11773 consumer checks pass.
Native 171-sample sequence matches the reviewed candidate exactly. Paid north
service capture covers 71 images through kneel/work/stand/departure with normal
costs/failures; its target was explicitly selected, not an ordinary expedition.
West moving work identity is revised above; owner acceptance remains open. Three built-in
image calls, no Higgsfield. Current packages predate this repair.
[North identity handoff](BILL_NORTH_WORK_IDENTITY_2026-09-21.md).

**North/west fully standing work endpoints now match canonical idle**, in bare
and smaller-helmet variants. Eight PNGs changed; 4451 other inventoried runtime
files stayed identical. Profile-pivot alignment preserves scale and registration.
Seven focused tests, full 2214-frame validation and 11773 consumer checks pass.
Installed native review covers 171 samples/eight variants and matches the staged
candidate exactly. North and west moving work poses are revised above; owner acceptance remains open.
The f2ec1eb651c14137 packages predate these eight endpoint changes.
[Endpoint handoff](BILL_WORK_ENDPOINTS_2026-09-21.md).

**Bill's normal helmet is now about 14% smaller overall**, following the owner's
clarification. Shell height is capped at 48px (previously 56px), keeping the
original registration canvas and visor anchor; already-compact fits stay unchanged.
178 helmet PNGs changed; 4282 other inventoried runtime files stayed identical.
All bare-body art is unchanged. Six walk tests, two helmet-fit tests, 2214-frame
validation and 11773 consumer checks pass. Native transition review covers 171
samples across four directions and both equipment states, with zero missing
textures and exact bare-render parity. Historical size/hash statements below
refer to their dated checkpoints; this fit supersedes their normal helmet sizes.
[Helmet-size handoff](BILL_HELMET_SIZE_2026-09-21.md).

The four-direction walk/idle/work transition review is complete for the scripted
production-player sequence. North and west work identity are revised above;
owner visual acceptance and ordinary expedition review remain open.
[Transition review](BILL_WALK_TRANSITION_REVIEW_2026-09-21.md).
Prior release refresh completed for build f2ec1eb651c14137: matching Windows and Mac
packages include all four walks and the smaller helmet. Both exact PCK audits
and actual Windows EXE checks pass. Native Mac testing remains open.
[Release evidence](HELMET_RELEASE_2026-09-21.md).

**Bill north walk is now installed:** canonical upper-body, arm and helmet pixels
are retained under recorded translations, with a connected pelvis/leg transfer
from the motion study. No separate joint transforms; speed and stride unchanged.
Exactly12PNGs changed;4448other runtime files unchanged. Six surface tests,
2214-frame validation,11773consumer checks and paid native capture (480samples /
261north walks) pass. Full generated-body drafts remain rejected. All four walk
directions now have selected repairs; owner visual and ordinary-expedition review
remain open. Foot locking is not established; do not change speed merely to fit
opaque bounds. [Integration](BILL_NORTH_WALK_INTEGRATION_2026-09-21.md).
[Earlier source study](BILL_NORTH_CONTACT_STUDY_2026-09-21.md).

Four-direction gait follow-up: 48 clock/turn cases pass. South order
[0,4,5,3,1,2] is now installed in both equipment states: eight PNGs changed,
4452 other runtime files unchanged. Five surface tests, 2214-frame validation,
11773 consumer checks and paid native capture (480 samples / 270 south walks)
pass. Original whole-pose pixels, timing and stride are preserved. North is addressed
above; anatomical foot locking and owner visual acceptance remain open. These walk integrations are included in the current test packages.
[Integration](BILL_SOUTH_WALK_ORDER_INTEGRATION_2026-09-21.md).
[Earlier study](BILL_FOUR_DIRECTION_GAIT_AUDIT_2026-09-21.md).

- **Bill east walk is now installed:** six independently authored alternating
  connected poses, directional gear and 46x56 per-pose helmets. Exactly 12 PNGs
  changed; 4448 other runtime files unchanged. Four surface tests, 2214-frame
  validation and 11773 consumer checks pass. Installed paid station: 480 samples,
  251 unpaused east walks with actual getter verification and no overrides.
  Separate native bare/helmet capture covers 27 frames. Both side directions now
  select the new recipes; owner gait acceptance and world-space foot locking
  remain open. Current test packages include both integrations.
  [Evidence](BILL_EAST_WALK_INTEGRATION_2026-09-21.md).

- **Bill west walk:** six alternating connected poses with closer suit detail and
  normal-size per-pose helmets are now selected. Exactly12PNG changes;4448other
  runtime art/metadata files unchanged. Four surface tests,2214-frame validation
  and11773loader checks pass. Installed paid station:480samples,82unpaused west
  walks with actual getter verification and no candidate overrides. A separate
  well-lit native production-player clip covers27frames. East was unchanged at that checkpoint; see its later integration above;
  owner gait acceptance and anatomical foot locking remain open. Current exports include this integration. [Evidence](BILL_WEST_WALK_INTEGRATION_2026-09-21.md).
- **Earlier side-walk recovery:** connected original east/west poses replaced the local
  limb composite rejected by the owner for disjointed feet. Canonical rebuild and
  normal review CLI select complete poses and per-pose helmet registration.
  Exactly24bare/helmet PNGs changed;2239other art/metadata files are byte-identical.
  Full2214-frame validation, three surface tests and11773consumer checks pass.
  Paid station captures cover240west and125east walking samples, plus115south
  samples after the east run turns. Native controlled
  review covers both directions/equipment variants. Owner gait acceptance, full
  foot-contact review and action consistency remain open. The west work-body
  discrepancy identified in the transition review is addressed below.
  The mixed-surface and18-pose studies are historical, not pending installations.
  [Connected-source integration](BILL_CONNECTED_SOURCE_REVIEW_2026-09-21.md).
  Normal goal selection now stays idle until movement starts, removing the
  stationary wrong-facing walk flash after work. Paid native action captures cover
  north before/south after; Veld/Branforth pass. Bill's broad check retains the known
  protected Research q2 clearance failure. South stand-to-idle body bulk is now repaired
  by the canonical-source integration below. Current polish exports include these changes.
  [Departure/contact evidence](BILL_DEPARTURE_CONTACT_REVIEW_2026-09-21.md).
  West work helmet now retains the standing48x56 size instead of shrinking to34x40.
  Only18equipped west-action PNGs and fit registration changed; library/shell-pixel
  checks and198-frame native action capture pass. North/south work fits are now
  corrected too:36equipped PNGs changed, with matching shell-pixel/library checks
  and198-frame native action captures per direction. Body-style continuity remains
  separate. [North/south verification](BILL_WORK_HELMET_CONTINUITY_2026-09-21.md).
  [Helmet continuity](BILL_WEST_HELMET_SIZE_2026-09-21.md).
  West work body now uses the closer canonical-identity source: six connected
  lowering poses, arm-only work and reversed stand, with normal-size helmets.
  Exactly36PNG changes match native-reviewed candidates; all other runtime art and
  clearance remain unchanged. Continuity/helmet/library tests and11773loader checks
  pass. Corrected native capture covers198frames per equipment state; owner and
  ordinary-expedition acceptance remain open.
  [Current west integration](BILL_WEST_STYLE_INTEGRATION_2026-09-21.md).
  [Style-source study](BILL_WEST_STYLE_STUDY_2026-09-21.md).
  [Held-pose study](BILL_HELD_POSE_STUDY_2026-09-21.md).
  **South kneel/repair/stand now uses canonical-identity sources:**36bare/helmet
  images replace the broader action body. First kneel/final stand exactly match
  current idle at shared pivot; work changes hands only. Full2214-frame validation,
  continuity/shell tests and11773consumer checks pass. Independent installed native
  capture spans198frames per equipment state,0failures. Native fixture acceptance
  is separate from owner/ordinary-expedition acceptance. Current polish exports include it.
  [Current south integration](BILL_SOUTH_STYLE_INTEGRATION_2026-09-21.md).
  [Earlier south integration](BILL_SOUTH_ACTION_INTEGRATION_2026-09-21.md) is superseded.
  **North kneel/repair/stand is installed:** 36 bare/helmet PNGs replace the old
  action style and height pop, with corrected planted-foot registration. Full rebuild
  and validation pass; installed native capture covers 198 frames per equipment state.
  All other generated files remain unchanged. East endpoints already match.
  [North integration](BILL_NORTH_ACTION_INTEGRATION_2026-09-21.md).
  **West kneel/repair/stand is installed:** another 36 bare/helmet PNGs now use
  independent current-style art, planted forward-boot registration and matched work
  endpoints. Full validation and installed native captures pass (198 frames per
  equipment state). No other generated files changed. The repaired action family
  still needs owner motion and normal expedition review.
  The previous [west integration](BILL_WEST_ACTION_INTEGRATION_2026-09-21.md)
  is superseded by the canonical-identity source above.
  [Directional evidence](BILL_REMAINING_ACTION_REVIEW_2026-09-21.md).
- **Drones:** rigid chassis, articulated tools, attached welding beams and continuous
  hatch scaling installed; bounded native trips/phase guards pass.
  [Scope and remaining review](DRONE_MOTION_REVIEW_2026-09-21.md).
- **Carry/swim turns:** destination phase/travel reset and authored endpoint handoff
  verified in 36 actor/equipment cases. No ordinary-walk turn clip was added.
  [Turn handoff](CARRY_TURN_HANDOFF_2026-09-21.md).
- **Restore:** companions reuse same-identity textures in fresh actors with independent
  mutable state. Scoped synchronous 100-room probe dropped about 374 to 75 ms; this
  is not normal Continue latency or FPS. Companion and native staged-restore checks
  pass. Human clearance loaders now read selected profiles directly without changing
  envelopes. [Restore evidence](COMPANION_RESTORE_ART_HANDOFF_2026-09-21.md).
- **Layout/render correctness:** canonical Studio keys, saved deletion handling,
  repeated-setup furniture retention and prop-count cache checks repaired. Migrated
  runtime art bindings and release JSON dependency discovery repaired. See
  [split keys](SPLIT_LAYOUT_KEYS_HANDOFF_2026-09-21.md),
  [wall keys](WALL_LAYOUT_KEYS_HANDOFF_2026-09-21.md) and
  [release dependency repair](RELEASE_JSON_REPAIR_HANDOFF_2026-09-21.md).

## Room composition and library

Biodome polish follow-up is installed: one medium bought shrub trough replaces
loose-plant scatter, with the basin grouped near seating. Four saved/default keys
changed; all other layouts and library JSON remain unchanged. Four native views,
640 walking samples, zero visual overlaps and exact installed/candidate RGBA parity
pass. Card and Biodome ledger are refreshed. Owner visual acceptance remains open.
[Review and staged evidence](BIODOME_POLISH_REVIEW_2026-09-22.md).

Maintenance revision 05 and Bio Lab revision 04 are already installed; do not restart
from their rejected first pilot. Crew Hab retains provisional positive owner feedback.
Galley, Cold Store and Isolation Vault have matching saved/default furnishing;
Cold Store and Galley service targets follow bought equipment. Observation seating
follows the sofa, including the corrected Marsh seated depth.

Storage Bay, Battery Array, Data Archive and Life Support now use coherent large/medium
work groups, with four saved/default entries each, guarded backups and refreshed cards.
Their four-view navigation checks and fresh-profile pixel comparisons pass; native
scale review is recorded. **These are agent-reviewed playtest layouts, not owner visual
acceptance.** Named owner reference layouts were not changed in these passes.
Life Support now uses r4: an integrated twin-filter rack replaces the detached portable
compressor. Four saved/default views match; routes, live scale and refreshed card were
reviewed. The removal-only r3 stays rejected. [R4 evidence](LIFE_SUPPORT_COMPOSITION_R4_2026-09-21.md).

Current details: [room pilots](ROOM_COMPOSITION_PILOT_2026-09-20.md),
[Storage](STORAGE_COMPOSITION_HANDOFF_2026-09-21.md),
[Battery](BATTERY_COMPOSITION_HANDOFF_2026-09-21.md),
[Data Archive](DATA_ARCHIVE_COMPOSITION_HANDOFF_2026-09-21.md),
[Life Support](LIFE_SUPPORT_COMPOSITION_HANDOFF_2026-09-21.md),
[Cold Store](COLD_STORE_SERVICE_HANDOFF_2026-09-21.md),
[Observation](OBSERVATION_SEATING_HANDOFF_2026-09-21.md).

Hydroponics r3 is installed in four saved/default keys, with distinct growing
areas and a separate potting trolley. A higher-density bought foliage source replaces
the coarse enlarged tray. Four-view routes, 368 controlled meal-route samples,
live-scale review and saved/default pixel parity pass; the card is refreshed.
Owner visual acceptance remains open. [Integration evidence](HYDROPONICS_COMPOSITION_CANDIDATE_2026-09-21.md).

Reactor now has a reactor stack, cooling unit and operator console in four saved/
default views. Loose accessories are hidden in the layout; source library entries
are preserved. Routes, 560 controlled maintenance movement samples, live scale,
saved/default pixel parity and the refreshed card pass. Reactor/cooling bodies remain static;
owner composition acceptance remains open. [Evidence](REACTOR_COMPOSITION_2026-09-21.md).
Quarantine was reviewed without layout changes. Command Center now groups a
monitoring console, targeting display and central briefing station. Four saved/
default views match; doorway routes, live scale and the rebaked card were reviewed.
The first placement blocked the south approach and was rejected. All other layouts
and library marks are preserved. Two bought monitors now have restrained operating
traces; four-view motion/off/held-clock checks and live pause/resume clock checks
pass. Briefing hologram and machine bodies remain static; owner acceptance is open.
Included in the matching current Windows and Mac builds.
[Evidence](COMMAND_CENTER_COMPOSITION_2026-09-21.md).
Reactor console now has a restrained registered operating trace. Four native views
verify active motion inside the screen, off-state stability and held-clock parity.
All 10,507 registry entries validate. [Feedback evidence](REACTOR_CONSOLE_FEEDBACK_2026-09-21.md).

Library ns-154 now correctly reads Wooden storage crate in Storage; only its
title/category changed, with owner marks and source pixels preserved. Registry
validation passes. Included in the matching current Windows and Mac builds.

Library lab-20 registration was repaired without changing its source PNG or stable ID.
Earlier registry validation covered 10,507 props on 269 sheets; that count is dated
evidence, not a current whole-library quality certificate. Review reported defects
and current marks individually; keep small-prop retirement a separate decision.

### Salvage and Quarantine saved/default reconciliation
Salvage and Quarantine previously differed in all four saved/default rotations;
Crew Hab matched. The initial review is preserved in
[discrepancy evidence](ROOM_SAVED_DEFAULT_REVIEW_2026-09-21.md).

Salvage revision 3 is installed in four saved/default keys, grouping tools beside
the processing machine. Its fourth-rotation legacy restoration bug is repaired.
Four views/640 navigation samples pass; installed default RGBA images match,
live 52/75% views were inspected, and sorter on/off/held-clock checks pass.
The card is refreshed. [Evidence](SALVAGE_COMPOSITION_REPAIR_2026-09-21.md).

Quarantine now preserves its bought treatment/recovery/wash grouping in every
rotation, with explicit cabinet placement and obsolete inherited furniture hidden.
The third-rotation legacy restoration bug is repaired. Repeated-setup regression
fails eight checks before the fix and passes afterward. Four views/640 navigation
samples pass; installed default RGBA images match the candidate exactly. Live
52/75% views and refreshed card were inspected. The older clipped specimen-wall
candidate is superseded by this saved-layout reconciliation.
[Evidence](QUARANTINE_LAYOUT_REPAIR_2026-09-21.md).

Both changes preserve every other saved/default key, including the ten named
owner reference rooms. Owner visual acceptance remains open. The current matching Windows/Mac builds include these repairs, layouts and cards.

Construction Drone Bay and Biodome also had the fourth-view restoration defect.
Both now preserve saved standalone furnishing when the old wall bank is removed.
Native regression: 12 failures before / zero after; eight saved-layout views and
1,280 movement samples pass. Saved/default layouts and cards were not changed.
The subsequent current-layout audit covers seven wrappers / 28 views: no explicit
deletion returned, no duplicate IDs, and repeated setup preserves ID/rect maps.
Medical Center/Office and the owner's Ore Refinery pass without further changes.
This is not visual, route or animation acceptance.
[Audit evidence](CURRENT_WRAPPER_AUDIT_2026-09-21.md). [Evidence](REMAINING_BANK_RESTORATION_2026-09-21.md).

Construction Drone Bay furnishing is reconciled in four saved/default keys:
legacy bench hidden and staging platform separated from the forklift in each
rotation. Four-view navigation/live-scale review passes, and corrected complete
layout promotion yields exact RGBA parity with the candidate. The card is refreshed;
all other layouts are preserved. Sparse-override promotion initially dropped an
inherited size and was corrected before acceptance. Included in the current matching Windows/Mac builds.
[Evidence and inventory](CONSTRUCTION_LAYOUT_RECONCILE_2026-09-21.md).

Biodome now has an explicit fern-bed focal area and retains its bought growing,
potting, seating and water-feature groups without inherited machine overlaps.
Four complete effective saved/default keys are installed; other layouts preserved.
Four-view navigation, live-scale review and fern irrigation on/off/held-clock checks
pass. Installed default RGBA images match the candidate exactly; card refreshed.
Owner style/composition acceptance remains open; current exports include this update.
[Evidence](BIODOME_COMPOSITION_2026-09-21.md).

Power-room review: Turbine/Heat Recovery remain unchanged. Biomass now has the
installed r4c matte olive vessel with attached feed hopper, grouped sacks and
separate process controls. One built-in image edit; no Higgsfield or bought-atlas
changes. Exactly four saved/default keys changed; all other rooms preserved.
Four-view/640-sample checks pass, installed defaults match candidate RGBA exactly,
and the dedicated control-screen trace passes active/off/held-clock checks. Single
card refreshed. Owner visual acceptance and density refinement remain open.
Included in current f2ec1eb651c14137 Windows/Mac test packages.
[Integration and limits](BIOMASS_VESSEL_INTEGRATION_2026-09-21.md).
[Rejected candidates and source review](POWER_ROOM_COMPOSITION_REVIEW_2026-09-21.md).

Gravity Loom r2 is now installed: existing low central apparatus, bought controls,
and one calibration-weight bench. Removed small scatter and inherited directional
bench overlaps. Four-view640-sample routes, live scale, bounded operating effects,
installed RGBA parity and refreshed card pass. Exactly4saved/default keys changed;
all other rooms preserved. Solar/Tidal reviewed unchanged. Included in current
Windows/Mac test packages. [Evidence](GRAVITY_LOOM_COMPOSITION_2026-09-21.md).

Clone Lab and Shield Generator now have fixed functional machine positions,
logical recovery/reagent or power/control groups and removed duplicate equipment.
Inherited per-quarter scale and patch-rack overlaps are resolved. Eight native
views/1280samples pass without prop overlaps; installed RGBA parity and two refreshed
cards pass. Existing operating effects checked in all4views. All other layout keys
preserved; Anomaly reviewed unchanged. Included in current Windows/Mac test builds.
[Evidence and limits](CLONE_SHIELD_COMPOSITION_2026-09-21.md).

## Support-room review and Radio repair

Radio Lab's removed-bank handling now preserves standalone calibration furniture
in q2; three-room repeated setup regression passes. Radio r4 is now installed:
restored signal-routing panel, reception/calibration group, receiver/rack and dish
controls. Four native views/640 walking samples pass with no overlaps, installed
RGBA parity is exact, live 52/75-percent views and refreshed card were reviewed.
All other saved/default keys are preserved. This is a provisional composition;
owner visual acceptance remains open. Two signal displays now have bounded green
waveforms, dark offline glass and actual-pause verification. Source/layouts unchanged;
card refreshed. Included in current exports.
[Feedback evidence](RADIO_SIGNAL_FEEDBACK_2026-09-21.md).
Overall composition acceptance remains open. Current packages include the layout
and placement repair as well as the signal-display follow-up. [Evidence and next work](SUPPORT_ROOM_REVIEW_2026-09-21.md).

## Salvage Workshop composition

Restored the directional overhead teardown bench with its supported tools and motor,
paired bought machining equipment, and grouped cargo cart/crate at a smaller crate
scale. Removed empty table, loose tool board and redundant scrap box. Four views,
640 walking samples, exact installed RGBA parity and bounded power-indication checks
pass. Native live views and refreshed card reviewed; other saved/default keys remain
unchanged. Owner visual acceptance is open. Current packages include this change.
[Evidence and limits](WORKSHOP_COMPOSITION_2026-09-21.md).

## Holographic Core layered projector

Installed a room-specific static housing and clock-driven star projection, with
restored calibrator and correct saved-position handling. Four-view navigation,
operating/off/held-clock checks and repeated custom-renderer setup pass; actual
station pause freezes the visual clock and complete room RGBA. Saved/default parity
is exact; card refreshed; other layout keys and owner marks preserved. New source,
prompt, registration and deterministic rebuild are recorded. The separate chart now uses its original stand with a runtime dark/active panel;
off/on stand parity and actual pause pass. Owner visual acceptance remains open.
Current Windows/Mac exports include this integration. [Evidence and limits](HOLO_PROJECTOR_INTEGRATION_2026-09-21.md). [Chart follow-up](HOLO_CHART_INTEGRATION_2026-09-21.md).

## Medical support composition

Med Center now groups bed/IV, scanner/diagnostic controls, medicine storage and sink.
Med Office groups consultation seating, records workstation/chair and filing cabinets;
removed duplicated equipment and small loose props. Exactly8complete saved/default
keys changed; every other key, including all10owner rooms, is preserved. Med Center's
q3 wrapper now retains its explicitly placed console; repeated-setup regression
reproduces2failures before/0after. Final8views/1280samples, native scale and exact
installed RGBA parity pass;2cards refreshed. Owner visual acceptance remains open.
Current polish exports include this work. [Evidence](MEDICAL_SUPPORT_COMPOSITION_2026-09-21.md).

## Card sampling polish

Fan room-art thumbnails now contain the mip levels their existing tilted-card
filter requested. A cached card-only distance-field font theme also improves tilted
lettering without changing shared interface fonts. Native hand tests pass; 47 card
definitions show no new height overflow. Installed 1600x900 and 960x540 captures were
reviewed; small-window text remains tiny and owner sharpness acceptance is open.
Upright art retains nearest sampling. Included in the matching current Windows and Mac builds.
[Evidence and limits](FAN_CARD_SAMPLING_2026-09-21.md).

## Current test builds

**Windows and Mac: brinespace-b0d1640cfe18c6fc**.
Windows: builds/BrineSpace-polish-2026-09-22.
Mac: builds/BrineSpace-mac-polish-2026-09-22.
Includes the locker identity and shelf-fit repairs, Life Support console fixes,
latest Biodome composition and prior bunk/animation work. Both exact PCK audits
check 15216 assets with zero discrepancies. Actual Windows release New Game,
Continue, simulation and F8 pass with zero failures, debug=false and empty stderr.
49 bunk frame samples and 49 locker/card PNGs match reviewed RGBA source pixels.
Native startup screenshot inspected; this is not all-action gameplay acceptance.
Matching Mac source identity and Universal 2 structure pass. Native Apple Silicon
testing, owner visual judgment and broad expedition acceptance remain open.
Both folders include instructions, NOTICE, build metadata and SHA256 sums.
[Current release evidence](POLISH_TEST_BUILDS_2026-09-22.md).

### Historical bunk package evidence

**Windows and Mac: brinespace-c0508d641e858e5e**.
Windows: builds/BrineSpace-bunk-polish-2026-09-22.
Mac: builds/BrineSpace-mac-bunk-polish-2026-09-22.
Includes the four bought-bunk profiles, bed sharing/reachability fixes, reduced
Bill helmet and preceding installed room/animation work. Both exact PCK audits
check 15216 assets with zero missing/changed/remapped/unexpected files. Actual
Windows release New Game/simulation/F8 passes: exit 0, debug=false, zero failures,
empty stderr. All 49 packaged bunk-frame samples match reviewed RGBA hashes;
Bill's specific controller binding and native gameplay capture were checked.
Mac source identity matches Windows; Universal 2 structure, executable permissions
and absence of QA overrides pass. Native Apple Silicon launch/gameplay, signature
acceptance, owner art judgment and broader expedition acceptance remain open.
Both packages include instructions, NOTICE, build metadata and SHA256 sums.
[Earlier bunk release evidence](BUNK_WINDOWS_RELEASE_2026-09-22.md).

### Historical helmet package evidence

**Earlier Windows and Mac: brinespace-f2ec1eb651c14137**.
These packages predate standing endpoint/north-west work identity repairs and door-edge reuse.
Windows: builds/BrineSpace-helmet-2026-09-21.
Mac: builds/BrineSpace-mac-helmet-2026-09-21.
Includes the four selected walk repairs, smaller normal helmet, and prior room,
animation, reliability and performance work. Both exact 15,151-asset PCK audits
pass with zero missing/changed/remapped/unexpected assets. Actual Windows EXE:
exit 0, debug=false, zero failures and empty stderr; navigation, thirteen rooms
in four rotations/repeated setup, Holo effects, New Game/Continue, simulation,
card setup and F8 trace preservation pass. It checks 240 decoded Bill frames and
158 authoring-file omissions. Native gameplay screenshot inspected.
A first smoke attempt used the older fixture path and failed old helmet hashes;
that setup error is preserved separately. The corrected run is the acceptance
record. QA driver now resolves its sibling fixture; release workflow updated.
[Historical helmet release evidence](HELMET_RELEASE_2026-09-21.md).
[Prior polish package](POLISH_RELEASE_2026-09-21.md) remains preserved.

Mac matches the Windows source fingerprint. Universal 2, executable permissions
and no-QA-override checks pass. Ad-hoc test archive, not notarized. Native Apple
Silicon execution/Gatekeeper acceptance remain unverified; owner has M1-or-newer
hardware. Checklist is beside the ZIP. Earlier packages are preserved.

The dialogue-aware paid-station fixture completed an autonomous north
kneel/work/stand/departure at a Life Support tank. Its 71-frame room-following
capture and native poses were reviewed. [Navigation and motion evidence](NPC_REBUILD_REPLACEMENT_2026-09-21.md).
Ordinary expedition and owner motion/composition acceptance remain open.
Neither package is public-release acceptance.

Bill gait follow-up: a current paid-opening native capture records 240 walking
samples, 80 frames, north/east travel and a turn. Across 237 same-key pairs the
phase follows travelled distance consistently with no backward phase step.
One dialogue-paused sample is recorded. This eight-second stepping window contains
no stop/work transition; natural-motion acceptance remains open and no stride
change was made. [Evidence and clip](BILL_PAID_GAIT_REVIEW_2026-09-21.md).

A follow-up paid capture includes the approach, north-facing kneel/work/stand and
departure (86 images). Work anchor remains fixed; the sampled native pose sequence
has no missing limbs or obvious body jump. No art/timing change was needed from
this evidence. West-facing gameplay was subsequently captured; owner motion acceptance remains open.
[Transition evidence](BILL_WORK_TRANSITION_REVIEW_2026-09-21.md).

Westward follow-up: 150 samples/50 images include walking and a stop, with normal
costs/failures enabled. Forty same-key west pairs retain consistent distance-driven
phase; consecutive idle samples have zero displacement. No new timing change was
made. These bounded clips now cover north/east gait, west/stop and a north work
transition; they do not close owner smoothness or full expedition acceptance.
[West evidence](BILL_WEST_PAID_GAIT_2026-09-21.md).
South follow-up now has240native samples/crops at30Hz:235walk and5idle, all facing
south.234same-key pairs maintain distance-driven phase; idle position stays fixed.
Source/native poses and stop reviewed, with no new sprite/timing edit. Full-rate
clip supports owner review but does not establish anatomical foot lock or natural
motion acceptance. [South evidence](BILL_SOUTH_PAID_GAIT_2026-09-21.md).

## Powered-display retention

Radio signal console and Holo projector/chart now retain commands while unpowered.
Native before/after test reduces their12-frame off redraw counts from12/24 to0;
active animation remains12/24. With identical queue objects across on/off/on,
all24retained/direct comparisons are byte-exact. This is not an FPS claim.
New native regression is indexed; current exports include this and Radio feedback.
[Evidence and limits](POWERED_DISPLAY_RETENTION_2026-09-21.md).

## Construction-dialogue diagnostics

F8/crash bundles now include the optional dialogue trace, capped at 2 MiB. Native
isolated report tests pass, including missing-file and newest-event checks. This
improves reproduction evidence; the original early-dialogue report remains open.
[Timing audit and diagnostic verification](ROOM_DIALOGUE_TIMING_REVIEW_2026-09-21.md).

## Remaining work and evidence limits

Current polish performance review: simulation gate passes 800 updates (1.67 ms
mean, 24.9 ms worst). Native 50/100-room profiling has active drones in all sampled
frames; 100-room overview render CPU/GPU 21.16/18.47 ms versus close 6.23/4.23 ms.
Fit View's instrumented first frame reaches 205.895 ms, the next investigation
target. These are not gameplay FPS or before/after gains. Zero net crew motion in
the 100-room samples limits moving-crew conclusions.
[Current measurements and limits](POLISH_PERFORMANCE_REVIEW_2026-09-22.md).
Follow-up distinguishes that instant-jump diagnostic from the animated toolbar
button. The real button trace settles in17 sampled frames; expensive preparation
and settling frames reach125.710/122.957 ms. Benchmark now records both paths;
The initial trace preserved runtime behavior; the follow-up below is now installed.
[Actual button trace](FIT_BUTTON_PROFILE_2026-09-22.md).
Split-floor preparation is now enabled locally. Two candidate runs peak at
109.848/109.910 ms versus reference125.710/162.927 ms; total transition duration
is not improved. All four final images match exactly. Native retention checks
pass on the final default: zero strongly differing mid-zoom pixels among18642
samples, exact settled/full-rebuild parity, and a bounded three-frame hold.
Reference/candidate transition boards and full-size moving frames are reviewed.
Existing test packages predate this change; this is not a gameplay FPS claim.

Anomaly Lab review identifies the next repair: current bought props have no visible
power/time response in any quarter (eight native comparison failures), while routes
and640walking samples pass. Legacy animated equipment is absent. Also, q3's small
amber canister loses adjacency when the tanks move left. No production changes yet;
inspect source layers before restoring meaningful equipment feedback.
[Evidence and next repair](ANOMALY_ROOM_REVIEW_2026-09-21.md).

Anomaly screen-layer prototype now passes four-quarter native on/off/held-clock
checks: kiosk trace and tank level bars animate independently; all pixels outside
screen aperture masks remain unchanged versus baseline and across states. Output-only
study with production floor mapping; not installed. Orb baked-glow separation,
amber prop placement and retained/live pause checks remain open.

Orb separation is now staged too: original globe and stand sampled independently;
globe absent offline, subtle float when powered. Four-quarter independent orb pixel
checks pass with stable lower stand and held/offline states. No production changes.
Full effect-mask, retained/live pause and placement checks remain before integration.

Anomaly effects are now installed after resolving the failed integration: bought
props carry the wall-bank ownership flag, which caused an early return before screen
overlays. Only the three effect props bypass that return. All20native images now
match the reviewed prototype; retained on/off/on checks pass12direct comparisons.
Shared art/registry/layouts remain unchanged. Saved/default layout reconciliation,
q3 amber placement, actual station pause and card refresh remain open.

Anomaly layout/card reconciliation is now complete: four effective keys promoted
with unrelated keys preserved, q3 amber prop moved beside its tanks, eight native
saved/default comparisons exactly match the candidate. All four rotations/640walking
samples pass. Offline card refreshed and reviewed. Actual station pause remains
open, and current export packages predate this room pass.

Anomaly actual-station pause verification now passes in all four quarters: orb,
kiosk and tank screen regions animate independently, while a paused game process
step leaves the clock and full room crop unchanged. Native gameplay-scale crop
reviewed. Synthetic funded fixture, not economy/ordinary-expedition acceptance.
This closes the pending live-pause item above; owner visual acceptance and packaged
verification remain open. See ANOMALY_ROOM_REVIEW_2026-09-21.md.

Maintained powered-display regression now includes Anomaly alongside Radio/Holo,
using shipped defaults and independent motion checks for the orb and both screen
apertures. Native three-room/four-quarter on-off-on run passes with zero failures;
existing test index and UID retained. Evidence: maintained-retention.log in the
Anomaly review folder.

Solar Array (Thermal Power Control) and Tidal Condenser furnishing R1 is installed:
bought overlays no longer hide primary machinery. Medium supports are grouped;
eight native views/1280 walking samples pass with zero reported overlaps. Operating,
offline and held-clock checks pass; gameplay scale reviewed. Eight saved/default keys
changed, every other key preserved. Sixteen installed image comparisons are exact;
both cards refreshed. Owner acceptance remains open. Current test packages predate
this integration. [Evidence](GENERATION_ROOM_REVIEW_2026-09-21.md).

New autonomous native observation: 120 real-time seconds after controlled paid
setup, normal frame/cycle timers, no assigned goals. Survived cycles4-9 with1105
samples/1101 crops; four walk directions and hunger/curiosity/maintenance goals.
One paused sample. No work poses in this window, so work acceptance remains open.
The central chamber figure is confirmed as BRINE's intentional separate body art;
Bill's architect pod uses a different prop and recovered renderer. The suspected
duplicate is resolved without gameplay/art changes.
[Evidence and capture limits](BILL_AUTONOMOUS_NATIVE_2026-09-21.md).

All four Bill walk repairs and the north/west work identity repairs are installed.
Owner motion judgment, full foot-contact review and ordinary expedition acceptance
remain open. See the current animation section above; older east/west candidate
notes are historical stages, not pending integrations.

1. Gather owner motion/composition feedback and exercise normal expeditions: Bill's
   full gait, action transitions, room operation, opening power feedback, pacing and
   audio mix remain broader acceptance work. No headless or pixel test proves these.
   Current paid mining/salvage fixtures survived all four one/two-generator openings
   with Bill awake and failure rules enabled. Controlled blueprints and simulated
   updates limit this evidence; it does not establish human expedition acceptance.
   Salvage tracing resolved the lower two-generator observation total: both collected
   all 12 metal, but the second generator collected more during setup and finished
   sooner. No balance change followed from the misleading post-setup comparison.
   [Paid opening review](PAID_OPENING_REVIEW_2026-09-21.md).
2. Run the native Apple Silicon checklist when hardware evidence is available.
   Windows execution and bundle inspection cannot close that lane.
3. Preserve staged owner-room findings: Research q2 has a disconnected route with a
   one-prop candidate fix; Pressure Control has an inward-move candidate for clipping.
   Neither is installed. Listening Post's fitted-console extent needs visual judgment.
   Evidence: output/owner-room-references-2026-09-21. Do not silently edit these rooms.
4. Ordinary bought props now retain fixed drawing; operating screens stay live,
   while custom/portable props keep their renderer rules. A focused four-view
   native test has exact pixel parity and reduces Command Center prop redraws
   over 12 frames from 36 to 24 operating / zero off. This is not an FPS claim.
   The earlier one-pixel discrepancy is now fixed: copied mining tether artwork
   used its source ID for drawing but its copy ID for animation classification.
   Source-ID classification restores live updates without changing owner placement.
   Native copied-prop regression passes; the broad 49-room/31-pair station test
   passes with independently verified zero RGB difference in every pair, including
   active crew/drone/construction checks. These fixes are in the matching current Windows and Mac builds.
   [Retention evidence](LIBRARY_PROP_RETENTION_2026-09-21.md) and
   [copy-animation repair](COPIED_PROP_ANIMATION_2026-09-21.md).
   A paired native 100-room overview probe now measures content painting at
   .951 -> .510 ms, with retained-content redraws 55 -> 28 per sample. Close-view
   saving is negligible; total render-time changes are modest and not an FPS claim.
   [Method and limits](LIBRARY_RETENTION_TIMING_2026-09-21.md).
   Continue measured performance work. The restored-layout baseline recorded
   100-room overview render CPU/GPU 20.04/17.89 ms versus close 5.28/4.16 ms under
   forced-draw instrumentation; it predates subsequent furnishing changes and is not
   FPS. Door/light validation and live-room drawing remain candidates for investigation.
   Shadow geometry caching has isolated savings but no demonstrated overall render
   gain. An adjacency microbenchmark remains uninstalled. Avoid repeating benchmarks
   without a new question. Door variants now reuse department values within each call;
   2,401 pair results match the previous expression. A single native helper probe
   showed a modest reduction, without establishing an FPS gain.
   [Door evidence](DOOR_VARIANT_HANDOFF_2026-09-21.md).
   Door/light validation now reuses room light levels within each call. Production
   comparison preserves complete keys in five lighting snapshots, reducing100-room
   lookups280 to100 and scoped mean3.468 to3.054ms. This is not an FPS claim;
   current f2ec1eb651c14137 exports include this optimization and Biomass integration.
   [Call-local light reuse](DOOR_LIGHT_REUSE_2026-09-21.md).
   Door/light validation now also reuses symmetric connection results inside each
   call. Native100-room reference/production comparisons keep complete keys equal
   across seven states, including rotation and branch ownership, with queries
   400->220. Paired instrumented call means3.211->2.873ms (0.338ms), not FPS.
   No layout, render rules or gameplay changes. Latest 867eac6b1b17b4fc packages include this.
   [Call-local edge reuse](DOOR_EDGE_REUSE_2026-09-21.md).
   [Performance evidence](PERFORMANCE_BASELINE_2026-09-21.md).
5. Older owner notes remain in history: dialogue note 17 still needs its offending real-session line. The available trace
   contains only Bill waking; three controlled paid builds show no early completion
   announcement. [Timing review](ROOM_DIALOGUE_TIMING_REVIEW_2026-09-21.md).
   Fan-card note 14 now has native thumbnail/font comparisons and installed fixes;
   remaining work is owner readability acceptance and very small-window text, not
   an uninvestigated global viewport issue. See [card sampling](FAN_CARD_SAMPLING_2026-09-21.md).
   Inspector note 16 was completed September 17: current excavation, salvage,
   ward repair, pod thaw/charge and mining-load paths still use the shared bar
   helper. Do not rebuild this feature from the older unchecked list in history.
   This September 21 review confirms current call sites, not a new native acceptance
   run. Dead-doctrine cleanup is optional.

## Workflow

Room-review ledger audit: all 47 current cards decode, but card-bound reviews are
1 current / 3 stale / 43 missing. These are evidence-binding gaps, not missing-art
findings. The audit/report now distinguishes them and handles list-valued legacy
notes without crashing. Current status and newer handoffs govern work over old
ledger descriptions. [Audit and report](ROOM_REVIEW_LEDGER_AUDIT_2026-09-22.md).

Release collection excludes Bill's authoring sources from broad revision-folder
scans while retaining exact/formatted dependencies. The current actual Windows
release checks 225 selected authoring files absent; both exact PCK audits pass.
All selected runtime frames remain available. The original trimming regression
and 42-file checkpoint are historical evidence, not the current omission count.
[Selection evidence](BILL_AUTHORING_EXPORT_TRIM_2026-09-21.md).


Use maintained skills/brinespace-room-pipeline and skills/brinespace-character-pipeline;
sync verified reference changes to installed copies. The [visual bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md)
owns art direction; [release workflow](RELEASE_WORKFLOW.md) owns packaging gates.
Bill's construction provenance is archived: the canonical tools resolve those exact
inputs and retain frozen source hashes. Never regenerate missing originals to pass.

Scope searches away from output/. Read candidate evidence by its known path. Back up
and guard selected owner keys before writes. Native fixtures should await observable
startup state. Run only relevant checks; Python tests are separate from the Godot test
runner. Record experiments in dated handoffs and **replace the relevant summary here**
at milestones instead of appending conflicting status paragraphs.

Current bare-walk comparison renders Bill/Veld/Branforth in all four directions
through the production player:90native frames, zero missing textures. At the same
46world-units/sec, Bill north/south cadence matches Veld (~1.002seconds/stride);
side views are slightly quicker (~0.882seconds) from their selected shorter stride.
Rear-view sheet inspected; this does not prove foot locking or owner acceptance.
No runtime/art/layout changes. See CREW_GAIT_COMPARISON_2026-09-22.md and its inline
comparison artifact for feedback on the current repaired set.

Salvage motion follow-up:670native20Hz samples complete clearance/recharge/return
in33.5 simulated seconds; camera-corrected work capture reviewed unobstructed.
Chassis remains coherent and claws attached in inspected poses; current work face
is outside the bay floor. Synthetic setup, not ordinary real-time pacing or owner
acceptance. No art, runtime or owner-layout changes. See SALVAGE_MOTION_FOLLOWUP_2026-09-22.md.
