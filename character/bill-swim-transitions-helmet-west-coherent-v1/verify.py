from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-swim-transitions-west-coherent-v1';p=json.loads((HERE/'manifest.json').read_text());b=json.loads((BARE/'manifest.json').read_text());r=json.loads((HERE/'helmet-registration.json').read_text());h=json.loads((HERE/'frame-hashes.json').read_text());checks=0
def check(v,m):
 global checks
 assert v,m
 checks+=1
for key in ['frameWidth','frameHeight','pivot','standingHeight']:check(p[key]==b[key],key)
for state,base in zip(p['states'],b['states']):
 for key in ['frameDurationsMs','loop','waterKinds','waterPoses','facings']:check(state[key]==base[key],key)
 for file in state['frameFiles']:
  im=Image.open(HERE/file).convert('RGBA');box=im.getchannel('A').getbbox();check(im.size==(256,256) and box[0]>0 and box[1]>0 and box[2]<256 and box[3]<256,'bounds');check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==h[file],'hash')
component=Image.open(HERE.parent/r['donor']).convert('RGBA')
for reg in r['frames']:
 file=reg['file'];a=np.array(Image.open(HERE/file).convert('RGBA'));ba=np.array(Image.open(BARE/file).convert('RGBA'));erase=Image.new('L',(256,256));ImageDraw.Draw(erase).polygon(reg['erasePolygon'],fill=255);expected=ba.copy();expected[np.array(erase)>0]=0;result=Image.fromarray(expected);result.alpha_composite(component,tuple(reg['offset']));expected=np.array(result);yy,xx=np.indices((256,256));x,y=reg['foregroundMaxXMinY'];fg=(yy>=y)&(xx<=x)&(ba[:,:,3]>0);expected[fg]=ba[fg];check(np.array_equal(a,expected),'exact canonical composition');check(np.array_equal(a[reg['protectedBodyFromY']:],ba[reg['protectedBodyFromY']:]),'protected body');check(np.array_equal(a[fg],ba[fg]),'foreground ownership');check(reg['scale']==1,'native helmet scale');check(hashlib.sha256((HERE.parent/r['donor']).read_bytes()).hexdigest()==reg['donorSha256'],'donor hash')
start=p['states'][0];stop=p['states'][1]
for i in range(6):check(np.array_equal(np.array(Image.open(HERE/start['frameFiles'][i])),np.array(Image.open(HERE/stop['frameFiles'][5-i]))),'exact reverse')
for file,authority,offset in zip([start['frameFiles'][0],start['frameFiles'][-1]],r['endpointAuthorities'],r['endpointOffsets']):
 canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(Image.open(HERE.parent/authority).convert('RGBA'),tuple(offset));check(np.array_equal(np.array(canvas),np.array(Image.open(HERE/file))),'exact equipped endpoint')
(HERE/'verification.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'paired clocks,exact component/composition/endpoints/reverse,protected bodies/hashes; visual/native acceptance separate'},indent=2)+'\n');print(str(checks)+' checks PASS')
