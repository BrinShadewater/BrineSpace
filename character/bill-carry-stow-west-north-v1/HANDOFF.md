# Project handoff

Updated: 2026-10-01 · Project: BrineSpace · Task: Bill West arrival settle/turn/stow

## Objective and acceptance
Continue the full master-matching set by connecting West carry arrival to the
actual workshop's North-facing unloading. Complete goal remains active.

## Accepted decisions and constraints
Reuse original master sources at148/(128,224), preserve grade/detail/identity.
Actual workshop destination remains North. Owner geometry/normal selected loader/
normal title Continue unchanged. Preview-only actor/player; no new raster artwork.

## Current state
character/bill-carry-stow-west-north-v1/stow_actor.gd (+UID) and stow_player.gd (+UID)
retain exact last submitted carry texture80ms, finish the remaining West gait,
reverse authored first-step interiors to exact held master, turn West/North, then
use original North unload. Native arrivals both gears occur fromgait1:27program
rows,1.69s settle/yaw prefix + original2-second unload (520ms source + final hold).
Only unload timer waits for prefix; normal controller/needs continue. Staged active
presentation/action elapsed routes the program through actual grid player rather
than bypassing it via normal frame_at_elapsed. Next unload tick does not restart.
First-step parent fixed: idle/pickup ordinary nonempty motion is not an active
turn; pending carry-facing change must complete its turn before arming first-step.

## Verification
46existing source joins/registration checks; all audited source hashes unchanged.
Final actual main/workshop/prescribed graph-clear West lane run4950checks0fail/
69.61s engine0:both gears/all6bridge/all6gait + all27arrival rows, fixed destination
foot, continuing hunger and original unloading timer.56native/source samples:
54planned rows verified exact sourceRGBA, plus2completion sources. Six boards and
full source/idle North ending audit reviewed; browser82/148 source-clock review.
Final unload/idle body heights148bare/154helmet and physicalsole223 match; 148/193
upper pixels still differ (breathing/detail), not an exact final-idle pixel claim.
Existing unload10-to11 crown rises22source pixels in35ms: abrupt rise remains a
motion polish issue. Floor case in old final art disappears at normal idle;
final case ownership/disposition is unresolved, no new gameplay prop invented.

Separate stow source guards83checks0/7.79s (partial first-step/contact, exact prior
source,2second unload, completion/no restart, gear/backwards/state cancellation).
Updated first-step guards71checks0/4.98s prove actual pickup->carry and pending
South/West turn ordering. All reported intervals scratch APPDATA/2931owner non-log
files unchanged. Three failed native intervals retained:75.67s exact process139832
stopped after absent-plan fixture error;51.48s admission failed because empty-clip
motion dictionary was mistaken for active animation;80.17s5144checks2fail exposed
first-step arming before turn. Final4950interval passes both repairs. No prelaunch
code freeze claim; endpoint source hashes retained and checked after final run.
GIF samples recorded source timestamps every20ms with500ms completion hold;
not continuous native footage, anatomical stance-lock or owner acceptance.

## Next action
Polish existing North unload rise with authored intermediate posture, actual foot
contact and floor-cargo semantics; add South/North matching gait/start sources.
Natural routes, short-leg/other arrival phases, actual service/hazard interruption,
medium/gear, paused/fresh-scene Continue and normal adoption remain required work.
No commit/export/publish; full Bill goal incomplete.

## Follow-up: North unload rise candidate — October 1, 2026
New bill-unload-north-rise-v1 stages14rows/640ms with two authored lower poses,
original2s controller hold/unchanged standing endpoint.6/8/6crown steps replace
old22px leap;123package/4968native checks pass. Old evidence above retains original
12-row scope. Wider build/contact/floor-case semantics unresolved. Added missing
paired stow_actor.gd.uid; script behavior unchanged.
