from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-swim-west-coherent-v1'
p=json.loads((HERE/'manifest.json').read_text());b=json.loads((BARE/'manifest.json').read_text());r=json.loads((HERE/'helmet-registration.json').read_text());h=json.loads((HERE/'frame-hashes.json').read_text());checks=0
def check(v,m):
 global checks
 assert v,m
 checks+=1
for key in ['frameWidth','frameHeight','pivot','standingHeight','strideDistanceCells']:check(p[key]==b[key],key)
for key in ['frameDurationsMs','loop','waterKinds','waterPoses','facings','depthOffsets']:check(p['states'][0][key]==b['states'][0][key],key)
donor=Image.open(HERE.parent/r['donor']).convert('RGBA');check(hashlib.sha256((HERE.parent/r['donor']).read_bytes()).hexdigest()==r['donorSha256'],'canonical donor hash');check(np.array_equal(np.array(donor),np.array(Image.open(HERE/'sources/canonical-head.png'))),'exact stored donor')
for reg in r['frames']:
 file=reg['file'];original=Image.open(BARE/file).convert('RGBA');ba=np.array(original);a=np.array(Image.open(HERE/file).convert('RGBA'));mask=Image.new('L',original.size);ImageDraw.Draw(mask).polygon(r['erasePolygon'],fill=255);expected=ba.copy();expected[np.array(mask)>0]=0;canvas=Image.fromarray(expected);canvas.alpha_composite(donor,tuple(reg['position']));expected=np.array(canvas);yy,xx=np.indices(ba.shape[:2]);x,y=reg['foregroundMaxXMinY'];fg=(yy>=y)&(xx<=x)&(ba[:,:,3]>0);expected[fg]=ba[fg]
 check(np.array_equal(a,expected),'exact canonical composition');check(np.array_equal(a[reg['protectedBodyFromY']:],ba[reg['protectedBodyFromY']:]),'protected body');check(np.array_equal(a[fg],ba[fg]),'foreground ownership');check(hashlib.sha256((BARE/file).read_bytes()).hexdigest()==reg['bareBodySha256'],'bare body hash');check(reg['scale']==1 and reg['rotationDegrees']==0,'native canonical scale');check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==h[file],'frame hash');box=Image.fromarray(a[:,:,3]).getbbox();check(box[0]>0 and box[1]>0 and box[2]<p['frameWidth'] and box[3]<p['frameHeight'],'clipping')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'exact head/component composition,body/foreground preservation,paired metadata and hashes;visual/native acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(str(checks)+' checks PASS')

