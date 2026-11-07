# BRINESPACE — Visual Aesthetic Bible

An implementation reference for AI coding agents, environment artists, and procedural room systems.

## 1. Purpose and source of truth

Project edition: incorporates the owner's south-facing machinery and unused-doorway
infill decisions. The imported department guidance is preserved below; section 12
adds the production contract and records current implementation gaps.

Preserve a coherent visual language across BrineSpace's chunky, top-down pixel-art room cards. A player should recognize a room's department, function, condition, and navigable space before reading a label.

This document preserves the environmental system established in the **BrineSpace Aesthetic Bible** conversation. The shared-architecture section and explicit implementation constraints extend that system. These extensions are design guidance, not claims about existing code or assets. Exact colour values, tile sizes, door footprints, camera settings, and engine APIs were not established in the source; inherit them from the project rather than inventing replacements.

> **Colour identifies function. Material identifies department. Clutter identifies use. Damage identifies history. Lighting identifies mood.**

### Requirement vocabulary

- **MUST / MUST NOT:** visual invariants for implementation.
- **SHOULD / SHOULD NOT:** defaults; deviate only for a clear room function or authored story beat.
- **MAY:** optional variation within the system.

When modifying an existing project, inspect its assets and relevant project instructions first. Reuse compatible conventions. If a requested change conflicts with this bible, apply the explicit request locally and record the exception; do not silently redesign other departments.

## 2. Overall station design language

BrineSpace is **industrial retro-futurism + utilitarian space architecture + biopunk + subtle cosmic horror**. The station was built pragmatically, expanded repeatedly, repaired imperfectly, and eventually inherited by BRINE.

Avoid both universally sleek futurism and uniformly filthy industrial horror. Clean laboratories, warm quarters, heavy machinery, and unsettling spaces need contrast to matter.

Every department MUST inherit the same underlying station construction:

- Chunky modular wall panels and exposed structural ribs.
- Visible bolts, seams, access panels, and believable maintenance boundaries.
- Heavy pressure doors and modular cardinal airlock connections.
- Shared floor-grid and door dimensions.
- Dark structural framing beneath departmental finishes.
- Inset floor lighting and functional service routing.
- Pipes and cabling appropriate to the department, exposed or concealed deliberately.

Department identity is a finish and functional arrangement applied to common architecture. A Science Lab and Engineering Bay MUST look like parts of the same station. Smooth Medical and BRINE surfaces conceal more of the structure; they do not abandon its dimensions or connection rules.

## 3. Visual hierarchy and inheritance

### Construction hierarchy

Resolve a room in this order:

1. **Station base:** grid, silhouette, walls, hull structure, connection sockets, floor boundaries.
2. **Primary department:** architectural palette, material treatment, trim, normal lighting character.
3. **Room function:** focal equipment, workstation arrangement, storage, circulation.
4. **Secondary functions:** localized equipment and accents from other departments.
5. **Use and occupancy:** tools, possessions, working clutter, routine wear.
6. **Condition:** damage, emergency systems, dereliction, contamination.
7. **Readability pass:** preserve entrances, routes, interactive objects, and the room's focal hierarchy.

Later layers modify earlier layers; they MUST NOT arbitrarily erase them. Advanced anomaly transformation may obscure department identity as an authored exception, while traversal and interaction remain legible.

### Priority when visual rules conflict

1. Gameplay readability and accurate collision/interaction cues.
2. Shared station structure and connection compatibility.
3. Primary department identity.
4. Room function and secondary equipment.
5. Narrative condition and decorative detail.

A visual overlay MUST NOT imply a blocked path, open doorway, broken window, or usable console when gameplay says otherwise. Implement actual state changes alongside their visuals.

## 4. Department palette, material, lighting, and character

Palette names are semantic roles, not prescribed hex values. Base surfaces SHOULD dominate area; department colours SHOULD appear in readable panels, equipment groups, and trim; emission SHOULD remain localized.

