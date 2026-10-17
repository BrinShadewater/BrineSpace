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
check(all(f['scale']==.28 and f['targetCrownAxis']==[154,104] for f in r['frames']),'fixed scale/head axis')
for folder,authority in [(HERE,'bill-swim-east-coherent-v1'),(HERE.parent/'bill-death-water-helmet-east-coherent-v1','bill-swim-helmet-east-coherent-v1')]:
 p=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));h=json.loads((folder/'frame-hashes.json').read_text(encoding='utf-8'));s=p['states'][0]
 check(p['pivot']==[128,128] and p['standingHeight']==148,'physical registration')
 check(s['id']=='death-water-east' and not s['loop'] and s['frameDurationsMs']==[180,180,220,220,260,500],'retained one-shot death clock')
 check(s['waterKinds']==['death']*6 and s['facings']==['east']*6 and s['waterPoses']==[True]*6 and s['depthOffsets']==[0]*6,'water contract')
 expected=Image.new('RGBA',(256,256));expected.alpha_composite(Image.open(HERE.parent/authority/'frames/swim-east/000.png').convert('RGBA'),(6,40))
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(folder/file).convert('RGBA');a=np.array(im);box=im.getchannel('A').getbbox()
  check(im.size==(256,256),'canvas');check(0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained alpha');check(hashlib.sha256((folder/file).read_bytes()).hexdigest()==h[file],'frame hash')
  if i==0:check(np.array_equal(a,np.array(expected)),'exact swim entry')
  if folder!=HERE and i in [1,2,3,4,5]:
   b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[135:],b[135:]),'protected suit/legs');check(np.array_equal(a[128:135,160:][b[128:135,160:,3]>0],b[128:135,160:][b[128:135,160:,3]>0]),'protected forward arm')
helmet=HERE.parent/'bill-death-water-helmet-east-coherent-v1';hr=json.loads((helmet/'helmet-registration.json').read_text(encoding='utf-8'))
check(hr['componentNativeScale']==1,'native helmet scale');check((helmet/hr['component']).read_bytes()==(HERE.parent/hr['donor']).read_bytes(),'exact canonical helmet source')
closed=np.array(Image.open(helmet/'sources/canonical-closed-head.png').convert('RGBA'));native=np.array(Image.open(helmet/hr['component']).convert('RGBA'));mask=np.ones(native.shape[:2],bool);mask[16:19,28:33]=False;check(np.array_equal(closed[mask],native[mask]),'original shell/face pixels outside eye patch');check(not np.array_equal(closed[16:19,28:33],native[16:19,28:33]),'authored eye expression differs');check(hashlib.sha256((helmet/hr['expressionSource']).read_bytes()).hexdigest()==hr['expressionSourceSha256'],'expression source hash')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'paired staged packaging, provenance, exact swim entry, finite death clock, protected body and unchanged helmet outside authored eye patch; runtime selection and owner acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} paired death packaging checks PASS')
