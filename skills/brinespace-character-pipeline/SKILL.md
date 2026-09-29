---
name: brinespace-character-pipeline
description: Create, animate, repair, package, or integrate BrineSpace crew characters such as Major Bill and Dr. Veld. Use for character identity, sprite motion, and character-specific NPC integration; room machinery animation belongs to the room pipeline.
---

# BrineSpace character pipeline

For companion rescue crates, occupant reveals and recovery handoffs, read
[companion rescue workflow](references/companion-rescue.md) and use both pipelines.

For existing Desktop selections, installation audits and acceptance closeout, read
[selected artwork audit](references/selected-art-audit.md). Start from current status
and the latest dated owner decisions before carrying forward older next steps.

For the September 26 room/animation closeout, read the active checkout's
`docs/ROOM_ART_SESSION_CLOSEOUT_2026-09-26.md` after CURRENT_STATUS.md.
It supersedes historical pending drone installation steps; immersion ideas remain deferred.

For drone NPC animation, launch/recovery effects or their closeout, read
[drone production lessons](references/drone-animation.md). Use both room and
character workflows when changing a drone and its dock interaction.


For coarse existing sprites, local detail/motion repair, or replacement of a full
active library, read [source density and replacement](references/source-density.md).

For nonhuman companions, swimming/flotation, or their animation closeout, read
[companion motion lessons](references/companion-motion.md).

For everyday crew actions, cargo transitions or their session closeout, read
[crew-life lessons](references/crew-life.md) for source extraction, furniture
contact, equipment fitting and checkpoint evidence.

For new matching portraits, profile revisions, accepted portrait masters and safe
native portrait verification, as well as procedural comms effects, read
[comms portrait guidance](references/comms-portraits.md).

For session consolidation or resuming interrupted animation work, read
[handoff guidance](references/handoff.md) to reconcile current source coverage,
transition defects and the limits of native or packaged evidence.

Deliver the requested character work with consistent identity, registered motion,
and evidence appropriate to its scope. Preserve accepted work and make revisions
inexpensive. This skill owns character decisions; existing sprite tools own
packaging, and the project visual bible owns shared art direction.

For current scope, read `docs/CURRENT_STATUS.md` first. For takeover or closeout,
use `docs/CLAUDE_HANDOFF_2026-09-24.md` and the maintained
`docs/ASSET_PIPELINE_AND_WORKFLOW.md`; dated reports retain their original scope.

## Locate the project and select the scope

Locate the active BrineSpace checkout through the workspace, not a fixed drive.
Read its AGENTS.md, `docs/DEVELOPMENT_NOTES.md`, and `NOTICE.md`. Project paths
below are relative to that checkout, even when this skill is installed elsewhere.
The repository's `skills/brinespace-character-pipeline/` is the maintained source;
prefer its newer references to an installed snapshot.

Infer the deliverable from the request and prior authorization:

- **Concept:** establish identity and same-scale appearance. Read
  [character-direction.md](references/character-direction.md).
- **Animation pack or repair:** establish required motion and engine exports.
  Read [animation-contract.md](references/animation-contract.md); read character
  direction when creating or changing identity.
- **Integrated NPC:** deliver the pack plus the requested behavior and runtime
  verification. Also read [godot-integration.md](references/godot-integration.md).

For swimming, death or wearable-equipment extensions, also read
[underwater-equipment.md](references/underwater-equipment.md). Track new coverage
separately from the accepted dry pack, including missing states and integration.

Read the applicable section of [acceptance.md](references/acceptance.md) before
review or handoff. A concept does not require NPC code; a walk repair does not
require extra actions. Continue already-authorized work without inventing new
approval gates. Ask only for information that materially blocks the requested result.

## Establish and exercise the contract

Inspect the current character sources, manifest, and consumers before specifying
dimensions or states. Record identity, department, canonical reference, camera,
frame registration, state/direction coverage, timing, and requested scope.

Use the available `sprite-animation-maker` skill for general sprite production
and its existing helpers when applicable. Use the available image generation
capability for new visual sources; preserve a user-selected authoring method.
Local scripts handle deterministic processing, not invented replacement artwork.
If a capability is missing, complete independent local work and report the missing
capability; a reference to another skill does not install it.

For new packs, prove a representative idle, walk, and role action before expanding
the matrix. For narrow repairs, work directly on the failed portion. Preserve raw
sources and exact prompts; save each generated result into the project immediately.
Record rejected candidates and intentionally omitted states separately.

Package accepted sources into frames, manifest, requested engine exports, and
review media. Rebuilds should use local sources without calling a generation
service. Review identity and motion at actual station scale as well as full size.

## Non-obvious constraints

- Bill/Veld's 92 × 92 canvas and foot pivot (46, 86) are a compatibility profile,
  not a universal character size. Inspect the consumer before changing them.
- Opposite views cannot be mirrored when equipment, markings, or lighting would
  change sides incorrectly. Record derived/reversed frames separately from new art.
- A fixed pivot does not mean forcing every pose to the same bounding-box height.
  Kneeling must lower the body while the ground contact remains registered.
- Veld's `repair` state means sample inspection. Preserve controller compatibility
  while recording character-specific action meanings.
- Pixel/manifest tests do not certify visual identity, smoothness, occlusion, or
  owner acceptance. Record technical checks and visual review separately.

Use `skills/brinespace-room-pipeline/SKILL.md` in the active checkout when the task
also changes room art, prop registration, or door layouts. Existing room geometry
is input to character integration; do not redesign rooms merely to pass a crew test.

Report the requested scope, completed states, generation/packaging/integration
status, checks actually run, and remaining limitations. When revising this skill,
use [evaluation cases](evals/cases.json) and the evaluation guidance in acceptance.

## September 28 engineering notes

- Crew navigation: corridor `library/tileset-` pieces never block crew; hallway furniture blocks walkers but not swimmers (`swim_blockers`).
- Crew animation packs still load eagerly (~2.3 GB at startup); load each crew member on first appearance once this pipeline's session is idle.
- Cleanup rule: unreferenced `review/` candidate folders may go; `generated/` and `sources/` stay because build tools and playtests read them.
