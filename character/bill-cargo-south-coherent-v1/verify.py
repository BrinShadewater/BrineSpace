import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'manifest.json').read_text());legacy=json.loads((ROOT/'review-retained/manifest.json').read_text());old={s['id']:s for s in legacy['states']};hashes=json.loads((ROOT/'frame-hashes.json').read_text());checks=0
def check(value):
    global checks
    assert value;checks+=1
check(m['pivot']==[128,224]);check(m['standingHeight']==148)
states={s['id']:s for s in m['states']}
for s in m['states']:
    check(len(s['frameFiles'])==(6 if s['id']=='carry-south' else 12));check(s['loop']==old[s['id']]['loop'])
    check(sum(s['frameDurationsMs'])==sum(old[s['id']]['frameDurationsMs']))
    for field in ['facings','waterKinds','waterPoses','depthOffsets']:
        expected=old[s['id']][field]
        check(s[field]==(expected if s['id']=='carry-south' else [v for v in expected for _ in range(2)]))
    for f in s['frameFiles']:
        a=np.array(Image.open(ROOT/f));check(a.shape==(256,256,4));check(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==hashes[f])
        check(a[:,:,3].max()>180);check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any())
for a,b in zip(states['pickup-south']['frameFiles'],reversed(states['unload-south']['frameFiles'])):check((ROOT/a).read_bytes()==(ROOT/b).read_bytes())
check(len({(ROOT/f).read_bytes() for f in states['carry-south']['frameFiles']})==6)
check(len({(ROOT/f).read_bytes() for f in states['pickup-south']['frameFiles']})==12)
idle=Image.open(ROOT.parent/'crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png').convert('RGBA')
pad=Image.new('RGBA',(256,256));pad.alpha_composite(idle,(36,52));idle_a=np.array(pad)
first=np.array(Image.open(ROOT/states['pickup-south']['frameFiles'][0]));y,x=np.indices(first.shape[:2])
case=(first[:,:,3]>180)&(idle_a[:,:,3]==0)&(x>80)&(x<175)&(y>190)
check(int(case.sum())>100)
stride=[]
for f in states['carry-south']['frameFiles']:
    a=np.array(Image.open(ROOT/f));y,x=np.where(a[:,:,3]>180)
    stride.append(int(y[(x<128)&(y>190)].max())-int(y[(x>=128)&(y>190)].max()))
check(sum(v>=3 for v in stride)>=2);check(sum(v<=-3 for v in stride)>=2)
endpoint=np.array(Image.open(ROOT/states['pickup-south']['frameFiles'][-1]));ey,ex=np.where(endpoint[:,:,3]>180)
check(abs(int(ey.max()-ey.min()+1)-148)<=3)
print(f'South cargo:{checks} checks pass;30 references;timing/profile/alpha/hash/reverse/alternating gait checks')
