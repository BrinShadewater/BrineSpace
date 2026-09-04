# Synergy Discovery Progression Design

## Purpose

BrineSpace should feel like an ongoing investigation into a damaged station rather than a game where the player begins with a solved recipe list. Room relationships are hidden until the player creates and powers them. Each discovery should visibly transform the station, teach the player something permanent, and place a new blueprint into their hands quickly enough to invite another experiment during the same run.

The core progression loop is:

1. Experiment with room placement and door connections.
2. Power a previously unknown compatible room pair.
3. Discover the synergy through a visible activation event.
4. Keep at least one link of that synergy functioning for three consecutive cycles.
5. Stabilize the pattern, permanently decrypt its reward blueprint, and insert one prototype copy into the current run.
6. Use the new room to search for further hidden relationships.

## Goals

- Make discovery a primary player verb alongside building and surviving.
- Keep undiscovered recipes genuinely secret: no room-pair names, recipe names, or explicit partner hints.
- Give every functioning synergy a persistent graphical identity on both rooms and their connecting doorway.
- Deliver a useful blueprint during the same run in which its prerequisite is stabilized.
- Persist discovered knowledge and stabilized unlocks between runs.
- Support a branching authored discovery graph without progression dead ends.
- Preserve the existing doctrine deck, directive, Resonance, and run-summary systems.

## Non-goals

- A research shop or currency-driven blueprint store.
- Random blueprint rewards unrelated to the discovered rooms.
- Requiring victory before a stabilized blueprint becomes permanent.
- Revealing silhouettes, partner names, or adjacency recipes for undiscovered synergies.
- Shipping final particle art in the first implementation. Procedural effects are sufficient for the vertical slice.

## Player-facing Rules

### Hidden knowledge

Before discovery, the game may state only that experimentation can reveal unknown patterns. Cards, inspectors, and the archive must not identify a missing partner or hidden synergy name. An undiscovered recipe does not appear as a named entry.

The first powered cycle with a valid door-connected pair discovers the recipe. The discovery event reveals:

- synergy name;
- participating room types;
- cycle effect;
- stabilization requirement;
- blueprint that can be decrypted.

Discovery is permanent even if the link later stops functioning or the run fails.

### Functioning links

A synergy link functions only when:

- both required rooms occupy orthogonally adjacent cells;
- their touching sides have matching doors;
- both endpoint rooms are powered for the current cycle.

Topology alone creates a candidate link, but it does not grant a cycle bonus, advance stabilization, satisfy a functioning-link directive, or display the persistent active effect. A discovered but unpowered candidate may use a faint dormant treatment so the player understands why a known recipe is inactive.

### Stabilization

Stabilization is tracked per synergy recipe, not per individual link. At least one functioning link of that recipe advances the counter by one each cycle. Multiple copies do not accelerate it. A cycle with no functioning link resets an unfinished counter to zero.

The discovery cycle counts as stabilization cycle one. At three consecutive cycles, the synergy becomes permanently stabilized. Already stabilized recipes continue granting normal gameplay bonuses but do not repeat their blueprint reward.

### Blueprint reward

When a recipe stabilizes:

1. Its authored blueprint reward is permanently unlocked in meta progression.
2. One prototype copy is placed on top of the current draw pile.
3. If the hand has an empty slot, normal refill rules may draw it immediately.
4. The blueprint joins future decks only when it is allowed by the selected doctrines or the essential blueprint list.

If the blueprint was already unlocked by an older save, the synergy is still marked stabilized, but no duplicate prototype is injected. Terminal recipes without another room reward grant Research instead and are explicitly marked as terminal content.

## Feedback and Presentation

### First discovery

The first activation uses the strongest discovery feedback:

- a brief pulse from each room toward the shared doorway;
- a doorway flash in the synergy's color;
- a centered `PATTERN DISCOVERED` message with the newly revealed name;
- a notification explaining the effect and `STABILIZING 1/3`;
- immediate archive insertion.

### Persistent functioning effect

While functioning, every concrete link uses its synergy's authored FX profile:

- endpoint edge glow on both rooms;
- animated particles or signal motes traveling through the shared door;
- a restrained pulsing link line;
- consistent color and motion shared by all copies of the recipe.

The effect is visible during normal play but remains below placement previews, warnings, and cascade banners. It stops when either room is unpowered. A known connected link then falls back to a dim, non-animated dormant line.

Initial FX profiles are procedural:

