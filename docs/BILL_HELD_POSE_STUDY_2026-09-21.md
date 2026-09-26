# Bill held-pose study

Updated: 2026-09-21. Review candidate only; broad animation/room/release goal remains open.

## Objective and constraints

Repair Bill's awkward walk while retaining his identity and independently authored
east/west artwork. No Higgsfield, new generation, owner-room changes or live asset
replacement in this study. Preserve the stride and six original key poses.

## Finding and current state

The installed side walk holds six poses for 170/130/150/170/130/150 ms of a
900 ms animation cycle. These are animation-phase durations, not fixed wall-clock
holds: playback follows traveled distance. During the longest hold, the root moves
17.3778 source-pixel equivalents while every sprite pixel stays fixed relative to
the root. Earlier boundary-anchor and phase checks cannot rule out this motion.
Source-to-cell scale is .17/148; do not call 384-room-local units station world units.

Staged 18-pose bare/helmet east/west candidate: 72 PNGs, including 24 pixel-identical
installed key poses and 48 inbetweens. Independent retained limb surfaces and boots
are fitted to interpolated hip/ankle targets with knee IK. Upper bodies remain held
at the original keys. Integer subdurations preserve each original pose boundary,
the 900 ms total and the existing stride. No production files changed.

All scripts, source hashes, samples, manifests, comparison GIF and leg contact sheet:
`output/bill-foot-hold-2026-09-21/`. Run `candidate.py`, `probe.gd -- --candidate`,
then `check_candidate.py` to reproduce the candidate check. `probe.gd` without
the candidate flag plus `analyze.py` reproduces the installed comparison.

## Verification and limits

- Installed CrewSpritePlayer, headless Godot 4.7.2: 3,604 controlled samples each
  for baseline and candidate; all six/eighteen expected frames observed per state.
- Candidate maximum sampled hold travel is below 5.83 source pixels in all four
  states. This measures within-pose motion only, not total anatomical stance drift.
- All 24 original key poses compare pixel-identically; retained limb SHA guards pass.
- The complete bare east/west leg sheet was visually inspected. Motion, hip seams,
  knee contour changes at original keys, helmet rendering and station-scale quality
  still require native visual review. The generated GIF is a diagnostic reconstruction,
  not a station capture or visual acceptance. No claim of a finished gait repair.

## Next action

Superseded by owner feedback: feet look weird and disjointed. The 18-pose candidate
is set aside, not queued for installation. A six-pose east/west comparison against
Bill before the local rig and installed Veld/Branforth shows rougher ankle joins and
tangled crossing silhouettes in installed Bill. The other characters also have local
rig processing; do not claim this is categorically absent from their pipeline.
Bill's surface repair replaces rows119:153, then restores old rectangular foot bounds;
this can reintroduce surrounding old limb pixels and deserves isolation. This code
observation is a hypothesis about mechanism, not a completed root-cause test.

Comparison source/script: output/bill-joint-review-2026-09-21/compare.py and
comparison.png. Restore coherent connected leg/boot shapes from preserved Bill poses
as the next candidate baseline, then assess gait and stance. Do not optimize density
or preserve visually defective key poses as a requirement. Live art remains unchanged.
