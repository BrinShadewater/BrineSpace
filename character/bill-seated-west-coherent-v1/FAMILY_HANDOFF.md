# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill west sitting/rising

## Objective and acceptance
Complete the full master-consistent Bill animation set, followed by full-set
consistency/polish. This milestone stages independent west sit/rise artwork in
both gear states. Owner acceptance and selected-runtime use remain separate.

## Accepted decisions and constraints
Keep the west master identity, close brown hair/beard, readable face, matte quilted
charcoal suit, muted burgundy patch, hardware/backpack and anatomical shoulders.
Use independent west source art, not mirrored east frames. Shared256px plane,
pivot128,224/standingHeight148, selected sole223; never normalize each pose height.
Existing north lounge seats and south reading sofa retain their authored facing.
No live east/west seated consumer was found in crew_room_activity.gd; room
rotation alone does not prove rotated furniture. Do not invent activity changes.

## Current state
Four gear states/24refs: sit-down-west and exactly reversed sit-rise-west,
six poses per800ms finite transition. Exact selected standing frame at entry.
Five authored source poses show knee bend/hip lowering and upright seated rest.
Raw source/prompt retained: generation exec-c51243ea-d2e4-4815-b545-afd67a643d71.
build.py uses fixed ruler .27/(148/456), anatomical head axes and post-resize
opaque front-boot registration. grade.py pools source material transforms against
the selected west idle, with west-facing face/shoulder regions. Native selected
west helmet is fitted at unchanged scale; body below headAxisY+31 is protected.
Helmet sibling: character/bill-seated-helmet-west-coherent-v1. No runtime changed.

## Verification
48 package checks and181 native checks PASS10.24sec. Exact currently loaded
standing entry in both gear states, source/frame bindings, shared plane, contained
sole223, protected body, actual Bill life-stage elapsed selection,800ms holds,
paused playback and intermediate life snapshots pass. Full-size bare/helmet
and fresh native82px paired transition boards reviewed. All2,914 real non-log
profile files unchanged under scratch APPDATA. Raster paths retain Git LFS.
Candidate injection proves player/stage compatibility, not normal family selection,
actual furniture contact, autonomous activity choice or disk checkpoint restore.

## Next action
Author west seated breathing/reading and tablet take-out/put-away with exact
seated endpoint joins; consolidate/select the six-state family. Continue remaining
life/rest coverage, actual consumers and full-set material/proportion/pacing polish.
Full Bill goal remains active. Current source lowering deserves animation review
alongside the other directions before final polish acceptance.
