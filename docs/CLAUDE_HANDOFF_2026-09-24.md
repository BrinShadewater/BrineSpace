# BrineSpace takeover handoff for Claude

Updated: September 24, 2026 · Project: `C:/Users/Alex/Documents/Brine Space`
Task: Prepare BrineSpace handoff forClaude

## Objective and acceptance

The owner asked to wrap up all BrineSpace sessions, update skills, asset pipeline,
workflow and bible, and leave detailed notes for Claude. This closeout consolidates
the existing work; it does not declare the broad polish goal complete. The next
developer should be able to identify current source, preserve owner work, choose
the next bounded investigation and distinguish technical evidence from acceptance.

Read in order: `CLAUDE.md`, `AGENTS.md`, [CURRENT_STATUS](CURRENT_STATUS.md), this
handoff, then the relevant section of [asset pipeline/workflow](ASSET_PIPELINE_AND_WORKFLOW.md).
For gameplay, read [development notes](DEVELOPMENT_NOTES.md); for visual work read
the [bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md) and the appropriate repository skill.
Do not read every historical report before starting a scoped task.

## Accepted decisions and constraints

BrineSpace is a Godot 4.7 passive roguelite station builder, locally tested with
4.7.2. The north star is restoring a silent underwater station, learning satisfying
placement decisions and watching systems interact. BRINE is dry, damaged and a
little haunted. Avoid cheerful assistant-like dialogue.

Normal expeditions spend room costs and enforce resource failures. Doctrines,
timed directives and scenario victory remain retired; use Conclude Expedition.
Recipes stay hidden until functioning rooms discover them. Three consecutive
functioning cycles stabilize a pattern; later-loop bonuses double, Archived Data
is awarded and the related blueprint becomes half price. Stabilization does not
decrypt rooms. Blueprints, crew and companions use the Meta Progression shop.
Encountered crew play for that loop; buying them makes them return in later loops.
Existing ownership stays owned and free. Do not alter these rules to help tests.

No broad refactor of `scripts/main.gd`. No new generation, commit, push, publication,
release export or deletion of old source/builds is part of this closeout. Local
deterministic art repair was authorized; Higgsfield still requires a fresh explicit
owner request. Paired `.gd`/`.uid` files and prototype saves must survive intact.

All 27 owner-finished rooms in CURRENT_STATUS are protected in every rotation.
Other rooms preserve their first rotation; intentionally cleared secondary views
are authoring space. The latest eight completions supersede the September 23
cleanup list. Owner completion is not a new navigation or visual test pass.

## Current state: use this checkout, not HEAD alone

At intake, branch was `main`, HEAD `f380c42c046de276b0efe26364e7596ca2410ec7`.
The index and HEAD each contained 32,097 paths, with no missing or extra index
paths. The checkout is populated correctly; it is also extensively dirty:
3,058 status entries before this closeout, including 2,423 character entries,
211 docs, 150 tests, 97 assets, 71 tools, 44 rooms, 41 scripts and 18 skill entries.
These are status entries, not a claim that each is a newly authored file today.
Full inventory: `output/claude-closeout-2026-09-24/git-status-before.txt`.

**A fresh clone or reset loses the local delivered state.** No commit was created
by this task. Work directly in this checkout or deliberately transfer the dirty
files, LFS art, ignored originals and owner data. A Git diff alone does not carry
untracked files or ignored resources. This closeout snapshot is not a full project
backup. It saves changed guidance and targeted owner layout/mark copies under
`output/claude-closeout-2026-09-24/pre-edit/`.

On another machine, clone with `git -c core.longpaths=true` and check index/tree
completeness before trusting it. Install/use Git LFS for rasters. Pointer files
are not broken images. `vendor-art/` contains licensed originals and is ignored;
obtain that folder from the owner if source repairs need it. Do not publish it.
Rights are governed by [NOTICE](../NOTICE.md).

## Local runtime and important locations

| Item | Location / meaning |
|---|---|
| Editor used in recent evidence | `C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64_console.exe` |
| Configured F5 entry | `res://scenes/title_screen.tscn`; gameplay is `scenes/main.tscn` |
| Design/default window | 1920×1080 / 1600×900; map capture coordinates accordingly |
| Owner profile and diagnostics | `%APPDATA%/Godot/app_userdata/BrineSpace/`; profile `brine_save.json`, bug reports, session reports |
| Owner Studio layouts | Same user directory, `room_layouts.json`; recovery files must also be preserved |
| Shipped/default layouts | `rooms/full-wall-v1/default-layouts.json`; separate from user layouts |
| Bought prop registry and owner marks | `rooms/tileset-library/` |
| Converted sheets / originals | `assets/new-tilesets/` / ignored `vendor-art/` |
| Active character registry | `character/ACTIVE_ASSETS.json`; actor catalogs/manifests and source contracts select exact art |
| Current skills | `skills/brinespace-character-pipeline/`, `skills/brinespace-room-pipeline/` |
| Installed mirrors | `C:/Users/Alex/.codex/skills/` with the same two names |
| Evidence | `output/`; access exact known paths, never recursively search the whole tree |