- `flow`: cyan or green fluid motes for atmosphere and biosphere systems;
- `power`: amber electrical pulses for engineering systems;
- `signal`: blue scanning packets for research and command systems;
- `care`: teal heartbeat pulses for crew and medical systems;
- `containment`: violet segmented fields for anomaly systems;
- `logistics`: warm white directional ticks for material movement.

### Stabilization and unlock

Active known links show recipe stabilization progress in the room inspector. Completion produces a `BLUEPRINT DECRYPTED` banner, highlights the rewarded card entering the draw pile, and adds an explicit archive state of `STABILIZED`.

## Progression Content Graph

New clean saves begin with a smaller foundation set:

- Solar Array
- Reactor
- Mining Drone Bay
- Hydroponics Bay
- Life Support
- Crew Hab
- Research Lab
- Storage Bay
- Med Bay
- Quarantine Cell
- Corridor
- Corner

The first authored graph uses these discovery rewards:

| Discovery recipe | Blueprint reward | Stage |
| --- | --- | --- |
| Hydroponics Bay + Life Support — Closed Air Loop | Biodome | Foundation |
| Hydroponics Bay + Crew Hab — Green Commons | Crew Lounge | Foundation |
| Crew Hab + Med Bay — Field Clinic | Med Office | Foundation |
| Med Bay + Life Support — Clinical Airlock | Cryo Chamber | Foundation |
| Storage Bay + Corridor — Logistics Spine | Maintenance Bay | Foundation |
| Mining Drone Bay + Storage Bay — Ore Buffer | Ore Refinery | Foundation |
| Solar Array + Reactor — Load Balancing | Battery Array | Foundation |
| BRINE Core + Research Lab — Core Diagnostics | Data Archive | Foundation |
| Research Lab + Quarantine Cell — Sterile Observation | Xeno Lab | Foundation |
| Biodome + Life Support — Biodome Atmosphere | Bio Lab | Developed |
| Crew Hab + Crew Lounge — Crew Commons | Med Center | Developed |
| Cryo Chamber + Life Support or a powered medical room — Safe Wake Protocol | Clone Lab | Developed |
| Mining Drone Bay + Ore Refinery — Industrial Chain | Salvage Drone Bay | Developed |
| Reactor + Battery Array — Stable Power Flow | Shield Generator | Developed |
| Research Lab + Data Archive — Research Pipeline | Radio Lab | Developed |
| Xeno Lab + Quarantine Cell — Containment Sector | Anomaly Lab | Developed |
| Radio Lab + Research Lab — Signal Triangulation | Command Center | Advanced |
| BRINE Core + Command Center — Core Relay | Holographic Core | Advanced |

Existing recipes such as Drone Foundry, Shielded Reactor, Living Circuit, Signal Command, and Medical Network become terminal mastery discoveries in the initial content set. Two additional terminal recipes, Clone Lab + Med Center — Genomic Triage and Anomaly Lab + Holographic Core — Impossible Model, ensure those advanced reward rooms also lead to a final discovery. Terminal recipes grant Research on first stabilization until later room or variant rewards are authored.

Every non-terminal reward room must participate in at least one recipe at the same or a later stage. A validation test fails if a reward references an unknown room, is unreachable from the foundation set, or creates an unmarked dead end.

## Architecture

### Synergy definitions

`scripts/synergy_manager.gd` remains the source of recipe data. Each definition gains:

- `unlock_room_id`, optional for terminal recipes;
- `stabilize_cycles`, default `3`;
- `fx_profile`;
- `fx_color`;
- `terminal_reward`, optional Research amount;
- existing bonus, effect, message, and room requirements.

It continues to detect candidate door-connected links. It must not write saves, inject cards, or own cycle timing.

### Runtime discovery state

`scripts/main.gd` coordinates the cycle:

1. Room economy assigns powered and unpowered room cells.
2. Candidate synergy links are evaluated from topology.
3. Candidate links with two powered endpoints become functioning links.
4. Only functioning links contribute cycle bonuses and directive metrics.
5. Newly functioning unknown recipes are discovered through `MetaState`.
6. Per-recipe run stabilization counters advance or reset.
7. Newly stabilized recipes persist and award their prototype.

Runtime state is separated into:

- `connected_synergy_links`: all topologically valid links;
- `active_synergy_links`: currently functioning powered links;
- `synergy_stabilization_progress`: run-local counters by recipe ID.

