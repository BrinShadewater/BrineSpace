# BrineSpace checkpoint — September 6, 2026

**Later checkpoint:** [September 7 integrated build/playtest](INTEGRATED_BUILD_PLAYTEST_2026-09-07.md)
supersedes the combined-package and seeded-traffic acceptance status below.
This document remains the original dated workstream snapshot.

Prepared at the owner's request to stop expanding work and conserve credits.
This is the starting document for the next session. It consolidates current
source, selected assets and project evidence; older reports remain historical.

## Session wrap-up

All other BrineSpace tasks were idle or not loaded when inspected. No additional
agents or generation jobs were started. Task history is preserved, not archived.
No recurring automation files were found in the local automation directory.
This consolidation makes documentation/skill edits only; it does not run another
gameplay expansion, export, commit, push or publication.

| Task | State at checkpoint | Where its work stands |
|---|---|---|
| Expand Brine Space gameplay | Idle | Core station loop, operations, room rendering, navigation/Continue and performance work implemented; large-station and furnishing follow-ups remain. |
| Create next 10 production rooms | Idle; latest recorded turn interrupted | Original ten integrated; work expanded into the 40-room furnishing rollout, mat repairs and package/traffic testing. Preserve unfinished acceptance work. |
| Reimagine major bill character | Idle | Three architects have dry, water and helmet pipelines; current motion/transition artwork remains provisional. |
| Animate cover image loop | Idle | Layered animated title cover, shared menus, settings, checkpoint/recovery and station decision UI implemented. |
| Add station background assets | Idle | Habitat library and three composed exterior sites integrated; environment-specific Windows export evidence exists. |
| Add drone NPC systems | Not loaded | Three drone types, finite harvesting, batteries and cargo implemented; broader economy and congestion tuning remain. |
| Add derelict cryopod room | This consolidation | Cryo/architect unlocks, BRINE tank, airlock, 85 refreshed decoration assets and appropriate placement across 40 rooms implemented. |
| Create BrineSpace aesthetic bible | Not loaded | Bible maintained in the shared checkout; current underwater/low-wall rules supersede old orbital studies. |

Task state was checked through the app. Some recent task reads returned empty
turn bodies; detailed claims below are grounded in current repository records,
source and saved verification, not inferred from a task title.

## What the game currently is

BrineSpace is a Godot 4.6 underwater station-restoration roguelite prototype.
The current entry point is `scenes/title_screen.tscn`; gameplay is `scenes/main.tscn`.
The project name is BrineSpace, version `prototype-2026.09.06-menu`.
The goal is satisfying placement and interdependent systems, not click speed.

The current owner-directed loop is open-ended. Starting doctrines, timed
reconstruction directives and legacy orbital POIs are retired. Paid construction,
resource failures, hidden recipe discovery and three functioning stabilization
cycles remain. Conclude Expedition banks the loop. Do not restore old deadlines
because an early prototype document still describes them.

## Implemented in the source project

