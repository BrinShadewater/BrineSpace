# Character animation expansion

Updated: September 9, 2026 · BrineSpace · companion and Marsh animation coverage

## Objective and acceptance

Implement the owner's request for all proposed additions: Marsh's dedicated sitting, reading, resting, pickup/carry and distinct swimming/treading; directional Margot sit/groom/nap plus stretch/yawn; River and Josh start/stop/turn transitions; River startup and Josh standby.

## Accepted decisions and constraints

Preserve Margot's frog bonnet, River's compact olive/ivory body and Josh's muted bluish lavender upper body with charcoal treads. Josh still assists paid crew repairs with his blowtorch. Animation phases use simulation time and survive checkpoints. Existing assets remain available. Source checkout updated; executable not rebuilt.

## Current state

- `character/animation-expansion-v5/`: seven installed packs, source sheets/prompts, source hashes, build report, contact sheet and [animated review](../character/animation-expansion-v5/review.html). 339 clips / 1,440 frame references across the complete packs, including retained states.
- `tools/build_animation_expansion.py`: deterministic key extraction, anatomical registration, binary alpha, shared 64-color palettes and 92px frames. Quarter turns also support reverse rotation and composed half turns. No synthetic painted in-betweens.
- `scripts/companion_motion.gd` and companion runtime: simulation-time transitions, acceleration/braking, checkpoint state, directional cat actions, startup after River spawns and Josh's ambient standby/reawaken sequence. New script UID paired.
- `scripts/grid_canvas.gd`, `scripts/marsh_npc.gd`: Marsh v5 pack and conservative clearance union installed. No route-clearance reduction.
- `tests/test_animation_expansion.gd` and native sprite review expanded; UID paired.

## Verification

- Build passes frame bounds, binary alpha, palette and timing checks for every exported frame.
- `output/animation-expansion/coverage-final.log`: PASS, four-direction action coverage, distinct Marsh actions, paused/restored poses, directional nap-to-pet wake, movement acceleration, turn/brake selection and motion checkpoints.
- `output/animation-expansion/repair.log`: PASS, paid-job torch behavior and 25% assist gating.
- `output/animation-expansion/personality.log`: PASS, real-station rescue, routing, action checkpoints, pause, pet/wake and paid torch interaction.
- Native sprite review PASS; final changed swim/tread/turn captures also PASS (`native-final.log`). Inspected source sheets, native carry/groom/swim/tread/turn captures and the contact sheet. GIF gallery available for owner motion review; browser autoplay was not reviewed through automation.
- PNGs remain covered by Git LFS attributes.

## Source corrections and limits

The first Marsh water sheet overlapped cell boundaries; a spaced replacement is used. Explicit gutters preserve its two-pixel row gap. Incorrectly facing side-tread cells are reassigned, one wrong rest intermediate is omitted, and Margot's incorrect grooming exit endpoints use the matching authored sit-sheet standing pose. Her nap sheet's east/west rows are mapped to their actual facings. Josh's original standby sheet had a gray background; an image edit produced the keyed replacement. Both rejected sources remain for provenance.

Reverse transitions reuse authored poses. Some older Marsh states outside this request still reuse legacy art (including underwater cargo and helmet variants). This pass does not claim to replace every legacy animation.

## Next action

Owner visual review of the installed animations. No required implementation work remains for this requested batch; executable packaging is a separate step if desired.
