# Saved versus shipped layout audit

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Identify local Studio overrides that make fresh-install rooms differ from local
previews. Reconcile only after native composition and circulation review. Preserve
the ten named owner rooms and all library marks. Broad project work remains open.

## Accepted decisions and constraints
No bulk synchronization. Explicit null can hide a built-in prop and is not
equivalent to an absent key. Ignore numeric serialization differences below 1e-9
for triage; use native pixels for visual evidence. No Higgsfield.

## Current state
Read-only audit of 47 catalog entries. Twenty room types have raw overrides;
Current Turbine and Biomass Digester differ only through numeric rounding.
Ten remaining entries are protected owner rooms. Eight other entries require
review: Maintenance Bay, Crew Hab, Airlock, BRINE Core, straight corridor, corner,
tee corridor and Observation Room. No layouts, cards or source art changed.

Evidence: `output/layout-default-audit-2026-09-21/`. `saved-snapshot.json` freezes
the inspected owner data. `summarize.py` produces `classified.json` with input
hashes, explicit-null distinctions and native RGBA comparisons. Original raw
comparison is `audit.json`.

## Verification
Ran maintained `tools/review_room_composition.gd` twice, first with defaults and
then the saved snapshot, for all eight unprotected candidates: 32 views and
5120 walking samples per run. Native RGBA differs in 29 of 32 paired captures.
Both runs exit 1: neither is a clean acceptance result.

Defaults report 12 failures: Airlock hatch bounds in q1/q2/q3, Observation Room
north furniture bounds in q0, plus one doorway approach in each corner/tee view.
Saved reports 12 approach failures: the same eight corner/tee cases plus straight
corridor q1/q3 side 3 and corner/tee q1 side 3. Defaults have 14 visual-overlap
warnings and saved has eight. Overlap is not by itself proof of an art defect.

Corner/tee common failed endpoints report no blocking prop. Investigate room
geometry and the preview's fixed endpoint before treating these as live navigation
regressions. Additional saved-only failures need a route probe too.

Visually inspected Observation Room q0 at native resolution: defaults retain
legacy wall shelves and a desk; saved uses bought seating, telescope, storage and
plant. This establishes a substantive furnishing mismatch, not owner acceptance
of either composition. Other captured views still need visual review.

## Next action
Probe corridor graph/geometry and actual per-frame route state to separate fixture
assumptions from blocked furnishing. Review Observation Room and Airlock in all
quarters before promoting selected layouts and rebaking cards. Review provenance
of Maintenance Bay/Crew Hab size edits before any changes. Protected rooms remain
untouched; no release refresh has been performed for this audit.

## Corridor diagnosis and correction
The initial corner/tee captures are invalid identity evidence: the review instantiated
the shared corridor renderer without setting `room_id`, unlike the Studio.
`tools/review_room_composition.gd` now assigns catalog identity before `_ready`.
Separately, a direct identity-correct probe (`probe-before.log`) proves the layout
view declared a corner as a cross and a tee as an elbow. Corrected kind indices in
`scripts/corridor_layout_view.gd` to match the existing floor geometry. No floor
shape or gameplay navigation algorithm changed.

Correct identity exposed the generic preview's inappropriate north-wall call for
corridors (null wall textures). `tools/bake_current_architecture_cards.gd` Preview
now leaves corridor hull rendering to its own renderer. Maintained card baking
already excludes corridors; no cards were rebaked.

`tests/test_corridor_foundations.gd` now compares declared doors against walkable
floor endpoints in 48 combinations, alongside its existing 18 foundation checks;
passes. Final native defaults: 12 views/1920 walking samples, zero failures. Final
saved: 12 views/1920 samples, two failures, both straight corridor q1/q3 west
approaches; no remaining null-texture errors. See `final-defaults`/`final-saved`
and their logs. Saved q1 native still reviewed: small furnishing lines both edges.
These two graph failures remain unresolved; don't claim live navigation failure
or promote the corridor furnishing yet. The original 29/32 image-difference count
includes the incorrectly identified corner/tee views and is superseded for those
identities by these corrected captures.

