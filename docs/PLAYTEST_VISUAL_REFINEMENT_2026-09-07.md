# Human playtest visual pass — September 7

Implemented in the working checkout:

- Exterior drones render before station surfaces. Native under-hull and no-drone images are byte-identical; an exterior drone changes the image. Vehicle simulation and resource rules are unchanged.
- Selected connections use thin translucent muted green strokes. Synergy pulses have much lower opacity, smaller motes and slower motion; containment no longer alternates abruptly.
- Shared room light pools are quieter and less green. Legacy door brightness multipliers and blue washes are reduced; door indicator whites are muted.
- Life Support, Quarantine Cell and Tidal Condenser preparation benches use local material tints. Their selected cards are regenerated and their hashes updated.
- Generated neutral deck plates feed the shared floor renderer while preserving department floor colours. Existing authored drains and dressing remain.
- Generated door surfaces are registered onto the existing two sliding leaves, retaining the 72-unit aperture and existing opening/collision behavior.
- The inspector room action now draws a generated industrial switch with a 0.18-second rocker animation and ON/OFF labels. It still uses Button input/focus and the original suspend/resume handler; resumption is scheduled for the next cycle. Salvage, repair and excavation keep their own actions.

Built-in image generation supplied the new art. Sources, exact prompts and hashes are under `assets/playtest-visual-v1/`. The pressure transparency repair failed and is retained as a rejected source; equipment-only registration excludes the checkerboard from the usable candidate.

## Pressure Control decision remains open

The refined large-gauge U-shaped machinery is integrated into the baseline pressure renderer. During this pass another active task introduced `rooms/full-wall-v1/pressure_control_view.gd`, which replaces its upper machinery with a new orange manifold. The owner has been asked which focal design to retain. The candidate gauge card is `output/playtest-visual-v1/catalog/pressure_control-card.png`; the station capture shows the concurrent manifold. Do not claim the gauge is selected in the live full-wall variant.

## Verification

- Native catalog: 40 baseline room identities, 320 rotation/state renders, plus shared-edge captures. This audit uses `rooms/decoration-integration/rooms.json`; it is not acceptance of every concurrently added full-wall variant.
- Native custom fixture: room toggle assertions, switch transition frames, exact drone occlusion comparison, and 1280/1600/2560 viewport captures. `tests/playtest_visual_refinement.gd` uses isolated save files.
- Native door review: four presets, 32 bidirectional crossings, four mixed-power/pause comparisons passed.
- Station operations, drone lifecycle and gameplay polish tests passed; preview doors reported 160 cases and zero failures.
- Godot editor import passed. Logs were checked for engine/script errors, not only exit codes.

Evidence lives under `output/playtest-visual-v1/`; logs are `output/visual-*.log`. Inspected native station, Life Support, Quarantine, pressure candidate and mixed-department door captures. The pressure source rectangle bounds were subsequently tightened to the existing floor envelope; final native station captures include that adjustment.

The September 7 packaged executable remains unchanged. These results describe the working project; a new frozen package must reconcile the concurrently changing art selections. Only the three named bench-room cards were replaced by this pass; a final catalog bake should follow settled room selections.