| Department / category | Primary palette | Materials | Lighting | Visual character |
|---|---|---|---|---|
| Science | White + blue; cool grey and cyan | Ceramic/composite plating | Cool white / cyan | Precise, sterile, analytical |
| Command & Operations | Deep red + gunmetal; brushed steel and white | Finished/brushed metal | Warm white with red accents | Controlled, military, authoritative |
| Engineering | Burnt orange + charcoal; steel and hazard yellow | Raw industrial steel | Amber/orange; harsh white task lamps | Heavy, mechanical, dangerous |
| Agriculture / Bio | Green + white; pale grey and natural plant colours | Composite, glass, moisture-resistant surfaces | Bright full-spectrum white with green accents | Organic, humid, alive, hopeful |
| Medical | White + teal; pale cyan | Seamless ceramic, glass, soft-edged equipment | Soft white / teal | Calm, clinical, humane |
| Crew / Habitation | Cream + warm orange; brown and muted grey | Painted panels, textiles, plastic, synthetic wood | Soft warm amber/yellow | Cozy, improvised, human |
| Logistics / Storage | Yellow + neutral grey; black markings | Raw modular metal | Neutral industrial | Practical, modular, cluttered |
| Robotics / Drones | Dark grey + cyan; yellow handling details | Precision finished industrial metal | Cyan / white | Automated, precise |
| Security | Deep red + black; dark gunmetal | Armoured metal | Red / stark white | Defensive, intimidating |
| Life Support | Cyan + green + grey | Industrial surfaces and insulated piping | Cool white | Mechanical-organic, sustaining |
| Data / Computing | Black + cyan; dark blue | Dark finished metal and glass | Local cyan / blue in dark surroundings | Quiet, cold, computational |
| Anomaly / Xeno | Purple / ultraviolet + black; sickly cyan | Altered host materials, unknown/composite surfaces | Violet, unstable, localized | Forbidden, uncanny |
| BRINE / Core | Pearl white + cyan; aquamarine and glass | Ceramic, glass, smooth metal, water | Soft aquatic cyan | Unique, serene, uncanny |
| Derelict / Abandoned **condition** | Rust + brown over inherited colours | Corroded original station materials | Emergency amber where power remains | Decayed, dangerous |

Derelict is listed for palette reference but MUST be implemented as a condition, not as a replacement department. Anomaly can be a dedicated room identity or an intrusion into another department; preserve the host where applicable.

## 5. Department specifications

### 5.1 Science

**Architecture:** White ceramic/composite panels, cobalt-blue structural sections, cool-grey support surfaces. Science has among the smoothest ordinary station finishes. Use pale-grey flooring with blue navigation markings.

**Layout and equipment:** Recessed instruments, clean mounting, tidy cable channels, symmetrical workstations, screens, sample storage, and analysis surfaces. Precision and controlled experiments drive the layout.

**Room examples:**

- General Science Lab: benches, microscopes/scanners, sample cabinets, restrained holographic displays.
- Chemistry / Materials Lab: containment cabinets, chemical storage, analysis machines.
- Physics Lab: one large experimental apparatus dominates the room.
- Anomaly Research: white/blue host architecture with localized purple/black contamination.
- Xenobiology: Science architecture, green biological equipment, optional anomaly intrusion.

**Do:** use ordered instrumentation and clean material boundaries. **Don't:** replace scientific identity with generic cyan glow or make every lab an anomaly chamber.

### 5.2 Command & Operations

**Architecture:** Deep-red panels and stripes over gunmetal and brushed steel. Finishes are deliberate and architectural. Red MUST generally be an accent or panel group rather than an all-surface bright-red fill.

**Layout and equipment:** Large consoles, maps, status boards, wall displays, and central command tables communicate authority, information, and control. Operator positions SHOULD face the primary information source.

**Room examples:** Command Center with a central tactical/navigation display and surrounding stations; Communications with signal controls; Navigation with star charts and orbital maps; Observation / Operations with reinforced windows and outward-facing consoles; Drone Control with cyan robotics consoles inside red command architecture.

**Do:** organize information around a clear command focus. **Don't:** substitute exposed workshop machinery or Security's bunker-like armour for finished Command surfaces.

### 5.3 Engineering

**Architecture:** Burnt-orange sections over charcoal and raw steel. Show welds, grates, pipes, conduits, pressure tanks, cable bundles, and access panels. Maintenance needs determine the architecture.

**Lighting:** Amber work lamps, orange equipment indicators, occasional harsh white maintenance lights. Keep machine silhouettes readable against the dark structure.

**Room examples:** Reactor with a massive central machine; Power Distribution with transformers, breakers, cabinets, and conduits; Battery Room with modular banks; Solar Control with more electronics; Shield Generator with a large electromagnetic apparatus; Maintenance Workshop with tools and dismantled equipment; Waste Processing with additional grime.

**Do:** imply mechanically connected systems and service access. **Don't:** scatter pipes as random texture, cover the entire floor in hazard stripes, or obstruct all circulation with machinery.

### 5.4 Agriculture / Bio

**Architecture:** White composite walls, green accents, pale-grey supports, glass, transparent tubing, and moisture-resistant surfaces. Share Science's construction family with a softer, living character.

**Lighting:** Bright full-spectrum growing light and sunlight simulation. Green marks identity; it SHOULD NOT turn the entire room into a monochrome green wash.

**Room examples:** Hydroponics with growing trays, water feeds, and LED grow systems; Biodome with trees, grass, water, and possibly artificial weather inside a station shell; Algae / Nutrient Production with green-liquid tanks and processors; Seed Vault with cooler, darker, extremely organized storage.

**Do:** use plants and water to create a hopeful contrast. **Don't:** treat ordinary growth as contamination or hide the station's structural boundaries beneath decorative foliage.

### 5.5 Medical

**Architecture:** Seamless white ceramic, teal equipment, pale-cyan accents, soft-edged fittings, and glass medical cabinets. Keep Medical visibly distinct from Science: Science studies; Medical sustains life.