## Remaining straight-corridor findings resolved in scope
`probe-route.gd` retains the original failed 16px-grid result, then temporarily
builds a 4px graph using identical `can_stand` and `segment_clear` predicates.
`dense-probe.log` finds a segment-checked west route in both q1/q3, with 958 nodes.
The route passes at y=4 through a gap between padded blockers ending at y=2 and
starting at y=8. The 16px preview lattice misses this six-pixel band. This is a
preview sampling limitation and cramped furnishing, not a sealed geometric route.

Production inspection and `live-geometry-probe.log` confirm
`GridCanvas.bill_room_geometry` returns zero props/edges and `corridor=true` for
all 12 corridor identity/rotation cases. Live crew use the corridor floor shape;
these furnishings are not currently physical blockers. No navigation rule changed
and no claim of an actual live traversal test is made. The current Studio still
cannot traverse that narrow band, so the original two failures remain correctly
recorded. Do not hide them with a denser audit-only success or globally increase
navigation density without measuring cost.

Next furnishing review can widen this aisle if those props are retained. It does
not block independent Airlock/Observation Room reconciliation. No owner layouts
or runtime assets changed during this diagnosis.

## Airlock staged repair
Reviewed all four saved Airlock captures. Saved null overrides remove both
`pressure_chamber` and `outer_hatch`. The former is functional: its collision keeps
roaming crew in the dry area, and its draw call owns chamber rails, controls and
gate effects. The floor alone remains visible, disguising this omission.
Restoring these props also exposes bought case/cylinder/spool overlap with the wet
chamber. Do not promote the original saved layout.

Staged `airlock-r2-candidate.json` removes those eight null entries, moves q0's
equipment case below the seating, and groups side-view cylinders/spools outside
the chamber. R1 obstructed q3's east approach and is rejected; R2 puts that supply
group southeast, clearing the door. No owner/default layout has been written.
Native R2: four views, 640 walking samples, zero failures. Only four expected
chamber/hatch overlap reports remain. q0/q1/q3 revised stills reviewed; q2 positions
unchanged from the restored baseline. All four original saved views reviewed.

`tools/review_room_composition.gd` now uses the existing Airlock test's 200px hull
envelope specifically for `outer_hatch`; its prior generic 192px side/south limit
incorrectly rejected this code-owned threshold. No general bounds relaxation.

Next: verify chamber cycle/helmet handoff and dry-area exclusion against R2, then
promote only four complete effective Airlock keys with fresh-input guards, compare
saved/default native output and rebake its card. R2 is staged, not installed or
release-verified; owner visual acceptance remains open.

R2 functional fixture now passes all four quarters: chamber exists, its center
excludes roaming crew, production `BillNPC.can_stand` permits the locker target,
the preview graph reaches within the service's 12px tolerance, dry/exterior images
differ, returning to dry matches exactly, and shelf visibility changes pixels.
Evidence: `airlock-function-check.gd`, `airlock-functions-final.log` and
`airlock-functions/`. This exercises static cycle poses and shelf visibility,
not a timed live equip/remove action or full station cycle.

Initial q2 locker failure was a fixture mismatch: target x=-172.88 is outside the
Studio's 172px limit but within production's 176px bound. The temporary R3 seating
move did not address it and is discarded; R2 remains selected. Probe evidence in
`airlock-probe-r3.log`; no owner data changed. Next integration still requires
guarded effective-key promotion and installed parity/card review. A live timed
handoff remains a separate verification scope, not proved by this fixture.

## Airlock integration milestone
R2 is now installed. `promote-airlock.py` checked the audited defaults hash and
fresh owner target keys, merged complete effective Airlock overrides and wrote
only four keys in each layout file. Backups and `airlock-promotion.json` preserve
provenance; all other keys, including the ten protected rooms, remain unchanged.
Both `airlock-installed-defaults` and `airlock-installed-saved` pass four native
views/640 walking samples. `airlock-installed-parity.json`: eight exact RGBA matches
to R2. Refreshed `assets/room-cards-v2/airlock.png`, visually reviewed, LFS filter
confirmed. No shared prop art or source registration changed.

Timed live helmet handoff, full station cycle and packaged verification remain
open; static functional checks do not substitute for those. Observation Room is
the next saved/default reconciliation candidate. Broad goal remains unfinished.

