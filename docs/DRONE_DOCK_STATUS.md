# Drone cradle operating-cue repair

The shared fleet renderer replaced the original ROV art in Mining and Salvage,
but its early return bypassed each host's former operating marks. Native v1
fixtures each failed four ROV motion assertions; these failures are preserved in
`output/batch-two/{mining,salvage}-fleet-native-v1.*`.

`rooms/production-ten/drone_dock_status.gd` adds two neutral, slowly varying
diagnostic lenses on the cradle posts. They retain dark fittings offline and use
the existing machine clock/operating flag. Parked drones stay still, without
exterior work animation. Deployed-vehicle logic, source pixels, room footprints,
crew and economy were not changed. The cradle cue also exists when the dock is
empty; it indicates the dock's operation, not a vehicle task or invented charging
resource mechanic.

## Verified scope

`{mining,salvage}-dock-status-native-v1` each exits 0 with no engine errors:
four quarters, per-host operation/offline/pause comparisons, containment,
non-overlap, canonical sockets and 728 route samples. Each records 29 full
1600x900 frames and four 257-square room crops. Both four-quarter crop sets and
both 512-square card exports were visually reviewed. Room silhouettes and aisles
remain clear; fine machine details merge at distant zoom. The four-corner base
composition still dominates and is not considered final organic-composition
acceptance. New fleet-art bounds still inherit the registered ROV proxy; these
checks do not establish a newly authored occlusion/collision map for every limb.

Cards now use `assets/drones/fleet-v1/mining-bay-card-dock-v2.png` and
`salvage-bay-card-dock-v2.png` in station previews, variants, deck lookup and the
production manifest. Both raster paths use Git LFS. Originals remain preserved.
The current profile dependency audit passes 15 profiles. Fresh 1280/2560 tests,
empty-dock state review, detailed crew occlusion and a post-repair export remain
pending. V30 packaged evidence predates these diagnostic lenses and cards.

## Revision hashes

| Artifact | SHA256 |
|---|---|
| Dock status helper | `683ad6e7c83fa231b53ea4d098fef60b277b36f0792ed1edc5d37dcec5523390` |
| Mining renderer | `49219956e7cb16b8b1f42d72e0c04d198fe9796221ae1fe83ce5ce7f963c1fad` |
| Salvage renderer | `88e8264cc1debdd8137d6e7e80476b50ce6e0ec4a16b03eef696805a9660d8ff` |
| Mining card | `62dde6ff7703facc9ef5980127d8803ad13c359a0c4b342e1b1c895f2a03bf36` |
| Salvage card | `0a715c644e6f1c9a3fb64f3e6823852db62496302a3d63a62b32a0bca7cfcb77` |

## Empty-dock and resolution follow-up

`tests/drone_dock_checks.gd` now drives the real fleet's phase dictionary and
exercises the normal grid-to-room binding. It does not merely set a view flag,
which the grid would overwrite. In every quarter it compares occupied and empty
cradle pixels, active/offline diagnostics, paused frames, and exact restoration
when the vehicle becomes docked again. The exterior vehicle is positioned away
from the room for this controlled state fixture. This does not simulate launch,
mission progress, delivery or docking timing end to end.

Six native runs pass with exit 0 and no engine errors:

- `mining-empty-dock-1600-v1`, `salvage-empty-dock-1600-v1`;
- `mining-empty-dock-1280-positive-v2`, `salvage-empty-dock-1280-positive-v1`;
- `mining-empty-dock-2560-positive-v1`, `salvage-empty-dock-2560-positive-v1`.

All evidence is under `output/batch-two/`. Each records 61 actual-size full
frames plus four room crops: 366 full frames across the six accepted runs.
The existing per-host, pause, containment and 728-route checks remain enabled.
Empty Mining q0 operating at 1600 and empty Salvage q3 offline at 2560 were
visually reviewed: the cradle stays visible after the vehicle disappears, and
darkness remains confined to the room. Fine details stay subtle at room scale.

`--negative-empty-dock` deliberately keeps the fleet docked. Its clean v2 run
exits 1 with precisely 12 expected binding/vehicle-presence assertions, showing
the new checks reject a failed deployment display. Negative v1 and Mining
1280 positive v1 also encountered temporarily missing concurrent card/scenery
files; they are retained, not counted as clean acceptance runs.

The helper SHA256 is
`9402477058067746d7a25859875b5814266fbb3b9bdf44ef3651652388507e56`.
Concurrent fleet work has since added hatch rendering and selected newer v3
cards; the v2 hashes above are historical repair evidence, not an assertion
that v2 is still the latest consumer. Dock status helper bytes remain unchanged.
Detailed crew occlusion and broader composition work remain pending. The bible's dock/vehicle distinction is
unchanged; both workflow copies now explain testing owner-driven display states.

