# Marsh east/north swimming turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue crew animation work.

## Objective and acceptance

Add the east-to-north swimming turn and its reverse, maintaining Marsh's bare
head, suit, current endpoint registration and destination-loop handoff.
Technical integration is complete; owner visual acceptance remains open.

## Accepted decisions and constraints

No Higgsfield. Built-in image generation produced two preserved source sheets;
local deterministic extraction produced the runtime sprites. No room, gameplay,
helmet, audio or release changes. Reverse direction reverses poses, not pixels.

## Current state

- `tools/build_marsh_swim_turns.py` selects the first two poses from source 01
  and the corrected rear pose from source 02. The original rear pose had excessively
  long projected legs. Both sheets and exact prompts live in
  `character/marsh-swim-turns-v1/sources/`.
- Two 400 ms clips, five frames each, now live in
  `character/marsh-v2/supplemental/swim-turn-east-north/`. Canvas 184x208,
  pivot 92,172, standing height 148; added height is transparent padding.
  Both endpoints preserve existing swim frame-zero pixels exactly.
- Canonical rebuild, catalog, supplemental hash contract and derived clearance
  include the new clips. Existing runtime PNGs did not change. North and east
  lower clearance extent is now 8.38054 world units; the route gate is rerun.
- Review contact sheet and GIF are in
  `character/marsh-swim-turns-v1/review/east-north-01/`. GIF holds endpoints longer
  for inspection. Runtime timings are 60/90/100/90/60 ms.

## Verification

- Python reproduction: ten frames, binary alpha, exact endpoints and reversal pass.
- Native player fixture: 120 rendered samples, both turns selected and both handoffs
  return to destination frame zero; zero failures. Captured pose inspected.
- Maintained handoff test: 38 actor/body/equipment cases, zero failures, including
  pause/restore. Extended assertions preserve distance clocks where configured and
  recognize Marsh's existing time-driven swim clock. No player code changed.
- Complete packs: 19,765 checks, zero failures. Fixture source-image-loading
  warnings remain; this is not packaged-export evidence.
- Validator: 162 body states / 784 frame references, no errors or border touches;
  211 original source frames and one source manifest unchanged.
- Native battery/route gate: PASS, 93 route samples with the enlarged clearance.
- Evidence: `output/marsh-swim-turns-2026-09-22/`. No new export produced.

## Next action

Continue the remaining ten directed swimming turns, then twelve carrying and
twelve swimming-with-cargo turns. Review these transitions in ordinary station
play as well as the controlled native player fixture. General crew/room polish
and Apple Silicon release testing remain unfinished.
