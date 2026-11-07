# Physical iPad playtest — October 19, 2026

Owner requested hands-off testing. Tested installed Validation2 `brinespace-0e63ab6e9c2e7500` on iPad13,18/A14/4GB/iPadOS27.2. No game source/build changes or public/frozen release changes. Mixed UI/load/background checks lasted about15minutes; disposable active run reachedcycle12 with2completed rooms and1pendingorder. This is bounded functional/performance evidence, not hours-long or large-station clearance.

Passed: card return clears selection; Rotate button changes Solar Array to rotation2, cost4paid, construction finishes andpowerproduction observed; crew moves/resourcecycles advance; dialogueClose works andplacementbuttons hide while dialogue visible; Home/activate returns paused/intact; Codex scroll through contentedge swipe, Next paging andClose; Save/Continue preserves cycle12 resources/cards/rooms/draw/discard/rerolls/corruption/timer andonependingMiningDroneBay. Native probe reads only copied saves with isolated profile/owner-save guards. White time skins were not observed at captured checkpoints; intermittency not ruled out.

Active report: zero game errors/automaticreports; lastSave119951usec; largest retained frame218.418ms nearplacement. This report retains only its available history, not every frame in the entire run. Initial loading multi-second toast stillobserved, so not a general stall fix.812valid1Hznative samples across869seconds, including UI/background/helper interruptions: footprintpeak1827655152B/last1608764864B. Smaller disposable station contributes to lower ending footprint; no causal RAM-saving claim.

## Automation gaps and failures

Initial Home command killed the helper because app.frame becameinfinite whilebackgrounded and JSON serialization rejected it. Reproduced log retained; helper now skipsbackground framequery andsanitizesnonfinitevalues. Build andHome/activate rerun pass. This local test-helper fix is outside game source. Experimental whole-app twoFingerTap failed XCTest endpoint discovery in Godot andwasremoved; whole-app pinch acknowledgments didnotestablish zoomchange. No new physical acceptance forpinch/pan/twofingerrotation; existingfixtures/owneracceptance are historicalevidence only. Lock/unlock unavailable throughhelper; Home/backgroundtested instead.

First Codex drag overcardbody didnotestablishouter-scrollmovement; contentedge swipe visiblyreachednextrow, pagingalsopassed. Second placement intendedHydroponics savedpendingMiningDroneBay instead; coordinate/selectiontargeting duringdialogue/layout/handreorderisambiguous. Correct secondblueprintplacementunaccepted; do not labelthisa proven gamebug withoutreproduction. Two completedrooms only; pendingorderrestorecheckedexplicitly.

## Owner restoration

Allfive originalcore save/checkpoint files copiedback andhashverified beforelaunch. Fullgameplaystate andtimer match original afterContinue/Save: cycle64/sevenrooms/speedindex2/timer1.11834893097652. Only _path/event_history/saved_at differ. FinalPID5993alive, paused/menuclosed/originalselectedConstructionDroneBay. Originalbackup and disposabletestcopies remainoutsideGit.

Current two-hour helperPID64358 active11m06s atfinalcheck andleft running. Recheck session-state.json before reuse; do not restart routinely. No new ownerauthorization was needed inthispass. Details: [summary](ipad-memory-placement-evidence-2026-10-19/extended-playtest/SUMMARY.json). Full local logs/screenshots/savecopies: `/Users/Shared/BrineSpace-ipad-optimization-20261018/extended-physical-playtest`; helperinstructions `/Users/Shared/BrineSpace-ipad-touch-control/SESSION_NOTES.md`. Initialloading, widerplacement/gestureautomation, long-session/larger-station memory and iPadreleasegates remainopen.
