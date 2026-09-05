# Room art renewal and three discovery branches

Status: proposed detailed design for owner review. The hybrid art direction and
three playable branches are approved; implementation has not started.

## Purpose and boundaries

Make rooms recognizable at station scale, rewarding to watch while functioning,
and worth experimenting with. Renew all 31 current room identities (including
BRINE and routing rooms) and introduce three unlockable rooms. This produces 34
room identities, 33 playable blueprints and 34 discovery patterns (25 existing,
nine new). Preserve existing recipes and rewards rather than redirecting them.

This is two coordinated workstreams: art replacement in reviewable batches, and
a data-driven gameplay expansion. Neither requires splitting main.gd, changing
save format, adding resources, relocation, or introducing three-room recipes.

## Visual contract

Use the approved hybrid: cleaner compositions and prominent machinery with worn
metal detail. Retain the overhead cutaway view, quiet dark floors, restrained
colored light, consistent hull thickness, transparent exterior and clear routes.
Distinguish rooms by silhouette, not color alone. No baked labels or synergy hints.

Preserve every existing gameplay footprint and canonical door mask, even when
the old illustration disagrees with the room definition. Match door openings to
the renderer's connection positions. Do not introduce decorative false doors.
Give Data Archive its own archive silhouette instead of sharing Holographic Core.

Generate individual square PNG assets, not a concept board used as a spritesheet.
Use a shared 1280x1280 output canvas with consistent wall and door anchors; inspect
and normalize generated results before integration. Keep originals and save new
assets under rooms/hybrid/<room_id>.png through Git LFS. Update runtime PNG loading
and card thumbnails together. Existing alternate-art selection must not silently
fall back to the old style: use the new canonical image for all selections until
matching variants are deliberately authored. Do not change rotation or topology.

Approve the first Reactor, Hydroponics and Mining Drone Bay production previews
at actual game scale before extending the same style to the remaining batches.
Generated concept previews are not production acceptance evidence.

### Art batches (complete scope)

1. Pilot: reactor, hydroponics_bay, mining_drone_bay.
2. Infrastructure: solar_array, battery_array, salvage_drone_bay, ore_refinery,
   storage_bay, maintenance_bay, shield_generator, corridor, corner.
3. Living station: life_support, crew_hab, cryo_chamber, clone_lab, med_bay,
   biodome, bio_lab, crew_lounge, med_center, med_office.
4. Intelligence: brine_core, research_lab, quarantine_cell, data_archive,
   xeno_lab, anomaly_lab, command_center, holographic_core, radio_lab.
5. Expansion: tidal_condenser, mycelium_nursery, gravity_loom.

## New rooms: initial balance values

All are one-cell rooms, locked on a clean save, and use existing resources.
Costs are paid once; inputs and outputs below are per functioning cycle.

| ID / category / rarity | Build cost | Inputs | Outputs | Door layout | Future-run doctrines |
| --- | --- | --- | --- | --- | --- |
| tidal_condenser / Engineering / uncommon | 7 Metal, 2 Data | 2 Power | 2 Water | west, east, south tee | industry, biosphere |
| mycelium_nursery / Bio / uncommon | 7 Metal, 3 Biomass | 1 Power, 1 Biomass | 3 Food | west, east, south tee | biosphere, recovery |
| gravity_loom / Anomaly / rare | 12 Metal, 8 Data, 3 Rare Minerals | 4 Power | 1 Data, 1 Rare Mineral | four doors, perimeter path | science, anomaly |

No new storage bonuses. Condenser trades meaningful power demand for reliable
water. Nursery spends an existing biological resource, not a new waste currency.
Loom is intentionally inefficient alone and becomes useful through placement.
These are testable starting values, not claims of validated balance.

## Discovery graph (developer-only spoilers)

Each recipe requires matching connected doors and both endpoints functioning.
Bonuses below are additional to base production. New unlock recipes grant one
permanent blueprint and one current-run prototype using the existing pipeline.
Each further synergy grants 3 Research once upon stabilization, like existing
terminal patterns. No old terminal rewards or discovery IDs change.