## Gameplay and performance transfer

### Procedural underwater sites

New expeditions now preserve a familiar opening while varying terrain, finite
resources and scenery and spacing recoveries farther apart. First profile sightings
are Veld → Branforth → Marsh, assigned on survey separately from rescue and shop
eligibility. Later repeat encounters use an expedition-wide seeded shuffle; saved
occupants are stable. Legacy saves preserve maps. 463 exterior props are hidden
from new Studio placement while existing placements remain editable.

[Procedural sites](PROCEDURAL_SITES_2026-09-23.md) records 1,000 deterministic
seeds and three normal paid native openings. Seeds 32/73/118 rescue Veld and conclude
at cycles 15/16/15. The longer seed-32 and seed-73 all-recovery results are checkpoint
chains with test-player corrections, not uninterrupted human expeditions. The
seed-73 chain concluded at cycle 290; earlier 163/221 cutoffs remain failed all-three
assertions. Do not erase those limits. Review the [owner page](PROCEDURAL_SITES_OWNER_REVIEW.md)
for provisional scenery. Owner art and pacing acceptance are still open.

### Repair, routing and stalls

[Owner report fixes](OWNER_BUG_REPORT_FIXES_2026-09-23.md) cover cramped flooded
doorway escape, repair route retention across water changes, furniture-aware work
positions, projected air budgeting, bounded retry for unavailable repair jobs and
preventing remote meals on unjoinable routes. A native replay seals the reported
Reactor and checks disk Continue. These fixes do not grant free resources or air.

[Follow-up](EXPEDITION_FIX_FOLLOWUP_2026-09-23.md) includes a paid seed-32 run ending
at cycle 16 and a lone-swimmer avoidance optimization. Warm doorway search dropped
from about 199 to 125 ms, still visibly slow. The next investigation is graph-valid
paths rejected by final smoothing, using the preserved report and temporary state
probes before changing route semantics. Related [routing](PROCEDURAL_ROUTING_HANDOFF_2026-09-23.md)
and [performance](PROCEDURAL_PERFORMANCE_HANDOFF_2026-09-23.md) reports contain exact
fixtures. Means improved substantially, but 162–369 ms spikes remain across the
different recorded probes. These are CPU measurements, not accepted rendering FPS.

### Power and drones

[Stored-Power charging](DRONE_STORED_POWER_2026-09-23.md): mining/salvage drones
charge independently of bay cycle allocation, preserving a shared reserve of 3.
Charging resumes above that; prepaid charge persists. Manual suspension, global
pause and station Power-off still hold it. Focused and native 16/3/4-Power checks
passed at that revision.

[September 24 report](DRONE_FULL_POWER_REPORT_2026-09-24.md): seed 3862060672,
cycle 457, Power 22/22. Both mining drones were already at 100%; the only discovered
mining deposit was depleted, while nearby surveyed piles required salvage. Charging
was not broken in the captured state. Inspector battery/work status now precedes
charging totals; depletion also reports correctly with no wreck entries. Do not
reopen a charging fix merely from the FULL label or a docked drone. Inspect battery,
eligible surveyed stock, route, suspension and reserve separately.

## Studio and artwork transfer

[Studio fixes](STUDIO_OWNER_DECORATION_FIXES_2026-09-23.md) cover front/back ordering,
late floor detail editing, fallback-host deletion persistence, Mining Bay walls,
ordinary floor/riser joins, the Airlock 180° locker and bench under-seat coil.
Dragging defers walking-preview navigation: 6.457 to 0.014 ms/update in the isolated
probe. Long-session hitch acceptance is still open. 44 cards were refreshed there;
that number is not a claim of current owner-approved cards.

[Deletion persistence](STUDIO_DELETION_PERSISTENCE_2026-09-23.md) checks all 188
room/rotation source combinations and Pressure Control q1 across reload/rotation.
Preserve authoring semantics: Studio free placement, live dressing filters and
paused wall decorations are deliberate. Follow the workflow guide before editing.

