# Marsh west/south swimming turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Complete the last adjacent-direction swimming pair with consistent registration
and exact destination-loop joins. Technical integration passes. Owner visual
acceptance and ordinary station play review remain open.

## Accepted decisions and constraints

No Higgsfield. Built-in image generation authored independent west/south views.
Return motion reverses pose order, without mirroring. Existing rooms, gameplay,
equipment and release packages are preserved.

## Current state

- Frozen sheet and exact prompt: `character/marsh-swim-turns-v1/sources/west-south-01.*`.
- Pair-aware builder `tools/build_marsh_swim_turns.py` includes west/south; the
  canonical rebuild already consumes its pair list. Explicit measured shoulders
  register the poses at .23 scale without changing earlier recipes.
- Runtime: `character/marsh-v2/supplemental/swim-turn-west-south/`. Two clips,
  ten frames, 400 ms each (60/90/100/90/60), non-looping water poses. Canvas184x208,
  pivot92,172, standingHeight148. Endpoints preserve existing swim pixels exactly.
- Catalog and supplemental hash contract updated. Earlier runtime PNGs and
  clearance are unchanged. No export, commit or publication.
- Review GIF/contact: `character/marsh-swim-turns-v1/review/west-south-01/`.
  Preview endpoint holds are longer than runtime.

## Verification

- Reproduction checks all forty frames across four pairs, binary alpha, exact
  endpoints and reverse ordering; passes.
- Native player fixture: 120 rendered samples, both selected clips and exact
  frame-zero handoffs, zero failures. Agent inspected contact and native capture
  for registration/foreshortening; comprehensive subjective motion review remains open.
- Maintained turn handoff test: 44 actor/body/equipment cases, zero failures,
  including pause/restore and proper clock continuation.
- Complete pack: 19,939 checks, zero failures. Existing source-loading fixture
  warnings are not release-export evidence.
- Validator: 168 body states, 814 references, zero errors/border touches;
  211 original source frames and one source manifest unchanged.
- Evidence: `output/marsh-west-south-turns-2026-09-22/`. No repeated route run
  for the unchanged clearance bounds.

## Next action

Four opposite-facing swimming turns remain, followed by twelve carrying and
twelve swimming-with-cargo turns. All eight adjacent swimming turns are installed.
Review motion in normal station play, then prepare fresh stable builds and test
on Apple Silicon; these acceptance steps remain pending.
