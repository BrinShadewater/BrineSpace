The fourteen-room wall rollout is complete in the local checkout. Current acceptance: [full report](WALL_ROOM_ROLLOUT_ACCEPTANCE_2026-09-08.md). Earlier incremental statuses below are historical.

# Fourteen-room wall-art rollout

Updated: 2026-09-08 · Project: BrineSpace · Goal remains active

## Objective and acceptance
Complete all nine listed continuous wall installations and five door-aware split
installations, improving the maintained skill, workflow and visual bible as
verified lessons emerge. The authoritative scope/provenance/stage ledger is
`assets/wall-room-rollout-v1/rollout.json`.

## Accepted decisions and constraints
Darker restrained department palettes; all wall-bank interfaces face inward.
Preserve actual door topology, player layouts, existing functional props and source
images. No gameplay-balance changes, publishing or export requested.

## Current state
Verified pilot: Salvage Drone Bay, Construction Drone Bay, Anomaly Lab. Seven
selected source sheets, ten source versions including rejected attempts; ten
directional registrations. Station wrappers and three cards selected. Floor hosts
updated. New fleet placements reserve vehicle/hatch bounds before fitting furniture
and suppress stale routes. Existing Mining placement behavior retained; its older
vehicle overlap is outside this batch and was not newly certified by the scoped
relocation check.

Radio Lab is now also verified: top-down side decks place screens/windows toward
the wall and hand controls toward crew space. Eight floor anchors and four-rotation
crew routes pass; both side placements and default card updated. Earlier wall
elevations, rear-facing studies and all-left pairs are rejected/superseded.

Remaining: Shield Generator, Quarantine Cell, Med Center, Med Office,
Biomass Digester; split banks for Life Support, Hydroponics, Battery Array, Storage
Bay and Command Center. These remain briefed, not generated or integrated.

Pipeline: `tools/record_wall_source.py` preserves sources and prompts with separate
review status. Native full-wall review accepts a room filter and validates retained
fleet hosts. Skill reference `wall-room-rollout.md` and bible updated; three changed
skill files compared before syncing to the installed snapshot.

## Verification
- Pilot and Mining regression: four rooms × four rotations × two operating states;
  full-wall bounds, door lanes, relocated furniture, vehicle/hatch identities pass.
- Pilot floor anchors: 24 placements, zero missing.
- Pilot production crew routes: all three rooms × four rotations, zero assertions.
- Source audit: seven view identities / ten versions with verified hashes.
- Native pilot q0–q3 images reviewed; 25 enclosed white-background apertures removed
  from vector registrations, raster bytes unchanged. Three native cards refreshed.
- Evidence under `output/wall-rollout-pilot-v2`, corresponding review, anchor and
  route logs, and `output/wall-rollout-pilot-provenance-v1`.
- Native default-layout acceptance does not establish packaged or owner approval.

## Next action
Continue Shield Generator, Quarantine, Med Center, Med Office and Biomass, then
the five split banks. Ten rooms remain. Radio side-first generation did not
eliminate corrections; assistant confusion between facing direction and camera
elevation caused additional rejected revisions. Preserve the final owner contract:
fixed top-down view, fronts toward crew in the playable interior. Audit all
fourteen rooms and pipeline/bible updates before goal completion.

### Radio flush correction
Straight-flange source `radio-flush-v2.png` replaces the tapered side pair. Runtime mounts it to the canonical inner wall face at +/-184; scoped wall-mount envelopes retain draft safety and hull limits. Native four-rotation contact/door checks, eight floor anchors and twenty side/draft regression variants pass. Evidence: `output/wall-rollout-radio-flush/` and matching logs. Earlier registrations preserved under `assets/wall-room-rollout-v1/pre-flush-registrations/`.

### Shield source milestone
Generated and preserved `shield_generator.png` (1536x1024 side pair) and
`shield-pressure-wall.png` (2067x761 horizontal), with exact prompts and provenance
in the rollout ledger. Subjects retain the room's gunmetal/orange pressure-testing,
sealant and hull-patch identity. Side controls face the central aisle; outer
flanges are straight. Three vector registrations are staged under `shield-staging`
without changing runtime art. Actual regions: north 1976x423, sides 321x927 each.
Next: inspect cutouts and measured wall-contact seams, integrate the wrapper,
resolve floor/dressing hosts and card, then native four-rotation and crew tests.
Four rooms remain verified; Shield is generated, nine others remain briefed.


### Shield integration accepted by scoped checks
Shield now uses its full-wall wrapper, measured side registrations, grid preload, floor profile and refreshed room card. Native four rotations/two operating states passed bounds and door lanes; source hashes verified for both sheets. Floor anchor fallbacks fixed five missing placements, yielding eight placed and zero missing. Production crew routes passed all four rotations with zero assertions. Evidence: output/wall-rollout-shield/, matching review/anchors/routes logs, and wall-rollout-shield-provenance-v1. Pipeline reference and bible updated; installed reference synced after prefix comparison. Five rooms verified; nine remain. Next: Quarantine, Med Center, Med Office, Biomass, then five split installations.