## Packaged follow-up: V31

`output/batch-two/windows-validation-v31/verification.json` records a clean
Windows debug export and controlled tour: 30 arrivals, 84 reciprocal transitions
and 6493 movement ticks. PCK SHA256:
`367771f5c75b02766cd7cd4d638831b1eda225750b203685a90e20ec271d4f08`.

Both drone bays pass individual exported fixtures against that same package at
1280x720, 1600x900 and 2560x1440. Evidence is in
`output/batch-two/drone-dock-export-{1280,1600,2560}-v1/verification.json`.
All six runs exit 0, reject engine errors, exercise input isolation, and check
61 full-frame dimensions each (366 total). Four rotations include occupied,
empty, operating, offline, paused and restored states alongside existing routes.
Exported Mining q0 empty/active at 1280 and Salvage q3 empty/offline at 2560 were
visually reviewed: cradles remain visible and room-local darkness is retained.
These frames do not certify crew occlusion or end-to-end vehicle missions.

The generated fixture bridge now includes both drone bays and their state helper
(18 source records); all six bridge consistency tests pass. A subsequent
concurrent Archive fixture edit was detected by two consistency failures, then
the generated bridge was refreshed and all six passed again. That refresh does
not change or extend V31's frozen package evidence. Four-corner composition and
the new fleet sprites' inherited collision/occlusion proxies remain next work.

## Registration diagnostic

`tools/audit_drone_prop_registration.gd` decodes the runtime matte and measures
occupied, stationary atlas alpha envelopes at the actual draw transforms.
`output/drone-registration-audit-v1.log` records 16 combinations (two rooms,
ROV/hatch, four quarters). All decoded envelopes remain inside the walls, but
none is fully enclosed by its inherited visual proxy. Cradle alpha extends
about 1.4865 world units below the sort line; hatch alpha extends 1.0 unit.
The old Mining ROV visual envelope is 130.03 units tall versus 91.49 actual;
Salvage is 118.26 versus 87.46. North placements are consequently shifted using
obsolete upper silhouettes. This is evidence for refreshing visual registration,
not evidence that those alpha envelopes should become ground blockers or that
sort order must follow a shadow's last pixel. The diagnostic excludes lenses,
moving hatch apertures, filtering fringes and crew rendering. Next: separate
current visual bounds from authored ground contact/depth and inspect crew passes.

## Visual-bound repair

`drone_prop_bounds.gd` now supplies conservative current atlas draw quads for
ROVs/cradles and hatches, replacing only their inherited visual envelopes in
both room views. Bounds remain stable when deployed and include cradle lenses
and the hatch aperture envelope. Ground footprint sizes and sort anchors are
unchanged; wall clamping now uses the new art, so some prop positions change.
The alpha-enclosure regression exits 1 before this repair and 0 afterward
(`output/drone-registration-{red,green}-v1.*`); all 16 measured envelopes are
contained and inside walls. This remains separate from crew-overlap acceptance.

`output/{mining,salvage}-bounds-native-v1.*` records clean native 1600 runs:
each passes four-quarter operation/offline/pause, occupied/empty/restored states,
non-overlap, straight sockets and 728 route samples. New 512-square cards
`assets/drones/fleet-v1/{mining,salvage}-bay-card-bounds-v4.png` were inspected
and integrated in station/card/variant consumers and the manifest; originals
remain. Production composition dependency audit passes nine profiles. Godot
import exits 0 and assigns the helper's paired UID. New-card in-game review,
post-bound-change exported coverage and detailed crew depth review remain;
V31 predates this repair. The previously documented bounds lesson applies
without another change to the bible's aesthetic intent.

## Static crew depth evidence

`tools/capture_drone_crew_depth.gd` exercises the actual room sort queue with
Major Bill's current south sprite and compares it to explicitly ordered native
draws. V4 (`output/drone-crew-depth-v4/`) passes 48 static poses with no ordering
or sensitivity failures: both rooms, ROV and hatch, all four quarters, front,
behind and a deliberately non-walkable overlap pose. All 32 natural front/behind
positions are standable in the complete room before the diagnostic isolates a
prop. Forty overlap poses differ under reversed ordering; eight natural
behind-hatch poses correctly have no overlapping pixels and test clearance only.
This is not continuous movement, full-room wall occlusion or open-hatch safety.