**Layout and equipment:** Calm spacing, accessible treatment positions, clean task surfaces, and soft white lighting.

**Room examples:** Medbay with perimeter beds and diagnostics; Surgery with a central operating platform; Cryo Chamber with orderly pod rows; Clone Lab with Medical architecture, scientific instrumentation, and translucent biological tanks.

**Do:** let advanced procedures become subtly biopunk through equipment. **Don't:** make all medical spaces sinister, blue scientific labs, or blood-covered rooms by default.

### 5.6 Crew / Habitation

**Architecture:** Cream and muted-grey painted metal, warm-orange details, brown synthetic surfaces, fabric, plastic, and occasional rugs. Lighting is soft, warm, and human-scaled.

**Room examples:** Crew Quarters with beds, lockers, and personal belongings; Lounge with couches, tables, screens, and games; Galley combining an industrial kitchen with communal dining; Hygiene rooms with compact utilitarian modules; Recreation with exercise and entertainment equipment.

**Occupancy:** New quarters may be sparse. Lived-in spaces MAY accumulate posters, mugs, plants, laundry, photos, books, tools, and questionable decorations. Personalization SHOULD cluster around the people and activities implied by the room.

**Do:** use clutter to tell human stories. **Don't:** make warmth depend on Engineering's burnt-orange industrial finish or let possessions obscure paths and interaction targets.

### 5.7 Logistics / Storage

**Architecture:** Neutral-grey raw modular metal, yellow handling zones, black markings, neutral industrial illumination.

**Room examples:** Storage with crates, shelving, and containers; Ore Storage with bulk bins; Cargo Airlock with large loading doors and handling equipment; Salvage Processing with messier storage and machinery; Refinery with Engineering structure and Logistics markings.

Yellow communicates **move / store / handle this thing**. Use it on loading areas, container identifiers, handling equipment, and transfer routes. Hazard warnings need a distinct stripe pattern or symbol.

**Do:** group cargo into plausible storage and transfer zones. **Don't:** confuse decorative crate density with blocked movement or paint all structural surfaces yellow.

### 5.8 Robotics / Drones

**Architecture:** Dark-grey precision industrial metal, cyan diagnostics and active stations, limited yellow handling details. The room feels like Engineering cleaned up by robots.

**Room examples:** Droid Bay with perimeter charging stations, repair benches, and diagnostic arms; Drone Bay with racks, launch rails, and airlocks; Drone Maintenance with partly disassembled units, spare components, and automated repair machinery.

**Do:** use repeated docking forms and precise service geometry. **Don't:** make Robotics indistinguishable from dark server rooms; physical drones, manipulators, rails, and repair stations establish its function.

### 5.9 Security

**Architecture:** Deep red, black, dark gunmetal, armoured plating, reinforced floors, and visibly heavier doors. Command uses red elegantly; Security uses it aggressively.

**Room examples:** Security Station with surveillance monitors, weapon lockers, and a holding area; Armoury with dense secured storage and limited but readable access space; Brig with sparse, cold cells and almost no decoration; Defensive Control with weapons/turret interfaces.

**Do:** communicate reinforcement through thick frames, layered plates, and controlled access. **Don't:** rely on red alone to distinguish Security from Command or imply stronger gameplay protection solely through decoration.

### 5.10 Life Support

**Architecture:** Grey industrial surfaces with cyan/green systems, insulated pipes, ducts, fans, filtration equipment, pressure vessels, and transparent water tanks. This category sits between Engineering and Agriculture.

**Room examples:** Atmospheric Processor with large ventilation machinery; Water Recycling with tanks and visible fluid routing; Oxygen Generation with mechanical and biological systems.

**Do:** show connected infrastructure that visibly keeps the station alive. **Don't:** reduce Life Support to an orange workshop or a plant-filled greenhouse; processing and circulation are its defining forms.

### 5.11 Data / Computing

**Architecture:** Black and dark-blue finished metal/glass with localized cyan lights. These are unusually dark rooms, but navigable floors and doors remain identifiable.

**Room examples:** Data Archive with server racks arranged like library shelves; AI Processing with large computational structures; Sensor Processing with incoming telemetry displays. Human workspace is minimal.

**Do:** use repeated racks and restrained blinking lights to create a quiet, cold rhythm. **Don't:** flood all surfaces with cyan emission or borrow BRINE's pearl-white aquatic chamber treatment for ordinary computing.

### 5.12 Anomaly / Xeno

**Core rule:** Purple is primarily something that **happens to other rooms**, not ordinary department paint.

Begin with a legible host room when depicting research or contamination. Introduce violet specimen light, discoloured panels, growth through seams, impossible screen patterns, and increasingly strange geometry. Unknown/composite surfaces, ultraviolet, black, and sickly cyan become stronger as transformation advances.

**Progression example:** Science → Xeno Science → Contaminated → Anomaly. This describes a possible visual story, not a mandatory simulation sequence.

