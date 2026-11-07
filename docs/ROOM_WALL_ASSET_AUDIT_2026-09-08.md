# Room and wall asset audit — 2026-09-08

## Result

No missing/undecodable selected room cards, unregistered furnished-room props,
missing department floor profiles, or broken literal asset paths were found.
This is not a claim that every composition or animation is artistically final.

- 43 database room identities and their selected cards reconciled against the rollout ledger.
- 40 furnished rooms rendered at all four orientations: 160 native captures.
- All 40 use the layered renderer and department floor profiles; every enumerated
  prop has a registration (baked perimeter pieces use their dedicated crop renderer).
- 475 dependency files traced; 299 PNGs decoded without errors. Six formatted
  character/recovery paths are dynamic templates, not missing literal files.
- All 33 full-wall registration source hashes match their selected image bytes.
- Contact sheets visually inspected at 0°, 90°, 180°, and 270°.
- Native station fixture passed all 43 identities at 1280, 1600 and 2560 widths.
- Straight, bend and T-junction native checks passed all four rotations.
- No engine/script errors were reported by these native audit runs.
- Shared north hull uses riser-wall-kit-style-v2 and wall-dressing-style-v2;
  corridors use generated source samples on their authoritative hull polygons.
  Shared construction materials, plain floor underlays and low-wall geometry are
  intentional components, not temporary missing-texture placeholders.

## Follow-up: directional identity gaps

Pressure Control and Listening Post only use their distinctive baked U-shaped
installations at 0°. At 90°, 180°, and 270° the runtime deliberately uses their
older life-support/acoustic equipment arrangements. These are real registered
assets, but they do not preserve the same visual identity across orientations.
The responsible configure_embedded branch is in each room's view under
rooms/underwater/rare-dead-ends/. The full-wall wrapper explicitly retains these
original installations. Do not replace them with previously rejected bright art.
Next art work should provide matching directional versions of the accepted art.

## Evidence and limits

Native captures and runtime inventory: output/room-art-audit/.
Card reconciliation: output/layout-editor/art-inventory.json.log.
Source facts: output/room-art-audit/source-audit.json.
Source/runtime audit does not exhaust every animation frame, recovered-room state,
wall adjacency combination or packaged export. Personal Studio drafts were excluded;
project defaults remain active. No art assets or user layouts were replaced.

Reproduce furnished captures with tools/audit_selected_room_art.gd, then run
tools/review_room_art_contact_sheets.gd. Corridor and assembled-station coverage use
tests/playtest_corridor_routing.gd and tests/playtest_floor_catalog.gd respectively.

## Selected furnished-room renderers

