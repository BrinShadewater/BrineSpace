# Owner playtest checklist cross-check

September 12, 2026. All 45 entries in the newly pasted list are accounted for below.
This is a source/handoff audit, not a new runtime test or owner acceptance pass.
Other sessions are actively changing art and animation; their recorded repairs
are not independently revalidated here.

**Correction to the previous closeout:** the general cryopod animation complaint
is separate from cold particles and blue tint. It remains open for animation
review. The original power/reserve and west-turbine reports remain unconfirmed;
the demonstrated paid-cycle bay bug was fixed, but is not proven to explain both
reports. Do not describe the entire owner list as complete.

Status meanings: **Implemented** means gameplay source plus prior scoped test
evidence; **Reported repair** means another session's current handoff records a
repair; **Review open** means this audit does not establish completion. No status
means the owner has accepted the visual result or tested a new packaged build.

| # | Owner request | Status / remaining check |
|---|---|---|
| 1 | Low power; reserves should discharge like a battery | **Partly resolved.** Paid-cycle bay/charging defect fixed; reserve accounting tested. Original low-power experience and balance still require the reported save/build or a fresh normal playtest. |
| 2 | West-facing Current Turbine does not boost power | **Unconfirmed.** Four-direction clear/blocked tests pass. No directional defect reproduced; feedback improved. |
| 3 | Start without a room selected | **Implemented.** Empty blueprint selection. |
| 4 | BRINE starts dark; lights, then pod | **Implemented.** Staged lights/consoles/pod; pause, power and Continue checks. |
| 5 | Cryopod cold particles and blue emerging character | **Implemented.** Runtime mist/tint; source art unchanged. |
| 6 | Cryopod animation barely moves | **Review open.** Six-frame wake playback remains in `scripts/architect_cryo_art.gd`; effects/startup changes do not establish improved opening motion. Animation-session scope. |
| 7 | Lower BRINE corner-wall fixtures | **Implemented and native-reviewed.** Both corner banks moved six world units down in every quarter; BRINE route/return coverage passes. |
| 8 | Visible north exterior airlock door; ordinary interior door; cycling exterior hatch | **Implemented.** North closed face and departure/return interlock; native and complete-trip evidence. |
| 9 | Replace low-resolution worn diving helmet | **Review open.** Character session has Veld helmet work; that is not proof of replacement/acceptance for every character, including Bill. |
| 10 | Reduce Solar/Turbine orange brightness | **Reported repair.** Solar facing and Current Turbine owner-repair handoffs. |
| 11 | “The wall length mining drone bay” | **Incomplete request.** No specific defect follows the phrase. Global camera/style direction still applies. |
| 12 | Standing/walking Studio scale character | **Implemented.** Bill preview and placement; no layout mutation. |
| 13 | Medical treatment walls overhead/inward | **Implemented and native-reviewed.** One blue south overhead bank now turns exactly through all four walls. |
| 14 | Medical side bed orange to matching blue | **Implemented and native-reviewed.** The selected overhead family uses the preserved muted-blue upholstery repair. |
| 15 | Mycelium use south-style overhead walls | **Implemented and native-reviewed.** The populated south bank now turns exactly through all four walls. |
| 16 | Crew Lounge use south-style overhead built-in | **Implemented and native-reviewed.** The preferred four-seat south built-in now turns exactly through all four walls. |
| 17 | Drone service wall style, colors and inward camera | **Implemented and native-reviewed.** The actual Mining Drone Bay consumer uses one matte blue/graphite/yellow overhead service bank through all four walls. |
| 18 | Refinery orange and white cutouts | **Reported repair.** Refinery owner-repair handoff. |
| 19 | Cryo Chamber inward overhead wall equipment | **Reported repair.** Cryo owner-overhead handoff; separate from entry 6. |
| 20 | Listening Post competing styles | **Reported repair.** Listening owner-repair handoff selects the preferred family. |
| 21 | Xeno wall jumbles across layouts | **Reported repair.** Xeno owner-overhead handoff. |
| 22 | Maintenance overhead walls and muted orange | **Reported repair.** Maintenance owner-overhead handoff. |
| 23 | Crew Hab overhead/inward berths | **Reported repair.** Crew Hab owner-overhead handoff; owner visual acceptance remains. |
| 24 | Bio Lab use preferred south culture wall | **Reported repair.** Bio Lab owner-overhead handoff. |
| 25 | Clone Lab use preferred side growth wall | **Reported repair.** Clone Lab owner-overhead handoff. |
| 26 | Remove old Isolation enclosure; retain stronger emergency wall | **Reported repair.** New Isolation owner-repair supersedes earlier removal audit's open q0 wings. |
| 27 | Remove misplaced Isolation battery equipment; matte test bench | **Reported repair.** Inherited battery furniture removed from Vault; matte bench source retained for Battery Array. |
| 28 | Turbine overhead north and muted orange | **Reported repair.** Current Turbine owner-repair handoff; power behavior remains entry 2. |
| 29 | Biomass green, dark equipment and white service-bench cutout | **Reported repair.** Biomass owner-material handoff. Require visual acceptance of all three concerns. |
| 30 | Construction Bay overly metallic; possibly redo drone | **Implemented and native-reviewed.** Static equipment and the live drone now use matte room-matched materials. The shared fleet source and recognizable drone silhouette remain exact; docked, travelling and articulated working states were reviewed. Current evidence does not support a silhouette redesign. |
| 31 | Remove Hydroponics harvest stand | **Reported verified removal.** Functional harvester preserved. |
| 32 | Tidal overhead equipment and matching walls | **Reported repair.** Latest Tidal owner-repair records native directions, operating, retained and pause checks. |
| 33 | Command matching wall and overhead/inward assets | **Reported verified repair.** Matching architecture, overhead table/systems/comms, state, retained and station-pause checks are recorded. |
| 34 | Remove decorative power cables globally | **Implemented.** Draw/placement filters; 176 rotations and cable/pipe pixel checks. |
| 35 | Remove Shield hull cradle; reduce orange | **Reported verified repair.** Cradle is absent and all four walls use restrained rust beneath graphite/steel. |
| 36 | Observation rotation; portholes part of background riser | **Reported verified repair.** Furnishings rotate; portholes remain background architecture; retained and station-pause checks pass. |
| 37 | Salvage Workshop overhead/inward | **Reported verified repair.** Overhead bench and tote rotate through four layouts with state/pause evidence. |
| 38 | Galley overhead kitchen and large mess-hall tables | **Reported verified repair.** Overhead kitchen/serving and two communal tables rotate through all layouts. “Gallery” maps to Galley. |
| 39 | Cold Store scale, overhead assets, central fridges/coolers, blue palette; later frost effect | **Reported verified repair.** Blue overhead banks, two central coolers and powered frost pass crew-scale, retained and pause checks. |
| 40 | Research Lab use preferred south analysis wall | **Implemented and native-reviewed.** The preferred south bank now turns exactly through all four walls. |
| 41 | Quarantine facing and white cutouts | **Reported repair, independently re-reviewed.** Four current native directions face inward and show no white exterior cutout. |
| 42 | Data Archive random floor power cable | **Implemented.** Same global retirement as entry 34; native Archive capture reviewed. |
| 43 | Anomaly east/west facing and remove task light | **Reported repair, independently re-reviewed.** Current east/west banks are overhead/inward and the task light remains absent. |
| 44 | Battery Array overly orange assets | **Implemented and native-reviewed.** All directions use muted rust/graphite; north also received its remaining overhead camera conversion. |
| 45 | Move Continue Loop preview right | **Implemented.** Saved/no-save and compact/normal native checks. |

## Evidence and next action

Gameplay evidence: [power](GAMEPLAY_POWER_HANDOFF_2026-09-12.md),
[Studio/menu](GAMEPLAY_STUDIO_MENU_2026-09-12.md),
[startup/hatch/cables](GAMEPLAY_STARTUP_HATCH_HANDOFF_2026-09-12.md).
Current art checkpoints: [status](CURRENT_STATUS.md),
[removals](OWNER_ASSET_REMOVALS_2026-09-12.md),
[Isolation](ISOLATION_VAULT_OWNER_ASSET_REPAIR_2026-09-12.md),
[Construction](CONSTRUCTION_DRONE_BAY_OWNER_MATERIAL_REPAIR_2026-09-12.md),
[Command](COMMAND_OWNER_ASSET_REPAIR_2026-09-12.md),
[Tidal](TIDAL_OWNER_ASSET_REPAIR_2026-09-12.md).

Keep entries 1, 2 and 6 explicitly open. Entry 9 remains with the character art
session and entry 11 is incomplete owner wording. The Construction drone review in
entry 30 found that a silhouette redesign was unnecessary after the material repair.
The actionable room-art queue is source-complete and agent-reviewed, but still
requires owner acceptance before an export can be called final. See
[strict-overhead closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md).
