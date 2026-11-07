"""Freeze all selected South gait poses and separate identity/material references."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-south-walk-family-detail-v1';OUT.mkdir(exist_ok=True)
INV=ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-north-walk/inventory.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads(INV.read_text())
for e in [d['catalog'],*d['orderedBodyManifests']]:assert sha(ROOT/e['path'])==e['sha256']
refs=[]
for i,e in enumerate(d['states']['walk-south']['frames']):
    p=ROOT/e['path'];assert sha(p)==e['sha256'];im=Image.open(p).convert('RGBA');assert im.size==(184,184)
    g=OUT/f'target-{i:03}-1024.png';im.resize((1024,1024),Image.Resampling.NEAREST).save(g)
    refs.append({'slot':i,'source':e,'guide':g.relative_to(ROOT).as_posix(),'guideSha256':sha(g)})
idle=d['states']['idle-south']['frames'][0];p=ROOT/idle['path'];assert sha(p)==idle['sha256']
Image.open(p).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(OUT/'own-idle-1024.png')
master=ROOT/'character/marsh-motion-polish-v1/sources/south-standing-identity-01.png'
crop=OUT/'master-collar-suit.png';Image.open(master).crop((300,365,715,825)).save(crop)
report={'inventory':{'path':INV.relative_to(ROOT).as_posix(),'sha256':sha(INV)},'targets':refs,'ownIdle':idle,'idleGuideSha256':sha(OUT/'own-idle-1024.png'),'master':{'path':master.relative_to(ROOT).as_posix(),'sha256':sha(master)},'materialCrop':{'path':crop.relative_to(ROOT).as_posix(),'sha256':sha(crop),'sourceCrop':[300,365,715,825]},'method':'Whole184square guides to1024nearest; unpainted collar/suit crop; target geometry, current ownidle identity/grade, original master material construction distinct. No artwork fitting or source recolour.','normalAdmission':False}
(OUT/'references.json').write_text(json.dumps(report,indent=2)+'\n')
print('Six whole South gait guides, ownidle and unpainted master material crop frozen; current catalogue and92manifests verified.')
