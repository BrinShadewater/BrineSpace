"""Paired source, loop join, registration and protected-body contract."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
r=json.loads((HERE/'registration.json').read_text(encoding='utf-8'))
check(hashlib.sha256((HERE/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'source hash')
check(all(f['scale']==.25 and f['targetCrownAxis']==[128,110] for f in r['frames']),'fixed scale/head axis')
legacy=json.loads((HERE.parent/'major-bill-v3/clearance.json').read_text(encoding='utf-8'))
for folder,authority in [(HERE,'bill-swim-south-coherent-v1'),(HERE.parent/'bill-salvage-helmet-south-coherent-v1','bill-swim-helmet-south-coherent-v1')]:
 p=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));h=json.loads((folder/'frame-hashes.json').read_text(encoding='utf-8'));s=p['states'][0]
 check(p['pivot']==[128,128] and p['standingHeight']==148,'physical registration')
 check(s['id']=='salvage-south' and s['loop'] and s['frameDurationsMs']==[140]*6,'retained fatigue clock')
 check(s['waterKinds']==['salvage']*6 and s['facings']==['south']*6 and s['waterPoses']==[True]*6 and s['depthOffsets']==[0]*6,'water contract')
 check(np.array_equal(np.array(Image.open(folder/s['frameFiles'][0])),np.array(Image.open(folder/s['frameFiles'][5]))),'exact working loop join')
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(folder/file).convert('RGBA');a=np.array(im);box=im.getchannel('A').getbbox()
  check(im.size==(256,256),'canvas');check(0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained alpha');check(hashlib.sha256((folder/file).read_bytes()).hexdigest()==h[file],'frame hash')
  if folder!=HERE:
   b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[146:],b[146:]),'protected tool/hands');yy,xx=np.indices((256,256));mask=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<142);check(np.array_equal(a[mask],b[mask]),'protected forearms')
 gear='bare' if folder==HERE else 'helmet'
 boxes=[Image.open(folder/file).getchannel('A').getbbox() for file in s['frameFiles']];union=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)];extent=[(v-128)*65.28/148 for v in union];action=legacy['actions'][gear]['salvage-south'];swim=legacy['swim'][gear]['south'];allowed=[min(action[0],swim[0]),min(action[1],swim[1]),max(action[2],swim[2]),max(action[3],swim[3])];contained=all(extent[i]>=allowed[i] for i in [0,1]) and all(extent[i]<=allowed[i] for i in [2,3]);check(contained,'actual effective work clearance')
 (folder/'clearance-review.json').write_text(json.dumps({'worldExtent':extent,'effectiveRetainedClearance':allowed,'contained':contained,'scope':'exported alpha envelope against actual swim/action union;not station route evidence'},indent=2)+'\n',encoding='utf-8')
helmet=HERE.parent/'bill-salvage-helmet-south-coherent-v1';hr=json.loads((helmet/'helmet-registration.json').read_text(encoding='utf-8'))
check(hr['componentNativeScale']==1,'native helmet scale');check((helmet/hr['component']).read_bytes()==(HERE.parent/hr['donor']).read_bytes(),'exact canonical helmet source')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'paired staged packaging, provenance, closed working join, clocks, protected body; runtime selection and owner acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} paired salvage packaging checks PASS')