**Do:** concentrate early effects near the specimen, containment failure, or intrusion source; preserve host remnants into later stages. **Don't:** recolour an ordinary laboratory entirely purple as a shortcut or distort functional doors and collision boundaries without matching gameplay changes.

Dedicated anomaly spaces MAY be dominated by altered geometry. Their unusual character SHOULD remain exceptional within the station.

### 5.13 BRINE / Core

**Architecture:** Pearl-white ceramic, cyan and aquamarine illumination, glass, smooth metal, water, and subtle holographic elements. Almost no exposed machinery. This language connects to BRINE's pearl-white plating and transparent water chamber.

**Composition:** A central chamber combining computer core, aquarium, and an accidental shrine-like presence. Use perfect symmetry, a dark surrounding floor, soft aquatic reflections, tiny bubbles, and cables disappearing beneath the floor. The atmosphere is quiet, serene, and subtly uncanny.

**Do:** reserve visual space and attention for BRINE's chamber. **Don't:** add overt worship iconography without narrative direction, fill the room with Command-style screens, or spread this exclusive treatment across unrelated rooms.

## 6. Hybrid-room rules

> **Architecture = primary department. Equipment and accents = secondary function.**

Every ordinary hybrid MUST have one primary department. It owns wall finishes, structural trim, default flooring, and the room's normal lighting character. Secondary departments affect identifiable equipment groups, local task lights, labels, and functional zones.

Do not average palettes into a new unrelated scheme or divide every wall into competing department colours. A third influence SHOULD remain confined to a specific feature or condition.

| Hybrid | Primary architecture | Secondary contribution | Result |
|---|---|---|---|
| Clone Lab | Medical | Science instrumentation + Bio tanks | White/teal walls, blue instruments, green biological tanks |
| Ore Refinery | Engineering | Logistics handling | Orange industrial walls, yellow cargo markings |
| Xenobiology | Science | Bio equipment + optional anomaly condition | White/blue walls, green tanks, localized purple specimen glow |
| Drone Control | Command & Operations | Robotics consoles | Red finished metal, cyan drone interfaces |
| Salvage Processing | Logistics when sorting/storage dominates | Engineering machinery | Grey/yellow storage architecture with industrial processing equipment |

Choose the primary from the room's dominant function. A machine-led processing plant can inherit Engineering; a sorting warehouse can inherit Logistics. Record the choice explicitly rather than inferring it differently in each renderer.

## 7. Room condition layers

Condition is independent of department. Preserve underlying palette and construction wherever the narrative permits.

| Condition | Visual treatment | Constraint |
|---|---|---|
| New | Clean surfaces, complete panels, minimal clutter | Retain seams, ribs, and material identity |
| Operational | Active instruments, stocked work areas, normal light | Function must be apparent |
| Used | Local scuffs, tools, occupancy clutter, maintenance traces | Wear follows actual use |
| Damaged | Broken panels, leaks, exposed wiring, debris, failed equipment | Visual damage must agree with relevant gameplay state |
| Emergency | Backup illumination, warnings, partially failed normal lights | Keep route and door-state cues readable |
| Derelict | Rust/brown corrosion, dust, missing panels, abandoned contents | Retain original finishes in surviving areas; use emergency amber only where power remains |
| Contaminated | Biological/anomalous intrusion, altered light and surfaces | Identify the contamination type; ordinary plants are not automatically contamination |

The source's New → Operational → Used → Damaged → Emergency → Derelict → Contaminated sequence is a storytelling progression. Implementation SHOULD allow independent, compatible conditions: a used room can be operational; a damaged room can have emergency lighting; contamination need not wait for abandonment.

Examples:

- **Engineering:** orange steel → localized grime → leaking pipe and damaged wiring → backup lights → corroded abandoned machinery.
- **Science:** clean white/blue → active experiment clutter → broken glass and sample spill → emergency lighting → anomaly growth through panel seams.
- **Crew:** sparse cream panels → possessions around a bunk → displaced furniture and damaged lighting; personal traces remain visible.

Overlays SHOULD attach to plausible sources and surfaces. Avoid uniform noise, random rust on every material, or global tints that erase department identity. Emergency red is a temporary state cue; distinguish it from permanent Command/Security red using warning symbols, placement, or restrained animation.

## 8. Shared architecture and department transitions

The following rules extend the established station grammar to connecting spaces.

### 8.1 Corridors

- MUST share the station grid, structural framing, and connection dimensions used by rooms.
- SHOULD use neutral grey/gunmetal structure and dark ribs as the station-wide default.
- Use restrained destination-colour strips, signs, or doorway trim to indicate nearby departments.
- A corridor wholly inside a department MAY inherit its finishes while retaining common corridor proportions.
- Keep the walking lane visually continuous; place services along walls or in clearly bounded recesses.
- At junctions, pair directional markings with a department symbol or label. Do not turn a shared corridor into a competing rainbow of full-width floor colours.

### 8.2 Doors

- An unused connection socket MUST be filled by a flush, removable wall infill
  panel, not left as an exposed gap or apparent passage. Match the neighboring
  wall's thickness, structural frame, panel rhythm, and room-facing finish.
