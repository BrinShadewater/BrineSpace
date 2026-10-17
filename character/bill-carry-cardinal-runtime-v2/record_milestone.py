from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-cardinal-natural-v2'
v=json.loads((O/'validation.json').read_text());d=json.loads((O/'journeys.json').read_text());q=json.loads((P/'validation.json').read_text());h=json.loads((R/'output/bill-carry-cardinal-stow-v2/validation.json').read_text());assert v['passed'] and q['passed'] and h['passed']
assessment={'native':v,'guards':h,'independentSourceRootClock':q,'reviewedNativeBoards':['bare-natural-review.png','helmet-natural-review.png'],'nativeSourceViews':sum(len(j['captures']) for j in d['journeys']),'arrivalProgramRowsPerGear':26,'browserSizes':[82,148],'normalSelectionChanged':False,'goalComplete':False,'limits':['Not continuous native footage or anatomical support/contact proof','Natural physical arrival coverage West-to-North only; all directions headless','Snapshot/fresh Continue and priority interruption cases still open','Original idle/floor-case handoff and remaining full Bill actions incomplete']}
(P/'review-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
scripts=[P/'stow_player.gd',P/'stow_actor.gd',R/'tests/test_bill_carry_cardinal_stow_v2.gd',R/'tests/test_bill_carry_cardinal_natural_v2.gd'];(P/'input-hashes.json').write_text(json.dumps({f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in scripts},indent=2)+'\n')
lesson='''
## Bill unified cardinal arrival and gradual North rise — October 1, 2026

Staged `character/bill-carry-cardinal-runtime-v2` extends latest cardinal carry
player/actor, admits original reviewed `bill-unload-north-rise-v1` paired14rows,
and generalizes settling arrivals from all four directions. Cache the actual
last submitted bridge/gait texture with gear and time; reject cache older than
100ms or reversed clock. Arrival holds exact prior80ms, reverses a partial
entrance or finishes gait to contact0 then reverses bridge3..0, turns to North
where needed, and plays14-row unload/rise. Skip duplicated contact bridge4/5.
No new art, scaling, grade or master/pivot change; exact held/turn/unload joins
checked against original pixels. Original unloading budget2s retained after
settle/yaw prefix; inherited needs/service controller remains active. Snapshot
admission is still missing; normal loader/Title Continue unchanged.

873headless checks0failures/30.48s: both gears, all4arrival directions from
partial entrance and moving gait, every planned row/clock, exact prior source,
held/turn/unload joins, original2s budget, gradual rise14rows, final-source
stability, gear/clock/state cancellation and stale-cache rejection.

Final native natural workshop interval3832checks0failures/61.53s, unchanged
generated route [(7792,8416),(7760,8416)], actual East-West turn/West walk then
West-to-North arrival, both gears. Target root(7760,8416) stays planted after
arrival; needs progress. Each26-row arrival plan captured, including reused
walking textures. Settle/yaw1.27s plus2s unload; observed stage3.2833s at60Hz.
102native/source views (51per gear), both complete boards visually reviewed;
394recorded program sources independently equal bound latest PNGs, all14rise
rows observed. Independent798source/root/clock checks pass. Browser source-clock
arrival replay reviewed82/148, no continuous native-film claim.

Earlier native interval61.3s had2fixture failures: the planted-root check compared
the first arrived position against the previous moving frame. Preserve failed
logs/captures. Restrict the invariant to updates after actual arrival, preserving
the final production movement step. Corrected58.5s interval3774checks0 passed;
expanded per-program-row capture justified final rerun. All three native and
headless intervals scratch APPDATA; all2931 owner non-log files unchanged.

Lesson: an arrival must bind the actual last rendered texture and its equipment,
not an assumed gait slot. Review reused textures again at their stationary
arrival root; unique-source capture alone hides part of the settling choreography.
Separate the final approach step from the subsequent planted interval. Prefix
time must precede, rather than consume, the existing unloading stage; keep needs
and priority controller running. Full set remains incomplete. Next: cancellation
and actor/source/clock snapshot/fresh Continue coverage before normal adoption;
physical arrivals from other directions, North short-stride/stance review,
floor-case-to-idle disposition and full Bill action set remain.
'''
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+lesson)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+lesson)
status=R/'docs/CURRENT_STATUS.md';prior=status.read_text(encoding='utf-8');status.write_text(lesson.strip()+'\n\n'+prior,encoding='utf-8')
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Unified Bill arrival

## Objective and acceptance
Full master-matching Bill set, then cross-family polish; incomplete. This
milestone connects current carry arrival to settling, yaw and gradual North rise.

## Accepted decisions and constraints
Use latest directional masters/banks, exact prior source, paired equipment,
original unloading2s budget, scratch APPDATA. Existing reversible work authorized.
No new gameplay/room/inventory ownership, source grade or normal selection change.

## Current state
Staged runtime-v2 stow actor/player with UIDs extends unified-v1 banks, admits
North rise14rows, generic four-direction arrival plan and recent source cache.
New guard/native fixtures/runners,102native/source views, arrival replay,
independent verification/input hashes. Pipeline/bible/skills updated. Preserved
natural before-v1 evidence and first fixture-failure interval.

## Verification
873guards0fail/30.48s;3832native0fail/61.53s;798independent checks. Both gear
versions, all4arrivals headless, actual unchanged natural West-to-North arrival,
26program rows per gear fully captured/394recorded sources exact. Feet planted
after arrival; needs live;14rise rows and2s budget verified. Both boards reviewed,
browser82/148. Every interval owner2931 non-log files unchanged.

## Next action
Priority actor cancellation and source/actor/clock snapshot/fresh Continue
admission before normal selection. Other directions natural physical arrival,
North visible stride/stance and idle/floor-case handoff remain open. Complete
remaining Bill states/equipment coverage and full cross-family polish afterward.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');print('Recorded latest cardinal arrival evidence and remaining full-scope work')
