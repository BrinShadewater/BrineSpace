# Veld residency ownership inventory

Updated: October 5, 2026 · BrineSpace · Native isolated inventory, not shipped

## Objective and acceptance

Extend the six-frame residency experiment to the complete selected Veld body and
helmet banks. Count unique storage rather than animation references, identify
consumer constraints, and test whether a meaningful amount of storage can expire.
No gameplay eviction is accepted without a complete preparation/pinning policy.

## Accepted decisions and constraints

Use current source's full replacement-crew loader, restricted only to actor Veld.
Preserve its catalog order, overrides, generated frames, equipment validation and
pool behavior. The generator stores the source hash and copies the function;
runtime code and owner art remain unchanged. Native Windows scratch profile only.

## Current state

`output/veld-residency-inventory-2026-10-05/` contains the source-copy generator,
generated loader, native inventory/detachment fixture, guarded runner, source hash,
full clip-to-storage membership report and owner fingerprint results.

| Inventory | Result |
|---|---:|
| Body/equipment clip entries | 390 |
| Distinct frame wrappers | 3,186 |
| Unique image storage objects | 1,800 |
| Unique decoded storage | 365.35 MiB |
| Engine texture counter increase for loader | 487.06 MiB |
| Storage referenced by any bare clip | 184.56 MiB |
| Helmet-only storage | 180.79 MiB |
| Helmet-only storage excluding every death clip | 151.77 MiB |
| Non-pool images requiring estimated byte sizes | 0 |

Rows overlap through shared images; per-clip totals must not be added. All surviving
storage in this startup fixture maps to weak pool records with measured decoded
sizes. This does not prove live gameplay never generates additional textures.
Engine accounting is not a driver-residency, working-set or Mac unified-memory
measurement, and is deliberately separate from decoded bytes.

A second run detached only wrappers referencing the helmet-only, non-death set,
while retaining every bare/death image. It detached 1,321 wrappers, expired all
769 targeted image objects, and reduced the engine counter by **212,148,856 bytes
(202.32 MiB)**. No CPU image copies were retained. This fixture does not run a
character or restore those 769 images: it establishes an ownership/reclamation
upper bound, not a safe pin set or full-bank reload performance. Native pixel and
reload timing evidence remains limited to the earlier six-frame experiment.

### Consumer map and preparation constraints

| Consumer / trigger | Required protection |
|---|---|
| CrewSpritePlayer.frame / frame_at_elapsed | Current clip, authored turns, equipment, fallback facing, and immediately selectable successors must be resident before use |
| Grid room slots, current textures, water_death_last_frame | Keep displayed/retained wrappers pinned until references or draw commands are replaced |
| Veld death capture and playback | Reads pixels from entry/candidate frames; pin candidates needed for current pose before death, plus saved entry equipment and selected death clip |
| Interrupted South reading | reading_return_sources reads clip pixels; interruption searches exit-frame pixels; pin source and exit clips through completion |
| Startup mirrors / helmet composition | Reads source images; complete before releasing source storage, or provide a separately verified reconstruction recipe |
| Locker request, equipment completion | Begin preparation at request/approach; cancellation must preserve current equipment; new bank must be ready at original action completion |
| Save restore | Prepare restored equipment, active clip, transitions and saved death entry before gameplay resumes |
| Public set_helmet_equipped | Immediate switch contract; examined calls are fixtures/tests plus subclass forwarding, not proof of a normal UI bypass. Preserve that contract in tests and any future callers |
| Portrait panel | Examined panel uses Architects.selection_portrait; do not assume it pins this animation bank. Other consumers still require explicit coverage |

Normal gameplay equipment requests route through `airlock_service.gd` to
`request_helmet_at_locker`, then `begin_helmet_action_at_locker`; completion flips
equipment in `advance_helmet_action`. There is potential preparation lead time,
but it is not guaranteed by this inventory. At 4x simulation, wall-clock lead time
shrinks; pause/resume, a request while already near a locker, death, cancellation
and Continue must be tested. Do not turn a readiness miss into delayed gameplay.

Important new observation: `veld_npc.gd::reading_return_sources` and
`veld_death_motion.gd::capture` use `get_image()`/pixel comparisons at runtime.
This is both a residency dependency and a possible GPU-readback overhead source.
No cost is measured here. Source/pose identifiers or precomputed signatures might
replace the comparisons only after proving identical transition selection; simply
dropping them would change accepted joins. No such change is made in this pass.

## Verification

Two successful native runs: complete bank inventory, then actual upper-bound
detachment. Zero engine errors; all 2,936 owner non-log files unchanged in both.
Resolved user-directory guard ran before fixture writes. No live station,
minimum-hardware run, pixel comparison of the detached full bank or Mac run.
Changed output experiment files and this report, action register and current status.

## Next action

Prototype instrumentation at normal locker request/completion for one live Veld:
record actual wall-time preparation windows at 1x/2x/4x and the exact successor
clips requested. Initially retain all storage and log hypothetical pin/miss events;
this validates coverage without risking missing art. Include direct-read, restore
and interruption paths above, then choose a conservative set and measure its real
reclaimable bytes. Use bounded bytes/time for preparation, not one image per frame.

Only after coverage and deadlines pass should an isolated gameplay candidate detach
storage. A full 769-image reload is not certified by the five-image/41 ms experiment.
Do not claim a 202 MiB production saving until that candidate passes matched
gameplay, pixel/behavior and memory checks. Memory and release gates remain open.
