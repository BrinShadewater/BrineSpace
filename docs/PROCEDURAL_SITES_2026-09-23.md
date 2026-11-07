# Procedural underwater sites

Updated September 23, 2026 · BrineSpace · Implemented locally; verification complete within the scope below.

Latest follow-up: the progressed seed-73 checkpoint chain now completes all three
recoveries, and two measured crew performance costs have focused fixes. See the
[performance handoff](PROCEDURAL_PERFORMANCE_HANDOFF_2026-09-23.md) for passing
regressions, native recharge evidence and remaining timing limits.

## Objective and accepted decisions

New expeditions retain the 40×40 map and familiar Bill/core opening, with seeded
terrain, salvage, deposits and seven habitat regions. Three unidentified recovery
sites occupy Manhattan bands 4–6, 7–9 and 10–12 with five-cell minimum separation.
First sightings across a profile introduce Veld, Branforth, then Marsh, regardless
of exploration direction. Later owned starters remain selectable. Sighting is
separate from rescue/shop eligibility. Continue never regenerates geography.

All exterior scenery leaves the Room Layout Studio placement catalogue, while
existing placements, IDs, aliases, owner marks and indoor equipment remain intact.
No source-art modification, Higgsfield, commit, push or packaging is requested.

## Current state

- `scripts/site_generator.gd`: independent RNG; protected opening/intakes and
  companion approaches; connected rock walks, wrecks, finite deposits, reserved
  recovery approaches, seeded habitats and grouped scenery. At most 32 attempts,
  then a tested fixed fallback. Stores actual geography with seed/version.
- `scripts/site_discovery.gd`, `architects.gd`, `meta_state.gd`: ordered first
  sightings with atomic profile-write acceptance, unidentified wards and stable
  human/charging assignments. Existing met/owned characters migrate as sighted.
- Main/save/visibility/render integration: simulation-owned survey, strict new
  checkpoint validation, legacy preservation, seed-aware scenery caches, F8 seed
  metadata. Explicit authored-map metadata is restricted to script fixtures.
- `rooms/tileset-library/exterior.json`: 463 per-asset exterior classifications.
  Studio filters, variant lists, insertion, duplication and paste enforce them;
  existing placements still resolve and can move/delete.
- `scripts/site_scenery.gd`: provisional low boulders `uw1-188`, `mb-210` and
  timber `mat-130`, `mat-131`. Rocks are 0.20–0.38 cells, timber 0.35–0.55;
  no new collision or salvage behavior. Original coral/kelp remain after bought
  candidates failed projection/edge-pixel review. Existing saves keep old scenery.
- `tools/audition_exterior_scenery.py` produces the inventory, contact sheets,
  source hashes and explicit decisions; originals and owner marks are untouched.

## Verification to date

- 1,000 seeds: 1,000 distinct layouts, deterministic geometry, valid fallback,
  protected opening, separation, door approaches and early extraction access.
  Latest run: 279 total retries; worst generation 24.582 ms. This is generation
  CPU time, not a gameplay FPS claim.
- Discovery tests pass for all starters, partial/legacy profiles, reverse-distance
  exploration, simultaneous reveals, abandonment and failed profile writes.
- Save fixture passes unidentified/revealed/repair/wake phases and restores the
  September 23 frozen legacy checkpoint without new terrain. Partial Android
  charging and the portable legacy-format fixture also pass in the native rerun.
- Existing meta fields/isolation/shop, run-save, registry, wreck-clearance,
  architect-recovery and cryo timing checks pass. Registry: 10,507 props,
  zero registration problems. New Studio catalogue contract passes.
- Native initial map, Studio filter and paired existing/bought samples under
  production lamps/fog inspected. Native samples retain original coral/kelp and
  show why upright candidates/stray edge pixels were rejected. Owner acceptance
  remains separate. The final native audition waits for usable viewport dimensions.
- Sixty warm redraws of the paused four-room art fixture: environment CPU stage
  mean 305.2 / max 434 microseconds; fog mean 148.7 / max 173 microseconds.
  This is scoped CPU draw instrumentation, not active-expedition FPS or a before/
  after performance benchmark. Habitat changes retain decoded source textures.
- Initial paid seed 32 reached Veld rescue at cycle 18. Its frame-post-draw
  screenshot wait stalled when the window was minimized. The harness now explicitly
  renders captures. A subsequent run exposed a harness-only repair-reserve bug
  after rescue; corrected without changing production costs/failure rules.

