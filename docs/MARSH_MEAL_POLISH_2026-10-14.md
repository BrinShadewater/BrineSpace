# Marsh eating and drinking polish

Updated: October 14, 2026 · BrineSpace · eating/drinking continuation

## Objective and acceptance

Owner requested eating and drinking after seated/resting review. Polish current
appearance and handoffs, then provide a local review. Owner visual acceptance
was given in the next continuation request ("Those look better").

## Accepted decisions and constraints

Preserve current likeness, ivory boot panels, graphite soles, suit and asymmetry.
Whole generated bodies for anatomical changes; original source art retained.
Retain six-second eating/three-second drinking, station contacts, economy and
all accepted prior animation work. Corner lounge armchairs remain excluded.

## Current state

`character/marsh-meal-polish-v1/manifest.json` overrides only eat/drink South:
12 selected holds, seven complete authored drawings plus exact current idle at
both ends. Other six directional clips retain their original drawings. Bowl,
spoon and mug are part of each generated whole pose. One neutral-derived scale,
whole-body registration, original canvas184/pivot92,172/height148 and six150ms
holds. Source, exact prompt, reference guide and provenance remain under the
versioned folder. `tools/build_marsh_meal_polish.py` rebuilds locally and is called
last by the maintained Marsh rebuilder.

`scripts/marsh_npc.gd::meal_animation` derives presentation from the saved service
timer and fits seven bowl cycles into6s and three cup cycles into3s. Empty-handed
final holds precede drinking/idle, avoiding mid-bite cuts. Source timing stays
900ms; runtime eating cycles are approximately857ms and drinking cycles1000ms.
No new saved state or service timing change. Existing emergency interruptions
retain their previous behavior; new interrupted stow choreography is not claimed.

Review: `character/marsh-meal-review-2026-10-14/review/index.html`, built by
`tools/publish_marsh_meal_review.py`. Eight directional before/current source
comparisons and four native galley videos. Frozen selection has48 source hashes.

## Verification

- Python: two source preservation/scope/body tests pass. All48 old references
  retain exact hashes; exactly12 South selected holds differ. Metadata retained.
  Builder reproduces seven PNGs, manifest, provenance and board byte-exact.
- Meal contract8,665 checks; crew complete packs4,832 checks; retained rest and
  corner-contact regression69 checks. Zero failures. Baseline update is limited
  to the two South meal frame lists; all other actor/state metadata remains exact.
- Native actual main scene:9,281 checks/zero,936 samples at25Hz. Four default
  galley rotations, real reachable counter contact, ordinary arrival, complete
 6s/3s service, pause and final idle. Physical foot/facing stays fixed; snapshots
  remain valid; source/frame marker and transformed alpha bounds guard captures.
  **All four contacts face north.** South revision and East/West are source
  reviews, not native furniture acceptance in those directions. Room rotations
  are not four character facings.
- All four native hold boards and all48 source holds inspected, including new
  South bowl/spoon and mug grips. This is sampled/controller playback evidence,
  not continuous real-time viewing, autonomous approach or full disk Continue.
  Contract checks prove presentation resumes from saved service timer fields;
  they do not claim a fresh-process checkpoint test.
- Every Godot process used scratch APPDATA. Before/after owner fingerprints are
  recorded in `output/marsh-meal-2026-10-14/`; no owner game process stopped.
  All2,948 owner non-log files remain byte-exact. All eight source WebPs and
  four native MP4s fully decode.

Logs and evidence: `output/marsh-meal-2026-10-14/`. An initial copied fixture had
an indentation parse error; retained log records it. Corrected fixture passes;
no runtime assertion was weakened. Previous historical shutdown rebaker mismatch
was not rerun or changed by this scoped meal pass.

## Next action

Owner reviews eating/drinking clips. No export, commit, upload or automatic
follow-up. Corner-chair omission and all earlier accepted art remain selected.
