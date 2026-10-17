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
check(all(f['scale']==.27 and f['targetCrownAxis']==[128,110] for f in r['frames']),'fixed scale/head axis')
for folder,authority in [(HERE,'bill-swim-south-coherent-v1'),(HERE.parent/'bill-swim-distress-helmet-south-coherent-v1','bill-swim-helmet-south-coherent-v1')]:
 p=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));h=json.loads((folder/'frame-hashes.json').read_text(encoding='utf-8'));s=p['states'][0]
 check(p['pivot']==[128,128] and p['standingHeight']==148,'physical registration')
 check(s['id']=='swim-distress-south' and s['loop'] and s['frameDurationsMs']==[160]*6,'retained fatigue clock')
 check(s['waterKinds']==['swim']*6 and s['facings']==['south']*6 and s['waterPoses']==[True]*6 and s['depthOffsets']==[0]*6,'water contract')
 expected=Image.new('RGBA',(256,256));expected.alpha_composite(Image.open(HERE.parent/authority/'frames/swim-south/000.png').convert('RGBA'),(24,-24))
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(folder/file).convert('RGBA');a=np.array(im);box=im.getchannel('A').getbbox()
  check(im.size==(256,256),'canvas');check(0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained alpha');check(hashlib.sha256((folder/file).read_bytes()).hexdigest()==h[file],'frame hash')
  if i in [0,5]:check(np.array_equal(a,np.array(expected)),'exact swim join')
  if folder!=HERE and i in [1,2,3,4]:
   b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[146:],b[146:]),'protected suit/legs');foreground=(b[:,:,3]>0)&((np.indices((256,256))[1]<116)|(np.indices((256,256))[1]>140))&(np.indices((256,256))[0]<142);check(np.array_equal(a[foreground],b[foreground]),'protected forward arms')
helmet=HERE.parent/'bill-swim-distress-helmet-south-coherent-v1';hr=json.loads((helmet/'helmet-registration.json').read_text(encoding='utf-8'))
check(hr['componentNativeScale']==1,'native helmet scale');check((helmet/hr['component']).read_bytes()==(HERE.parent/hr['donor']).read_bytes(),'exact canonical helmet source')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'paired staged packaging, provenance, closed swim joins, clocks, protected body; runtime selection and owner acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} paired distress packaging checks PASS')