### Quarantine verified
Integrated quarantine-specimen-wall horizontal and paired side sources, wrapper, grid preload, floor anchors and card. Preserved original berth by prioritizing it during relocation; added four-rotation presence assertion after native review caught omission. Eight floor placements, zero missing; native bounds/doors/two states and production crew routes pass. Evidence: output/wall-rollout-quarantine and corresponding review/anchors/routes logs; three source versions in provenance-v1. Bible and pipeline updated and synced. Six rooms verified; eight remain: Med Center, Med Office, Biomass, Life Support, Hydroponics, Battery, Storage, Command.


### Med Center verified
Added medical-diagnostic-wall sources/registrations/wrapper, grid mapping, floor hosts and room card. Both treatment and imaging apparatus survive all rotations; assertions added. center_dressing now participates in host cleanup, removing stale service references. Source edit darkened enamel and corrected side keyboard orientation. Native four rotations/two states, eight anchors and production routes pass without script errors. Evidence: output/wall-rollout-med-center and matching logs; provenance-v1 records three source versions. Bible and pipeline updated and synced. Seven rooms verified; seven remain: Med Office, Biomass and the five split banks.


### Med Office verified
Integrated medical-records-wall horizontal/side sources, wrapper, grid preload, floor profile and card. Prioritized exam couch and consultation seats; presence assertions pass every rotation. office_dressing participates in host filtering. q1 records marking scale reduced to 0.5; eight anchors now resolve. Native bounds/doors/two states and production crew routes pass. Evidence: output/wall-rollout-med-office and matching logs; two source versions verified by provenance-v1. Bible and pipeline synchronized. Eight rooms verified; six remain: Biomass plus Life Support, Hydroponics, Battery, Storage and Command split banks.


### Biomass source milestone
Saved side pair biomass_digester.png, north biomass-processing-wall.png (RGBA, 2172x724), and south biomass-processing-wall-south-v2.png with white background. Earlier frontal-side and opaque-checkerboard south versions retained as rejected. Runtime unchanged. Power baseline has a large power_machine and bespoke service/effect drawing, so integration must adapt its wrapper rather than blindly relocate a duplicate full skid; retain functioning feedback. Next register alpha/white sources correctly, integrate all four directions, resolve anchors/card and validate native/crew. Eight rooms verified, Biomass generated, five split rooms briefed.


### Biomass verified; continuous set complete
Integrated alpha north and white side/south registrations, power-specific wrapper, grid preload, floor hosts and card. Wall skid replaces original power_machine; operating indicator preserved on new art. South bank flush placement uses wall_contact and a matching native assertion. q3 drain scale 0.6 yields eight anchors with zero missing. Native four rotations/two states and production crew routes pass. Evidence: output/wall-rollout-biomass and matching logs; five versions audited in provenance-v1. Bible/pipeline updated and synced. Nine rooms verified. Remaining original scope: five genuinely split banks for Life Support, Hydroponics, Battery, Storage, Command; all still briefed. Do not mask the middle of continuous art. Need separate sections, door approach clearance, directional variants, cards, anchors, native and crew tests, then full fourteen-room completion audit.


### Life Support split source milestone
Generated life-support-split-north.png with separate fan and filter sections; rejected initial camera retained. tools/register_split_wall_props.py added and exercised on real source: two 712x465 regions, no divider contact. Staged JSON under life-split-staging. Runtime untouched. Remaining directions west/east/south must be authored; then two-footprint helper, door-clearance and retained-equipment checks, anchors/card/native/crew verification. Nine rooms still verified; Life Support generated-partial, other four split rooms briefed. Pipeline and bible updated/synced.


### Life Support directional sources complete
Saved life-support-split-sides.png (1448x1086, four cells) and life-support-split-south.png (1680x936, two cells). Side gauges face inward, south gauges face north. All eight sections registered without divider contact; staging paths are in the ledger. Four source versions verified in wall-rollout-life-split-provenance-v1. Runtime remains unchanged. Next implement separate two-section placement, using cardinal sources q0 north/q1 east/q2 south/q3 west, inner wall contact +/-184, and a clear central doorway lane; then preserve tank/console, operating feedback, floor hosts and cards and run native/crew checks. Nine rooms verified, Life Support generated, four other split rooms briefed.


