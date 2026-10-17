from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
head=json.loads((R/'output/bill-carry-cardinal-snapshot-v3/validation.json').read_text());resume=json.loads((R/'output/bill-carry-cardinal-continue-v3/validation.json').read_text());priority=json.loads((R/'output/bill-carry-cardinal-priority-v3/validation.json').read_text());assert head['passed'] and resume['passed'] and priority['passed']
old=json.loads((R/'character/bill-carry-cardinal-runtime-v1/input-hashes.json').read_text());old.update(json.loads((R/'character/bill-carry-cardinal-runtime-v2/validation.json').read_text())['sourceHashes']);changes=[f for f,h in old.items() if hashlib.sha256((R/f).read_bytes()).hexdigest()!=h];assert not changes
e={'headless':head,'freshContinue':resume,'priority':priority,'reviewedBeforeAfterBoards':['bare-continue-review.png','helmet-continue-review.png'],'nativePairs':6,'reviewedSourceDependencyHashes':len(old),'reviewedSourceDependencyChanges':changes,'fireDispatch':'Six fire cases dispatched fire-retreat; all retained geometry paths empty. No completed refuge claim.','normalSelectionChanged':False,'goalComplete':False,'limits':['Candidate wrapper only; normal Title Continue unchanged','Natural snapshot source coverage West entry/settle and North rise, not every direction/stage','Hazard dispatch/source cancellation is not full hazard choreography or successful evacuation','Full Bill action/equipment set, contact cadence and final cross-family polish remain']}
(P/'review-assessment.json').write_text(json.dumps(e,indent=2)+'\n')
scripts=[P/'stow_player.gd',P/'stow_actor.gd',P/'checkpoint.gd',R/'tests/test_bill_carry_cardinal_snapshot_v3.gd',R/'tests/test_bill_carry_cardinal_continue_v3.gd',R/'tests/test_bill_carry_cardinal_priority_v3.gd'];(P/'input-hashes.json').write_text(json.dumps({f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in scripts},indent=2)+'\n')
lesson='''
## Bill cardinal carry checkpoint and priority handoffs — October 1, 2026

Staged `character/bill-carry-cardinal-runtime-v3` adds version-bound snapshots
for active first step, settling row plan and last actual submitted carry source
(key/index/gear/time). Loaded admission validates finite clocks, gear, available
rows and entry cache identity; reconstruct the full arrival plan from the loaded
source cache and compare before mutation. Actor snapshots retain planted turn
clock/deadline and arrival deadline. Explicit checkpoint wrapper binds physical
actor, artwork, global visual clock, equipment and original2s unload budget;
standard Title Continue remains unchanged. No art, grade, proportions, source
timing or normal loader change;162reviewed source/dependency hashes unchanged.

591headless checks0failures/5.33s cover both gears/all4directional entry and stow
snapshots, exact same-clock/future source agreement, cache/plan roundtrip and
atomic rejection of wrong binding/gear/index/plan or missing loaded source bank.
495native checks0failures/220.67s: actual scratch disk write/read and six fresh
main scene restores, natural West entry, West settling, North gradual rise,
both gears. Exact source/root/global clock, paused stability, needs/service
timer and30future60Hz updates match uninterrupted scene. Six before/after source
pairs equalRGBA; both12native/source presentation boards visually reviewed.
Candidate wrapper only; this is not normal Title Continue admission.

445native checks0failures/40.39s cover18controlled actual-main priority cases:
real fire field/refresh retreat dispatch, public helmet setter and mortality API
at entry/settle/rise in both gears. Each replaces old pixels and clears plans
through15subsequent ticks. New actor clears pending carry/pivot/cache on inactive,
dead, nondry or emergency goal. First fire-settle native room reviewed. All6fire
cases have empty refuge paths in retained geometry; cancellation/dispatch does
not prove completed evacuation. No geometry workaround or refuge invention.
All3intervals scratch APPDATA/all2931 owner non-log files unchanged.

Lesson: persist the last submitted source as loaded key/index/equipment/time,
not a texture object. Validate semantic plan construction and actor/global clock
agreement before restore; structural fields alone can admit a different visual
sequence. Fresh-scene disk restore must match future controller needs and timers,
not merely the first PNG. Exercise real priority APIs while the sequence is live.
Keep emergency dispatch, source replacement and successful refuge as separate
claims. Full goal active/incomplete. Next evaluate normal Bill-only admission
of latest source/player/actor behavior, with production checkpoint/priority gates;
other natural directions, North stance/contact, floor-case-to-idle and remaining
action/equipment/full cross-family polish still open.
'''
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+lesson)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+lesson)
status=R/'docs/CURRENT_STATUS.md';prior=status.read_text(encoding='utf-8');status.write_text(lesson.strip()+'\n\n'+prior,encoding='utf-8')
handoff='''# Project handoff

Updated: October 1, 2026 · Project: Brine Space · Task: Bill carry persistence

## Objective and acceptance
Full master-matching animation set then cross-family consistency/polish; open.
This milestone persists unified carrying/arrival and verifies priority handoffs.

## Accepted decisions and constraints
Latest reviewed masters/banks and unload2s budget; existing reversible work
authorized. No source grade/size or owner geometry/save change. Scratch APPDATA,
preserve other actor work. Standard normal loader/Title Continue unchanged.

## Current state
Runtime-v3 actor/player/checkpoint and UIDs, bound entry/stow/cache snapshots,
loaded-plan reconstruction and atomic rejection. New unit/fresh/native-priority
fixtures/runners. Six native before/after pairs,18priority records, source hashes,
review HTML/evidence retained. Pipeline/bible/maintained and installed skills updated.

## Verification
591unit0fail/5.33s;495fresh-main/disk0fail/220.67s;445priority0fail/40.39s.
Both gears, four-direction unit persistence, natural West entry/settle and North
rise fresh restores/30future ticks; real fire/gear/death APIs. Six source pairs
exactRGBA,12native/source presentations reviewed.162source/dependency hashes
unchanged;2931 owner files unchanged every interval. Fire paths empty, not refuge.

## Next action
Evaluate Bill-only normal admission and production checkpoint/priority coverage,
instead of leaving improved set indefinitely staged. Natural remaining directions,
North stride/contact, floor-case-to-idle and other actions/equipment remain.
No full-goal completion from these scoped tests.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');print('Recorded persistence/priority milestone and preserved full remaining scope')