- A subtle seam or fasteners MAY identify the removable panel. An unused socket
  MUST NOT show an open threshold, passage shadow, active access light, or
  freestanding door jambs that imply usable access.
- A side with no supported socket remains an ordinary solid wall. A supported
  but unconnected socket remains in connection metadata beneath its infill.
- Remove infill only when a valid connection exists on both adjoining sides.
  Use one shared edge assembly; never stack two independent doors or covers.
- A connected-but-closed or locked door is NOT an unused socket. Retain its
  recognizable door leaf and corresponding state cues where those states exist.
- Suspension or loss of room power alone MUST NOT wall over a valid connection.

- Reuse the project's standard door footprints and cardinal sockets. Apply department styling within compatible frames.
- Normal door frames inherit station structure; room-facing trim MAY inherit the primary department.
- Open, closed, locked, and damaged states MUST differ by geometry or recognizable symbols as well as colour where those states exist in gameplay.
- Security doors use visibly heavier plates and frames. Cargo doors MAY use a supported larger module, not arbitrary resizing.
- Keep access controls visible and consistently placed where the asset system permits.

### 8.3 Airlocks

- Use heavy frames, pressure seals, threshold markings, status panels, and a clear chamber identity.
- Reuse modular cardinal connections; align adjoining room sockets exactly.
- Distinguish airlocks from ordinary doors through pressure-related equipment and chamber structure.
- Cargo airlocks inherit Logistics handling cues; personnel airlocks retain neutral station structure with destination accents.
- Visual seals, warning states, and apparent openings MUST match implemented pressure/door states where simulated. Decorative detail does not create new airlock mechanics.

### 8.4 Windows

- Use thick reinforced frames, restrained glass highlights, and visible supports.
- Maintain a clear distinction between glass, a screen, an open passage, and the exterior void.
- Observation/Operations windows SHOULD align with outward-facing consoles; laboratory and medical observation glass SHOULD support the room's function.
- Large windows reuse structural bays and imply reinforcement. Do not erase all hull support for a panoramic view.
- Cracks and breaches SHOULD correspond to actual state where they affect traversal or pressure.

### 8.5 Hull and walls

- Separate dark structural hull from interior department cladding.
- Maintain consistent wall thickness, panel rhythm, corner treatment, and exposed outer edges using existing project conventions.
- Department colour belongs mainly to interior panels, trim, and selected structural sections; it SHOULD NOT recolour the entire external hull.
- Damage MAY reveal the common dark skeleton beneath different department finishes.
- Smooth departments still retain readable module boundaries and maintenance access.

### 8.6 Floors

- Use the shared floor grid and consistent perspective. Floors SHOULD remain quieter than equipment and interactive objects.
- Science: pale grey with blue navigation details. Engineering: steel/grates with localized hazard markings. Agriculture: pale moisture-resistant surfaces with green zones.
- Medical: clean light surfaces and teal guidance. Crew: warmer painted surfaces and limited textiles. Logistics: neutral loading surfaces with yellow handling zones.
- Command: finished dark/neutral surfaces with restrained red trim. Security: reinforced dark panels. Robotics: precision service pads and cyan docking cues.
- Life Support: service flooring around fluid/air systems. Data: dark aisles separated from rack bases. BRINE Core: dark floor supporting the bright central chamber.
- Mark machine footprints and transfer zones deliberately. Do not make harmless floor ornament resemble pits, obstacles, or interactable objects.

### 8.7 Signage

- Establish a consistent station-wide sign frame, placement convention, and icon style.
- Combine department colour with a symbol and, where readable, a short label. Meaning MUST NOT depend on hue alone.
- Keep navigational, identification, and warning signs visually distinct.
- Logistics yellow denotes handling; yellow/black warnings add a hazard pattern or symbol. Red department trim is distinct from active alarm signage.
- At gameplay scale, icons and large graphic blocks take priority over tiny text. Decorative microtext MAY add texture but MUST NOT carry required information.

### 8.8 Department transitions

- Keep the underlying ribs, wall thickness, floor grid, and door sockets continuous across a boundary.
- Change finishes at a believable panel seam, doorway, vestibule, or floor threshold.
- Each side of a doorway MAY carry its own department trim around a shared neutral structural frame.
- Secondary equipment near a boundary does not automatically recolour the host architecture.
- Transition examples: neutral corridor → blue/white lab portal; Command red/brushed-metal side → Security red/armoured-black side; Engineering orange service area → grey/yellow cargo threshold; Science blue/white structure → increasingly localized purple intrusion.
- Do not use a soft colour gradient as a substitute for material changes. Anomaly spread may cross seams organically, but ordinary department boundaries are constructed.

## 9. Pixel-art and gameplay readability