## Observation interaction review
All four saved native views reviewed. Bought sofa/table/seating form the reading
area, telescope/stool sit by the upper wall, storage/plant move for the west entry.
The reading interaction already targets the bought sofa. A native activity probe
found the q3 watch anchor (0,-80) blocked by the new seating, despite ordinary
doorway checks passing.

`scripts/crew_room_activity.gd` now chooses a clear lattice point near the intended
watch anchor. It uses a separate shallow data copy for that lookup: the service
helper caches its result on the input dictionary, so sharing the sofa lookup would
alias two different anchors. `tests/test_observation_sofa.gd` adds blocked-watch
and repeated cached-sofa coverage; passes. Native `observation-activities-final.log`
confirms all eight read/watch stations are reachable across four saved views.
This proves fixture routes, not autonomous activity selection in a full expedition.

No Observation layout or card changed yet. Reconcile its four saved/default keys
next, with fresh guards and installed visual parity. Airlock work remains intact.

## Observation integration milestone
`promote-observation.py` verifies the four target keys against reviewed saved and
default snapshots, then merges their complete effective values into both files.
All other keys are preserved, including the installed Airlock and protected owner
rooms. Backups: `observation-before-0.json` and `observation-before-1.json`.
Both installed composition runs pass four views/640 samples; `observation-parity.json`
records eight exact matches to the reviewed original saved captures.
`assets/room-cards-v2/observation_room.png` is rebaked, visually reviewed and LFS
tracked. Source art unchanged. No packaged or autonomous-expedition acceptance is
implied. Remaining catalog differences include Maintenance Bay, Crew Hab, BRINE
Core and the corridor types; preserve fresh owner edits while reviewing them.

## Observation lookup reuse
The corrected watch lookup now caches under `observation_watch_stations` on the
same geometry dictionary, separate from the sofa's `reachable_service_stations`.
`reachable_stations` accepts an optional cache key; existing callers retain their
default. This avoids repeating the nearest-clear-point scan on each watch lookup.
Focused sofa tests verify reuse and cache separation; pass. Native crew activity
test passes 36 room/rotation/actor approach, facing and save checks (Pressure
Control, Listening Post and Crew Hab; these are fixtures, not owner-layout edits).
Evidence: `observation-cache-test.log`, `crew-activity-native.log`.
No FPS improvement is claimed. The initial headless activity attempt was stopped
before completion; it is inconclusive, not a proven hang or unsupported lane.
The test's screenshot branch is conditional, contrary to the interim commentary.

## Crew Hab functional audit
Reviewed saved/default q3 native images. Saved removes the functional
`hab_berth_east` and substitutes bought `library/tileset-mb2-14`, with kitchenette,
lockers and seating. `CrewRoomActivity` only supplies the sleep/rest registration
for `hab_berth_*`; the bought bunk falls through to generic activity stations.
The former review accepted any nonempty station list as a sleeping berth.

`tools/review_room_composition.gd` now requires an explicit sleep station with a
rest point. Fresh saved review: four views/640 samples, one failure (q3 missing
sleeping berth). Fresh defaults: four views/640 samples, zero failures. Evidence:
`hab-functional-saved` and `hab-functional-defaults` with corresponding logs.
No layout/art changed and no Crew Hab promotion performed. Next: register the
bought bunk's actual resting pose and reachable approach, with native sleep motion
review, or retain an existing functional berth while reviewing a replacement.
Do not certify decorative furniture from a generic fallback service point.

Sleep-source inspection: current Bill `sleep-east/000.png` is already horizontal
with head left; `sleep-west/000.png` is head right. The bought bunk's pillows are
left, so east is the appropriate candidate direction. Do not reuse the legacy
north-facing berth registration or rotate the sprite arbitrarily. Runtime standing
scale is 65.28/148 for this revision. The bunk's saved displayed bounds are
72.46131 by 73.99651 room units; mattress placement and frame/ladder occlusion still
need a native composite and lie/get-up review. Existing `CrewLife.head_alignment`
can only use rest-head correction when the selected frame supplies the metadata;
do not assume every sleep clip does. No art or interaction registration changed
in this inspection.

