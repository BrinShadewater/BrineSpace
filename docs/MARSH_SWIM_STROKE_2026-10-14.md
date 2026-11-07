# Project handoff

Updated: October 14, 2026 · Project: Brine Space · Task: Marsh swimming arm strokes

## Objective and acceptance

Owner found the arms held a glide instead of swimming. Repair all four unloaded
swim cycles, using other crew as motion guidance while retaining Marsh's identity.
This extends the earlier endpoint-only repair; that test pass did not establish
credible stroke choreography.

## Accepted decisions and constraints

Whole-body generated drawings, no local arm grafts or mirroring. Retain the exact
registered first pose in each direction, repaired turn handoffs, 720 ms cycle,
distance-driven stride, density declaration, pivot and water/depth meanings.
Silhouette changes in new articulated interiors are necessary for the requested
stroke; the prior endpoint repair's unchanged-silhouette scope is historical.
No gameplay, loaded cargo, treading, dry animation or release export change.

## Current state

`character/marsh-swim-stroke-v1/manifest.json` is the final Marsh catalog override.
Four loops now have six 120 ms holds: four preserved entry drawings plus twenty
new complete-body interiors. East/west use pull, bent-elbow recovery and extension;
north/south use a visible breaststroke sweep, tuck and forward recovery. Source
order/extraction/registration is explicit in `provenance.json`. First north draft
lengthened the body and is rejected; north02 retains the compact boot/torso view.

Five raw generated sheets, exact prompts and reference hashes are preserved in
`sources/`. Bill's selected six-pose swimming supplied motion guidance; Marsh's
directional identity masters and existing swim bodies supplied identity/camera.
The east source is explicitly reordered to follow the visible arm through its
stroke. One uniform density per direction and head registration preserve scale;
all new frames use a padded 208-square canvas, pivot (92,172), standing height148.
Largest-connected-body extraction removes neighboring cell fragments and faint
provider-alpha halos. No pose stretching or anatomical stamping.

`tools/build_marsh_swim_stroke.py --install` rebuilds locally without generation;
the maintained rebuilder runs it after the endpoint installer. That earlier
installer now excludes the later stroke override when resolving its own inputs.
The crew baseline is refreshed. Native review uses `test_marsh_swim_stroke.gd`
and paired UID, a small extension of the existing capture fixture, registered in
`tests/index.json`. The earlier review page links to this current revision.

[Current animated before/after gallery](../character/marsh-swim-stroke-v1/review/index.html).
Previews reconstruct authored holds and are not station-world footage.

## Verification

- Native installed source-clock review: 132 checks / zero failures, 16 complete
  chronology boards at 1x and 0.5x, including four six-pose loops and twelve turns.
  All 24 swim poses visually inspected in native chronology. Arm extension, pull,
  tuck/recovery and cyclic return are present; head registration is stable.
- Carry-turn handoff: all72 cases pass, including saved/paused restoration and
  destination/phase joins. Crew swim packs pass with zero failures.
- Crew complete packs and walk regressions pass. Full baseline comparison admits
  exactly four Marsh swim clips; all other actors/clips/equipment/strides match.
- All four first poses remain registered-pixel exact despite transparent padding.
  Each cycle has six distinct drawings and totals720ms. No opaque frame edges.
- Narrow rebuild byte-identical; all2,948 non-log owner-profile hashes exact under
  isolated APPDATA. No task Godot processes remain; the owner's existing app is left.

Evidence: `output/marsh-swim-stroke-2026-10-14/`, source scope receipt, before/after
owner fingerprints, native boards and runner logs. Native/handoff:
`output/test-runs/20261014-200041-{native,headless}`; crew regressions:
`output/test-runs/20261014-200226-headless`.
Browser automation rejected the local-file protocol; no bypass attempted. Native
chronology and lossless previews supply the review evidence, not continuously
watched browser playback or final owner acceptance. All media remain local.

## Next action

Owner reviewed the comparison and accepted the revised swimming strokes: "that looks better".
Requested strokes are installed in source. Natural station travel,
water occlusion and a rebuilt playable release remain separate verification scopes.
