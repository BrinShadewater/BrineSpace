# BrineSpace Development Notes

**Session checkpoint:** [September 6 consolidated handoff](BRINESPACE_HANDOFF_2026-09-06.md)
records all workstreams, incomplete acceptance, learned rules and next priorities.
The source project is newer than the last combined validated package; preserve
and reconcile it before starting another asset or gameplay expansion.

## Prototype North Star

BrineSpace should feel like restoring a silent underwater station: build a little, watch the systems find their rhythm, notice a strange connection, and decide whether to risk one more room. The interesting pressure should come from the station's interlocking needs, not from click speed. The underwater bible supersedes the orbital setting; existing reboot/run systems remain prototype implementation, not settled underwater fiction.

> **BRINE // DIAGNOSTIC**
>
> *"I have mapped thirty-seven ways to run out of oxygen. I recommend none of them."* ⚠️

## Current Focus

Diving Airlock is a buildable starting blueprint with suit lockers, a fitting
shelf, compressor, bench and a separate central pressure chamber. Its inspector sends Bill, Veld
or Branforth to fit/return their diving helmet using existing authored animation.
One fitting station reserves through crew state; power interruption, pause and
Save/Continue are supported. The chamber closes its inner door, floods and
equalizes before opening outside; returning closes the outer hatch, drains and
restores station pressure before opening inside. One derived cycle state prevents
both doors opening together. Power loss/suspension hold the cycle; saved phases
preserve water, pressure and door movement. Crew remain in the dry preparation
area; chamber transit, exterior travel and full suit changing remain future
work. See [airlock integration](../rooms/underwater/airlock-v1/README.md).

Airlock art now separates pressure-hull windows and wall fittings from floor
equipment. Ocean glazing, protected controls, valve manifold, shielded lamps,
flush drains and steel chamber framing replace the generic wall treatment.
See [hull fitting production](../rooms/underwater/airlock-v4/README.md) for source
alpha/proportion findings, current consumers and native verification limits.

BRINE Core now uses a slimmer crew-style suspended figure behind layered water,
glass reflections and the chamber's front rim. Slow floating and an occasional
single bubble replace the busy bubble field. Perimeter computer workstations and
a server cabinet retain all four door approaches and startup-pod access. See
[BRINE chamber renewal](../rooms/underwater/brine-core/renewal-v2/README.md) for
source history, native motion/route evidence and verification limits.

The open-loop operations pass adds a construction queue, ranked Station Health
priorities and a learned-pattern stabilization watch. Opening drafts stage existing
power, extraction, food, oxygen and corridor cards; paid costs and discovery rules
remain intact. Off-screen room drawing is culled with a one-cell margin. See
[Station Operations](STATION_OPERATIONS.md) for tests and measured limits.

Starting doctrine selection, timed reconstruction directives and legacy orbital
POIs are retired for now at the owner's request. New Loop begins directly with
an unlocked-only neutral blueprint deck. Runs have no directive deadline or
scenario victory; Conclude Expedition banks the loop through the existing summary.
Paid construction, resource failures, discovery stabilization and physical wreck,
rock and cryo recovery remain active. Continue clears legacy scenario/event state
while retaining the station and draft. Historic mastery remains stored but grants
no starting bonus. Older doctrine/directive balance notes below are historical.

Finite surveyed mineral deposits and scrap piles now replace abstract harvest
grounds. Stock and partial extraction persist; depleted sites become buildable.
Drones prefer exterior routes and can use matching service ports when enclosed.
The four paid opening-station economy checks survived five simulated minutes
without charge-power waits. See [Finite drone harvesting](FINITE_DRONE_HARVEST.md)
for current mechanics, native evidence and the limits of this automated playtest.

The first drone fleet pass is integrated: Mining, Salvage and Construction drones
now have separate bodies/cradles, deployment states and job effects. Paid room
orders wait for construction, and matching drones perform non-cryo clearance.
Bay harvest and clearance output return as cargo; basalt yields 4 Metal.
Mining/Salvage batteries support 12 seconds of extraction, then return to charge
from stored station Power (1 Power per 6 seconds of charge). Cuts persist across
trips; global pause freezes work and charging. Core emergency construction prevents a
first-bay deadlock. Native rotation/animation checks, gameplay regressions and an
isolated package smoke pass. See [Drone Fleet](DRONE_FLEET.md) for evidence and
prototype limits; construction/cargo pacing still needs human playtesting.

Architect recovery now seeds two fixed wards containing the two architects other
than the selected starter, one per ward. Wards support one or two occupants.
A matching-door expansion and paid repair absorb the existing room into the station.
Powered thaw sequences add named crew once, respect available berths and supplies,
and retain progress through pause and Continue. Bill, Veld and Branforth have
identity-specific six-pose emergence clips and join their matching walking NPCs
and the Crew roster only upon completion. Bill is initially selectable; rescuing
the others permanently unlocks them for the title-screen architect selector.
A single BRINE Core pod wakes the selected architect at the start of each new loop.
Legacy checkpoints retain their old population behavior. New Loop, pause-menu restart
and summary reboot now open a shared Architect selection screen. Unrescued identities
remain unknown with a cryo recovery hint; recovered records show face, name, job and
starting supplies. Bill starts with +4 Food/+4 Oxygen, Veld +6 Data/+2 Biomass,
and Branforth +6 Metal/+1 Rare Mineral. These provisional perks apply only on a
fresh loop, never on rescue or Continue. Cancel leaves the saved selection untouched.
See [architect recovery](../rooms/architect-cryo-v1/README.md) and
[the original cryo recovery record](../rooms/derelict-cryo-v1/README.md).

