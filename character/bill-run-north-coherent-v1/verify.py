from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
m=json.loads((P/'manifest.json').read_text());reg=json.loads((P/'registration.json').read_text());checks=[];hashes={}
def check(ok,label):assert ok,label;checks.append(label)
check(m['standingHeight']==148 and m['pivot']==[128,224],'Master density')
check(sum(m['states'][0]['frameDurationsMs'])==540 and m['states'][0]['loop'],'540ms loop')
for i,f in enumerate(m['states'][0]['frameFiles']):
 p=R/f[6:];im=Image.open(p).convert('RGBA');check(im.size==(256,256),'Plane');box=im.getchannel('A').getbbox();check(box[0]>0 and box[1]>0 and box[2]<256 and box[3]<256,'Unclipped alpha bounds')
 check(reg['frames'][i]['scale']==[148/480]*2,'Shared anatomical ruler');hashes[f]=hashlib.sha256(p.read_bytes()).hexdigest()
check(len(set(hashes.values()))==6,'Distinct six source poses')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'sha256':hashes,'scope':'packaging/fixed ruler/distinct pixels; limb biomechanics, loop cadence and identity visual acceptance separate'},indent=2)+'\n')
print(str(len(checks))+' package checks pass')
