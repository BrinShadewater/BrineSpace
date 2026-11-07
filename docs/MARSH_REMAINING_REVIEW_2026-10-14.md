# Marsh remaining animation review

Updated: October14,2026 · BrineSpace · remaining-animation continuation

## Objective and acceptance

Owner accepted eating/drinking and requested continuation through the remaining
animations. Review the cargo swimming/return, carrying turns, water reactions
and retained compatibility clips; preserve working art. New review is ready at
`character/marsh-remaining-review-2026-10-14/review/index.html`.

## Accepted decisions and constraints

Prior swimming strokes, locomotion, east run, work, gestures, rest and meals stay
selected. Marsh remains sealed/helmet-free and does not need oxygen. Corner
lounge armchairs stay excluded. Do not enable legacy air/helmet behavior merely
to demonstrate its retained sprites.

## Current state

Reviewed remaining inventory:60clips/360holds. Loaded water24/148, dry carrying
turns12/76, water reactions12/64, compatibility air/helmet12/72. The low-air
distress subset in water reactions is also deliberately inactive in normal play.
Source sheets from this pass show complete cargo/turn chronology;
water reactions were also covered by the earlier gesture source review.

No new art or runtime change needed: all16pickup/drain joins and48directed-turn
endpoints match the adjoining selected whole poses exactly, after pivot-aligned
transparent padding only. No silhouette/colour/timing changes. All360 frozen
source hashes and manifest contracts remain exact. Do not mistake this for owner
acceptance of every retained drawing or universal route/physical-contact proof.

`tools/publish_marsh_remaining_review.py` publishes60source clips, four complete
pickup→loaded swim→drain→carry→unload source chains, and native cargo-turn movie.
Original clocks are preserved in source clips. Native turn grid uses normalized
progress per column: its24fps movie is a selection demonstration, not identical
authored speed for differently timed turns. Source clips give authored timing.

`tests/playtest_marsh_water_turn_match.gd` now resolves current ordered manifests
for source/timing comparison and accepts a separate capture-output directory.
Its historical installation map was superseded by material/registration work:
the first run compared old source files and failed108source assertions while
all76turn holds/selection checks passed. First log is retained. Final comparison
uses current148cargo-water holds; no art was changed to satisfy stale assertions.

## Verification

- Source preservation and gallery publisher:60clips/360holds unchanged,
  64exact joins; all64source/chain WebPs decode.
- Native current player:148source matches,76selected turn holds,108captures,
  zero failures; all12directed turns and four loaded loops. Representative native
  turn and loop frames inspected at source and station scales. Full source
  boards inspected for all active cargo/water/turn drawings. Compatibility
  sources are inventoried and available for review, not newly visually approved.
  The changed test's ordinary-swimming branch also passes100current source
  matches,76turn holds and72captures/zero failures.
- Real rotation-zero expedition regression runs separately against actual
  dispatch, airlock, pickup, loaded return, drain, unload, delivery credit and
  loaded/draining checkpoint restores. Its report/log are in the evidence folder.
  Final result: one completed journey/zero failures, all12phases, six pickup
  holds, five drain holds, four unload holds and two actual loaded return turns.
- All Godot runs use isolated scratchAPPDATA. Owner before/after fingerprints
  are recorded with the results; no pre-existing game process was stopped.
  All2,948owner non-log files remain byte-exact. All64source/chain WebPs and the
  native MP4 decode. `family-coverage.json` accounts for all228selected state keys
  across this review and earlier accepted passes; this is source-family coverage,
  not one combined native proof of every action or route.

Evidence: `output/marsh-remaining-2026-10-14/`. First stale-source log retained.
Native player captures are sampled, not continuous watched game motion. Source
review of shutdown/diagnostic clips is distinct from actual injury/death gameplay.
Earlier historical shutdown rebaker mismatch is unchanged and was not rerun.

## Next action

Owner reviews the remaining-animation gallery. No additional artwork replacement
is needed by the observed join/selection checks. No export, commit, upload or
automatic follow-up.
