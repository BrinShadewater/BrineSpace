"""Verify paired south death source registration and protected helmet fit."""
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
check(hashlib.sha256((HERE/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'primary source hash')
check(r['unusedSourcePoses']==[0,5],'omitted primary source poses')
for f in r['frames']:
 check(f['targetCrownAxis']==[128,110],'fixed crown registration')
 check(f['scale']==(.09 if f.get('outputPose')==5 else .26),'independent fixed source ruler')
 if 'source' in f:check(hashlib.sha256((HERE/f['source']).read_bytes()).hexdigest()==f['sourceSha256'],'independent terminal source hash')
for folder,authority in [(HERE,'bill-swim-south-coherent-v1'),(HERE.parent/'bill-death-water-helmet-south-coherent-v1','bill-swim-helmet-south-coherent-v1')]:
 p=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));h=json.loads((folder/'frame-hashes.json').read_text(encoding='utf-8'));s=p['states'][0]
 check(p['pivot']==[128,128] and p['standingHeight']==148,'physical registration')
 check(s['id']=='death-water-south' and not s['loop'] and s['frameDurationsMs']==[180,180,220,220,260,500],'finite death clock')
 check(s['waterKinds']==['death']*6 and s['facings']==['south']*6 and s['waterPoses']==[True]*6 and s['depthOffsets']==[0]*6,'water contract')
 expected=Image.new('RGBA',(256,256));expected.alpha_composite(Image.open(HERE.parent/authority/'frames/swim-south/000.png').convert('RGBA'),(24,-24))
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(folder/file).convert('RGBA');a=np.array(im);box=im.getchannel('A').getbbox()
  check(im.size==(256,256),'canvas');check(0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained alpha');check(hashlib.sha256((folder/file).read_bytes()).hexdigest()==h[file],'frame hash')
  if i==0:check(np.array_equal(a,np.array(expected)),'exact selected swim entry')
  if folder!=HERE and i>0:
   b=np.array(Image.open(HERE/file).convert('RGBA'));check(np.array_equal(a[146:],b[146:]),'protected suit and legs')
   yy,xx=np.indices((256,256));m=(b[:,:,3]>0)&((xx<116)|(xx>140))&(yy<142)
   check(np.array_equal(a[m],b[m]),'protected forearms outside helmet')
helmet=HERE.parent/'bill-death-water-helmet-south-coherent-v1';hr=json.loads((helmet/'helmet-registration.json').read_text(encoding='utf-8'))
check(hr['componentNativeScale']==1,'native helmet ruler')
check((helmet/hr['component']).read_bytes()==(HERE.parent/hr['donor']).read_bytes(),'exact selected rear helmet source')
check(all(f['position']==[112,106] for f in hr['frames']),'helmet registration')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'paired staged provenance, independent source rulers, exact swim entry, finite timing and protected body/forearms; native and visual evidence separate'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} paired south death packaging checks PASS')
