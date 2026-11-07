"""Freeze phase4 geometry and distinct matching face/material authorities."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-east-walk-halfcycle-polish-v1';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[('geometry','character/marsh-v2/frames/bare/walk-east/004.png'),('style','character/marsh-east-walk-bob-contact-v1/004.png'),('oppositePhase','character/marsh-east-walk-bob-contact-v1/001.png'),('ownIdle','character/marsh-v2/frames/bare/idle-east/000.png')]
records=[]
for role,rel in sources:
    p=ROOT/rel;guide=OUT/f'{role}-1024.png'
    Image.open(p).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(guide)
    records.append({'role':role,'path':rel,'sha256':sha(p),'guide':guide.relative_to(ROOT).as_posix(),'guideSha256':sha(guide)})
for i in range(6):
    p=ROOT/f'character/marsh-east-walk-bob-contact-v1/{i:03}.png';records.append({'role':'priorFamily','slot':i,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
(OUT/'references.json').write_text(json.dumps({'references':records,'normalAdmission':False,'method':'Whole184square sources to1024nearest, no pose fitting or drawing changes.'},indent=2)+'\n')
print('Phase4 geometry/style/opposite-phase/idle guides and prior six sources frozen.')
