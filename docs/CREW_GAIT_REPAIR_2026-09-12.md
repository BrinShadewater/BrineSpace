# Project handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: three-crew gait repair

## Objective and acceptance

Complete the Veld, Branforth and Marsh animation/state replacement following Bill,
including convincing motion. The source replacements and fitted human locker clips
are selected; complete motion acceptance remains open.

## Accepted decisions and constraints

Preserve character identity, painted material detail, limb lengths and gameplay
movement speeds. Review stance/swing alternation, frame joins, planted feet and
equipment alignment. Distinct PNGs and complete manifests do not prove a stride.
Bill remains unchanged. No export requested.

## Current state

`tools/review_human_crew_art.py --filmstrips` now shows every selected pose at its
native dimensions, allowing padded transition canvases without clipping. Portable
walk/run reviews and filmstrips are under each actor's `focused` output folder.

Visual review found repeated same-leading-leg side walks for Veld and Branforth,
and very little meaningful stance change in Marsh's east walk. Veld's north walk
does show alternation. `tools/inventory_crew_gaits.py` inventories all 16 walk/run
clips and proved all four original Marsh run directions reused their walk pixels. These are
remaining animation defects, not reasons to undo the detailed source replacement.

`character/crew-gait-v2/sources` preserves three Veld generated edits and exact
prompts. None is selected: the direct edit repeated the near leg forward, the
first seam edit changed the poses, and the second retained more pose structure
but simplified painted identity/material detail. A hybrid lower-leg study remains
unselected. Its `guideChecks` describe the rig, not proof about generated pixels.
The second seam edit's input strip is frozen beside the sources.

`tools/repair_crew_walk.py` creates a local Veld east study from independently
reconstructed original frame 2. It reuses Bill's rigid source-part and knee helpers
with character-specific masks, source knee caps and separate near/far stance and
swing phases. Review is in `character/crew-gait-v2/review/veld-east-local-01`:
source donor, all frames, contact sheet, rig/joint provenance and portable moving
`motion.html`. This local source-pixel version is now selected for Veld's east
and west walks, plus Branforth east/west and all four Marsh walk/run directions. Fitted equipment is rebuilt from the same
poses with matching per-direction stride overrides. The independent donor path
explicitly disables repair so the installed frames never feed their own rebuild.
`RIGS` stores per-character recipes and `SELECTED_GAITS` explicitly lists promoted
clips; authoring another recipe does not automatically activate it.

## Verification

Candidate stance ankle drift is 0 source pixels for both legs; stance sole error
is 0 pixels. Proposed stride is 76 source pixels per cycle, converted to world
cells in `rig.json`; it must be installed in both playback paths if accepted.
`tests/playtest_crew_walk.gd` (with UID and native lane) passed 60 distance-driven
comparisons of the renderer-selected body against independently rebuilt pixels.
It also renders body at source/station scales and fitted equipment. Native
contact/opposite phases were inspected under
`output/crew-replacement-2026-09-12/veld/walk-native`. The selected alternating
step is an improvement over the old repeated-leg cycle at station scale.

Veld's complete pack validator reports zero errors/border touches; all 670 original
frames/108 manifests remain unchanged. Locker endpoint/reverse checks pass. The
actual selected three-crew pack test passes at
`output/test-runs/20260912-101802-headless`.

Latest milestone: Veld west and Branforth east each passed 60 native selected-frame
comparisons and source/station-scale visual checks. Native renders/logs are under
each actor's `walk-native/<direction>` directory and `walk-<direction>-native.log`.
The shared native fixture now takes actor/direction and reads cadence from the
independent rig record. Both human pack validators and locker joins/reversal pass;
the final selected-pack check passes at `output/test-runs/20260912-102802-headless`.
Branforth's 669 original frames and 108 manifests remain unchanged.

## Next action

September 12 follow-up: Branforth west and Marsh east walk/run each passed 60
native distance-selected comparisons. Native source/station-scale captures were
inspected. Marsh's run uses 96 source pixels per cycle versus 72 for walk, with
two airborne phases. All 211 original Marsh source frames reproduce unchanged;
its selected pack retains 140 states/676 references and no equipment. Complete
selected-pack checks pass at `output/test-runs/20260912-104357-headless`.

Changed tools: `repair_crew_walk.py`, both crew rebuilders, and the native gait
fixture. Registry keys now identify actor and full clip; explicit state overrides
prevent frozen source aliases from routing a repaired run back to walk. Human
locker endpoint replacement excludes Marsh's vestigial body aliases. The native
fixture fails promptly if a selected stride is missing.

Marsh west follow-up: dedicated west-source limb masks now drive separate walk
and run clips. Each passed 60 native distance comparisons; the source filmstrips
and native station-scale run capture were inspected. Pack validation reports no
errors or border touches, and all 211 original source frames remain unchanged.
Selected-pack checks pass at `output/test-runs/20260912-104656-headless`.
The current gait inventory reports only `marsh/run-north` and `marsh/run-south`
as walk aliases. Original front/back filmstrips are captured at
`output/crew-replacement-2026-09-12/marsh/vertical-donors.png`; uneven leg ordering
requires dedicated front/back work rather than mirroring the side rig.

Review page generation now describes native validation as separate evidence;
selection alone must not label a newly generated preview as tested.

Marsh front/back follow-up: all four north/south walk/run revisions are selected.
They retain each view's original torso and costume sides, varying projected leg
lengths and body height. This is image-space foreshortening, not side-view IK:
`projectedSoleErrorPx` checks registration only and does not prove world planting.
The native fixture now advances actual vertical positions for north/south.
Each changed clip passed 60 selected distance-frame comparisons, source/station
captures were inspected, and the gait inventory now reports zero run/walk aliases.
Pack checks pass at `output/test-runs/20260912-105035-headless`; Marsh retains
140 body states/676 references, zero equipment, and 211 unchanged original frames.
Full motion polish and owner acceptance remain distinct from those checks.

Changed files this milestone: `tools/repair_crew_walk.py`,
`tests/playtest_crew_walk.gd`, Marsh revision frames/manifests, gait review outputs,
the visual bible, current status and maintained/installed source-density reference.

Continue the
remaining action/transition reviews and retain the airlock integration limitations
in [the fitted helmet handoff](CREW_FITTED_HELMETS_2026-09-12.md).