Bill's four walks, north/west work identity, standing endpoints, locker identity
and approximately 14% smaller normal helmet are installed. Do not repeat the
helmet shrink from an old note. Branforth's selected south/north/west repair chains
are installed; the broad/young west studies were rejected. Veld's reviewed art
remains unchanged. All four cast have reviewed unmirrored bought-bunk profiles;
that does not accept other bed orientations/sizes.

Marsh has maintenance draw/check/stow, all four swimming starts/stops, all twelve
directed turns in each of normal swim, dry carry and loaded swim, four-direction
loaded pickup/loops and cargo drainage transitions. The earlier missing-turn TODOs
are superseded. Controller review caught omitted pickup timing and suppressed
exterior turns; both were repaired. Drainage rising poses track saved water progress
and hold planted feet during equalization. See the dated reports indexed in
[the preserved pre-closeout status](CURRENT_STATUS_HISTORY_2026-09-24.md), especially
`MARSH_EXPEDITION_PRESENTATION_2026-09-22.md` and `MARSH_CARGO_DRAIN_2026-09-22.md`.
Complete coverage and successful playback still do not establish owner motion acceptance.

Life Support console contact and reachable bunk/activity checks are implemented.
Drone chassis/tool shear, hatch scale continuity and clearance-face selection have
recorded fixes. Preserve intended hull occlusion. BRINE/tank and earlier appearance
reports must be reconciled against selected current assets before a new art pass.

The latest style task is **Explore Graveyard Keeper 2 Style**. Its retrievable
preview says the owner likes that reference's graphics, camera and art style and
asks how BrineSpace could move toward it. Recent turns returned empty item arrays
even with outputs enabled. No detailed proposal or later approval could be verified
through the task reader. Preserve the task as recoverable history; do not fabricate
its conclusion. The current installed art contract remains the documented top-down,
inward-facing equipment with bought-prop compositions until that decision is recovered.

## Packages and acceptance boundaries

Latest recorded Windows/Mac test build: **brinespace-6600876d650b0d68**.
Windows: `builds/BrineSpace-stability-2026-09-23/BrineSpace.exe` with its PCK.
Mac: `builds/BrineSpace-mac-stability-2026-09-23/BrineSpace.zip`.
[Build report](STABILITY_TEST_BUILDS_2026-09-23.md) records matching 15,619-asset
audits, actual Windows New Game/Continue/Fit/F8, crew/pod pixel checks and hatch
boundary checks. They include Continue dialogue, open-empty pod and tiny-aperture
hatch fixes. They predate procedural sites and subsequent source/Studio/drone fixes.
No new packaging was performed for this handoff.

The Mac archive is Universal2, ad-hoc and not notarized. Native Apple Silicon
launch, controls, gameplay, saves and Gatekeeper behavior remain untested here.
Windows success and ZIP inspection cannot close that gap. Music measurements and
bounded audio captures passed in earlier reports; owner listening remains open.

## Next action: choose one bounded objective

1. Recover the latest style discussion with the owner before any camera/art
   conversion. Use a separate preview only if newly requested; protect current art.
2. For engineering continuation, reproduce the preserved doorway routing spike,
   inspect graph-versus-smoothing rejection and measure the same workload after a
   narrow fix. Maintain actual crew safety and paid rules.
3. Continue a normal paid source expedition through survey, rescue, crew activity,
   save/Continue and conclusion. Label automated strategy and checkpoint chains.
   Capture actual defects rather than accumulating unrelated fixture passes.
4. Obtain owner review of scenery, crew motion, room coherence and listening, plus
   native Mac testing when hardware is available. These need human/hardware evidence.
5. Preserve staged owner-room concerns (Research q2 route, Pressure Control clipping,
   Listening Post console extent) without installing old proposed edits automatically.
   Later owner furnishing supersedes earlier compositions. Dialogue note 17 still
   needs its exact offending real-session line; avoid speculative timing fixes.

## Verification and closeout files

This task changes documentation and skill guidance only. The existing gameplay,
art, owner layouts and packages remain in place. Appropriate checks are local link
resolution, skill structure, installed/source mirror equality, Git index integrity,
and preservation of owner-data hashes. No gameplay rerun is claimed for this task.

Files maintained here: `CLAUDE.md`, `docs/CURRENT_STATUS.md`, this handoff,
`docs/CURRENT_STATUS_HISTORY_2026-09-24.md`, `docs/ASSET_PIPELINE_AND_WORKFLOW.md`,
the bible, development/release workflow entry links, and each pipeline skill's
entrypoint/handoff reference. Session IDs, closure outcomes and final verification
are recorded in `docs/BRINESPACE_SESSION_CLOSEOUT_2026-09-24.md`.

Older reports retain their dates and scope. Closing the tasks preserves unresolved
work here; it does not certify the whole game or delete their recoverable history.