Placement cascades may still score newly created candidate links immediately, but hidden recipes use generic `UNRESOLVED PATTERN` wording until their first functioning cycle. They must not leak names or partner details.

### Persistent meta state

`scripts/meta_state.gd` adds `stabilized_synergy_ids`. The existing `discovered_synergy_ids` continues to mean learned recipes. Blueprint unlocks continue using `unlocked_room_ids`.

Save loading remains backward compatible:

- missing stabilization data defaults to empty;
- rooms present in older saves remain unlocked;
- shrinking the foundation list does not revoke previously unlocked rooms;
- discovered recipes are not assumed stabilized.

### Deck integration

`scripts/run_manager.gd` continues to build doctrine decks from unlocked rooms. A prototype reward bypasses doctrine filtering only for its one injected current-run copy. It is appended to the draw pile because the current draw implementation pops from the back.

The doctrine chooser preview reflects permanent unlocks only. It does not reveal locked room names, hidden recipe counts, or potential partners.

### Rendering

`scripts/grid_canvas.gd` renders discovered links from the two runtime collections:

- functioning: colored animated profile plus endpoint accents;
- known but dormant: faint static line;
- unknown candidate: no persistent link rendering before discovery.

The renderer uses the existing visual time source and procedural drawing primitives for the first pass. No new external art dependency is required.

## UI Changes

- Archive entries have `DISCOVERED` and `STABILIZED` states.
- Unknown recipes appear only as an aggregate count, never as individual silhouettes tied to rooms.
- The inspector shows active stabilization progress for revealed recipes touching the selected room.
- Card synergy hints mention only already discovered recipes. All rooms use the same generic experimental language while unknown recipes remain, so the presence or absence of a hint cannot reveal which room has a missing partner.
- The run summary lists recipes discovered, recipes stabilized, and blueprints decrypted during that run.
- A prototype card receives a temporary `NEW` marker until selected or until one cycle after it first enters the hand.

## Edge Cases

- If two unknown recipes first function in the same cycle, both are discovered and advance to `1/3`; their notifications queue rather than overwrite each other.
- If several links of one recipe function, stabilization advances once.
- If all links of a recipe lose power, unfinished progress resets on that cycle.
- Stabilization cannot reward the same recipe twice across runs.
- A prototype is not injected when its room is already permanently unlocked.
- If the draw pile is empty, the prototype becomes the next draw before discard reshuffling.
- Removing or replacing rooms is not currently supported, so topology invalidation is limited to future systems; power loss must still deactivate effects and bonuses immediately.
- A run ending on the same cycle as stabilization preserves the unlock before the summary is shown.

## Testing Strategy

Tests are written before production changes and cover:

- hidden candidate links do not reveal recipe data through card or cascade text;
- both powered endpoints are required for functioning status and cycle bonuses;
- discovery occurs on the first functioning cycle and persists;
- one functioning link advances stabilization once per cycle;
- duplicate links do not accelerate stabilization;
- losing all functioning copies resets unfinished progress;
- three consecutive cycles stabilize exactly once;
- stabilization unlocks the authored room and injects one prototype;
- already unlocked rewards do not inject duplicates;
- terminal recipes grant their configured Research reward;
- old save files load without stabilization fields;
- all authored unlock targets exist;
- all non-foundation blueprints are reachable from the foundation set;
- every non-terminal reward room participates in a later recipe;
- doctrine decks remain viable with the smaller foundation pool;
- archive, inspector, discovery, dormant, active, and unlock states render without overlap.

Representative visual captures include an unknown candidate before power, first discovery, `2/3` stabilization, a dormant known link, an active functioning link, and the blueprint-decrypted banner.

## Rollout

Implementation proceeds as one vertical slice while preserving save compatibility:

1. Add recipe metadata and graph validation tests.
2. Split connected links from powered functioning links and gate bonuses correctly.
3. Add discovery and stabilization state with persistence.
4. Add prototype deck injection and the smaller clean-save foundation pool.
5. Update archive, inspector, cards, summary, and notifications to avoid information leaks.
6. Add procedural persistent FX and visual captures.
7. Balance stabilization length and starting-room coverage through full doctrine-pair playtests.

The feature is complete when a clean save can discover, stabilize, and immediately use at least one blueprint chain; the recipe remains learned after failure; the blueprint remains permanently unlocked after stabilization; inactive links stop their effect and bonus; and the authored graph validation reports no unreachable or accidental terminal rooms.
