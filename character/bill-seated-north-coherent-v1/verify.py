from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;H=P.parent/'bill-seated-helmet-north-coherent-v1';checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
r=json.loads((P/'registration.json').read_text(encoding='utf-8'));hr=json.loads((H/'helmet-registration.json').read_text(encoding='utf-8'))
for source,digest in r['sources'].items():check(hashlib.sha256((P/source).read_bytes()).hexdigest()==digest,'authored source')
check(len({tuple(f['targetFrontBoot']) for f in r['frames']})==1,'local boot registration')
check(all([f['scaleX'],f['scaleY']]==(r['primaryRuler'] if f['source'].endswith('sit-v1.png') else r['interiorRuler']) for f in r['frames']),'fixed rulers by source')
heads=[76]+[f['headAxis'][1] for f in r['frames']];check(all(a<=b for a,b in zip(heads,heads[1:])),'crown lowers monotonically')
for folder,authority in [(P,P.parent/r['idleAuthority']),(H,P.parent/hr['donor'])]:
 m=json.loads((folder/'manifest.json').read_text(encoding='utf-8'));hashes=json.loads((folder/'frame-hashes.json').read_text(encoding='utf-8'));down,rise=m['states'];idle=Image.new('RGBA',(256,256));idle.paste(Image.open(authority).convert('RGBA'),(36,52))
 check(m['pivot']==[128,224] and m['standingHeight']==148,'dry plane')
 check(down['id']=='sit-down-north' and rise['id']=='sit-rise-north','paired finite actions')
 check(down['frameDurationsMs']==[100,120,140,160,160,120] and rise['frameDurationsMs']==down['frameDurationsMs'][::-1],'retained800ms/reversed pacing')
 check(rise['frameFiles']==down['frameFiles'][::-1] and not down['loop'] and not rise['loop'],'authored reversed rise')
 check(down['depthOffsets']==[0,8,16,24,32,40] and rise['depthOffsets']==down['depthOffsets'][::-1],'retained depth metadata')
 check(down['waterPoses']==[False]*6 and rise['waterPoses']==[False]*6,'dry states')
 for i,file in enumerate(down['frameFiles']):
  im=Image.open(folder/file).convert('RGBA');a=np.array(im);box=im.getchannel('A').getbbox();check(im.size==(256,256) and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained alpha');check(hashlib.sha256((folder/file).read_bytes()).hexdigest()==hashes[file],'frame binding')
  if i==0:check(im.tobytes()==idle.tobytes(),'exact selected standing endpoint')
  elif folder==H:
   f=next(f for f in hr['frames'] if f['frame']==i);b=np.array(Image.open(P/file).convert('RGBA'));check(np.array_equal(a[f['protectedBodyFromY']:],b[f['protectedBodyFromY']:]),'original body below collar')
check(hr['nativeScale']==1,'native selected helmet')
check(hashlib.sha256((P.parent/hr['donor']).read_bytes()).hexdigest()==hr['donorSha256'],'helmet donor binding')
check(hashlib.sha256((H/hr['component']).read_bytes()).hexdigest()==hr['componentSha256'],'canonical component binding')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'headYs':heads,'scope':'paired source,rulers,local boot,crown progression,standing endpoint,finite800ms,reverse/protected body;seated loop/real furniture contact/installation pending'},indent=2)+'\n',encoding='utf-8');print(f'{checks} north sitting package checks PASS;headYs={heads}')