The [sub-biome environment pack](../assets/environment/sub-biomes-v1/README.md)
adds sulfur vent sediment, sponge reef rubble, brine salt flats, kelp meadows,
cold coral gardens, manganese nodule fields and iron seeps, with two matching props per
habitat and soft ground transitions. These are fixed visual
regions beneath the station; hazards, resources and procedural site generation
remain separate design work.

The low-growth and service-wreckage packs add fine seagrass, encrusting algae,
mussel beds and four exterior debris identities in fixed authored groups.
They remain decorative beneath construction. Environment source ledgers now
verify hashes and explicit runtime selections for these packs and the seven
sub-biomes; see [the environment library](../assets/environment/index.html).

Major Bill now has collision-aware room wandering and a basic hunger, fatigue,
exploration, and equipment-check behavior loop. Connected doors remain his travel
routes; room interiors use registered prop footprints. This is a visual NPC
prototype, without resource costs or population effects. See
[Major Bill NPC](MAJOR_BILL_NPC.md) for behavior, limits, and verification.

Dr. Veld now accompanies Bill with independent needs and science-room preferences.
Her 72-frame pack includes four-direction walking/idling, scanner use and sample
inspection. Rooms render both crew members with prop depth, and connected doors
respond to either character. This remains a visual prototype without staffing,
resource or research rewards. See [Dr. Veld](../character/dr-veld-v1/README.md).

Crew polish adds local yielding/detours so Bill and Veld maintain foot clearance
while passing. Checkpoints now retain both NPCs' needs, routes, activities and
animation clocks; older checkpoints remain compatible. Head-on corridor and
save/Continue regression tests pass. See `tests/test_crew_polish.gd`.

