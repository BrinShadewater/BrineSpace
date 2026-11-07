# Large rooms and Moonbay missions

## Intent

Add four memorable, expensive rooms that change station planning. Each occupies a 2×2 grid footprint, has four station doors, and features fixed large equipment with walkable routes. A run offers one of the four cards later in its draft. The first four new runs introduce Hydroponics Farm, Storage Depot, Moonbay, and Tidal Power Plant in that order; subsequent runs choose one randomly. This is a prototype feature for discovering satisfying placement decisions, not a new timed objective.

## Accepted player rules

- Each room occupies four normal cells as one room. Placement, construction reservation, selection, save/restore, flood/fire state, power, crew navigation, and rendering treat those cells as one footprint.
- Four station doors sit on valid cell-aligned perimeter segments. Rotation rotates the footprint and its ports. No internal seam gets an exterior door. Doors must remain reachable around fixed machinery.
- The Moonbay has four station doors across its three non-ocean walls: two on one wall and one each on the others. Its fourth wall has a sub launch hatch and must face open ocean. The Tidal Power Plant also needs an open-ocean intake face. Placement preview marks the required face and rejects blocked ocean cells.
- The rooms use Green (Farm), Yellow (Depot), Cyan (Moonbay), and Yellow (Power Plant), following the existing department colors.
- The rooms cost substantially more than ordinary rooms. Initial tuning targets: Farm 16 Metal + 3 Biomass; Depot 18 Metal; Moonbay 20 Metal + 2 Rare Minerals; Power Plant 18 Metal + 3 Rare Minerals. The exact numbers remain subject to paid-run playtesting.
- A run chooses exactly one large-room type. One copy enters a later draft draw, outside the opening hand. Once built, it cannot return through the discard recycle. Rerolling the card keeps its single opportunity in circulation until built or the run ends. The other three types do not enter that run.
- The first-four sequence advances on a new run, including a run ended before building its card. Persist the sequence index in profile state so restarts do not reset it; existing profiles begin at the first introduction. Subsequent runs choose randomly among all four. Save/Continue preserves the selected type and card state.

## Room identities

| Room | Fixed centerpiece | Function | Placement pressure |
| --- | --- | --- | --- |
| Hydroponics Farm | Long grow beds, irrigation spine, large grow lights | Strong Food and Oxygen output for Water and Power | Large interior with traversable crop aisles |
| Storage Depot | Tall cargo racks and overhead gantry | Major resource storage capacity | Connects several station routes through a central cargo aisle |
| Moonbay | Mini sub, maintenance cradle and launch rail | Crew missions for survey, recovery and deep access | Needs an open-ocean wall for the launch hatch |
| Tidal Power Plant | Turbine housing, shaft and heavy conduits | Major Power output while its intake faces open ocean | Its output depends on preserving an exposed ocean face |

Fixed centerpieces are not movable in Layout Studio. Smaller props may remain editable where that does not block ports or required routes. Art is top-down and inward-facing on all station walls. The four rooms need distinct card art at the existing card UI size; the cards do not occupy four card slots.

## Moonbay mission loop

The player assigns an available crew member and a destination. The crew member walks to the bay, boards the sub, and is unavailable for other station jobs until return. The dry hangar remains at station pressure. A separate sealed launch chamber floods for departure and return; its ocean hatch and station access are never open together. The player watches the mission unfold without steering.

Three orders share the trip: **Survey** reveals distant site information, **Recover** brings resources from a surveyed site, and **Deep Access** reaches sites beyond diver range. Routine missions are slow and dependable. Clearly marked hazardous sites offer better rewards but can damage the sub and force an early return. A damaged sub needs repair before another launch. Launch and mission progress obey pause, power loss, crew availability, and Save/Continue. First release can use simple route and work animations rather than a new piloting interface.

## Technical shape

Use a footprint/port helper shared by placement, construction, occupancy, navigation, environmental simulation, selection, and drawing. A room has one anchor, footprint size, and cell-aligned perimeter port positions. Occupancy maps all covered cells back to that one room; iteration over placed rooms still processes it once. Existing 1×1 rooms preserve their current behavior. Whole quoted `res://` paths name every new image.

Keep 2×2 geometry separate from room-specific effects. Existing deck generation owns the per-run large-room selection, while the Moonbay mission state lives beside existing crew/exterior mission systems. Avoid a general rewrite of `scripts/main.gd`; add small helpers and integrate at its existing call sites.

Placement checks every footprint cell against map bounds, terrain, deposits, wrecks, other rooms, and queued construction. It requires at least one matching station door. Ocean-facing checks include every cell needed by the hatch or intake and account for rotation. A rejected placement explains the actual obstruction. If a queued build is obstructed before completion, it remains safely pending or fails with its reserved resources accounted for; it must never partially occupy the grid.

Save/Continue stores the room anchor, rotation, type, footprint, and mission state. Loading older single-cell saves uses a 1×1 default. Each large room remains one damage/flood/power unit unless playtesting shows a need for per-cell simulation.

## Delivery and verification

Build in dependency order: (1) 2×2 placement, perimeter ports, rendering and save support; (2) four room data, fixed visual layouts, costs and draft scheduling; (3) room-specific production/storage/intake behavior; (4) Moonbay crew assignment, mission outcomes, repair and launch sequence. A playable milestone requires all four rooms and all three mission orders.

Use focused Godot subsystem tests for footprint collision, rotated port matching, ocean-facing rejection, one-card run sequence/randomization, discard behavior, paid construction, save/restore, crew routes, flooding/fire/power, and mission pause/resume. Run native visual checks for each room and rotation, card readability, fixed-prop clearance, ocean hatch, and the sub launch cycle. Run every test/probe with scratch `APPDATA` and fingerprint the owner's real save folder before and after, per `AGENTS.md`. Headless checks alone do not establish visual acceptance.

## Limits and open tuning

The initial values for production, capacity, mission duration, hazard frequency, and repair cost should be tuned through paid-run playtests. No direct sub steering, combat, permanent crew death, or new timed run objective is included. The prototype save format is not versioned; loading old saves still needs a safe 1×1 fallback.
