# Project handoff

Updated: 2026-10-03 · Project: BrineSpace · Task: Krusher seated actions

## Objective and acceptance
Continue the full Krusher character animation goal. This milestone provides sit-down, sit-idle, sit-rise and seated read enter/loop/exit in four directions, paired bare/helmet. Full goal remains active/incomplete.

## Accepted decisions and constraints
Krusher Dom, System Administrator, AI & Robotics, matte muted cyan #527C80, James utility suit. Preserve selected source motion, seat/foot registration and original action metadata. Candidate only; no normal runtime/roster/save changes.

## Current state
48states/288references/104unique outputs; original184x192canvas, foot92/172, standing148. Bodies, seated poses and tablet motion from frozen James seated-family-v1 and seated-read-phases-v1. Exact padded canonical standing endpoints,40exact shared-source joins;8read-loop-to-exit joins retain original subtle source pose variation and are not byte-equal. Original flags/timing preserved. Per-pose head tracking handles shifted seated torso instead of assuming standing center. Markings follow actual shoulder location; collar, helmet shell, visor cool highlights and hands/tablet protected. Independent helmet body marking masks handle differing source shoulder pixels.

Changed files: tracking/build/validation scripts, paired manifests/PNG/masks, source/head/output hashes; native/review.gd+UID and scratch-safe runner;144native screenshots, four paired all-pose chronology boards,30.64s MP4 and mobile HTML. Preview keeps2x pixel geometry without squashing192px height.

## Verification
156composition/1024independent/1990native checks pass. Native checks every288pose hold, equipment admission, original pivot/height/cycle,16ordinary seated/reading loops and finite endpoint selection. Engine0/12.0s, no logged errors; scratch APPDATA/all2930owner files unchanged. Source hashes, exact metadata, protected body/helmet alpha/lower limbs and hand/tablet foreground checked. Reviewed all288poses on four paired chronology boards, plus native East reading at148/74 equivalent scale. Video replays original poses/holds; physical chair contact in the live station and arbitrary read-loop exit phase transitions still need full-library world review.

## Next action
Full coverage now162bare/72helmet states;176missing per gear. Continue remaining rest/lying/sleep, cargo, recovery/emergency and water families. Preserve frozen source inventory; do not declare complete from staged coverage. No blocker or live job.