Bunk native fit study: `bunk-fit.gd` loads the current Bill catalog additively and
places sleep-east frame zero at candidate room anchors (112,-104) upper and
(112,-62) lower. `--front-study` adds a diagnostic 100-unit depth offset only to
the in-memory texture. Upper mattress fit is plausible at native scale; this is
not selected production depth or a completed sleep interaction. Evidence in
`bunk-fit/`, final logs `bunk-front-final.log` and `bunk-baseline-final.log`.
Initial loader omitted additive mode; the failed process was stopped. Initial
empty composites also assigned actors before configure_embedded cleared them;
the corrected fixture assigns actors after room setup. Do not infer occlusion
from those invalid captures. No runtime sprite metadata, art or layout changed.
Next: use corrected baseline versus front study to choose room-local draw ordering
and inspect lower-bunk fit, then review lie/get-up motion and navigation.

Lower-bunk motion study (`bunk-fit.gd --motion-study`, `bunk-motion.log`) captures
18 native samples of current lie-down/get-up-east at 0.1s intervals. Candidate
navigation approach (48,-80), draw offset +14.592y, resting draw anchor (112,-62).
Reviewed lie-down start/middle/end. Static lower sleep fits, but midpoint crosses
the left bedpost and the boots draw ahead of the ladder. Reject this interpolation
as a production interaction. Neither a sleep-point registration alone nor a global
sprite depth override fixes the frame contact. No runtime changes were made.
Next candidate needs a front-side approach and room-local front frame/ladder
occlusion, followed by complete lie/get-up review. Upper-bunk activation would
add a climbing requirement and is not the selected shortcut.

Front-entry study: same 18 current-source samples using navigation approach
(112,-24), normal +14.592y draw offset and lower rest anchor (112,-62).
`bunk-front-entry.log` and `bunk-fit/front-entry-*.png`. Reviewed lie-down start,
middle and end: it avoids the left post but reclines below the mattress and then
slides upward, so remains rejected. No live interaction enabled.
The registered atlas region is (10,783,236,241), pivot (128,1024), displayed scale
0.30703947. `bunk-source-region.png` is an inspected diagnostic source crop. Its
ladder and front rail are separable foreground elements; do not repair this with
an across-the-board character depth change. Correct transition timing/poses and
room-local foreground composition are both required. No source PNG was edited.

Foreground prototype (`bunk-fit.gd --foreground`) restores the ladder in front
of boots using source rectangles (177,883,49,141), (10,783,14,241) and
(24,997,153,18). Native resting still reviewed. However, empty-bunk comparison
also changes pixels in screen bounds (332,156)-(403,235), so additive redraw is
not accepted: it alters the furniture without a crew member. Matching the base
polygon/UV drawing path did not remove this difference. Evidence:
`bunk-foreground-polygon.log`, `bunk-fit/empty-foreground.png` and lower-foreground.
Next implementation must split the original base and foreground into disjoint
pieces, not paint the foreground twice; verify empty-room exact parity before
using it in the animation. Production source art/layouts remain unchanged.

Bunk foreground extraction now passes empty-room exact RGBA parity using
`--masks --nearest`. The prototype builds complementary in-memory atlas masks
once, retaining original quad geometry/UVs and nearest filtering; each source
pixel is drawn in one layer only. `empty-nearest-masks.png` exactly matches
`empty-nearest.png`; `lower-nearest-masks.png` visually reviewed with ladder ahead
of boots. Source files unchanged. Disjoint-polygon alternatives retained small
sampling differences and are superseded. Evidence `bunk-masks.log`; prototype
remains output-only. This resolves the static layer experiment, not entry motion,
all-cast fit, installed interactions or arbitrary scaled/filtered variants.

Shared-cast lower-bunk check completed for current Veld, Branforth and Marsh
catalogs using the same unadjusted candidate anchor and complementary masks.
Native stills `lower-nearest-masks-{veld,branforth,marsh}.png` reviewed. Veld and
Branforth lie too low; Marsh is hidden. Metadata probe confirms Bill/Veld/Branforth
sleep-east use pivot (128,224), depth 96 and standing height 148; Marsh uses
(92,172), depth 0, height 148. Veld/Branforth supply rest-head offsets; Bill/Marsh
do not. Logs `bunk-*-metadata.log`. Thus Bill's single anchor/depth behavior cannot
be copied across the cast. No character source or metadata changed. Next work:
derive per-cast pillow placement and check Marsh's missing sleep depth against its
other existing furniture consumers before any canonical metadata correction.

