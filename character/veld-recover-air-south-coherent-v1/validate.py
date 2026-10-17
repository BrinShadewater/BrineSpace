from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1];checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
r=json.loads((P/'registration.json').read_text());hr=json.loads((P/'helmet-registration.json').read_text())
check(hashlib.sha256((P/r['source']).read_bytes()).hexdigest()==r['sourceSha256'],'raw source')
check(all(f['scale']==r['scale'] for f in r['frames']),'shared source ruler')
check(len({tuple(f['frontBootTarget']) for f in r['frames']})==1,'planted front boot')
for file,authority in [('manifest.json',r['idleAuthority']),('helmet-manifest.json',hr['donor'])]:
 m=json.loads((P/file).read_text());s=m['states'][0];idle=Image.new('RGBA',(256,256));idle.paste(Image.open(ROOT/authority).convert('RGBA'),(36,52))
 check(m['pivot']==[128,224] and m['standingHeight']==148,'dry standing plane')
 check(s['frameDurationsMs']==[500]*6 and not s['loop'],'three second finite clock')
 check(s['waterPoses']==[False]*6,'dry poses')
 for i,f in enumerate(s['frameFiles']):
  im=Image.open(P/f).convert('RGBA');a=np.array(im);box=im.getchannel('A').getbbox()
  check(im.size==(256,256) and 0<box[0]<box[2]<256 and 0<box[1]<box[3]<256,'contained alpha')
  if i in [0,5]:check(im.tobytes()==idle.tobytes(),'exact selected endpoint')
  else:
   y,x=np.where(a[:,:,3]>180);check(220<=y.max()<=225,'planted sole')
   if file=='helmet-manifest.json':
    row=next(f for f in hr['frames'] if f['frame']==i);bare=np.array(Image.open(P/f'frames/recover-air-south/{i:03}.png'));check(np.array_equal(a[row['protectedBodyFromY']:],bare[row['protectedBodyFromY']:]),'body below collar preserved')
check(hr['nativeScale']==1,'helmet unchanged ruler')
(P/'validation.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'source binding,shared ruler,boot,exact endpoints,finite clock,protected helmet body;native/controller/owner acceptance pending'},indent=2)+'\n')
print(f'{checks} south recovery package checks PASS')
