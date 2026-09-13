# Crew-relative room art scale

Updated: September 12, 2026 · Project: BrineSpace · Task: crew-relative art polish

## Objective and acceptance

Review in-game furnishings, machinery, doors and fixtures against existing crew sizes. Owner confirmed this scope. Native visual review is complete; owner acceptance and a playable export are not claimed.

## Accepted decisions and constraints

Use selected production Bill artwork at its existing 65.28 world-unit standing height, including source pivot metadata. Scale individual human-use objects by function: beds must accommodate crew, chairs and controls must be plausible to use, industrial installations may remain substantially larger. Preserve overhead direction, departmental material, floor contact and current room inventories. Character sources and timing remain unchanged.

## Current state

Reviewed all 47 current room identities and their supported catalog rotations. Adjusted 153 placements in 22 rooms: Hab, Lounge, Observation, the three medical rooms, Cryo, Current Turbine, Heat Recovery, Biomass, Mycelium, Clone, Bio, Anomaly, Xeno, Research, Solar, Shield, Listening, Maintenance, Reactor and Isolation. Other installations and doors retained after comparison. Cryopods now share a 62 by 90 footprint and no longer overlap in q0/q2.

- `rooms/full-wall-v1/default-layouts.json`: authored sizes/positions, preserving floor foot anchors or outward wall edges. Editor aliases and actual full-wall authoring identities agree.
- `rooms/full-wall-v1/med_center_view.gd`, `med_office_view.gd`: retained q3 stations honor saved size and position.
- `rooms/full-wall-v1/mycelium_nursery_view.gd`: source-polygon drawing and visible bounds follow resized bench/filter geometry; effects use those bounds.
- `tools/fit_equipment_to_crew.py`: bounded one-time migration; requires frozen before evidence and refuses a missing baseline.
- `tools/capture_room_catalog.gd`, `bake_current_architecture_cards.gd`, `bake_corridor_variants.gd`: optional production crew reference for review, absent from normal cards.
- `assets/crew-scale-v1/`: 22 refreshed cards, hashes, per-placement migration record and complete 47-room decision ledger. Selected card bindings updated in `scripts/room_card_art.gd` and `scripts/grid_canvas.gd`.

Native review: [47-room gallery](../output/crew-scale-review/index.html), [Hab/Lounge](../output/crew-scale-review/rotations-04.png), [Cryo](../output/crew-scale-review/rotations-05.png), [cards](../output/crew-scale-review/cards.png). Before evidence: `output/crew-scale-catalog-before/`. Latest merged captures and runtime geometry: `output/crew-scale-review/review.json`.

## Verification

- All 153 target sizes checked against final native card-bake geometry; zero mismatches.
- `test_preferred_room_layouts`: 176 layouts pass, including door connectivity (latest `output/test-runs/20260912-223220-headless/`).
- `test_cryo_recovery`: passes after normalized pod sizes and positions in that same run.
- Native scoped crew-life fixture: zero failures across 36 Hab/Lounge/Observation room/rotation/actor cases; checks approaches, activity transitions, saves, restoration and interruption. `output/crew-scale-life-native.log`. Captures establish placement/scale; they are not a new acceptance of all seated/sleeping animation artwork.
- Three changed leaf renderers: 12 room/rotation views across off/on/two clocks, including reused retained slots after power changes. All four direct/retained comparisons are pixel-identical. `output/crew-scale-render-states/`. This component check holds the clock explicitly; it is not a fresh whole-station pause test.
- Native visual inspection of all 47 room identities and the refreshed 22 cards; selected-card inventory passes 47 identities with zero errors. New PNG paths use Git LFS.
- Broader crew-life test has three Salvage q1 reachable-approach failures. Reproduced against the frozen pre-scale layout; untouched Salvage behavior is a pre-existing issue. The earlier Observation q0 approach failure is resolved by the scale pass. Native logs include existing raw-image export warnings; no release validation claimed.

## Next action

Review the gallery or current source build. No implementation work remains for this scale pass. Track Salvage q1 approach and wider crew animation acceptance separately; use the release workflow if a playable export is requested.
