from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
summary='''Bill north bowl/cup counter reaches revised — October 1, 2026.
Built-in sources exec-479bc9c5-11c2-4694-86ca-24e2fc57cba2 (bowl) and
exec-a3b388ed-144e-4dd0-8ab7-b238b8f60895 (cup), raw PNGs/exact prompts retained.
Prior parent exports/config/evidence archived in revisions/counter-reach-v1.
Five interiors each; raised connected arms, unchanged planted feet, exact idle/
held endpoint donors and reversed returns. Bowl fixed ruler [.337,.345], cup
[.338,.3574]. Selected rear material grade retained. No geometry/runtime change.
28 package checks each; 87 native each (12.84s bowl,11.91s cup). Rebuilt north
family:39 assembly/299 native checks PASS12.31s. Actual current-layout contact
audit:103 checks PASS42.78s,8 stations/24 captures,all 2,914 owner files intact.
Native 82px family and actual station captures reviewed. Reach silhouettes sit
closer to the front counter edge; rear occlusion prevents certifying exact hand/
worktop contact. Remains staged, not owner-accepted or normal saved phase proof.
Current owner counters both face north; south production contact unavailable.
Next resolve contact readability/physical target evidence, then saved meal phase
integration, interruptions and disk restore. West/rest/dry death/wider inspection
and full-set polish remain. Full objective remains unfinished.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · BrineSpace · Bill north counter reach revision

## Objective and acceptance
Complete Bill's master-consistent animation set and full-set polish.
This milestone revises the north pickup reach; contact acceptance remains pending.

## Accepted decisions and constraints
Preserve master size, matte materials, planted stance and exact endpoint donors.
Retain owner counter geometry and original eating/drinking durations.
Native test art injection is a static review, not installed activity phase behavior.

## Current state
'''+summary+'''
## Verification
Source checks, native loading/joins and real chooser/renderer checks pass.
Technical passes do not establish exact occluded hand contact or owner acceptance.
All tests used scratch APPDATA; owner non-log profile fingerprints unchanged.

## Next action
Review reach/contact readability against both actual counters before installing
normal saved pickup/core/return phases. Then prove interruptions and Continue.
No commit, release or export requested.
'''
families=[('bill-meal-entry-north-v1','bill-meal-entry-north-candidate-native-v1',28,87),('bill-drink-entry-north-v1','bill-drink-entry-north-candidate-native-v1',28,87),('bill-meal-north-family-v1','bill-meal-north-family-candidate-native-v1',39,299)]
for name,out,package,native in families:
    p=ROOT/'character'/name;report=json.loads((ROOT/'output'/out/'validation.json').read_text())
    assert report['passed'] and not report['realProfileChanges']
    old=p/'candidate-evidence.json';archive=p/'revisions/counter-reach-v1';archive.mkdir(parents=True,exist_ok=True)
    if old.exists() and not (archive/old.name).exists():shutil.copy2(old,archive/old.name)
    (p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
    paths=[f for f in p.iterdir() if f.is_file() and f.name!='candidate-evidence.json']
    if (p/'sources').exists():paths+=list((p/'sources').glob('*'))
    paths+=[ROOT/'output'/out/'validation.json',ROOT/'output'/out/'loaded-water-carry.png']
    evidence={'status':'staged_candidate','checks':{'package':package,'native':native},'native':report,'scope':'raised north reach candidates; exact source/native joins; contact acceptance and normal saved phases pending','sha256':{f.relative_to(ROOT).as_posix():sha(f) for f in paths if f.is_file()}}
    old.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
p=ROOT/'character/bill-meal-contact-audit-v1';out=ROOT/'output/bill-meal-counter-contact-candidate-v1'
old=p/'audit-evidence.json';archive=p/'revisions/waist-reach-audit-v1';archive.mkdir(parents=True,exist_ok=True)
if not (archive/old.name).exists():shutil.copy2(old,archive/old.name);shutil.copy2(p/'HANDOFF.md',archive/'HANDOFF.md')
(p/'HANDOFF.md').write_text(handoff,encoding='utf-8')
report=json.loads((out/'validation.json').read_text());assert report['passed']
paths=[p/'HANDOFF.md',out/'validation.json',out/'contacts.json',out/'contact-detail-review.png',out/'index.html']+list(out.glob('q*-station*.png'))
old.write_text(json.dumps({'status':'raised_reach_contact_review_pending','native':report,'checks':103,'stations':8,'captures':24,'scope':'actual stations and static source injection; saved phases not installed','finding':'raised silhouettes improve counter-edge readability; exact hand/worktop contact occluded and not certified; no south production station','sha256':{f.relative_to(ROOT).as_posix():sha(f) for f in paths}},indent=2)+'\n',encoding='utf-8')
heading='## Bill north counter reach revision — October 1, 2026\n\n'
for relative in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    f=ROOT/relative
    with f.open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')
with f.open('a',encoding='utf-8') as stream:stream.write('\n'+heading+summary)
f=ROOT/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-meal-contact-audit-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded raised reach candidates, fresh native evidence and contact limits')