Marsh provenance audit: `rebuild_marsh_art.py` builds sleep/lie/get-up from the
preserved `marsh-rest` sheet and sends them through
`rebuild_human_crew_art.write_candidate`. That writer copies source depth metadata
and currently overrides only Marsh's south seated actions, not sleeping.
`marsh-sleep-metadata.json` inventories all twelve selected sleep/lie/get-up clips:
each currently has zero depth values. This is broader than the east bunk case,
so a global 96 override is not yet justified. Preserve transition ramps and test
existing single berths in every direction before modifying the canonical writer.
The exact source of the omission is now located; no shared manifests were patched.

Existing-berth depth probe: `marsh-berth-depth.gd` renders current Marsh sleep-north
at the existing default berth rest point in all four room quarters with depth
0 and diagnostic 96. Native q0 pair and source sleep-north frame inspected.
Depth 0 hides most of Marsh; 96 reveals a horizontal body across the foot of the
vertical mattress. The source itself is horizontal despite its north clip label.
Therefore reject a global depth-only fix: canonical sleep facing and pillow
registration must be corrected together for the single berth. Eight captures in
`marsh-berth-depth/`, log alongside. Other six captures are not yet visually
accepted. No art, source manifests, gameplay metadata or owner layouts changed.

Marsh vertical source candidate generated with one built-in image call, no
Higgsfield. Original rest sheet inspected: all four nominal directions use
horizontal sleep poses. Reference was current idle-south. Raw candidate copied to
`output/layout-default-audit-2026-09-21/marsh-north-sleep-raw.png`; brief alongside.
1024x1536 RGBA, alpha range 0..254; source SHA256 recorded in the adjacent JSON.
Visual source review: correct vertical head-top orientation and recognisable
cream suit identity, but soft halo and non-opaque body pixels require cleanup.
Not installed or accepted at game density. Next: deterministic alpha/palette
cleanup, mattress registration, then connected lie/get-up source work. Preserve
the raw and all current runtime sprites.

Candidate cleanup is reproducible via `clean-marsh-sleep.py`: alpha threshold 128,
57x148 nearest-resampled body on 184x184 canvas, pivot (92,172), palette quantized
from opaque canonical idle pixels. Raw untouched; cleaned PNG/recipe JSON alongside.
First palette attempt incorrectly took sorted darkest colors; rejected and fixed
to derive a representative 256-color palette. Native candidate berth fixture uses
the existing rest-head anchor and candidate head source (92,34). It explicitly
marks the texture `crew_frame_92` to use the production pivot renderer; the initial
unmarked texture took a legacy crop path and is invalid evidence. Final log
`marsh-candidate-berth-final.log`; q0/depth96 candidate viewed. Still a single-pose
prototype, not installed animation or final identity acceptance.

One built-in six-pose transition source generated, no Higgsfield:
`marsh-lie-six-raw.png`, brief `marsh-lie-source-brief.md`. Visual source review
shows the required rear-standing to front-seated turn and increasingly reclined
poses, with consistent cream suit identity. Final generated pose has soles facing
camera and does not exactly match the selected sleep endpoint; preserve canonical
idle and selected sleeping endpoint when extracting. Raw remains unmodified.
Next: gutter extraction at one anatomical scale, endpoint continuity and native
bed contact review. This source is not installed or a completed animation.

`extract-marsh-lie.py` extracts six real alpha-separated pose columns, uses one
standing-derived scale and the canonical idle-north start. Palette derives from
opaque canonical idle pixels. Native-density source board inspected. The separate
vertical sleep candidate caused a large last-frame size/pose jump, so that join is
rejected; its endpoint is preserved as `rejected-separate-endpoint.png`. The current
alternate uses the same sheet's supine final pose, keeping source scale consistent.
`marsh-lie-extracted/recipe.json` records crop boxes and raw hash. Next: native bed
registration for this alternate and full forward/reverse motion review. No runtime
clip or source art changed; these are output-only candidates.
