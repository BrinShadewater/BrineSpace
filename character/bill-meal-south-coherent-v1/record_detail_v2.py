from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-meal-south-candidate-native-v1'
cfg=json.loads((P/'source-rulers.json').read_text());v=json.loads((P/'verification.json').read_text());n=json.loads((OUT/'validation.json').read_text())
assert cfg['source']=='sources/eat-detail-v2.png' and v['passed'] and n['passed'] and not n['realProfileChanges']
assert '71 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill south eating detail v2 candidate

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
Corrected south eating chest badge and head proportion; remaining meals pending.

## Accepted decisions and constraints
Selected front idle owns design/perspective/materials/proportions. Left bowl hand,
right spoon hand, two connected arms, upright planted stance. Separate bounded
face/hair/burgundy grade from matte neutral suit. No redesign of master badge.

## Current state
Built-in correction exec-a8be08e2-52ab-4707-b320-e87dd2f39a62/raw/exact prompt
retained in sources/eat-detail-v2.png/prompt-eat-detail-v2.txt. Original v1 source
and prompt retained; original exports/config/evidence archived revisions/eating-v1.
Six465/465/465/465/463/463px figures, fixed[.31,.3175] ruler,density1.06,
selected south grade and sole223. One bare staged state/seven960ms slots/exact
closure.256plane/pivot128,224/H148/dry0. Subdued steel chest badge replaces red
source badge; head and boots closer to selected master. No normal runtime change.

## Verification
24package/71native checks PASS12.18s after correction. Native148/82/idle boards
reviewed, stable bowl support and spoon path, no obvious extra hands/steps.
Frame0 head bounds115–140 now exactly equal master115–140 (previous114–142).
Boots102–155 vs master101–155 (previous102–156); legs107–151 vs106–149.
Crown76–77 vs master77, sole223 throughout. Hair117–138 vs119–137, fine torso/
harness/suit detail and modest leg asymmetry remain for full polish. Badge visual
match improved; alpha-band comparisons alone cannot prove design/color acceptance.
All2,914 owner non-log files unchanged under scratch APPDATA. Actual service
contact/pickup/return/interrupt/restore unproved; structural candidate checks only.

## Next action
Author south drinking with selected idle as identity authority and corrected
eating only as material/context reference; do not copy remaining fine-detail drift.
Then south bowl/cup pickup-return/full family, actual N/S phase/contact/interrupt/
restore proof, west meals/rest/drydeath and full cross-animation polish. Goal active.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill south eating badge/detail v2 correction — September30,2026.
Built-in exec-a8be08e2-52ab-4707-b320-e87dd2f39a62/raw/exact prompt retained;
v1 source/prompt retained and prior exports/config/evidence revisions/eating-v1.
Six465/465/465/465/463/463px figures, fixed[.31,.3175] ruler,density1.06,
selected south matte/face/hair/burgundy grade/sole223. Steel subdued chest badge
replaces bright red drift. Frame0 head115–140 equals master115–140 vs old114–142;
boots102–155 vs master101–155/old102–156; legs107–151 vs106–149. Crown76–77 vs77.
24package/71native PASS12.18s; fresh148/82 and idle boards reviewed, owner2,914
non-log files intact under scratch APPDATA. Bare staged only; no actor/loader change.
Lesson: correct distinctive badges in authored source before propagating action
families, retain prior evidence and remeasure new source rather than reuse old
atlas ruler after editing. Independent head/boot bands reveal improvements that
whole-body height misses. Fine hair/leg/harness detail still needs full polish;
neither fixed-height checks nor improved badge alone establishes full consistency.
Next south drinking/pickup-return/full family, actual N/S service/contact/saved
interrupt/restore proof, west/rest/drydeath and full-set polish. Goal active.
Handoff:character/bill-meal-south-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south eating badge/detail correction — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','verify.py','manifest.json','verification.json','HANDOFF.md','index.html','source-rulers.json','registration.json','frame-hashes.json','material-grade.json','contact-sheet.png','master-comparison.json','compare_master.py','select_detail_v2.py']]+list((P/'sources').glob('*'))+[OUT/'validation.json',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_meal_south_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':24,'native':71},'native':n,'scope':'corrected eating source/native loop; fine detail/proportion and actual meal phases/contact/interrupt/restore pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded authored south badge/head correction, prior evidence and native review')