| Area | Current capability | Evidence and limits |
|---|---|---|
| Rooms | 40 database identities: 37 furnished views and three narrow corridor shapes; registered furniture, low hulls, real door masks, four rotations and state effects. | [Furnishing status](ROOM_FURNISHING_STATUS.md), [rollout ledger](ORGANIC_ROOM_ROLLOUT.json). Integration is broader than final visual acceptance. |
| Latest decoration pass | 85 source assets restyled; appropriate selections integrated across all 40 rooms. Rugs, work mats, drains, access covers, cables/pipes and corridor fittings replaced; cards/variants updated. | [Integration manifest and notes](../rooms/decoration-integration/README.md): 320 native state/rotation renders, 37 shared-edge captures, 28 station captures, 875 active host references checked. No new executable includes this whole pass yet. |
| Architect recovery | Bill, Veld and Branforth; selected starter wakes from a BRINE Core pod. Two fixed wards hold the other architects; ward format supports one or two occupants. Paid connected repair absorbs the room; powered thaw adds named crew once and permanently unlocks them. | [Architect cryo](../rooms/architect-cryo-v1/README.md). Pause, berth/supply checks and Continue supported. Starting supply perks are provisional, not distinct role gameplay yet. |
| BRINE room | Slimmer suspended character, layered glass/water, slow floating, occasional bubble, BRINE label near tank top, perimeter computers and startup pod access. | [Renewal record](../rooms/underwater/brine-core/renewal-v2/README.md). Preserve the accepted face/body and glass containment. |
| Airlock | Buildable locker/preparation room plus central pressure chamber. Inner/outer door interlock; flooding/equalization and draining; helmet Fit/Return for all three architects. | [Airlock record](../rooms/underwater/airlock-v1/README.md). Power interruption, pause and saved cycle state supported. Crew still remain in dry preparation space. |
| Crew | Dry movement/actions; four-direction swim/tread; ground/water death; helmet overlays; composed pickup/don/remove/deposit actions. Facing changes preserve locomotion phase. | [Current water revision inventory](../character/crew-underwater-v1/revisions/README.md), [locker work](../character/crew-underwater-v1/locker/README.md). Passing frames/manifests are not continuous visual acceptance. |
| Drones | Mining, Salvage and Construction bodies/bays/deployment/job effects; paid construction queue, cargo return and non-cryo clearance; finite deposits/scrap; extraction batteries recharge from stored Power. | [Fleet](DRONE_FLEET.md), [finite harvesting](FINITE_DRONE_HARVEST.md). Isolated package smoke exists for that revision; human pacing and larger fleets remain unproven. |
| Environment | Eleven reviewed habitats in the environment export, terrain/growth/debris library, physical wreck/rock blockers and three authored composed sites. | [Composed sites](ENVIRONMENT_COMPOSED_SITES.md): environment-export-v23 checks 93 PNGs, 22 renderer caches and 66 textures. Decorative scenery is not automatically a hazard or resource. |
| Menus and saves | Animated title, shared Settings/Codex/progression, architect selection, Save/Continue, recoverable progression backup, display recovery and workspace restoration. Continue shows a station schematic and reserve warnings. | [Menus](MENU_SETTINGS.md), [navigation/Continue](STATION_NAVIGATION_AND_CONTINUE.md), [priority implementation](NEXT_PRIORITY_IMPLEMENTATION.md). Hardware/input matrix is not complete. |
| Station usability | Search/locate rooms, actionable health priorities, construction queue, reserve and drone-charge feedback, blueprint costs/known links, learned-pattern watch and event history. | [Operations](STATION_OPERATIONS.md), [learning](LEARNING_UI.md), [decision UI](DECISION_UI.md). Forecasts describe current assumptions; they do not promise survival. |
| Performance | Visibility culling, cached prop geometry, retained static room contents/floors/walls/doors/lights, staged navigation rebuild during Continue. | [Latest retention pass](RETAINED_LIGHTS_AND_STAGED_RESTORE.md). Local measured improvements exist, but 101-room Fit/cold transitions and initial art loading remain expensive. |

## Work in progress and unresolved acceptance

1. **One current integrated build.** Windows catalog40-v2, mat-package v2/v3,
   menu validation, finite-harvest PCK and environment v23 cover different
   snapshots/scopes. None proves the complete latest source project. The new
   decoration cards also invalidate older card-hash visual approvals. Refresh
   old per-pack card selections/review-board metadata before the next export.

2. **Crew traffic reliability.** The initial mat package exposed opposing crew
   waiting indefinitely. Automatic yielding, Continue rebinding and a planning
   margin were subsequently implemented. Package v2 completed its tour. V3
   initially timed out, then a same-PCK replay passed, but crew RNG histories
   differed. Later seeded native repeats produced matching Bill traces and a
   second seed passed. Source files changed concurrently during those runs.
   Next acceptance must use an immutable package, record all crew seeds, retain
   failures and examine peer trajectories. This is not still an untouched bug,
   and it is not established broad traffic reliability. See
   [the complete failure/fix chronology](MAT_REPAIR_PACKAGE_FOLLOWUP.md).

3. **Swimming and equipment visual continuity.** All twelve actor/direction
   swim pairs are inventoried; eleven use revisions and Veld north retains its
   pilot. Continuous loops, turns and swim-to-tread transitions remain under
   review. Locker actions now include pickup/deposit; an older parent README
   still says these are missing. Current joins show body/head/shoulder and helmet
   shape differences. Bill selects pickup v4/candidate 07, Veld v1/01, Branforth
   v2/02. Dry east helmet placement and sampled turning passed, not a continuous
   autonomous deployment sequence. Some older captures predate current sources.

4. **Complete airlock traversal.** Connect actual crew movement through the
   chamber to flood/pressure state, water locomotion and exterior navigation,
   including safe return, interruption and Save/Continue. Full suit changing
   remains absent. Working helmet actions and a door interlock do not complete
   this gameplay loop.

