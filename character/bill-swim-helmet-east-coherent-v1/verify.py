from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from PIL import ImageDraw
HERE=Path(__file__).resolve().parent;BARE=HERE.parent/'bill-swim-east-coherent-v1'
p=json.loads((HERE/'manifest.json').read_text());b=json.loads((BARE/'manifest.json').read_text());h=json.loads((HERE/'frame-hashes.json').read_text());r=json.loads((HERE/'helmet-registration.json').read_text());checks=0
def check(v,m):
 global checks
 assert v,m
 checks+=1
for key in ['frameWidth','frameHeight','pivot','standingHeight','strideDistanceCells']:check(p[key]==b[key],key)
s=p['states'][0];bs=b['states'][0]
for key in ['frameDurationsMs','loop','waterKinds','waterPoses','facings','depthOffsets']:check(s[key]==bs[key],key)
donor=Image.open(HERE.parent/r['frames'][0]['donor']).convert('RGBA');mask=Image.new('L',donor.size);ImageDraw.Draw(mask).polygon(r['polygon'],fill=255);da=np.array(donor);da[:,:,3]=np.minimum(da[:,:,3],np.array(mask));da[da[:,:,3]==0]=0
component=Image.fromarray(da);stored=Image.open(HERE/'sources/canonical-head.png').convert('RGBA');check(np.array_equal(np.array(stored),da[20:59,72:115]),'exact canonical source component')
for file,reg in zip(s['frameFiles'],r['frames']):
 a=np.array(Image.open(HERE/file).convert('RGBA'));ba=np.array(Image.open(BARE/file).convert('RGBA'));yy,xx=np.indices(a.shape[:2]);protected=(yy>=95)|(xx<124)|(xx>=167)
 check(np.array_equal(a[protected],ba[protected]),'protected body');fg=(yy>=88)&(xx>=154)&(ba[:,:,3]>0);check(np.array_equal(a[fg],ba[fg]),'forward sleeve foreground');check(reg['offset']==[52,36] and reg['scale']==1,'fixed canonical registration');check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==h[file],'hash');box=Image.fromarray(a[:,:,3]).getbbox();check(box[0]>0 and box[2]<208 and box[1]>0 and box[3]<184,'clipping')
 erase=Image.new('L',(208,184));ImageDraw.Draw(erase).polygon([(136,61),(164,61),(164,87),(146,90),(135,81)],fill=255);expected=ba.copy();expected[np.array(erase)>0]=0;canvas=Image.fromarray(expected);canvas.alpha_composite(component,(52,36));expected=np.array(canvas);expected[fg]=ba[fg];check(np.array_equal(a,expected),'exact canonical composition');check(hashlib.sha256((HERE.parent/reg['donor']).read_bytes()).hexdigest()==reg['donorSha256'],'donor hash')
(HERE/'verification.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'source/frame/registration/body-preservation and paired-clock checks; visual/native acceptance separate'},indent=2)+'\n')
print(str(checks)+' checks PASS')
