# Placement experiments

Updated: October 20, 2026 · Project: BrineSpace · Task: discoverable placement experiments

## Objective and acceptance

Help players notice room-connection experiments without exposing hidden recipes.
Owner approved a subtle geometry-based cue, including replacement of the existing
hidden-recipe passage hint. The preceding sampled owner playthrough reached cycle
23 with supplies stabilized and no patterns learned; this motivated the change,
but was not a blind novice test or evidence of the player's intent.

## Accepted decisions and constraints

Different neighboring room types with matching doors receive the same experiment
wording whether or not a hidden recipe exists. Names come from visible neighbors.
When disconnected, rotation advice appears only if some blueprint rotation can
match the existing neighbor's door. Occupied targets and identical room types do
not receive this cue. No success rating or recipe-derived recommendations.

Cost, intake and build-access warnings precede the cue. Inspector guidance explains
that functioning connected rooms can reveal patterns, and not every connection
yields one. Discovered recipe previews remain explicit. Discovery, operation,
stabilization, costs, artwork and animation rules are unchanged.

## Current state

- `scripts/main.gd`: generic experiment cue and inspector explanation; passage
  detection in preview is gated on prior discovery, including its suppression of
  overlapping known pair previews. Floating feedback refits its height when a
  long warning becomes a short cue.
- `tests/test_placement_experiments.gd` and paired UID: geometry, rotation,
  hidden/non-recipe equivalence, known passage and read-only regression checks.
- `tests/test_placement_experiments_native.gd` and paired UID: actual preview,
  warning ordering, bounds and shrinking checks at 1600x900 and 1280x720.
- `tests/index.json`: focused subsystem and explicit native lane.
- `docs/CURRENT_STATUS.md`: current acceptance and remaining human test.

Source only; no export, signed package replacement or publication.

## Verification

59 focused headless checks pass. Existing construction-preview (21 checks) and
synergy-manager tests pass. Native fixture also reruns construction controls.
Four native captures reviewed across normal/compact sizes: connected cue and
long construction warning; all text remains inside the station region, warnings
come first, and the short panel shrinks after the long one.

Evidence: `D:/bs-placement-experiments-20261020` (logs, before/after protection,
source baseline). Final captures: `output/placement-experiments-20261020`.
Runner creates isolated APPDATA profiles. All 2,971 owner files hash-equal and
signed ZIP stat unchanged. Initial fixture attempts corrected a Dictionary API
mistake and workshop door orientation; these were test setup errors, not gameplay
rule changes. Native lane override was added after auto-classification skipped it.

## Next action

Play a fresh opening with these source changes and ask whether the cue causes a
deliberate placement experiment without suggesting guaranteed success. Human
discoverability/fun and packaged behavior are not yet validated. The existing
frozen release does not contain this change.
