from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/bill-meal-fresh-continue-v1';S=R/'output/bill-meal-continue-producer-v1'
assert not (P/'continue-evidence.json').exists(),'Record later revisions separately'
producer=json.loads((S/'validation.json').read_text());log=(S/'native.log').read_text();report=json.loads((O/'validation.json').read_text())
assert producer['returnCode']==0 and '104 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and producer['nativeScreenshot']
assert report['nativePassed'] and report['processes']==20 and report['checks']==400
for result in report['results']:
    log=(O/'cases'/result['id']/'native.log').read_text()
    assert result['returnCode']==0 and result['freshCapture'] and '20 checks,0 failures' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log
assert (P/'continued-contact-review.png').exists()
guard_changes=sorted({name for result in report['results'] for name in result['realProfileChanges']})
summary='''Bill meal fresh-scene Continue matrix — October 1, 2026.
Production RunSave checkpoint producer creates20 cases from two actual galley
contacts, two bare activities and five saved points: draw/use/natural stow,
partial-draw power cancellation and loop power cancellation.104 producer
native checks pass, all snapshots valid and readable with exact expected PNGs.
Each case copies only the producer scratch profile into its own scratch APPDATA
and launches an independent engine. Actual title Continue plus actual loading
transmission Continue restore the station through normal production code.
20 checks per case/400 total pass: live Bill/stage, exact saved timer, direction,
equipment, physical foot, retained object kind/loop pose, source image pixels,
unchanged hunger, valid full actor snapshot and paused pose stability.20 fresh
actual-world captures; native crops reviewed together by contact/action/phase.
This adds full-checkpoint fresh-process proof beyond prior actor-only disk
round trips. All cases use actual North galley directions; this is not East/
South/West furniture proof. Owner visual acceptance, resumed service/route,
wider hazard/gear interruptions, wrist/object/worktop fine contact and full-set
master anatomy/material/cadence/perspective consistency remain separate.
No production/art changes were needed for Continue; new fixtures with paired
UIDs, producer/fresh runners, review generator/HTML and evidence only.
Current source-only inventory records212 bare/189 helmet manifest-selected
keys. Original-catalog run clips and helmet torch draw/stow remain to inspect
against masters; accepted specialized bunk and inactive sealed-mouth meal
rows must not be labelled defective just for source age. Inventory is not
native reachability/visual fidelity proof. Dated source audit preserved at
character/bill-selected-source-audit-2026-10-01/source-inventory.json.
'''+f'''Producer {producer['seconds']}s; fresh20-process matrix {report['seconds']}s,
all engines0/clean/fresh captures. Overall passed={report['passed']}; strict
owner-profile guard changed {producer['realProfileChanges']} during producer,
fresh guard changes={guard_changes}; {producer['realProfileFileCount']:,} real
non-log files fingerprinted. Independent scratch profiles confirmed. Failed
guards retained, attribution unproven, no owner restore or clean-interval retry.
Next inspect helmet torch draw/stow, then remaining run/diagonal coverage,
full-set visual consistency/polish and resumed-context evidence.
Full Bill goal active; no commit/export.
Lesson: preserve per-case scratch profiles and use both visible Continue flows
to prove a restored presentation. Actor-only restore cannot establish complete
checkpoint behavior. Keep saved object kind and retained source pose distinct
from the live-loop timer, particularly after a service cancellation.
'''
handoff='# Project handoff\n\nUpdated: October 1, 2026 · Project: Brine Space · Bill meal Continue proof\n\n## Objective and acceptance\nComplete Bill animation set and full master consistency/polish.\n\n## Accepted decisions and constraints\nPreserve selected art, existing activity timers/economy, current physical contacts and owner saves.\n\n## Current state\nNew producer/fresh Continue fixtures with UIDs and isolated runners;20 case descriptors/checkpoints in producer scratch,20 independent engine profiles/captures; review generator/HTML and dated evidence. Production meal runtime unchanged.\n\n## Verification\n'+summary+'\n## Next action\nFull-set visual/motion audit and polish, resumed meal service and broader physical interruption contexts.\n'
(P/'CONTINUE_HANDOFF.md').write_text(handoff,encoding='utf-8')
files=[P/name for name in ['prepare_continue_validation.py','build_continue_review.py','record_continue_milestone.py','continued-contact-review.png','continue-review.html','CONTINUE_HANDOFF.md']]
files.extend(S/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png','continue-cases.json'])
files.append(O/'validation.json')
for result in report['results']:
    c=O/'cases'/result['id'];files.extend(c/name for name in ['native.log','validation.json','profile-before.json','profile-after.json']);files.append(O/(result['id']+'.png'))
files.extend(R/name for name in ['tests/test_bill_meal_continue_producer.gd','tests/test_bill_meal_continue_producer.gd.uid','tests/test_bill_meal_fresh_continue.gd','tests/test_bill_meal_fresh_continue.gd.uid','tools/run_bill_meal_continue_producer_validation.py','tools/run_bill_meal_fresh_continue_validation.py','scripts/bill_meal.gd','scripts/bill_npc.gd','scripts/grid_canvas.gd','scripts/crew_life.gd','scripts/run_save.gd','tools/audit_bill_selected_sources_2026_10_01.py','character/bill-selected-source-audit-2026-10-01/source-inventory.json','character/bill-selected-source-audit-2026-10-01/SOURCE_HANDOFF.md'])
(P/'continue-evidence.json').write_text(json.dumps({'nativeSubsystemPassed':True,'producerChecks':104,'freshContinueChecks':400,'processes':20,'strictProducerGuard':producer,'freshReport':report,'scope':'fresh actual title/loading Continue; two real galley contacts/two bare activities/five phases; paused exact restoration, broader resumed contexts pending','currentFileSha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
section='\n\n## Bill meal fresh Continue — October 1, 2026\n\n'+summary+'\nHandoff: character/bill-meal-family-v1/CONTINUE_HANDOFF.md.\n'
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (R/name).open('a',encoding='utf-8') as f:f.write(section)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(section)
status=R/'docs/CURRENT_STATUS.md';status.write_bytes((section.lstrip()+'\n').encode()+status.read_bytes())
print('Recorded20 fresh meal Continue cases:504 native checks; strict guards and remaining context scope retained')