- MUST preserve the chunky top-down room-card approach and the project's established camera/pixel conventions.
- Use large readable colour masses and accents; identity MUST survive viewing at actual gameplay size.
- Keep wall, floor, object, and void values sufficiently distinct. Verify in greyscale as well as colour.
- Organize each room around a clear focal apparatus or functional group. Place supporting machinery against walls/corners where practical; central reactors, surgery platforms, experiments, and BRINE's chamber are intentional exceptions.
- Preserve readable paths between cardinal entrances and usable stations. Check routes against actual collision rather than appearance alone.
- Use a small, consistent set of shade roles per material. Avoid photographic texture, excessive micro-detail, uncontrolled gradients, and noisy dithering.
- Reserve the strongest contrast for the focal object and important interaction/state cues. Decorative lights SHOULD NOT compete with them.
- Cyan is shared by several departments: distinguish Science by white/blue instruments, Robotics by docking machinery, Life Support by pipes/tanks, Data by dark racks, and BRINE by a pearl-white aquatic centrepiece.
- Red is shared by Command and Security: distinguish finished control architecture from heavy armour and confinement.
- Animate lamps, bubbles, and anomaly effects sparingly. Motion SHOULD reinforce function or condition without obscuring targets.
- Maintain pixel alignment and compatible sprite scale; use the existing project's scaling/filtering policy. Do not introduce mismatched asset resolution or subpixel shimmer.

## 10. Implementation contract for an AI coding agent

### Before implementing a room

1. Inspect the existing grid, room dimensions, sprites, palette, connection logic, lighting, and collision conventions.
2. Select one primary department and a specific room function.
3. Identify secondary equipment influences and independent conditions.
4. Define the focal object, walkable routes, cardinal entrances, and service zones.
5. Reuse station geometry and semantic material/palette roles before adding assets.

### Suggested data separation

The following is illustrative, engine-independent metadata. Adapt names to the repository; it is not an existing API or a requirement to create a new framework.

```yaml
roomType: xenobiology_lab
primaryDepartment: science
secondaryFunctions:
  - agriculture_bio
condition:
  wear: used
  damage: none
  emergency: false
  abandoned: false
  contamination:
    type: anomaly
    extent: localized
focalFeature: specimen_containment_tank
architecture: inherited_station_modules
paletteRoles:
  wallBase: science_white
  departmentAccent: science_blue
  equipmentAccent: bio_green
  localEffect: anomaly_violet
connections: inherited_cardinal_sockets
```

Keep architectural inheritance, prop selection, and condition overlays separately configurable where feasible. Prefer existing project mechanisms over unnecessary new abstraction. Store exact palette values in the project's shared palette rather than duplicating ad hoc colours per room.

### Do / don't summary

| Do | Don't |
|---|---|
| Derive rooms from a shared station kit | Invent unrelated architecture for every room |
| Let the primary department own architectural finishes | Average every hybrid's colours across all surfaces |
| Use secondary colours on functional equipment groups | Add extra colours without a function or story source |
| Preserve department remnants under wear and damage | Replace all damaged rooms with generic brown wreckage |
| Separate appearance from gameplay state and keep them consistent | Suggest a usable door or hazard that does not exist |
| Keep clean, warm, industrial, and uncanny spaces in contrast | Make every room equally dirty, dark, or sinister |
| Reserve BRINE's composition and material combination | Turn every AI/server room into another BRINE Core |
| Use restrained, localized anomaly progression | Treat purple as ordinary paint everywhere |

### Worked room briefs

**Operational Hydroponics:** Station ribs frame white composite walls with green panels. Plant trays form readable rows around a clear access lane. Bright white grow lamps illuminate foliage; transparent tubing connects trays to a water system. Green appears in trim and living material, with no anomaly effects by default.

**Damaged Drone Control:** Command's red finished-metal architecture remains dominant. Cyan drone consoles face a shared control display. One damaged console has localized exposed wiring and a matching inactive state. Emergency lighting supplements the surviving normal lights; the doors and central path remain readable.

**Derelict Ore Refinery:** Engineering orange and charcoal survive beneath rust and missing panels. Heavy processing machinery anchors the composition. Logistics yellow marks cargo transfer zones. Abandoned bins and debris collect at plausible work areas; any blocked route matches collision. Remaining backup lights use emergency amber.

**BRINE Core:** Shared station dimensions contain a perfectly symmetrical chamber. Pearl-white ceramic and glass surround the central transparent water chamber, with aquamarine illumination and tiny bubbles. Dark flooring frames the focal object; service cables disappear beneath it. Keep peripheral consoles and exposed machinery minimal.

## 11. Acceptance checklist

Before considering a room or room-system change complete, verify:

- [ ] The room reads as part of the same station as existing rooms.
- [ ] Its primary department is recognizable at gameplay scale.
- [ ] Material, equipment silhouette, and layout support identity beyond colour alone.
- [ ] Hybrid influences are localized and the primary architecture remains coherent.
- [ ] Condition effects tell a plausible history and preserve host identity where intended.
- [ ] Cardinal connections align with the project grid and supported door dimensions.
- [ ] Every unused socket is visually sealed; valid connections have one shared
  assembly, with no duplicate frames, infill over a passage, or uncovered void.
