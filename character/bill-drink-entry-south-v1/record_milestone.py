from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;F=P.parent/'bill-meal-south-family-v1'
OUT=ROOT/'output/bill-drink-entry-south-candidate-native-v1';NATIVE=ROOT/'output/bill-meal-south-family-candidate-native-v1'
for package,out,count in [(P,OUT,87),(F,NATIVE,299)]:
 assert json.loads((package/'verification.json').read_text())['passed']
 n=json.loads((out/'validation.json').read_text());assert n['passed'] and not n['realProfileChanges']
 assert f'{count} checks,0 failures' in (out/'native.log').read_text(encoding='utf-8')
cup='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill south cup pickup/return candidates

## Objective and acceptance
Complete Bill's master-consistent full animation set, then full-set polish.
South cup transitions join exact selected idle to current drinking hold.

## Accepted decisions and constraints
Front idle owns identity/proportions/perspective/matte materials. Right cup hand
viewer left reaches; left arm stays down. Two hands, grey chest badge, muted
burgundy shoulders, planted upright body. Original service clocks unchanged.

## Current state
Built-in exec-96a429af-3216-4956-8b5f-7f2f63d25527/raw/exact prompt retained
in sources. Six512/511/512/512/512/512px figures; five interiors0..4, redundant
hold5 retained unused. Fixed[.267,.289] ruler,density1.16, selected south neutral/
face/hair grade and shoulder-plate interior sampling from bowl transition lesson.
Exact idle/drink000 donors, sole223. Two bare staged states/14refs/seven580ms
slots/exact reverse,256plane/pivot128,224/H148/dry0. Build/verify/preview/hash/
registration/evidence retained. No normal loader/actor/geometry/reward changes.

## Verification
28package/87native PASS11.89s. Source/donor bindings, exact loaded pixels,
finite pacing/hold, dry metadata, exact idle/held joins and reversed poses.
Native148/82/idle boards reviewed. Badge stays grey, cup correctly held, free arm
down and no obvious steps/extra waist hands. Fine suit/harness/face material and
interior body/arm/contact/readability differences remain for full-set polish.
All2,914 owner non-log files unchanged under scratch APPDATA. Source cup contact
does not establish real worktop reach. Actual phase/contact/interrupt/restore pending.

## Next action
Full south meal family assembled separately. Audit actual N/S galley contact and
install/test saved meal phases, interruption and disk restore. Finish west meals,
rest/drydeath, wider inspection audits and full cross-animation polish. Goal active.
'''
family='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill south full bare meal candidate family

## Objective and acceptance
Complete Bill's full master-consistent animation set, then full-set polish.
Six-state south meal family assembled/native reviewed; real service pending.

## Accepted decisions and constraints
Four source parents retain generation/grade/ruler provenance. Whole literal res
paths/no duplicated rasters. Shared256plane/pivot128,224/H148/dry0,580ms transitions,
960ms loops, original6s eat/3s drink preview. Selected idle owns identity and size.
Steel chest badge, matte suit, bounded face and shoulder-interior grading lessons.
Actual current galley approaches N/S; helmet meals retain inspection.

## Current state
Six staged states/42refs: eat-enter/eat/eat-exit/drink-enter/drink/drink-exit south.
Parents bill-meal-entry-south-v1,bill-meal-south-coherent-v1 (corrected detail v2),
bill-drink-entry-south-v1,bill-drink-south-coherent-v1 (corrected badge v2).
Build binds all parent manifests/frame hashes/pacing and all exact joins/reversals.
Preview full meal beside selected idle. No normal selection/registry/actor changes;
old bare south meals remain normal until actual service integration.

## Verification
39assembly/299native candidate checks PASS11.77s.42 exact loaded source refs,
metadata/pacing/finite holds/loop repeats/closure, five adjacent joins, both reverse
transitions and full idle closure. Native82 six-row family board reviewed; parent
148/82/idle separately reviewed. All2,914 owner non-log files intact in both scratch
runs. Fine suit/harness/material and interior proportion/contact/arm progression
remain for full polish; exact endpoints do not prove consistency of all interiors.
Presentation6+3s clocks are not actual saved activity evidence. World counter reach,
normal phase selection, interruption and disk restore remain unproved.

## Next action
Audit north/south authored reaches at actual galley contacts before declaring meal
service accepted; keep physical geometry unchanged. Normally install meal families
and implement/test saved pickup/core/return with original clocks/rewards, contact/
hazard/power loss and fresh disk Continue. Keep helmet reader and other actors'
behavior. Finish west meals/rest/drydeath/inspection broader audits, then full
cross-animation consistency/polish. Goal active; no commit/export requested.
'''
(P/'HANDOFF.md').write_text(cup,encoding='utf-8');(F/'HANDOFF.md').write_text(family,encoding='utf-8')
note='''
Bill south cup transitions/full meal candidate family — September30,2026.
Cup built-in exec-96a429af-3216-4956-8b5f-7f2f63d25527/raw/exact prompt retained.
Six512/511/512/512/512/512px figures, five interiors0..4, fixed[.267,.289]
ruler,density1.16, selected south matte/face/hair grade and bounded shoulder
plate interior sampling, sole223/exact idle-drink donors. Two bare states/14refs,
seven580ms slots/exact reverse.28package/87native PASS11.89s;148/82/idle reviewed.
Full south family assembled:sixstates/42whole literal refs/no image copies;
39assembly/299native PASS11.77s, all parent pixels/pacing/joins/reversals/closure,
native82 board reviewed. All2,914 owner files intact in both scratch runs.
No normal loader/actor/geometry/reward changes. Source/contact pose and exact
endpoint joins do not establish physical counter reach or actual saved service.
Fine harness/suit/material/interior proportion and return/contact readability
remain for full-set polish. Next actual N/S galley contact audit before normal
meal phase installation/saved interruption/disk Continue proof; keep geometry
unchanged. West meals/rest/drydeath/inspection wider audits/full polish remain.
Full goal active. Handoffs:character/bill-drink-entry-south-v1/HANDOFF.md and
character/bill-meal-south-family-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill south full meal candidate family assembled — September30,2026\n'+note+'\n').encode()+status.read_bytes())
for package,out,counts,extra in [(P,OUT,{'package':28,'native':87},['source-rulers.json','registration.json','frame-hashes.json','verify.py','build_preview.py','grade_shoulders.py','contact-sheet.png']),(F,NATIVE,{'package':39,'native':299},[])]:
 files=[package/name for name in ['build.py','manifest.json','verification.json','HANDOFF.md','index.html']+extra]+list((package/'sources').glob('*'))+[out/'validation.json',out/'loaded-water-carry.png']
 (package/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':counts,'native':json.loads((out/'validation.json').read_text()),'scope':'source/candidate native joins only; normal phase/contact/interrupt/restore and full polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded south cup transitions/full meal family and actual contact/service next')
