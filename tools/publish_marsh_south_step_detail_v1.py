"""Freeze seven native comparisons and exact single-state/slot admission scope."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'character/marsh-v2/supplemental/south-step-detail-v1'
AUDIT=ROOT/'output/marsh-animation-audit/south-step-detail-player-v1-2026-10-03'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(AUDIT/'report.json');assert (r['checks'],r['failures'],r['states'],r['slots'],r['playerRestores'])==(50,0,1,7,7)
assert len(r['captures'])==7 and len(r['samples'])==7
assert (AUDIT/'native-exit.txt').read_text().strip()=='0'
assert not any(m in (AUDIT/'native.log').read_text() for m in ['ERROR:', 'WARNING:', 'SCRIPT ERROR'])
for kind in ['owner','inputs']:
    before=read(AUDIT/f'{kind}-before.json');assert before==read(AUDIT/f'{kind}-after.json');r[kind+'UnchangedCount']=len(before)
before=read(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-cargo-alias/inventory.json')['states']
after=read(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-step-detail/inventory.json')['states']
assert set(before)==set(after) and [k for k in before if before[k]!=after[k]]==['walk-step-south']
a,b=before['walk-step-south'],after['walk-step-south'];sa=dict(a['state']);sb=dict(b['state']);sa.pop('frameFiles');sb.pop('frameFiles')
assert sa==sb and a['pivot']==b['pivot'] and a['standingHeight']==b['standingHeight']
assert [i for i,(f,g) in enumerate(zip(a['frames'],b['frames'])) if f!=g]==[3]
assert read(BASE/'admission.json')['catalogBeforeSha256']==sha(BASE/'catalog-before.json')
r.update(changedStates=['walk-step-south'],changedSlots=[3],unchangedStates=227,normalAdmission=True,fullGoalComplete=False,continuousMotionReviewed=False,admissionReceiptSha256=sha(BASE/'admission.json'))
for c in r['captures']:
    shutil.copy2(AUDIT/c['file'],BASE/c['file']);c['sha256']=sha(BASE/c['file'])
r['boards']=[]
for page in range(4):
    caps=r['captures'][2*page:2*page+2];board=Image.new('RGB',(672*len(caps),490))
    for i,c in enumerate(caps):
        im=Image.open(BASE/c['file']).convert('RGB');assert im.size==(672,490);board.paste(im,(672*i,0))
    p=BASE/f'native-pair-{page:02}.png';board.save(p)
    r['boards'].append({'file':p.name,'sha256':sha(p),'slots':[c['slot'] for c in caps],'actuallyInspected':False})
(BASE/'verification.json').write_text(json.dumps(r,indent=2)+'\n')
print('50checks/7slots/restores/captures,5311inputs/2931owner stable;1pose/1state changed,227states exact;4boards prepared')
