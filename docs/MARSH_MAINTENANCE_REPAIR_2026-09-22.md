# Marsh maintenance and transition handoff

Updated September 22, 2026. Project: Brine Space.

## Objective and acceptance

Make Marsh's equipment-check action readable and connected, and establish which
water/carry transitions are missing. Preserve android behavior, owner rooms and
existing source art. Native/controller checks are not owner visual acceptance.

## Accepted decisions and constraints

No Higgsfield or new image generation was used. No room, gameplay timer, navigation,
save, battery or helmet rule changed. No commit, publication or new export.

The shared controller's maintenance goal means checking equipment: one second of
preparation, four seconds checking and one second finishing. It uses the historical
state IDs kneel/repair/stand. Actual construction/hull welding is separate. Marsh
now draws a handheld diagnostic controller, checks it and stows it instead of
bowing and snapping upright with almost-idle hand motion. This deliberately reuses
his existing authored diagnostic art; it is not newly authored kneeling artwork.

## Current state

48 selected PNGs changed across all four facings: three preparation, six work and
three stow frames per facing. Frame counts, durations, manifests, pivots, clearance
and catalog remain byte-identical. Welding, interact, eating and other legacy
aliases are untouched. Exactly 48 of 732 runtime PNG/JSON files changed; 684 are
unchanged, none added.

`tools/marsh_repair_revision.py` obtains the existing diagnostic source poses via
`veld_scanner_revision.replacement`, uses frozen current idle endpoints under
`character/crew-repair-polish-v1/sources/marsh/`, and selects explicit maintenance
states only. `tools/rebuild_human_crew_art.py` calls this override in the shared
candidate writer. Work loops stay equipped and close exactly; stow reverses draw.
The three distinct work poses repeat intentionally. This pass does not repair any
remaining identity differences inside the previously selected diagnostic artwork.

Recipes and mobile-sized preview:
`character/crew-repair-polish-v1/review/marsh-diagnostic-repair-01/`.

## Verification

- `tests/test_marsh_repair_chain.py`: three tests pass, covering all 48 exact
  rebuilt frames, binary alpha, current idle and action joins, active-pose variety,
  and explicit exclusion of unrelated states/actors.
- Human crew validator: zero errors/border touches; all 152 body states and 734
  frame references present, no equipment; 211 original source frames and one
  original source manifest unchanged.
- Complete crew packs: 19,475 checks, zero failures. Existing raw-image fixture
  warnings are not release-export evidence.
- Native production-player review in four directions: 92 captures. The actual
  Marsh controller progresses preparation -> repair -> finish -> normal behavior
  at samples 0,31,152,183 (30Hz). Pause holds the timer; android remains helmetless.
  Final run exits zero, no engine errors. This controls a powered service fixture
  and manually steps one actor; it does not prove autonomous room selection/routes.
- Initial fixture lacked powered service and correctly interrupted into stand.
  Its failure evidence is retained separately; only the fixture was corrected.

Evidence: `output/marsh-repair-review-2026-09-22/` contains before/changed JSON,
controller traces, native captures, and validation/rebuild/pack logs.

## Remaining transition coverage

The production player was exercised for every requested transition: 12 dry carry
turns, 12 swim-carry turns, 12 swim turns and eight swim start/stop clips. All 44
are absent as authored clips; all 44 return valid ordinary movement/tread frames.
This avoids missing textures but still permits abrupt pose changes. The complete
requested-key and selected-fallback list is in `transitions.json` beside its log.
No transition art was installed or claimed complete in this pass.

## Next action

Author and review a representative swim start/stop pair first, using the selected
tread/swim endpoints, fixed body scale and actual distance-driven playback. Expand
to the other facings only after the representative motion works, then address
carry turns while preserving cargo contact. Current test exports predate this work.