5. **Room composition acceptance.** The decoration rollout is complete as an
   integration pass, not as blanket owner approval of every room. Life Support's
   orange cart/service endpoints still need a coherent relationship; Battery
   grouping has been under refinement. Nursery, Hydroponics and several other
   revisions postdate older package/review records. Review Medical Office powered
   as well as unpowered. Preserve coherent rooms such as the accepted lounge
   composition instead of endlessly adding accessories. Reconcile findings to
   the latest card hashes, not older filenames.

6. **Economy, performance and release.** Longer paid expeditions, varied architect
   starts, larger drone fleets, congestion and human enjoyment need playtesting.
   A later controlled opening test found 242 seconds of charge starvation with
   one generator versus zero with two; older finite-site fixtures had different
   results/setup. Do not combine them into a universal balance claim. Large
   station profiling and runtime-only packaging remain open. Gamepad, OS scaling,
   multi-monitor behavior and broader hardware acceptance are not complete.

7. **Future design, not half-implemented promises.** Distinct architect placement
   incentives, reachable seeded site layouts and richer exterior/hazard gameplay
   need deliberate design. Do not add generic output bonuses, procedural terrain
   or unrelated room batches merely to make the prototype larger.

## Repository checkpoint and preservation

At inspection: branch `main`, HEAD `ab327b2b491d566fc5ec7d7d7dcedb1f3561c689`.
The index and HEAD each contain 656 paths: no empty/partial-index clone symptom.
There were 20 modified tracked files and 107,570 untracked files, including
generated assets, studies, captures and other working material. Counts will change
as this handoff is saved. They are not a count of finished game assets.

The work is saved locally but this is **not a committed or remote-backed-up
checkpoint**. Before further expansion, review what belongs in source control,
retain necessary provenance, confirm LFS coverage and make a deliberate project
checkpoint. Do not blindly stage the entire directory, delete historical sources,
or treat generated output as disposable without checking runtime references.

## What we learned

- Geometry owns walls, sockets, floor clearance and collision; generated art does
  not. Rotate room positions while keeping large south-facing props upright.
- Low underwater hulls are current art direction. Windows show the exterior
  ocean. Tall posters/ducts in a library do not justify taller room walls.
- Generated transparency, dimensions, proportions and atlas positions require
  inspection. Preserve raw sources, exact prompts and deliberate alpha-gap seeds.
- Draw mats and covered services below actors/furniture. Attach possessions to
  physical supports and equipment endpoints rather than scatter them.
- A card can conceal shared-wall ownership defects. Review connected rooms,
  power states, real crew routes and normal station scale.
- Static poses, current-controller movement, visual acceptance and packaged
  verification are separate evidence. Passing one does not confer the others.
- Tie evidence to source/card/PCK hashes and all relevant RNG seeds. Concurrent
  edits prevent frozen-source claims even when two observed traces match.
- Clear retained canvas commands before freeing meshes; invalidate retained room
  contents when a cell is replaced by a corridor. Preserve animation/lighting
  state in cache keys and keep rejected optimizations as evidence, not features.
- Accept a coherent room and stop. The next useful work is acceptance and play,
  not another undirected generation batch.

## Recommended next work, in order

1. Review and preserve the local source/LFS checkpoint; establish one selected
   runtime asset manifest and reconcile stale card/export/review records.
2. Build one frozen Windows debug package from that checkpoint. Verify title,
   New Loop for each unlocked architect, cryo rescue, all 40 room identities,
   environment/drone loads, pause, Save/Continue and equipment state.
3. Run seeded multi-crew traversal on that exact package: repeated identical
   seeds, then varied seeds. Investigate any stall before changing tolerances or
   timeouts. Record actual peer motion, not only Bill's itinerary.
4. Complete the airlock-to-water-to-airlock crew loop and repair the specific
   animation joins revealed by continuous in-game playback.
5. Conduct a short paid human expedition and a targeted powered visual review.
   Fix demonstrated readability, pacing and composition problems. Then profile
   large stations and trim release packaging based on measured costs.
6. Only after that stable slice, explore architect-specific choices and seeded
   replayability. Defer more asset volume unless the playtest identifies a need.

## Skill maintenance in this wrap-up

Updated the maintained room and character skills and their installed mirrors.
New handoff references distinguish generated/integrated/visually reviewed/exported
work, bind evidence to selected sources, preserve failed runs, and prevent stale
status from restarting completed work. Generation lessons remain in the project
room workflow; animation/locker lessons remain in the character workflow. Generic
bundled tools were not rewritten to contain project-specific policy. Validation
is structural and synchronization checking, not a new behavioral skill evaluation.

Resume instruction: read this checkpoint and the linked current manifests first;
start with preservation, selection reconciliation and one immutable acceptance
build. Do not restart art generation or treat every historical TODO as current.