Evidence: `output/procedural-sites-2026-09-23/`, including `scenery-comparison.png`,
`bought-candidates.png`, `audition-decisions.json`, per-suite logs and per-seed events.

## Paid native acceptance

All three final runs use the actual dealt hand, legal placement/rerolls, normal
resource costs/failures and the player's normal 4× speed control. No resource,
blueprint or clock injection. Each writes a disk checkpoint, creates a fresh
scene through Continue, compares the restored map/resources, rescues Veld and
selects Conclude Expedition. Logs have no engine/script errors.

| Seed | Veld rescued at cycle | Concluded at cycle | Rooms at conclusion | Failures |
|---|---:|---:|---:|---:|
| 32 | 11 | 15 | 9 | 0 |
| 73 | 10 | 16 | 8 | 0 |
| 118 | 10 | 15 | 8 | 0 |

Final per-seed evidence lives in `expedition-<seed>-accepted/`. Earlier runs are
retained as diagnostic evidence, not counted as passing acceptance. Later scenery
anchoring/cache edits affect decoration only; terrain, deposits, costs and recovery
mechanics in these paid runs are unchanged. The final native art fixture separately
covers the renderer. Source rasters and owner layouts/marks were not rewritten.

## Follow-up: longer paid expedition and capture correction

The `--all-crew` mode in `tests/playtest_procedural_expedition.gd` now retains
rescue/final checkpoints and accepts `--resume` with the run's isolated `--profile`.
It extends the route to subsequent wards using normal costs, dealt cards, legal
rotations and the existing individual/full-hand reroll controls. It budgets food
before adding a Hab (which brings its own resident), accepts supported Galleys,
and prefers legal door rotations that leave an outward route. These are test
player changes; production balance, cards and resource rules were not changed.

The first extended strategy depleted food at cycle 32 after building extra Habs.
The supply-gated run then survived to its cycle-112 time limit, with Veld recovered
at cycle 10 and Branforth repaired at cycle 55. Continuing that exact checkpoint
recovered Branforth at cycle 153 and survived to cycle 180. Long waits and detours
reflect this deliberately limited automated player, not accepted human pacing.
These diagnostic runs are not additional passing all-crew acceptance tests.

The final bounded continuation from cycle 180 passed with all three recoveries:
Veld at cycle 10, Branforth at 153, Marsh at 224, followed by explicit conclusion
at 224 with 47 rooms and six crew. All three wards retain unique occupants, paid
repairs and completed wake/charge state. Final reserves include 65 Food, 65
Oxygen, 12 Power and 160 Metal. No free building, disabled failures, resource
injection or accelerated test clock was used; the player-facing 4x control remained
active. Resume checks compared saved map, wrecks and resources. The final log
has zero test failures and no engine/script errors.

Evidence chain: `expedition-32-extended-supplied/final.loop` (cycle 112),
`expedition-32-extended-resumed/final.loop` (180), and
`expedition-32-extended-final/final.loop` (224), with event timelines and native
captures in each directory. `paid-32-extended-final.log` is the final passing leg.
This is one paid checkpoint chain with test-player corrections between legs,
not a fresh uninterrupted run or a pacing target. Earlier failed/time-limited
legs remain in the report rather than being counted as passes. The final Marsh
capture was inspected; owner art and human pacing acceptance are still separate.

The standalone runtime capture previously rendered before the camera had settled.
`tests/test_site_runtime.gd` now waits for the viewport and checks BRINE's camera
position. Its native rerun passes (`runtime-framing.log`), and the corrected
`native-site-32.png` was inspected. The original source/native art comparisons
remain available.

A paused review of the cycle-112 paid checkpoint captured two surveyed timber
groups without altering survey, lights or terrain. `generated-scenery-22-13.png`
shows readable grounded timber between rooms and a wreck; the farther
`generated-scenery-22-11.png` remains obscured by production fog. The review
script, placement metadata and log are retained in the evidence directory.
Owner visual acceptance remains open.

## Follow-up: explicit repeat-encounter shuffle

