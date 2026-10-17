from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-drink-south-candidate-native-v1'
n=json.loads((OUT/'validation.json').read_text());assert n['passed'] and not n['realProfileChanges'] and json.loads((P/'verification.json').read_text())['passed']
assert '71 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill south drinking candidate

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
South drinking loop authored/corrected/native reviewed; transitions pending.

## Accepted decisions and constraints
Selected south idle is design authority; corrected eating gives material context.
Right cup hand (viewer left) lifts, left free arm hangs down. Upright planted body,
front orthographic camera, small cup at lips without hiding whole face. Steel-grey
chest badge, muted burgundy shoulders, matte suit, bounded skin/hair grade.

## Current state
Original built-in exec-35b290b6-5737-4411-be32-a2cbab7c2f37/raw/exact prompt
retained sources/drink-v1.png/prompt-drink.txt. Two source poses had red badge.
Authored correction exec-69619da3-5262-4867-bed2-becf4b963b96/raw/exact prompt
retained sources/drink-badge-v2.png/prompt-badge-v2.txt and used for all exports.
Six464/464/465/463/463/463px figures, one[.30,.318] ruler,density1.06, selected
south neutral/face/hair/burgundy grade/sole223. One bare staged state/seven960ms
slots/six distinct poses/exact closure,256plane/pivot128,224/H148/dry0.
Build/verify/preview/registration/hash and cross-action evidence retained.
No normal loader/registry/actor/galley geometry/reward changes.

## Verification
24package/71native PASS12.33s: source/master binding, exact loaded pixels,
direction/drink metadata, shared plane, pacing/repeated loops/closure. Fresh
native148/82/idle and three-row idle/eating/drinking boards reviewed. Grey badge
throughout; correct cup grip, no extra waist hand or foot step seen. Independent
frame0 bounds: head116–140 vs master115–140; legs105–151 vs106–149; boots101–155
equal master. Crown76–77 vs master77. Fine hair117–138 vs119–137, leg width,
panel/harness/suit texture differences remain for full-set polish. Alpha bands
support visual review, not final design or actual service contact acceptance.
All2,914 owner non-log files unchanged under scratch APPDATA. Actual pickup/
return/contact/saved service phase/interruption/disk restore remain unproved.

## Next action
Author south bowl/cup pickup-return with exact selected idle/current held donors,
then assemble full south family. Prove actual N/S meal service phases/contact/
interruptions/restore; west meals/rest/drydeath, wider inspection audits and full
cross-animation polish remain. Full goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill south drinking candidate / cross-action comparison — September30,2026.
Original exec-35b290b6-5737-4411-be32-a2cbab7c2f37/raw/prompt retained; red
badge in two poses corrected before packaging with built-in
exec-69619da3-5262-4867-bed2-becf4b963b96/raw/exact prompt retained. Six
464/464/465/463/463/463px figures, fixed[.30,.318] ruler,density1.06, selected
south matte/face/hair/burgundy grade/sole223. Right cup lift/free left arm down,
one bare staged state/seven960ms slots/exact closure.24package/71native PASS
12.33s; native148/82/idle and idle/eat/drink boards reviewed. All2,914 owner
non-log files intact under scratch APPDATA; no actor/loader/geometry changes.
Frame0 head116–140 vs master115–140; boots101–155 exactly match; legs105–151
vs106–149; crown76–77 vs77. Fine hair/leg/panel/harness detail remains for polish.
Lesson: explicit badge instructions can still drift in individual source poses;
inspect every pose before export and correct across the entire source sheet so
the color does not flicker through a loop. Retain original/corrected sources,
and remeasure corrected atlas. Cross-action metrics and native pacing do not
prove real counter contact/saved service acceptance. Next south pickup-return/
full family, actual N/S service/contact/interruption/restore proof, remaining
west/rest/drydeath and full-set polish. Full goal active.
Handoff:character/bill-drink-south-coherent-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south drinking candidate / master comparison — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=[P/name for name in ['build.py','verify.py','manifest.json','verification.json','HANDOFF.md','index.html','source-rulers.json','registration.json','frame-hashes.json','material-grade.json','contact-sheet.png','master-comparison.json','cross-action-review.png','cross-action-review.html','cross-action-review.json']]+list((P/'sources').glob('*'))+[OUT/'validation.json',OUT/'loaded-water-carry.png',ROOT/'tests/test_bill_drink_south_candidates.gd']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':24,'native':71},'native':n,'scope':'staged corrected drinking loop/cross-action review; real service/contact/interrupt/restore and fine polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded south drinking, authored badge correction and cross-action proof')
