from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;p=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'));r=json.loads((HERE/'registration.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/'frame-hashes.json').read_text(encoding='utf-8'));checks=0
def check(v,m):
 global checks
 assert v,m
 checks+=1
check((p['frameWidth'],p['frameHeight'],p['pivot'],p['standingHeight'])==(256,256,[128,128],148),'common water pivot')
for authority,offset in zip(r['endpointAuthorities'],r['endpointOffsets']):
 folder=authority.split('/')[0];pack=json.loads((HERE.parent/folder/'manifest.json').read_text(encoding='utf-8'));check([offset[0]+pack['pivot'][0],offset[1]+pack['pivot'][1]]==p['pivot'],'endpoint world registration preserved')
check(all(x['scale']==.21 for x in r['frames']),'frozen scale');check(hashlib.sha256((HERE/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'source hash')
for state in p['states']:
 check(len(state['frameFiles'])==6 and sum(state['frameDurationsMs'])==520 and not state['loop'],'clip contract');check(state['waterPoses']==[True]*6,'water pose')
 for file in state['frameFiles']:
  im=Image.open(HERE/file).convert('RGBA');box=im.getchannel('A').getbbox();check(im.size==(256,256),'dimensions');check(0<box[0] and 0<box[1] and box[2]<256 and box[3]<256,'clipping');check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==hashes[file],'frame hash')
a=p['states'][0];b=p['states'][1]
for i in range(6):check(np.array_equal(np.array(Image.open(HERE/a['frameFiles'][i])),np.array(Image.open(HERE/b['frameFiles'][5-i]))),'exact reverse')
for file,authority,offset in zip([a['frameFiles'][0],a['frameFiles'][-1]],r['endpointAuthorities'],r['endpointOffsets']):
 canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(Image.open(HERE.parent/authority).convert('RGBA'),tuple(offset));check(np.array_equal(np.array(canvas),np.array(Image.open(HERE/file))),'exact endpoint on shared pivot')
(HERE/'verification.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'metadata,exact endpoints/reverse,registration and provenance; visual/native acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(str(checks)+' checks PASS')
