# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Bill cardinal meal integration

## Objective and acceptance
Finish full master-consistent Bill animation set, then cross-animation consistency/polish.

## Accepted decisions and constraints
Preserve masters and original6s eat/3s drink, economy, helmet inspection, other crew and owner save.

## Current state
New character/bill-meal-family-v1 manifest/build/preview/review/evidence, scripts/bill_meal.gd with UID, Bill snapshots/cancellation, CrewLife pose/elapsed and normal grid selection/texture hook, ACTIVE_ASSETS, native fixture with UID and scratch runner.

## Verification
Bill cardinal meal family and saved service phases selected — October 1, 2026.
Normal Bill loader replaces east-only meal selection with24 bare cardinal meal
states/168 whole literal references to112 unchanged authored PNGs. Existing
masters/material/detail/density remain source authorities,256px/p128,224/H148.
New scripts/bill_meal.gd selects580ms draw/stow and960ms loop from existing
saved six-second life_eat and three-second life_drink timers. Cosmetic visual
time does not drive phase selection. Bill/MajorBill only, alive/dry/bare only;
helmeted meals retain existing inspection and other actors are excluded.
Normal CrewLife pose/elapsed and Bill grid texture dispatch use the helper.
First60ms of normal stow retains the actual preceding loop pose. Power-service
cancellation reverses a partial draw, preserves a loop pose or remaining stow,
then returns to idle. New meal_return pose[-1,6]/kind eat or drink fields are
snapshotted/restored with strict active/dry/bare/idle/no-route/no-goal/.58s
validation. Missing fields default for older snapshots. Interrupted return
finishes before choosing a new goal; no completed-meal hunger reward.
1659 actual-native checks pass: normal exact pixels/clocks/density for24states,
real galley chooser/contact samples on all4rotations/two actual contacts,
controlled power cancellation at10 points ×4facings ×2activities, source-pose
retention, valid actor snapshots and exact actor disk restore, cancellation
no-reward, original6s→3s completion and one original hunger reward, sealed
helmet inspection. Direction overrides in cancellation tests are source/clock
proof at one real contact, not physical furniture proof in four directions.
12 normal actual north galley captures and native screenshot crops reviewed.
Fine wrist/bowl/cup/worktop contact and overall source/master motion/material
polish still need review. No new geometry/economy/timer durations or crew meals.
Actor disk restore is NOT fresh-scene Continue or complete RunSave proof.
First1659-check run failed14 drink snapshot checks because the fixture reused
the post-cancellation actor after it chose a new route. Reset each activity
section at its real station; initial failed interval preserved. Production
behavior was not changed to make that fixture pass.
Corrected native 40.38s, engine0/clean/fresh capture under
scratch APPDATA. Full owner-profile guard FAILED: ['last_session.json'],
2,931 non-log files. Attribution unproven; retained
failed guard, no owner restore or retry for a clean interval. Current selected
rest/bunk/inspection work and concurrent James/Veld/settings edits preserved.
Next fresh-scene meal Continue/remaining interruptions and full-set identity,
anatomical proportions, perspective, materials and cadence polish. Full Bill
goal remains active, no commit/export.
Lesson: reusable activity fixtures must reset the actor after cancellation
before testing another service. Save the retained object action and loop pose,
not just elapsed time, so returning a bowl cannot resume as returning a cup.
Use existing service clocks for cosmetic transitions and retain final loop
pose before authored stow; source closure alone cannot prove arbitrary joins.

## Next action
Fresh-scene Continue at draw/loop/stow/interrupted return, broader real interruption contexts and full-set polish.
