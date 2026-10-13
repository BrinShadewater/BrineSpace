"""Freeze original gait geometry and registered style as separate authorities."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'character/marsh-east-walk-bob-polish-v1';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inventory=json.loads((ROOT/'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json').read_text())
records=[]
for slot in [1,2,5]:
 old=ROOT/inventory['states']['walk-east']['frames'][slot]['path']
 assert sha(old)==inventory['states']['walk-east']['frames'][slot]['sha256']
 registered=ROOT/f'character/marsh-east-walk-family-contact-v1/{slot:03}.png'
 for label,p in [('geometry',old),('style',registered)]:
  guide=OUT/f'{label}-{slot:03}-1024.png'
  Image.open(p).convert('RGBA').resize((1024,1024),Image.Resampling.NEAREST).save(guide)
  records.append({'slot':slot,'role':label,'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'guide':guide.relative_to(ROOT).as_posix(),'guideSha256':sha(guide)})
for slot in range(6):
 p=ROOT/f'character/marsh-east-walk-family-contact-v1/{slot:03}.png'
 records.append({'slot':slot,'role':'registeredFamily','path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)})
for path,role in [('character/marsh-east-walk-family-detail-v1/own-idle-1024.png','ownIdle'),('character/marsh-east-walk-detail-v1/master-collar-suit.png','originalMaterialCrop'),('character/marsh-motion-polish-v1/sources/east-standing-identity-01.png','originalMaster')]:
 p=ROOT/path;records.append({'role':role,'path':path,'sha256':sha(p)})
(OUT/'references.json').write_text(json.dumps({'references':records,'method':'Native whole184square guides to1024nearest; original gait geometry separate from registered style; no anatomy fit/edit/paint; original material crop reused unmodified.','normalAdmission':False},indent=2)+'\n')
print('Three geometry/style guide pairs and full registered neighborhood frozen')