V1 had a fixture class-name parse error; V2 wrongly required overlap for low-hatch
clearance poses. V3 passed ordering but clipped the upper character in some
diagnostic frames; V4 enlarges the canvas to 800 square. Failed/limited runs are
retained. Reviewed front-ROV, behind-ROV and forced hatch overlap show expected
layer ordering; the forced pose is not a reachable gameplay position. No crew
or production depth-order change was needed. Fresh export and continuous
gameplay-scale crew circuits remain pending.

## V32 packaged bounds and separate Bio Lab failure

Both corrected drone bays pass V32 individual exported checks at 1280x720,
1600x900 and 2560x1440, including input isolation and 366 full-frame dimension
checks. Evidence: `output/batch-two/drone-bounds-export-{1280,1600,2560}-v1/`.
PCK SHA256: `2db03b8bbfa9d0251b3c80545dfdd0bc3bee9f43b06925178a38433c97adee32`.
Native focused graph runs each pass 1216 pairs, 416 compatible connections and
9568 graph segments (`output/{mining,salvage}-bounds-graph-v1.*`). These are graph
checks, not continuous sprite circuits.

V32's complete tour is rejected despite 30 arrivals/84 transitions/6360 movement
samples: Bio Lab inherited Biodome's new dressing routes after replacing their
host props. Runtime engine-error detection caught the missing hosts; the
successful assertion banner was insufficient. Bio Lab now clears the inherited
profile before replacing hosts. Concurrent work adds its own profile, preserved.
`bio-dressing-isolation-v1` passes native four-quarter/five-economy-state tests,
five current hosts and 1212 socket samples without engine errors.
`test_bio_dressing_isolation.gd` verifies parent route hosts and rejects parent
hosts in the child in four quarters. V1 test incorrectly forbade any child
profile; V2 permits valid child-owned profiles and passes. Godot import is clean.
A fresh whole-station package is still required after these Bio Lab changes;
V32 itself remains failed overall and its drone-only evidence stays separate.

## Mining activity-layout V5

Mining's western deployment group now stages the hatch between the parked ROV
and its tool trolley/inspection lamp. Authored canonical centers are hatch
`(-111,20)`, trolley `(-120,112)`, lamp `(-168,98)`; source art and ground sizes
are unchanged. Centers rotate with the room while sprites stay south-facing.
The east service machine, component table and tether reel retain their positions.
This breaks the former matching corner rows without inventing additional props.

`output/mining-activity-native-v1.*` passes native 1600 four-quarter host motion,
offline/pause, empty/occupied/restored states, containment, non-overlap and 728
socket-route samples. All four rotation views and the 512-square V5 card were
visually reviewed. `mining-activity-graph-v1` additionally passes 1216 room pairs,
416 compatible connections and 9568 production graph segments. Production profile
dependency audit passes nine profiles. New LFS card
`assets/drones/fleet-v1/mining-bay-card-activity-v5.png` is selected by station,
card, alternate-art and manifest consumers; earlier cards remain preserved.
New-card in-game review, all-size/package follow-up and crew motion around this
changed layout remain open. Existing static crew depth and V37 package evidence
predate this repositioning. Lighting and refined service-line design remain
separate polish opportunities; this is not final owner composition acceptance.

## Salvage activity-layout V5

The intake bench moves inward to `(-96,12)`, the sorter settles at `(-117,130)`
and the recovery hatch sits below the winch at `(111,55)`. This makes offset
inspection/sorting and winch/recovery groups, leaving quiet staging floor at
the lower right instead of matching bottom corner machinery. Source art, sizes,
door topology and south-facing orientation remain unchanged.

`output/salvage-activity-native-v1.*` passes four native 1600 rotations, host
operation/offline/pause, occupied/empty/restored dock, containment, non-overlap
and 728 socket routes. The four rotated room views and 512-square card were
visually inspected. `salvage-activity-graph-v1` passes 1216 room pairs, 416
compatible connections and 9568 graph segments. Selected LFS card:
`assets/drones/fleet-v1/salvage-bay-card-activity-v5.png`, SHA256
`9602a7fdbda499a8a291fb11fd1ad4a4f97892b9e1b5faa8f27a88338cdc1737`.
Station/card/alternate-art/manifest consumers select it; previous cards remain.
Both V5 layouts still require all-size packaged follow-up and current-layout
crew motion review. Earlier technical acceptance does not transfer automatically.

## V5 verification follow-up

`output/drone-crew-activity-depth-v1/` repeats the 48 static isolated crew-depth
poses against the revised placements: zero ordering/sensitivity failures.
Reachable front/behind poses and forced overlap probes retain their distinct
scope. This is not continuous full-room crew motion review.

