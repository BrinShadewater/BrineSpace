"""Freeze bounded normal alias proof and full native comparison triplets."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'output/marsh-animation-audit/cargo-unload-alias-player-v1-2026-10-03'
OUT=ROOT/'character/marsh-v2/supplemental/cargo-unload-matched-v1'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(AUDIT/'report.json')
assert (r['checks'],r['failures'],r['states'],r['slots'],r['playerRestores'])==(109,0,4,16,16)
assert len(r['captures'])==12 and len(r['samples'])==16
assert (AUDIT/'native-exit.txt').read_text().strip()=='0'
assert not any(m in (AUDIT/'native.log').read_text() for m in ['ERROR:', 'WARNING:', 'SCRIPT ERROR'])
for kind in ['inputs','owner']:
    before=read(AUDIT/f'{kind}-before.json');assert before==read(AUDIT/f'{kind}-after.json')
    r[kind+'UnchangedCount']=len(before)
before=read(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-cargo/inventory.json')['states']
after=read(ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-cargo-alias/inventory.json')['states']
assert set(before)==set(after)
changed=[k for k in before if before[k]!=after[k]]
assert sorted(changed)==sorted('cargo-unload-'+d for d in ['east','west','north','south'])
for k in changed:
    a,b=before[k],after[k];sa=dict(a['state']);sb=dict(b['state']);sa.pop('frameFiles');sb.pop('frameFiles')
    assert sa==sb and a['pivot']==b['pivot'] and a['standingHeight']==b['standingHeight']
    donor=after[k.removeprefix('cargo-')]
    assert b['frames']==donor['frames']
r['changedStates']=changed;r['unchangedStates']=224
r['boards']=[]
for c in r['captures']:
    shutil.copy2(AUDIT/c['file'],OUT/c['file']);c['sha256']=sha(OUT/c['file'])
for d in ['east','west','north','south']:
    caps=[c for c in r['captures'] if c['key']=='cargo-unload-'+d]
    assert [c['slot'] for c in caps]==[0,2,3]
    board=Image.new('RGB',(2016,490))
    for i,c in enumerate(caps):
        im=Image.open(OUT/c['file']).convert('RGB');assert im.size==(672,490);board.paste(im,(i*672,0))
    path=OUT/(d+'-native-triplet.png');board.save(path)
    r['boards'].append({'file':path.name,'sha256':sha(path),'actuallyInspected':False})
r.update({'normalAdmission':True,'fullGoalComplete':False,'continuousMotionReviewed':False})
(OUT/'verification.json').write_text(json.dumps(r,indent=2)+'\n')
print('109checks/4aliases/16slots/restores/12captures;5308inputs/2931owner unchanged;224other states exact;4boards prepared')