- [ ] Doors, windows, hazards, and damaged equipment visually agree with gameplay state.
- [ ] Paths and interactive objects remain readable under normal and applicable emergency lighting.
- [ ] Floor texture, clutter, glow, and animation do not overwhelm the focal hierarchy.
- [ ] Department transitions occur at believable construction boundaries.
- [ ] BRINE and advanced anomaly treatments retain their intended rarity and distinction.

Review representative rooms at actual gameplay size, including a clean room, a hybrid, a damaged or emergency room, and a department boundary when those are affected. Use the project's existing validation workflow; this document does not prescribe an engine, renderer, or test framework.

## 12. BrineSpace production decisions and migration

### Shared construction, distinct departments

Shared construction does not mean identical finishes. Preserve the working grid,
doorway dimensions, collision registration and depth ordering while applying
department-specific cladding, floors, equipment materials and task lighting.
The earlier ivory-machinery/dark-slate treatment is not a universal style master.
Mostly clean is the default condition, not a mandate that every department look
sterile. Engineering can be maintained and heavy; quarters clean and personal.
Do not introduce damage, grime or a global tint merely to differentiate rooms.

Current art requires a department-alignment pass before further batch production:

| Room | Primary department | Preserve | Adjust toward this bible |
|---|---|---|---|
| Reactor | Engineering | Central machine, perimeter route, local amber activity | Burnt-orange sections, charcoal/raw steel, deliberate service connections |
| Life Support | Life Support | Fans, vessels, readable circulation | Grey industrial finishes, insulated piping, cyan/green system accents |
| Hydroponics | Agriculture / Bio | Planted beds and growing-light function | Green cladding accents, moisture-resistant surfaces, connected irrigation |
| Mycelium Nursery | Agriculture / Bio | Fungal trays, reservoir and service bench | Bio architectural identity; scientific instruments remain secondary equipment |
| BRINE Core | BRINE / Core | Unique central presence | Reserve pearl-white aquatic serenity and concealed services for BRINE |

These are migration briefs, not a claim the existing assets already satisfy them.
Gameplay category names need not be renamed to establish an art department.

### Rotation: layout moves, big props face south

Locked geometry: floor tiles are 48 × 48 world units; doorway clear openings
are 72 world units (1.5 tiles), centered on their canonical wall sockets.
The shared layered-room geometry implements these dimensions; legacy painted
room images still require migration rather than being assumed compliant.

After rotating prop centers, translate each complete visible assembly inward as
needed to remain inside the inner wall edges, with a four-world-unit safety margin.
Include tall tops, attached pipes and floor grates, not just ground footprints.
Move artwork, effects and collision together; do not crop or shrink overflowing
props. Preserve south-facing artwork and recheck routes and depth sorting in all
four layouts. If an assembly cannot fit, revise the layout rather than hide it.

Rotate canonical connection topology and large prop ground centers with the room.
Keep large machinery front faces toward screen south and vertical height screen-up.
Do not quarter-turn the completed room bitmap. Keep each fixed-facing prop's
ground footprint orientation and dimensions aligned with its artwork; do not
rotate the collision rectangle underneath stationary-facing art. Recalculate
ground-contact depth sorting at the new position.

Prop-attached lamps, bubbles, controls and fittings translate with their host.
Floor service routes and inter-machine connections must be rerouted between the
new endpoints, not carried along as disconnected painted hoses. Floor conduits
may be flush/recessed; raised services must respect collision and circulation.
Perimeter routes around central machinery require their own checks, including
the rendered character's foot offset. All four layouts still require acceptance.

The south-facing rule is a deliberate readability convention, not physical room
yaw. Directional machinery views are an explicit exception, not an outstanding
requirement for every room. Operator/workstation relationships must remain
plausible within that convention; do not silently abandon it for one room.

### Unused-socket infill across consumers

Infill is reusable station architecture, not an independently generated patch
for each room. Preserve the current socket center and aperture dimensions.
Neutral structural backing stays common; the room-facing panel inherits its
primary department. A department boundary changes finishes at a real seam.

Normal station and isolated room previews should look intact when unconnected.
Blueprint cards should use sealed sockets too; communicate potential connections
with consistent non-emissive socket markings or UI port icons, not missing walls.
Placement previews may show only prospective valid openings, using the same
connection calculation as placement. Debug cutaway fixtures may expose all ports
when clearly labeled as technical views, not presented as finished room art.
When a connection is removed or becomes incompatible after an allowed rotation,
restore its infill. This rule does not authorize otherwise unsupported rotation,
door locking, pressure simulation or destruction mechanics.