`scripts/site_discovery.gd` now uses one expedition-wide Fisher-Yates shuffle
for known characters, with its own seed stream. Already assigned occupants and
the starter are filtered out; unseen introductions still take priority. The
remaining shuffled order reconstructs from the saved seed and assigned wards,
so Continue needs no new payload. Assigned identities are never rewritten.
Shuffle work is skipped when no newly surveyed sites need occupants.

The discovery contract now checks all starters across 24 seeds each, all six
remaining-roster permutations, location/batch independence and reconstruction
between reveals. `discovery-shuffle.log` passes. The native runtime contract
also compares uninterrupted reveals with an actual disk checkpoint taken after
one known-character reveal; `runtime-shuffle.log` passes with zero errors.

## Fresh seed-73 follow-up: bounded result, not a full-recovery pass

The final fresh run (`expedition-73-fresh-supported/`) kept its test-player
strategy fixed, used normal costs/failures and exercised disk Continue. It rescued
Veld at cycle 22, scheduled six surveyed basalt excavations and concluded alive
at the 600-second limit, cycle 111, with 33 rooms. Final reserves: 100 Metal,
67 Food, 67 Oxygen and 12 Power. Branforth was surveyed/identified but not repaired;
Marsh's site was still unidentified. **The all-three-recovery assertion failed.**
This run is resource/exploration evidence, not a second complete recovery pass.
The earlier seed-32 checkpoint chain remains the full paid-recovery evidence.
The final seed-73 scenery probe found no bought-art placements inside its surveyed
cells (`generated-scenery-review-73.json`); no additional bought-art acceptance is
claimed from this run. Its native overview was inspected, and the source/native
comparison sheets and seed-32 timber close-ups remain the visual evidence.

Earlier seed-73 diagnostic attempts are retained: `fresh-all-crew` discarded Life
Support while saving repair metal and failed at cycle 19; `fresh-retained` was
stopped after the initial deposit emptied and the driver idled; `fresh-excavation`
mined before establishing sufficient generation and failed at cycle 16. The final
driver retains essential support cards, establishes oxygen/power before recovery,
and schedules exposed, surveyed rock through the normal Mining Drone Bay. The
checkpoint probe confirmed an exhausted 12-load deposit, a working mining bay
and five surveyed rock cells. No generation rules, yields, construction costs or
failure conditions were changed to accommodate these tests.

The remaining paid-playtest limitation is efficient fresh-run routing through all
three chambers, plus human pacing acceptance. Do not repeatedly treat this greedy
automated player's detours or time limits as a map-balance verdict. A human route
review or a materially better route planner should precede more long repetitions.

## Deliverables and next action

Subsequent [routing validation](PROCEDURAL_ROUTING_HANDOFF_2026-09-23.md) corrected
test-player paths through occupied rooms and exhausted deposits. A new fresh
seed-73 run reached and repaired all three sites, rescued Veld/Branforth, and
concluded alive at cycle 111. Marsh was charged and powered but waiting for a free
berth; the all-rescue assertion remains unpassed. Production balance is unchanged.
The later native berth-strategy fixture now verifies that paid Hab construction
frees Marsh's berth and completes the six-person roster, using explicit fixture
hands. That result is distinct from a fresh dealt-hand expedition; see the routing
handoff for the retained failed fresh attempt and the duplicate-Hab correction.

- `map-comparison.png`: diagnostic layouts for the three tested seeds; teal markers
  are unidentified sites, not preassigned characters.
- `scenery-comparison.png` and `bought-candidates.png`: source comparisons and all
  twelve reviewed candidates; `audition-decisions.json` retains source hashes.
- `native-scenery-audition-final.png`: existing/bought pairs above four rooms,
  left-to-right rocks, coral, kelp, timber, using real exterior lighting and fog.
- `studio-filter.png`: native catalogue result; the isolated fixture also proved
  existing placements remain movable/removable and indoor equipment stays available.
- Dedicated subsystem: `python tools/run_tests.py --subsystem procedural-sites`;
  add `--native` for the render-bound lane. Paid and art-preview fixtures are
  intentionally run directly and keep their evidence separate.

Implementation and requested verification are complete. Owner art approval and
human pacing/balance review remain open; the three bounded automated journeys do
not establish human expedition pacing or native Mac acceptance. The longer seed-32
checkpoint chain now covers all three paid recoveries, with the limitations above. Current
Windows/Mac downloads predate this feature; no new packages, commits or pushes
were made. Maintained environment workflow and its installed copy are synchronized.
