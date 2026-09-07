# Rare dead-end gameplay rooms

Scope: Pressure Control Chamber, Deepwater Listening Post and Emergency Isolation
Vault. All are new rare one-cell rooms with one rotating doorway and U-shaped
interiors. This document is an implementation contract, not a shipped-feature claim.

## Pressure Control Chamber

Select a branch through a real connecting doorway. Preview every affected room and
crew member before committing. A valid branch has no alternate route around the
selected bulkhead and excludes BRINE Core. Flood/drain transitions cost stored
Power, advance only while the controller operates, pause with the game, and survive
Save/Continue. Ordinary flooded equipment becomes unavailable to production and
synergies. Explicitly compatible marine cultivation receives a useful benefit;
compatibility must be defined by room data, never inferred from blue artwork.
Unsuited crew cannot enter a flooded branch. Occupants must evacuate or equip
working diving gear before deliberate flooding begins. Emergency rescue and
draining must remain possible if the controller loses power or is removed.

Scene: grey steel/orange pressure tanks at the rear, valve manifolds along both
sides, front-side pump controls. Clear central approach and dry control position.

## Deepwater Listening Post

Offer a persistent choice of mineral, wreck and distress signals. Only one active
investigation per post, with a visible duration and Power cost; switching preserves
or explicitly discards paid progress. Resolution reveals a real reachable world
target, not an abstract reward disconnected from exploration. Exhausted targets do
not regenerate when a post is rebuilt. Wrecks respect physical clearance rules;
distress rescue respects named crew uniqueness and housing capacity. Broadcasting
must have a disclosed, implemented consequence before presenting it as risky.

Scene: rear acoustic display, hydrophone/recording racks on the left and analysis
consoles on the right. Restrained cyan instruments, grey-blue cladding, cable runs.

## Emergency Isolation Vault

Use the same branch preview and bridge validation. Arm a bulkhead against a local
breach or contamination event. Triggering stops propagation across that boundary,
disconnects production and synergies, and traps rather than teleports occupants.
Reserve power supports the protective latch; manual reopening requires the hazard
to be cleared or an explicit risky override. Rescue has a reachable interaction,
crew progress and persistence. Global resource shortages are not silently treated
as local breaches. Introduce local incident state and clear diagnostics first.

Scene: heavy bulkhead controls at the rear, reserve batteries and emergency racks
down the sides. Dark steel, restrained safety amber and a central branch diagram.

## Completion gates

- Rare acquisition works in normal play; a rarity label alone is insufficient
  because current deck building uses one copy for both rare and uncommon rooms.
- Actual single-door geometry, reciprocal connection and crew access at four rotations.
- Preview affected branch, costs, occupants and failure conditions before committing.
- Economy, discovery, crew routes and rendering agree on flooded/isolated state.
- Paid normal-play actions, pause, power loss, controller removal and save/load tested.
- Real signal targets, exhaustion, investigation choice and rescue verified.
- U-shaped interiors, card art and station rendering verified at gameplay scale.
- Existing airlock, drone, discovery and save regressions remain intact.

## Current implementation evidence

`scripts/station_branch.gd` provides non-mutating bridge-based branch planning.
It rejects disconnected doors, alternate paths and branches containing BRINE Core.
`tests/test_station_branch.gd` checks those conditions. It is a foundation module;
the room definitions, interactions, flooding, incidents, rescue and art are pending.


## First playable prototype — implementation status

All three room definitions and single-door U-shaped interiors are integrated,
reusing painted equipment from Life Support, Acoustic Comms and Battery Array.
Cards are in rooms/underwater/rare-dead-ends. One randomly selected specialist
appears per deck among the three unlocked definitions; each costs 1 Power/cycle.

Listening Post: 3 stored Power buys a three-functioning-cycle investigation of
one finite undiscovered mining or salvage site. Targets are reserved across posts;
resolution reveals the existing site and never resets its resource stock.
Pressure Control: preview a physical branch, require it to be empty of crew, pay
4 Power and run two functioning cycles. The boundary closes during the operation.
Ordinary flooded rooms stop production and links. Explicitly compatible Hydroponics
gets +2 Biomass/cycle while flooded. Emergency equalization releases immediately.
Isolation Vault: preview and arm an empty branch for 4 Power. The reserve latch
can trigger without operating power when a local incident occurs inside. Affected
rooms disconnect and stop production; occupants that entered after arming remain.
Local containment faults currently originate in a functioning containment-risk
room every eighth cycle. Unisolated faults cost 1 Integrity per affected room and
spread at most one neighboring cell per source per cycle. Individual repair costs
2 Metal. These are provisional gameplay/balance values, not owner-approved tuning.

Native evidence: output/rare-rooms-v7.log passes three room rotations, paid flood
transition and economy exclusion, branch closure/release, finite investigation,
armed incident containment, paid repair and checkpoint write/read. It does not
prove full Continue interaction or a crew rescue tour. All three cards were viewed.

Remaining original scope: distress and physical wreck investigation choices,
broadcast consequences, suited access to flooded space, progressive drain/rescue
interactions, complete pause/power-loss/active-save-load tests, controller-removal
edge cases and a paid normal-run balance/playtest. The original completion gates
above remain required; this prototype is not the fully completed three-room system.
