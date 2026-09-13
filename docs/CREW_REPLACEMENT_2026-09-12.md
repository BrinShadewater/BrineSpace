# Project handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: three-crew replacement

## Objective and acceptance

Replace all Veld, Branforth and Marsh animations/states following Bill's accepted
detailed local source rebuild. Improve motion and the pipeline skills/bible as
review reveals defects. Goal active; all three complete source revisions are now
selected, with motion/locker polish and final integration acceptance still open.

## Accepted decisions and constraints

Preserve identities, detailed palettes, world scale, action meanings and gameplay.
The owner's Bransforth refers to `branforth`. Marsh remains a blond human-looking
male android with temple plate and off-white suit, without oxygen/helmet needs.
Bill remains unchanged. No export requested.

Owner feedback on the displayed candidate: art looks good except the very large
helmet. Recommended implementation is character-specific precomposed helmeted
clips from preserved body motion and a shared helmet design, fitted per pose.
New source art is reserved for fits that fail, particularly donning/removal.
The owner has not yet reviewed the subsequent smaller dry-helmet revision.

## Current state

Latest fitted-helmet milestone and next work:
[fitted crew handoff](CREW_FITTED_HELMETS_2026-09-12.md). Both humans' revised
pickup/donning sources are now selected with exact idle joins and reverse removal.
The chronological notes below retain earlier evidence and superseded candidate
steps; use the latest handoff for current scope and verification limits.

Added `tools/inventory_crew_art.py` and `tools/map_crew_art_sources.py`.
Native baseline: `output/crew-replacement-2026-09-12/runtime-baseline-v2/`.
First capture failed on fixture type inference; corrected v2 succeeded. Capture
reads the actual loader block, freezes pixels/metadata/timing/strides/hashes and
refuses to overwrite existing evidence. Source maps retain identical alternatives.

| Actor | Body states / references | Loaded helmet states / references |
|---|---:|---:|
| Veld | 170 / 1,104 | 164 / 1,056 |
| Branforth | 170 / 1,104 | 164 / 1,056 |
| Marsh | 140 / 676 | 140 / 704 |

Marsh helmet rows are legacy loaded data, not playable equipment requirements.

`tools/rebuild_human_crew_art.py` now builds Veld and Branforth candidates under
`character/dr-veld-v2/` and `character/chief-engineer-branforth-v2/`, preserving all
170 body and 164 helmet states per actor. Bill's extraction helpers are imported,
not modified. Each actor's original base palette is retained. Human action/life
source crops reproduce 514 Veld and 513 Branforth originals before increasing
density. Output profiles pad body and equipment together, preserving world pivot.
Branforth's narrow north-swim joins now retain the full source instead of clipping.

Tread helmets have actor-specific fittings. Dry base helmets use dense per-frame
crown anchors with restricted head regions to avoid scanner/hand interference.
Both actors' final small dry fits have been rebuilt; Veld's detailed dry contact
and Branforth's native tread/walk page have been visually inspected.

Added `tools/validate_human_crew_art.py`, `tools/review_human_crew_art.py` and
`tests/playtest_human_crew_candidate.gd` with its UID/native lane override.
These cover candidates, not live selected bindings. Reviews/provenance live under
`output/crew-replacement-2026-09-12/{veld,branforth}/`.

### Selected three-crew milestone

Marsh's `tools/rebuild_marsh_art.py` reproduces all 211 distinct legacy source
frames exactly through the original two palette stages, then re-extracts all 140
states/676 references at density 2 using the retained 64-color palette. Selected
revision: `character/marsh-v2`, no helmet variants. Native 72-sheet catalog review
and complete source validator pass; tread/walk/work sheet visually inspected.

`scripts/crew_sprite_player.gd::REVISION_ROOTS` now identifies all four complete
crew libraries. `grid_canvas.gd` selects Veld, Branforth and Marsh catalogs.
`bill_npc.gd`, `crew_life.gd`, `marsh_npc.gd` and `airlock_service.gd` read revised
clearance/locker timelines. `tools/finalize_crew_art.py` derives envelopes and
preserves locker events; both builders call it after complete rebuilds.
`character/ACTIVE_ASSETS.json` records selection. Original migration contracts
are frozen in `tools/crew-art-source-contracts/`, separate from native PNG dumps.

