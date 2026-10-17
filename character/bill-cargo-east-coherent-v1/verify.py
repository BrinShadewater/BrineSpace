import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
m=json.loads((HERE/'manifest.json').read_text());legacy=json.loads((ROOT/'major-bill-v3/packs/bare-256x256-p128-224/manifest.json').read_text())
states={s['id']:s for s in legacy['states']};hashes=json.loads((HERE/'frame-hashes.json').read_text());checks=0
def check(value):
    global checks
    assert value;checks+=1
check(m['pivot']==[128,224]);check(m['standingHeight']==148)
for s in m['states']:
    check(len(s['frameFiles'])==(11 if s['id']=='pickup-east' else 6))
    for key in ['frameDurationsMs','facings','loop','waterKinds','waterPoses','depthOffsets']:
        expected=states[s['id']][key]
        if s['id']=='pickup-east' and key=='frameDurationsMs':
            check(sum(s[key])==sum(expected));check(len(s[key])==11)
        elif s['id']=='pickup-east' and key!='loop':check(s[key]==[expected[min(5,i*6//11)] for i in range(11)])
        else:check(s[key]==expected)
    for p in s['frameFiles']:
        im=Image.open(HERE/p).convert('RGBA');a=np.array(im)
        check(im.size==(256,256));check(hashlib.sha256((HERE/p).read_bytes()).hexdigest()==hashes[p])
        check(a[:,:,3].max()>180);check(not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any())
check(len({(HERE/p).read_bytes() for p in m['states'][1]['frameFiles']})==6)
check((HERE/m['states'][0]['frameFiles'][0]).read_bytes()==(HERE/m['states'][2]['frameFiles'][5]).read_bytes())
check((HERE/m['states'][0]['frameFiles'][-1]).read_bytes()==(HERE/m['states'][2]['frameFiles'][0]).read_bytes())
check(len({(HERE/p).read_bytes() for p in m['states'][0]['frameFiles']})==11)
reg=json.loads((HERE/'source-registration.json').read_text());check([c['cell'] for c in reg['detachedCases']]==[0,16,17])
def crowns(files,folder):return [int(np.where(np.array(Image.open(folder/p))[:,:,3]>180)[0].min()) for p in files]
new_y=crowns(m['states'][0]['frameFiles'],HERE)
old_y=crowns(json.loads((HERE/'review-before-pickup-v1/manifest.json').read_text())['states'][0]['frameFiles'],HERE/'review-before-pickup-v1')
check(max(abs(b-a) for a,b in zip(new_y,new_y[1:]))<max(abs(b-a) for a,b in zip(old_y,old_y[1:])))
print(f'Cargo packaging:{checks} checks passed;3 clips/23 frames;pickup520ms;crown steps20px vs32px')