| Pattern ID / name | Connected pair | Cycle bonus | Stabilization reward |
| --- | --- | --- | --- |
| thermal_reclamation / Thermal Reclamation | reactor + life_support | 1 Water | tidal_condenser |
| substrate_recovery / Substrate Recovery | hydroponics_bay + quarantine_cell | 1 Biomass | mycelium_nursery |
| inertial_containment / Inertial Containment | anomaly_lab + shield_generator | 1 Data | gravity_loom |
| nutrient_mist / Nutrient Mist | tidal_condenser + hydroponics_bay | 1 Food | 3 Research |
| chilled_cells / Chilled Cells | tidal_condenser + battery_array | 1 Power | 3 Research |
| culture_exchange / Culture Exchange | mycelium_nursery + bio_lab | 1 Biomass | 3 Research |
| restorative_culture / Restorative Culture | mycelium_nursery + med_bay | 1 Integrity | 3 Research |
| mass_sorting / Mass Sorting | gravity_loom + mining_drone_bay | 3 Metal | 3 Research |
| geometric_echo / Geometric Echo | gravity_loom + holographic_core | 3 Data | 3 Research |

Keep three consecutive functioning cycles, reset unfinished streaks on loss of
operation, and do not accelerate discovery with duplicate copies. Bonuses may
stack across valid copies under existing rules. Use start-of-cycle input budgets;
newly produced inputs cannot fund another room in the same cycle. Learned
forecasts show known bonuses only. No pre-discovery recipe names, partners or
rewards in cards, placement previews, journal, inspector or doctrine descriptions.

## Functioning graphics

Base art must remain intelligible with every effect disabled. New room machinery
effects are attached to the room itself and run only while it functions:

- Condenser: cyan tank fill motion and condensation along large chilled coils.
- Nursery: restrained light moving through fungal beds, with growth-like pulses.
- Loom: segmented rings and orbiting fragments suggesting localized distortion;
  no full-screen shader or camera movement.

Implement these as localized procedural overlays in grid_canvas using operation
state passed from main, separate from knowledge-gated synergy links. No global
time lookup that keeps machinery moving while paused. Suspension, starvation and
power loss stop machinery and active-link motion. Pause freezes motion. Preserve
existing brief discovery bursts and quiet learned-dormant indicators.

New recipes reuse flow, power, care, logistics, signal and containment profiles
where appropriate. Effects enhance rather than obscure doors and occupants. The
existing rooms retain these family-level functioning synergy effects; bespoke
animation strips for all 31 existing rooms are outside this expansion.

## Integration and failure handling

- room_database: three definitions, stable IDs, categories, layouts and tags.
- synergy_manager: nine additive recipes using the current evaluator.
- run_manager: unlocked room membership in the doctrines above; preserve finite
  deck weighting and essentials. Deduplicate membership across selected pairs.
- discovery_manager/meta_state: reuse current additive saves and reward paths;
  change only if tests reveal a compatibility defect, not for redesign.
- main/grid_canvas: new canonical art mappings, thumbnails and operation-state
  overlays. Keep changes localized and preserve the user's project.godot edits.

Missing/invalid new PNGs must be detected by asset validation before integration;
retain original art for rollback. Never replace source files with generation
failures or LFS pointers. Player saves are not used or overwritten by tests.

## Acceptance and verification

1. All 34 IDs have valid canonical art; no silent placeholder, shared unintended
   thumbnail, incorrect door opening, clipping or inconsistent room scale.
2. Clean-save graph reaches every new room; each recipe is physically placeable
   with the declared doors. Old saves retain their knowledge without free grants.
3. Tests prove paid costs, operating budgets, three-cycle rewards, interrupted
   streaks, duplicate copies, exactly one prototype and no repeated Research.
4. Locked rooms never enter normal drafts; unlocked rooms appear only through
   appropriate doctrine membership, except the explicit current-run prototype.
5. Tests cover hidden UI before discovery and known forecasts after discovery.
6. Native captures show each new room active, offline, suspended and paused, plus
   a real paid-build unlock and subsequent use. Inspect successive motion frames.
7. Run existing five regression/scene suites, GDScript parse checks and main-scene
   smoke. Inspect Godot logs for errors even when exit status is zero.
8. Inspect cards and station art at 1280x720, 1600x900 and 2560x1440, and fit a
   mature station. Keep doors, room identities and overlays readable.
9. Repeat matched and held-out seeded balance runs with real costs and deadlines;
   report discovery timing, new-room use and failures without treating bots as
   proof of fun. Include a targeted late-game Loom scenario if random runs miss it.

## Design review

Self-review: all rooms and art batches enumerated; no new recipe replaces an old
reward; new inputs use existing resources; nine recipes and three unlocks have
explicit values; visual previews and production acceptance are distinguished.
Implementation begins only after owner review of this written design and a
separate implementation plan. No gameplay or art assets changed by this document.