New `test_crew_complete_packs.gd` with UID verifies actual renderer selection:
19,259 checks pass (20260912-092255-headless), as does unchanged Bill's pack test.
The binding audit passes: 68 registered packs, 1,366 clips/8,022 references and
eight portraits across crew/companions. Native integration: crew medium, crew
polish and Marsh battery pass. The animation-expansion fixture needed an empty
`placed_rooms` list for the new fire guard and now selects the new Marsh catalog;
it passes headless with no script errors (20260912-092648-headless).

### Airlock investigation and remaining art

Broad native airlock check does not yet pass. A temporary state probe proved its
first failure was lazy layout loading: actor signature layouts:0 became layouts:2
on first render, canceling the active equip action during navigation rebuild.
`test_airlock.gd` now loads isolated fixture layouts before adding the scene. The
full rerun removes those initial completion/release failures, but return-service
and chamber-cycle failures remain (`integration-native/test_airlock-final.log`).
Focused Bill/Veld headless probes pass; that does not prove native acceptance.
Next probe should report actor/quarter and exact `Service.request` rejection state
at the first remaining return failure. Do not change gameplay to make a fixture pass.

Helmet review also confirms the original authored donning/removal sheets still
carry the large helmet inside their painted frames. Shrinking worn idle/walk fits
alone leaves a size jump at the locker transition. See
`veld/locker-fit-review.png` (first six slots only; each actual clip has 12 slots).
Repair or replace these sources, including held-helmet size, hands and endpoints;
do not declare the owner's helmet concern closed yet.

## Verification

Native capture passed; all 2,884 body references match preserved sources. Veld maps
to 670 source frames from 108 manifests; Branforth to 669 from 108; Marsh to 211
from the expansion manifest. Ten Branforth north-swim transition endpoints match
only after reproducing clipping into their 128px join canvas. Correct that defect
in the rebuild, preserving world pivot rather than retaining clipped edges.
Veld's current candidate passes source preservation (670 frames/108 manifests),
170/164 state and 1,104/1,056 frame coverage, matching gear profiles/timing,
binary alpha and zero border touches. Native catalog loading, every frame's
elapsed-time selection, pause and snapshot restoration pass with zero failures.
96 native sheets captured; tread/dry fitting and base contacts visually inspected.
Whole-library motion review and actual-room acceptance remain pending.

Branforth's final fitted candidate also passes the complete 170/164-state source
validator (669 original frames/108 manifests unchanged, zero border touches) and
native loading/playback/pause/snapshot checks with zero failures. Native sheets
include the padded transition profiles. These checks do not yet establish live
integration or subjective motion quality.

## Next action

Review all changed human clips
in motion, repair identified gait/transition defects, derive new clearance and
locker metadata, then select complete candidates and verify actual-room/save use.
Marsh's full source rebuild still needs `tools/build_animation_expansion.py` and
`tools/build_sprite_polish.py` provenance. Do not call the goal complete at the
candidate-density milestone or treat native sheets as continuous motion approval.

The preceding next-action paragraph describes the pre-selection plan. Current
priority is the remaining native airlock diagnosis and fitted locker sources,
then complete motion/room review for all three selected revisions. Marsh's full
source rebuild is now done; further pose/motion repairs remain within this goal.

## Fitted-source follow-up

Preserved and inspected `character/crew-helmet-fit-v2/sources/veld-donning-candidate-01.png`:
six edited poses with smaller held/worn shells. Exact prompt and references are
in that revision's README. `tools/review_fitted_helmet_source.py` produces a
deterministic extracted contact sheet and registration, without runtime promotion.
Pickup matching, endpoint comparison and motion review remain necessary.

Native airlock diagnosis found legacy room layouts applied only during drawing,
moving the locker target after navigation captured it. `bill_room_geometry` now
applies the same authored layout before snapshotting. The native rerun remains
failing: authored quarter-one locker containment/reachability is exposed earlier,
so this is not an accepted airlock fix. Evidence:
`output/crew-replacement-2026-09-12/integration-native/test_airlock-layout-parity.log`.
Continue the geometry diagnosis without relaxing reachability checks.
