from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
m=json.loads((P/'manifest.json').read_text());reg=json.loads((P/'registration.json').read_text());checks=[];hashes={}
def check(ok,label):
 assert ok,label
 checks.append(label)
check(m['status']=='selected_runtime','Selected catalog status')
check(m['standingHeight']==148 and m['pivot']==[128,224],'Master density')
check(sum(m['states'][0]['frameDurationsMs'])==720 and m['states'][0]['loop'],'720ms review loop')
for i,f in enumerate(m['states'][0]['frameFiles']):
 p=R/f[6:];im=Image.open(p).convert('RGBA');check(im.size==(256,256),'Plane');box=im.getchannel('A').getbbox();check(box[0]>0 and box[1]>0 and box[2]<256 and box[3]<256,'Unclipped alpha bounds')
 s=148/490;check(reg['frames'][i]['scale']==[s,s],'One fixed atlas ruler');hashes[f]=hashlib.sha256(p.read_bytes()).hexdigest()
check(len(set(hashes.values()))==6,'Six distinct pose files')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'sha256':hashes,'scope':'Selected packaging only. v7 one-atlas opposed contact poses and narrowed build; motion/identity owner acceptance and native selection evidence separate.'},indent=2)+'\n')
print(str(len(checks))+' selected packaging checks pass')