Chief Engineer Branforth now joins Bill and Veld with Engineering room preferences,
independent needs, diagnostic readings and equipment-service animation. His 72-frame
pack uses the shared crew playback contract. Rendering, connected doors and saves
include all three crew, and avoidance checks both peers. Three-crew headless/native
and old-save regression checks pass. See
[Branforth's pack and evidence](../character/chief-engineer-branforth-v1/README.md).
This remains visual NPC behavior without resource costs or repair rewards.

Room art now follows [the visual aesthetic bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md).
Its department-specific finishes supersede the universal ivory/slate pilot look.
Sections 12–22 establish the underwater design and distinguish proposals from
implemented systems. Section 23 preserves south-facing machinery and flush infill for unused
door sockets, with separate migration and consumer-verification work. Do not
equate earlier technical passes with aesthetic-bible acceptance.

The previous bible is archived under `docs/archive/`. Narrow underwater corridors
now have a shared geometry pilot and station/card integration. Their downward door
collar now uses a low cutaway, with an initial registered-surface art kit. V7 native
review covers animated crossings at production character scale. Station follow-up
checks actual walker paths and complete draft thumbnails; visual owner review
remains separate. See UNDERWATER_CORRIDOR_PILOT.md.

The real station fixture also passes from a checkout-independent PCK, including
raw room images and imported card-icon dependencies. Release export remains
unverified: no preset/template is configured. See STATION_PACKAGE_SMOKE.md.

The Mycelium Nursery gameplay branch is now present in the working checkout:
one locked Bio blueprint and three additional discovery patterns use the existing
paid-build, functioning-cycle and stabilization rules. Its data/deck/discovery
tests and existing regression suites pass. The layered component now draws in
the station, placement preview and card/inspector consumers. Single-room native
acceptance and a checkout-independent room-package smoke test are complete.
See `NURSERY_GAMEPLAY_INTEGRATION.md` for the requirement/evidence audit and
accepted art tradeoffs. This does not complete the broader room expansion.

The full-run follow-up is now on local `main`, alongside the remote documentation and CI changes. A matched 30-run automated sweep improved from 12 to 21 completions after adding slow draft recovery, with at least one completed run per doctrine pair. See [Balance Report](BALANCE_REPORT.md) for the full comparison and the remaining discovery droughts; these are bot results, not human completion-rate targets.

Rerolls rebuild one charge every four cycles below a bank of three, and the draft button shows the wait. Directive reward overflow is preserved. A full-run screenshot also exposed the old 22% minimum zoom clipping mature stations; Fit Station now supports a wider overview range.

The September discovery/polish pass completes the 12-foundation → 30-blueprint graph with 25 patterns. Rooms teach their relationships through functioning effects; the journal records knowledge after discovery, never before. Progress and rewards persist independently of winning a run.

Implemented in this pass:

- Three consecutive functioning cycles stabilize a recipe once; duplicate links stack output but do not accelerate discovery.
- Closed Air Loop reclaims Water so its Biodome prototype is affordable; Biodome Atmosphere recycles Water for the next bio branch.
- Every doctrine pair gets food and oxygen foundations; selected doctrines retain stronger card weighting.
- Shared per-cycle input budgets, operation-aware forecasts, limited recovery berths, and an actual corruption-cleaning Containment Sector.
- Click-to-inspect room suspension, a pausing spoiler-safe journal, a two-row resource HUD, compact cards, fit-station control and scrollable inspector/summary.
- Optional open expeditions after victory, with a menu cash-out and one-time victory/mastery rewards.
- Updated/old saves retain existing discoveries and blueprints. Old orbital events no longer shortcut blueprint decryption.

Verification: three headless regression suites plus a real-scene deterministic paid-build playtest pass. The native renderer was inspected at 1280×720, 1600×900, 1920×1080 and 2560×1440, including all six effect profiles, successive motion frames, unknown/discovered/stabilizing/dormant states, journal, prototype and victory screens. The full discovery sequence was captured at both 1600×900 and 2560×1440. See `tests/playtest_polish.gd` for reproduction; generated images/logs are not committed.

Remaining priorities:

- Make room door layouts and character paths match the production layout guide.
- Keep placement previews, door connections, and synergy feedback immediately readable.
- Improve the inspector, cards, and objective panels without obscuring the station art.
- Tune each doctrine pair's finite deck so power, metal, corridors, corners, and dead ends create interesting choices.
- Tune Resonance thresholds and cascade pulses through short runs; the intended delight is finding one placement that closes several useful links.
- Play full three-directive runs and tune targets, deadlines, resource rewards, reroll supply, and the 20-second base cycle.
- Expand the directive pool beyond the current doctrine-pair stage with goals that reward specific spatial patterns and orbital preparation without forcing a single solution.
- Make doctrine mastery choices more expressive after the starting-resource rank bonuses have useful playtest data.
- Replace the test walker with eventual cryo and clone population systems.

## Known Prototype Limits

Room-sized basalt blockers now form four connected shelves (fifteen cells) on
new runs. Clear each cell from a cardinally adjacent room using the same rig as
wreck salvage, then build normally. Connected rock shares a continuous material;
removal exposes new cliff edges. Excavation takes 18 seconds, saves progress,
respects pause and yields no metal. See the
[rock blocker notes](../assets/environment/rock-blockers-v1/README.md) for
geometry, source provenance, native evidence and prototype limits.

New runs now include four standard-cell wrecks: engineering, medical, habitation,
and hydroponics. They block construction until a single exterior salvage rig
finishes an 18-second dismantling job, reached from a cardinally adjacent room.
Work can pause and survives Continue; recovered metal pays once, respects storage
capacity, and leaves the cell available for normal paid construction. Existing
checkpoints without wreck data remain unchanged. Placement, duration and salvage
yields are prototype values requiring human pacing feedback. See the
[wreck asset and gameplay notes](../assets/environment/wrecked-rooms-v1/README.md)
for source art, rendering limits and verification.

The requested title-menu save pass adds a single active-loop checkpoint and
Continue, separate from existing progression. See [Save Game](SAVE_GAME.md) for
menu behavior, recovery, format limits and verification. Progression remains
prototype-level in its existing unversioned JSON file.

- The save/meta loop is intentionally lightweight while room and progression behavior are still changing.
- Some room variants and door placements need continued visual/layout verification.
- Resonance, doctrine mastery, directives, and reroll rewards are first-pass values and need balance data from complete runs.
- Directives currently measure room count, active links, distinct active patterns, total Resonance, or balanced development of the selected doctrine pair; orbital and geometric pattern-shape goals are not implemented yet.
- Borderless mode and unusual aspect ratios still need broader hardware testing. Standard 16:9 layouts have native-render screenshot coverage.
- The two-step discovery playtest uses a controlled draft order. The full-run sweep uses seeded random decks, but its automated player does not strategically suspend rooms or represent a human discovering the game at normal speed. Human pacing data is still needed.
- Bill, Veld and Branforth now have physical architect recovery; generic crew from legacy systems still do not each receive a unique NPC.
- Motion profiles are procedural and distinguish system families, not bespoke machinery animations for every room.
- Colorblind and reduced-motion options are not implemented yet. Status text supplements color, but does not replace that accessibility work.
- Terminal patterns award Research rather than room variants. Three-cycle stabilization and terminal Research rewards still need full-run balance data.

## Working Agreements

- Keep room definitions data-driven in `scripts/room_database.gd`.
- Keep generated Godot imports, local backups, and audit exports out of version control.
- Commit art through Git LFS. Run `git lfs install` after cloning.
- Prefer small, tested gameplay changes over broad refactors while the prototype is taking shape.

## A Good Next Session

1. Complete at least one run with each doctrine pair at normal speed.
2. Record the cycle reached, directive outcome, rerolls remaining, Resonance, and the resource that caused any failure.
3. Adjust the largest repeated frustration before adding another system.
4. Add doctrine-specific directives only after every pair can reliably reach the second stage.

That keeps the project moving forward without turning BRINE into a control panel with a space station attached. 🛰️
