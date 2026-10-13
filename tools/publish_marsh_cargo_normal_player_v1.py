"""Freeze all native player captures; prepare four cardinal carry triplets."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
root=Path(__file__).resolve().parents[1]
audit=root/'output/marsh-animation-audit/cargo-normal-player-v1-2026-10-03'
interval=root/'output/marsh-animation-audit/cargo-normal-v1-2026-10-03'
out=root/'character/marsh-v2/supplemental/cargo-matched-v1/player-review'
out.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(audit/'report.json')
assert (r['checks'],r['failures'],r['states'],r['slots'],r['playerRestores'])==(1653,0,48,272,272)
assert len(r['samples'])==272 and len(r['captures'])==144
assert (interval/'player-exit.txt').read_text().strip()=='0'
assert not any(m in (interval/'player.log').read_text() for m in ['ERROR:', 'WARNING:', 'SCRIPT ERROR'])
for kind in ['inputs','owner']:
    before=read(interval/f'{kind}-before.json')
    assert before==read(interval/f'{kind}-after.json')
    r[kind+'UnchangedCount']=len(before)
for cap in r['captures']:
    shutil.copy2(audit/cap['file'],out/cap['file'])
    cap['sha256']=sha(out/cap['file'])
r['boards']=[]
for direction in ['east','west','north','south']:
    caps=[c for c in r['captures'] if c['key']=='carry-'+direction]
    assert len(caps)==3
    board=Image.new('RGB',(2016,490))
    for i,cap in enumerate(caps):
        im=Image.open(out/cap['file']).convert('RGB');assert im.size==(672,490)
        board.paste(im,(672*i,0))
    name=direction+'-carry-triplet.png';board.save(out/name)
    r['boards'].append({'file':name,'sha256':sha(out/name),'actuallyInspected':False})
r.update({'normalAdmission':True,'fullGoalComplete':False,'continuousMotionReviewed':False})
(out/'verification.json').write_text(json.dumps(r,indent=2)+'\n')
print('1653checks/48states/272slots/restores/144captures frozen;4cardinal carry triplets prepared')