Current-state note: the layered station adapter already closes unconnected edges
with full wall spans. It has no separately styled removable-infill asset yet.
The card baker now seals every socket and includes two north fixtures; active
cards are Nursery v6 and Life Support/Hydroponics/Reactor v4. Standalone technical
scenes may still expose labeled ports. Shared station connections now render one
pair of retracting leaves, opened by the existing crew crossing animation.
The department door renderer now supplies leaves, threshold and frame using
registered surfaces and separate emission. Bio, Life Support, Engineering and
generic grey finishes share geometry. Same-department connections inherit their
finish; mixed/unknown pairs use generic. See DEPARTMENT_DOOR_ANIMATION.md for
current integration, side cutaway decisions and native verification. The original
dooranimated.png is preserved as a fallback.
See ORIGINAL_DOOR_ANIMATION_INTEGRATION.md for aperture mapping, depth ordering
and the edge-on side-view adaptation; the source artwork is preserved.
Legacy bitmap rooms also need auditing; this policy is not retroactive proof that
their painted door gaps have been repaired.

### Animation and lighting production contract

Door redesign direction (September 5): normal access/task lenses default to
neutral white, independently of department paint. Do not bake universal blue
glow into new door artwork. A room-specific light override may be authored later;
department colour should primarily live on trim and panels. The current layered
atlas material now uses white lenses; legacy bitmap doors are not yet migrated.
The original comparison is recorded in DOOR_REDESIGN_STUDY.json. Its surfaces now
drive the registered department door animation; the concept itself is not used
as a complete sprite. Generic grey is a material variant with the same white lamps.

For the replacement, author a fixed frame, left/right sliding leaves, floor-level
metal threshold and separate lenses. Retain the 72-unit clear aperture and one
assembly per connection. Build the side-facing projection explicitly, retaining
screen-up height, rather than turning the completed front bitmap. Preserve existing
access timing until replacement-frame traversal tests pass. Verify closed, moving,
fully clear, closing, paused and unpowered appearances before switching consumers.

Preserve a static, non-emissive base for each machine. Register moving parts,
screen content, emissive lenses and local effects separately against its ground
pivot. Use short authored loops for silhouette-changing mechanisms; procedural
motion is suitable for fans, bubbles, indicators and screen traces. Do not
regenerate an entire room per frame. Validate the full motion envelope against
walls, other machinery and protected doorway approaches. Keep operator/service
standing areas in layout briefs; current fixtures do not yet certify those areas.

Wall sconces are separate architectural fixtures with fixed wall attachment
points, a non-emissive housing, an emissive lens and an independent light pool.
Owner refinement: two sconces on screen-north in every room, at world-local
(-110,-188) and (110,-188). These are halfway between the 72-unit doorway aperture
edges and inner corners. Keep these anchors on north in every layout rotation,
including rooms without a north connection. The shared layered station renderer
and refreshed cards implement this pair; legacy bitmap rooms remain migration work.
They use camera-consistent wall-facing variants, not the south-facing machinery
rule. Keep them away from doorway trim and infill seams. Fixtures need not become
player-placeable items to be independently rendered and controlled.

Separate electrical power, machinery operation and emergency lighting. A powered
machine lacking inputs may stop operating without blacking out the room. Power
loss removes normal emission/task lighting, stops powered machinery effects and
leaves a readable low ambient level; emergency fixtures require an explicitly
defined backup-power policy. Do not invent backup-power gameplay from the art.
Crew movement remains independent; pause freezes animated transitions and loops.

Start with bounded per-room ambient shading and restrained local light overlays.
Do not bake powered glow into the sole source image, darken only the floor, or
allow light pools through solid walls. Cross-door light spill, dynamic occlusion
and shadows are later renderer work requiring native performance/visual tests.
Keep status UI readable independently of darkness. Avoid rapid flashing; include
reduced-motion/flash controls before adding warning strobes. At distant station
zoom, simplify local effects rather than letting overlapping glows obscure rooms.

Status: the isolated Nursery lighting pilot now demonstrates separate power and
operation controls, a procedural sconce/lens/floor pool, a registered fan, and
pause-aware power fading in all four layouts. See NURSERY_LIGHTING_PILOT.md.
The four layered room types now use paired north fixtures in the station, with
bounded floor light pools and cell-clipped post-assembly darkness. Failure reasons
distinguish NEEDS POWER/SUSPENDED from other idle conditions without changing
resource allocation. Lighting fades over 0.65 seconds and freezes when paused.
This is a visual interpretation of existing cycle results, not a continuous
electrical network simulation. Final fixture art, dynamic shadows and general
motion-envelope metadata remain separate work.

### Brief and acceptance additions

Record primary department, secondary equipment influences, independent condition,
focal feature, material/palette roles, normal lighting, circulation, socket mask,
service routing and functioning-effect anchors before each generation. Semantic
roles come from this bible; exact values and dimensions come from project sources.
Reference roles must distinguish shared geometry from departmental style.

Validate unconnected, connected, incompatible-neighbor, and removed-neighbor
edges in all four layouts. Include a department boundary, placement preview,
card and normal station; test closed/locked states only where implemented.
Review in colour and greyscale at actual gameplay/card size and mature-station
zoom. Keep generation, geometry, integration, technical verification and owner
art approval separate. Previous green tests do not establish bible compliance.