### Life Support split verified
Added split_wall_prop.gd (+UID), eight registrations, split specification and wrapper (+UID); wired grid/floor/card. Two separate 128-unit sections meet inner walls and leave 112-unit doorway gap. Tank/console retained and asserted, fan motion restored, layout overrides preserved. Native four rotations/two states, eight anchors and production crew routes pass. Evidence: output/wall-rollout-life-split and matching logs. Pipeline/bible synchronized. Ten rooms verified; Hydroponics, Battery, Storage and Command remain briefed. Final full fourteen-room audit still required, including scoped shared-code regressions and draft/visual acceptance.


### Hydroponics directional source milestone
Saved hydro-split-north/sides/south.png and eight staged crop/nursery registrations; rejected upright-tank and horizontal-side versions preserved. Five source versions verified in hydro-split-provenance-v1. Runtime unchanged. Next reuse split helper with sections crops/nursery, replace old hydro beds, preserve harvest/nutrient equipment as space permits (harvest required), and validate floor hosts/card/native/crew. Ten rooms verified; Hydro generated; Battery, Storage, Command briefed. Bible/pipeline updated and synced.


### Hydroponics split verified
Integrated eight registrations, split spec/wrapper, grid preload, floor hosts and refreshed card. Harvest and nutrient equipment preserved in all rotations with native assertions. Fixed missing-bed service rendering that drew phantom lines to origin. Native four rotations/two states, eight floor placements and crew routes pass without errors. Evidence: output/wall-rollout-hydro-split and corresponding logs. Bible/pipeline synchronized. Eleven rooms verified; Battery, Storage and Command remain. Full rollout audit and shared-code regressions remain required.


### Battery directional source milestone
Saved battery-split-north/sides/south.png and eight staged cells/distribution registrations. Side source is portrait 1024x1536; registration uses native dimensions. All source sheets passed divider checks and three hashes audited under battery-split-provenance-v1. No source repair generation required in this batch. Runtime unchanged. Next integrate split-battery-wall specification/wrapper, retain live control/regulator equipment, resolve anchors/card and native/crew tests. Eleven rooms verified; Battery generated; Storage and Command briefed.


### Battery split verified
Integrated eight sections, split-battery-wall spec/wrapper, grid/floor/card. Breaker and distribution retained and asserted in all poses. q1/q3 standing mats scale 0.45 gives eight anchors; native four-rotation/two-state placement and crew routes pass. Evidence: output/wall-rollout-battery-split and matching logs. Pipeline/bible synchronized. Twelve rooms verified; Storage and Command remain, then full fourteen-room completion audit and shared-code/draft/visual regressions.


### Storage directional source milestone
Saved storage-split-north/sides/south.png and eight staged cargo/inventory registrations. Two rejected versions retain the control/handle corrections. Runtime remains unchanged. Next reuse split helper, replace storage_shelves/storage_secured_rack, preserve storage_lift and storage_crates, then floor/card/native/crew checks. Twelve rooms verified; Storage generated; Command briefed; final full-set audit remains.


### Storage split verified
Integrated eight registrations, split specification/wrapper (+UID), grid/floor/card. Lift and original cargo retained and asserted in all rotations. Native four-rotation/two-state placement, eight floor anchors and production crew routes pass with no errors. Reviewed output/wall-rollout-storage-split/four-rotations.png. Thirteen rooms verified; Command remains briefed, then full fourteen-room completion audit and shared-code/draft regressions.


### Command directional source milestone
Saved command-split-north/sides/south.png and eight staged operations/comms registrations. Native alpha north/south and white side sheet registered at actual dimensions; source checks separate from runtime. Next split helper wrapper replacing command_ops and command_comms, retain command_table/command_systems and operating feedback, then floor/card/native/crew. Thirteen rooms verified; Command generated; full fourteen-room completion audit remains.


### Command split integrated and placement verified
Integrated eight registrations, split specification/wrapper (+UID), grid/floor/card and normalized per-direction display feedback. Chart table and systems console retained and asserted. Native four-rotation/two-state placement, eight floor anchors and four production crew routes pass with no errors. Reviewed output/wall-rollout-command-split/four-rotations.png. All fourteen rooms now individually verified for placement/routes; full-set completion audit remains, including current source/card bindings, shared-code/draft regressions and actual animation pause/offline pixels. Goal remains active.


### Completion audit, first pass
Current full native review passes 14 rooms x 4 rotations x 2 states (output/wall-rollout-final-native.log); 112 floor anchors pass; legacy side/draft regression passes 20 variants. New tests/test_wall_rollout_drafts.gd (+UID) found invalid horizontal drafts were accepted by pilot banks. Extended validation to all nine continuous rollout IDs; all 56 rollout room orientations now pass invalid fallback, valid positions, and unchanged saved-data checks. Initial assertion-stalled process terminated by its 90-second runner timeout; successful rerun is final-drafts.log. Remaining: source/registration/card binding audit, inspect final pack native images, actual pause/offline pixel checks for new operating effects, consolidate completion evidence. Do not mark goal complete yet.