| Room | Runtime view | Floor source |
|---|---|---|
| current_turbine | rooms/power-expansion-v1/current_turbine_view.gd | res://assets/department-floors-v1/engineering-tread.png |
| biomass_digester | rooms/power-expansion-v1/biomass_digester_view.gd | res://assets/department-floors-v1/wet-drainage.png |
| heat_recovery | rooms/power-expansion-v1/heat_recovery_view.gd | res://assets/department-floors-v1/engineering-tread.png |
| airlock | rooms/underwater/airlock-v1/airlock_view.gd | res://assets/department-floors-v1/wet-drainage.png |
| construction_drone_bay | rooms/production-ten/construction_drone_bay_view.gd | res://assets/department-floors-v2/robotics-service.png |
| brine_core | rooms/underwater/brine-core/brine_core_view.gd | res://assets/department-floors-v2/brine-ceramic.png |
| solar_array | rooms/underwater/thermal-control/solar_array_view.gd | res://assets/department-floors-v1/engineering-tread.png |
| reactor | rooms/whole-room/reactor_view.gd | res://assets/department-floors-v1/engineering-tread.png |
| battery_array | rooms/production-ten/battery_array_view.gd | res://assets/department-floors-v1/engineering-tread.png |
| mining_drone_bay | rooms/full-wall-v1/mining_drone_bay_view.gd | res://assets/department-floors-v2/robotics-service.png |
| salvage_drone_bay | rooms/production-ten/salvage_drone_bay_view.gd | res://assets/department-floors-v2/robotics-service.png |
| gravity_loom | rooms/underwater/gravity-loom/gravity_loom_view.gd | res://assets/floors-and-details-v3/anomaly-floor.png |
| tidal_condenser | rooms/underwater/tidal-condenser/tidal_condenser_view.gd | res://assets/department-floors-v1/wet-drainage.png |
| mycelium_nursery | rooms/full-wall-v1/mycelium_nursery_view.gd | res://assets/floors-and-details-v3/agriculture-floor.png |
| hydroponics_bay | rooms/whole-room/hydroponics_view.gd | res://assets/floors-and-details-v3/agriculture-floor.png |
| life_support | rooms/whole-room/underwater_life_support_view.gd | res://assets/department-floors-v1/wet-drainage.png |
| crew_hab | rooms/full-wall-v1/crew_hab_view.gd | res://assets/department-floors-v1/habitation-composite.png |
| research_lab | rooms/full-wall-v1/research_lab_view.gd | res://assets/department-floors-v2/science-panels.png |
| cryo_chamber | rooms/full-wall-v1/cryo_chamber_view.gd | res://assets/department-floors-v1/medical-sealed.png |
| clone_lab | rooms/full-wall-v1/clone_lab_view.gd | res://assets/department-floors-v1/medical-sealed.png |
| quarantine_cell | rooms/production-ten/quarantine_cell_view.gd | res://assets/department-floors-v1/medical-sealed.png |
| data_archive | rooms/underwater/batch-two/data_archive_view.gd | res://assets/department-floors-v2/data-access.png |
| ore_refinery | rooms/full-wall-v1/ore_refinery_view.gd | res://assets/department-floors-v1/engineering-tread.png |
| storage_bay | rooms/production-ten/storage_bay_view.gd | res://assets/department-floors-v2/storage-load-deck.png |
| med_bay | rooms/full-wall-v1/med_bay_view.gd | res://assets/department-floors-v1/medical-sealed.png |
| biodome | rooms/underwater/batch-two/biodome_view.gd | res://assets/floors-and-details-v3/agriculture-floor.png |
| xeno_lab | rooms/full-wall-v1/xeno_lab_view.gd | res://assets/department-floors-v2/science-panels.png |
| anomaly_lab | rooms/underwater/batch-two/anomaly_lab_view.gd | res://assets/floors-and-details-v3/anomaly-floor.png |
| bio_lab | rooms/full-wall-v1/bio_lab_view.gd | res://assets/department-floors-v2/science-panels.png |
| command_center | rooms/production-ten/command_center_view.gd | res://assets/department-floors-v2/command-gunmetal.png |
| pressure_control | rooms/full-wall-v1/pressure_control_view.gd | res://assets/department-floors-v1/wet-drainage.png |
| listening_post | rooms/full-wall-v1/listening_post_view.gd | res://assets/floors-and-details-v5/acoustic-floor.png |
| isolation_vault | rooms/full-wall-v1/isolation_vault_view.gd | res://assets/department-floors-v2/command-gunmetal.png |
| crew_lounge | rooms/full-wall-v1/crew_lounge_view.gd | res://assets/department-floors-v1/habitation-composite.png |
| holographic_core | rooms/underwater/batch-two/holographic_core_view.gd | res://assets/department-floors-v2/data-access.png |
| maintenance_bay | rooms/full-wall-v1/maintenance_bay_view.gd | res://assets/department-floors-v1/engineering-tread.png |
| med_center | rooms/underwater/batch-two/med_center_view.gd | res://assets/department-floors-v1/medical-sealed.png |
| med_office | rooms/underwater/batch-two/med_office_view.gd | res://assets/department-floors-v1/medical-sealed.png |
| radio_lab | rooms/underwater/acoustic-comms/radio_lab_view.gd | res://assets/floors-and-details-v5/acoustic-floor.png |
| shield_generator | rooms/underwater/hull-integrity/shield_generator_view.gd | res://assets/department-floors-v1/engineering-tread.png |
