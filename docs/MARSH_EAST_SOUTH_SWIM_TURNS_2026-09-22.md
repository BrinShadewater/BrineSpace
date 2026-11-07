# Marsh east/south swimming turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Add east-to-south swimming and its reverse with connected, foreshortened poses
and exact joins into existing swim loops. Integrated and technically verified;
owner visual acceptance and ordinary station play review remain open.

## Accepted decisions and constraints

No Higgsfield. Built-in image generation authored three new poses. Reverse motion
reverses their order, without mirroring. Preserve existing art, rooms and gameplay.

## Current state

- Frozen source and exact prompt: `character/marsh-swim-turns-v1/sources/east-south-01.*`.
  Frozen south endpoint added beside existing endpoint references.
- `tools/build_marsh_swim_turns.py --pair east-south` reproduces ten frames in
  `character/marsh-v2/supplemental/swim-turn-east-south/`. Canonical rebuild uses
  the extended pair list. Catalog and supplemental hash contract include both clips.
- Each clip lasts 400 ms, five frames at 60/90/100/90/60 ms, non-looping. Canvas
  184x208, pivot 92,172, standing height 148, water-pose metadata. Existing endpoint
  pixels remain exact with transparent padding only.
- Source shoulder registration is explicit. Middle and near-front poses shift
  left five and ten pixels from the first trial to remove sideways head drift.
- Review contact and GIF: `character/marsh-swim-turns-v1/review/east-south-01/`.
  Preview endpoint holds are longer than runtime. No prior runtime PNG or clearance
  changed. No new export, commit or publication.

## Verification

- Reproduction test: all thirty frames across three pairs match runtime exactly;
  binary alpha, exact original endpoints and reverse ordering pass.
- Native player: 120 rendered samples, two successful destination-frame-zero
  handoffs, zero failures. Agent inspected the contact sheet and native near-front
  capture for registration and foreshortening. Full subjective motion approval
  remains with the owner.
- Turn handoff: 42 actor/body/equipment cases, zero failures, including save/restore.
- Complete pack: 19,881 checks, zero failures. Existing fixture source-loading
  warnings are not release-export evidence.
- Validator: 166 body states, 804 references, no errors/border touches;
  211 original source frames and one manifest unchanged.
- Evidence: `output/marsh-east-south-turns-2026-09-22/`. Clearance unchanged,
  so no additional battery-route run was necessary.

## Next action

West/south pair, then opposite-facing swimming turns. Six directed swimming turns
and twenty-four cargo turns remain. Ordinary station visual review, stable release
updates and Apple Silicon testing remain pending.