V38's debug package passes import, furnishing-host gate, export and controlled
tour: 30 arrivals, 84 reciprocal transitions, 6473 collision/speed samples and
no engine errors. PCK SHA256:
`2be1c3e5f113ad1a380d51aae13297e87a104f37beb7a76eea51410ccc37471d`.
The host gate records 26 views, 22 profiles and 204 references. Six fixture-bridge
consistency tests pass. Individual room-state runs are under
`output/batch-two/drone-activity-export-{1280,1600,2560}-v1/`.
The 1280 Mining q0 active full frame was inspected: its selected card agrees
with the rearranged room, and major silhouettes remain legible; fine tools are
small at this zoom. This is not an all-frames visual acceptance claim.

All six V38 individual runs complete cleanly: both rooms at 1280x720, 1600x900
and 2560x1440, with input isolation and 61 actual-size full frames each (366
total). Four-quarter operation/offline/pause and occupied/empty/restored states
pass against the same PCK. Continuous crew circuits and final owner composition
review remain open, rather than being inferred from these state captures.

## Continuous cradle circuits

`tests/playtest_drone_crew_circuits.gd` runs single-crew scheduled circuits through
the production graph, smoothing and movement methods, with the traveled-leg
observer checking every step. The real station renderer consumes Bill's position,
direction and walk/idle state. No player saves, gameplay costs or production
controller rules are changed by the fixture.

`output/drone-crew-circuits-v1/` passes eight circuits (both rooms, four rotations),
32 arrived legs and 1128 swept movement ticks, exactly 141 per circuit. Native
child exit is 0 without engine errors. There are 197 full frames including the
base fixture captures; movement is simulated at 0.1-second ticks and sampled
every eight ticks plus arrivals. These are sampled images, not full-speed video.
Godot import passes and generated the fixture's paired UID.

Reviewed Mining q0 side/rear and Salvage q3 front samples show the character in
the actual furnished room. On the northern rear path Bill's head projects above
the low north hull; retain this as a visual edge-case review, not a collision
failure or blanket visual approval. This pass covers cradle circuits only, not
circling every hatch/bench, multi-crew traffic, input-driven play or motion pacing.

## Timed capture review

`docs/drone-crew-review.html` provides room/rotation selection, timestamp-driven
playback, frame stepping, speed selection and a CSS close-up of the original
station images. It starts paused, stops at sequence end and does not invent
intermediate frames. The eight sequences contain 24 captures each (192); the
five base-fixture images are intentionally excluded. Keep the output directory
alongside the page's repository-relative links; it is not a standalone art bundle.

`node --test tests/test_drone_crew_review.cjs` passes three checks: all image links
and 1600x900 dimensions, eight complete sequence selections, and timestamp/step/
end/error controller behavior. Local HTTP delivery returns 200. Browser automation
failed to initialize, so these checks do not establish rendered browser layout or
full-speed animation acceptance. The north-wall projection decision remains open.

## Floor-hatch continuous circuits

The same native fixture now accepts `--hatch-circuits`, selecting the actual
registered hatch footprint instead of the ROV cradle. Missing subjects fail
explicitly; each trace records its prop identity. No production geometry,
character size, drawing order, or controller behavior was changed.

`output/drone-hatch-circuits-v1/` passes both bays in four rotations: eight
circuits, 32 arrived legs, 961 swept movement ticks at 0.1 seconds per tick.
The Godot child exits 0, reports zero assertion failures and has no ERROR or
SCRIPT ERROR entries. The fixture saves 176 actual 1600x900 PNGs, including
five base captures, with per-capture state and a complete movement trace.
Existing assertion labels still say "Cradle"; the selected subject and final
summary correctly identify the hatch. Generalize those labels on the next fixture
revision; this does not change what footprint the run exercised.

Agent-reviewed samples: `mining-q0-leg1-step008.png` (rear approach) and
`salvage-q1-leg3-step008.png` (front approach). Both show Bill moving beside the
machinery in the furnished station. Fine foot/rim detail is small at this zoom;
these two stills are not blanket visual acceptance or full-speed animation review.
This is a closed-hatch circulation check, not permission for crew to cross an
open deployment aperture or evidence that fleet deployment is crew-safe.

The earlier north-wall sample was re-inspected: the whole head projects into
the seabed backdrop while the feet remain inside. Do not call foot clearance a
fix, or simply clip the sprite to the floor and truncate the head. A reviewed
rear-wall/cutaway presentation remains necessary; no new hull aesthetic is locked
by this test. The finishing queue now separates the current 35-room catalog
from V38's frozen 30-room packaged tour.
