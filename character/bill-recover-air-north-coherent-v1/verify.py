from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;H=P.parent/'bill-recover-air-helmet-north-coherent-v1';checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
r=json.loads((P/'registration.json').read_text(encoding='utf-8'));hr=json.loads((H/'helmet-registration.json').read_text(encoding='utf-8'))
check(hashlib.sha256((P/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'authored source')
check(all(f['scaleX']==.306 and f['scaleY']==.317 for f in r['frames']),'frozen source proportions')
check(len({tuple(f['targetFrontBoot']) for f in r['frames']})==1,'planted boot landmark')
for folder,authority in [(P,P.parent/r['idleAuthority']),(H,P.parent/hr['donor'])]:
 m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));s=m['states'][0];hashes=json.loads((folder/'frame-hashes.json').read_text(encoding='utf-8'));idle=Image.new('RGBA',(256,256));idle.paste(Image.open(authority).convert('RGBA'),(36,52))
 check(m['pivot']==[128,224] and m['standingHeight']==148,'dry plane')
 check(s['id']=='recover-air-north' and s['frameDurationsMs']==[500]*6 and not s['loop'],'retained three-second simulation clock')
 check(s['waterPoses']==[False]*6 and s['waterKinds']==['recover']*6,'dry recovery metadata')
 for i,file in enumerate(s['frameFiles']):
  im=Image.open(folder/file).convert('RGBA');a=np.array(im);box=im.getchannel('A').getbbox()
  check(im.size==(256,256) and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained alpha')
  check(hashlib.sha256((folder/file).read_bytes()).hexdigest()==hashes[file],'frame binding')
  if i in [0,5]:check(np.array_equal(a,np.array(idle)),'exact selected idle endpoint')
  elif folder==H:
   f=next(f for f in hr['frames'] if f['frame']==i);b=np.array(Image.open(P/file).convert('RGBA'));check(np.array_equal(a[f['protectedBodyFromY']:],b[f['protectedBodyFromY']:]),'original body below fitted collar')
check(hr['nativeScale']==1,'native helmet ruler')
check(hashlib.sha256((P.parent/hr['donor']).read_bytes()).hexdigest()==hr['donorSha256'],'selected helmet donor')
check(hashlib.sha256((H/hr['component']).read_bytes()).hexdigest()==hr['componentSha256'],'extracted native head')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'paired source,proportions,boot,exact idle endpoints,finite dry clock and original helmet body;native/owner acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(f'{checks} north recovery package checks PASS')
