# Project handoff

Updated: October 14, 2026 · Project: Brine Space · Task: East run jumpiness

## Objective and acceptance

Owner accepted the locomotion transition improvements but found the east run jumpy.
Retain those fixes and accepted swimming; identify and repair the specific east-run
problem, then show matched playback for owner review.

## Accepted decisions and constraints

Keep the six selected run drawings,6x100ms timing,.11027027027027027cell stride,
184canvas,pivot92/172,H148 and existing controller/root curves. A whole airborne
pose may be registered without repainting, resizing or moving planted-foot poses.
No new release export or owner visual acceptance of this correction is claimed.

## Current state

Selected pose2's head center was112.5px, versus99.5px on each neighboring pose
and103px on the opposite airborne pose5. This creates a13px forward/back source
lurch. The complete pose2 now translates10pixels left on the same canvas, making
its head center102.5px. Maximum adjacent source excursion falls13->6.5px; airborne
half-cycle difference9.5->0.5px. Vertical pixels and all foreground RGBA values are
preserved exactly; no foreground clipping. Other five drawings, including all
planted poses, stay exact. This fixes a registration outlier, not all possible
six-pose cadence or physical foot-lock limitations.

`character/marsh-east-run-smooth-v1/manifest.json` is the final catalog override;
one packaged PNG changes. `tools/register_marsh_east_run.py --install` rebuilds
locally; maintained rebuilder invokes it last. Baseline refresh changes exactly
Marsh run-east slot2 and its derived alpha extent, no other actor/state/metadata.
New registration regression/UID is in the crew group. Existing east-run production
test's expected slot2 path is refreshed; scratch guard and unique evidence directory
protect owner data and historical captures. No production controller code change.

[Current before/after review](../character/marsh-east-run-smooth-v1/review/index.html)
contains the exact source loop and paired60fps native route. The prior locomotion
gallery links here and retains its earlier footage. Both sides of this comparison
use the same60Hz simulation sampling; improved preview cadence is not presented as
a runtime change.

## Verification

- Source regression reproduces13px lurch/two failures before; after centers
  [104,99.5,102.5,99.5,106,103], maximum6.5px, zero failures.
- Normal east route before/after:1,520checks each/zero failures;216matched samples
  have exact keys/slots, physical feet, canvas positions, player phases, pause and
  run classification. Only12samples selecting pose2 change source pixels.
- Actual normal production test:226checks/zero, eight full disk checkpoints and
  eight fresh title-screen Continues,16captures. Existing pause/source/root/phase
  assertions pass. Functional evidence; all16production windows are not claimed
  independently visually reviewed here.
- Previous nine locomotion boundary checks still pass. Crew complete packs and
  walking regressions pass. All foreground RGBA pixels retained; rebuild exact.
- Native airborne pairs and source before/after inspected; video decodes216frames
  at60fps. All2,948non-log owner fingerprints unchanged under scratch APPDATA.
  Task Godot processes terminal; owner's pre-existing app left running.

Evidence: `output/marsh-east-run-smooth-2026-10-14/`. Production runner:
`output/test-runs/20261014-210948-native`; crew regressions:
`output/test-runs/20261014-211148-headless`; registration/boundaries:
`output/test-runs/20261014-210848-headless`.

Three exploratory generated sheets/drawings and exact prompts are retained in
`sources/`, all unselected: repeated/nonmatching limb phases did not justify new
art admission. Later measured head registration isolated the smaller repair.
The first head-mask probe included disconnected brown suit pixels; its receipt
is retained. Final connected-component face/hair measurement agrees with the
independent source analysis. No threshold or runtime validator was relaxed.

## Next action

Owner accepted the correction: “That looks better, keep going.” The registered
six-pose cycle remains selected. Cargo/work polish proceeds under that instruction;
see `MARSH_WORK_POLISH_2026-10-14.md`. No release rebuild, commit or upload.
