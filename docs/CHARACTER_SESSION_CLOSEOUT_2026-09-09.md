# Character session closeout

Updated: September 9, 2026 · BrineSpace · portraits, companion animation and flooding

## Objective and acceptance

Apply the completed animation work, close the session, and capture lessons in the
skills, workflow, asset pipeline and visual bible. Source integration is complete.

## Accepted decisions and constraints

River is the compact olive/ivory utility droid; Josh is the larger muted bluish
lavender robot with charcoal treads; Margot is the white/tabby cat in her frog bonnet.
Companions are unlocked by rescue and selected before expeditions, separate from
architect berths. Josh's torch assists paid crew hull repairs. Margot swims from 20%
flooding, River floats from 25%, and Josh stops at 50% and resumes after drainage.

## Current state

- [Active asset registry](../character/ACTIVE_ASSETS.json): nine selected animation
  manifests, 355 clips / 1,488 frame references including retained states, plus eight
  portrait paths. All are present and bound to their current source-game consumers.
- Marsh has dedicated seated/rest/cargo and swim/tread poses. Margot has directional
  personality actions, stretch/yawn and swimming. River/Josh have movement transitions,
  startup/standby; River has flotation. Josh's repaired tread colors and torch remain.
- [Animation gallery](../character/animation-expansion-v5/review.html) and
  [water gallery](../character/companion-water-v1/review.html) are retained for review.
- [Pipeline guide](../character/ANIMATION_PIPELINE.md) and read-only
  `tools/audit_character_bindings.py` now provide repeatable closeout checks and hashes.
- Visual bible updated with selected portrait direction, companion identity,
  realistic material/lighting requirements and animation/flood rules. Older BRINE
  V13 / realism-v2 statements are explicitly superseded by the current inventory.
- Maintained character skill and installed mirror updated with a focused companion
  reference and inventory-aware handoff guidance. Existing generic skills unchanged.

## Verification

Closeout audit: nine packs and eight portraits, zero errors; report in
`output/character-closeout/bindings.json`. Relevant recent runtime evidence remains
`output/animation-expansion/coverage-final.log`, `native-final.log`, `personality.log`
and `output/companion-water/native-final.log`, `dry-regression.log`,
`repair-regression.log`: all PASS for their recorded scopes. Native flooded Margot,
River and shut-down Josh captures were visually inspected. No new raster changes
were needed for closeout, so those visual results remain applicable.

Skill structure and changed installed mirrors checked separately; this is a targeted
lesson update, not a new independent skill-effectiveness benchmark. Current gameplay
tests, source captures and manifest audits do not claim packaged executable acceptance.

## Remaining limits and next action

Requested work is applied and this session is closed. Older Marsh secondary/helmet
aliases remain intentionally identified as legacy coverage. Continuous owner motion
review remains available through the galleries. No executable was rebuilt, no commit
or push was made, and concurrent room work was preserved.
