from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];checks=0
def check(ok,message):
    global checks
    checks+=1
    if not ok:raise AssertionError(message)
reg=json.loads((P/'registration.json').read_text());hashes=json.loads((P/'frame-hashes.json').read_text());bounds={};rows={}
for field,hashfield in [('source','sourceSha256'),('helmetSource','helmetSourceSha256')]:check(hashlib.sha256((R/reg[field]).read_bytes()).hexdigest()==reg[hashfield],'immutable source')
check(len({t['fixedScale'] for t in reg['tracking']})==1,'fixed atlas density')
for mode in ['bare','helmet']:
    pack=json.loads((P/(mode+'-manifest.json')).read_text());check(len(pack['states'])==1,'one West water death state');s=pack['states'][0];prior=json.loads((P.parent/'james-death-family-v1'/(mode+'-manifest.json')).read_text());old=next(st for st in prior['states'] if st['id']==s['id'])
    for field in ['frameDurationsMs','loop','waterPoses','waterKinds','facings']:check(s.get(field)==old.get(field),'retained finite contract '+field)
    check(not s['loop'],'finite death')
    images=[];extents=[]
    for file in s['frameFiles']:
        im=Image.open(P/file).convert('RGBA');a=np.array(im);images.append(a)
        check(im.size==(256,360),'canvas');check(hashlib.sha256((P/file).read_bytes()).hexdigest()==hashes[file],'frame hash');check(a[:,:,3].min()==0 and a[:,:,3].max()>180,'alpha');check(not np.any(a[[0,-1],:,3]) and not np.any(a[:,[0,-1],3]),'unclipped')
        x0,y0,x1,y1=im.getbbox();extents.append([(x0-128)*65.28/148,(y0-224)*65.28/148,(x1-128)*65.28/148,(y1-224)*65.28/148])
    endpoint=Image.open(P.parent/'james-air-family-v1/endpoints'/mode/'swim-west.png').convert('RGBA');check(np.array_equal(np.array(endpoint),images[0]),'exact selected swim entry')
    master_right=endpoint.getbbox()[2]-1
    for a in images[1:]:
        yy,xx=np.where(a[:,:,3]>0)
        check(abs(int(xx.max())-master_right)<=7,'compact projected boot reach against fixed-head selected swim')
    bounds[mode]={'death-water-west':[min(e[0] for e in extents),min(e[1] for e in extents),max(e[2] for e in extents),max(e[3] for e in extents)]};rows[mode]=images
for i in range(1,6):
    b,h=rows['bare'][i],rows['helmet'][i];x0,y0,x1,y1=reg['tracking'][i]['editRegion'];mask=np.ones(b.shape[:2],bool);mask[y0:y1,x0:x1]=False;check(np.array_equal(b[mask],h[mask]),'owned helmet region')
(P/'clearance-evidence.json').write_text(json.dumps(dict(bounds=bounds,scope='Union of candidate alpha envelopes; test actual selected room blocker gate without changing clearance'),indent=2)+'\n')
(P/'package-verification.json').write_text(json.dumps(dict(checks=checks,failures=0),indent=2)+'\n')
print(str(checks)+' package checks PASS; source/clock/head ownership contracts only')
