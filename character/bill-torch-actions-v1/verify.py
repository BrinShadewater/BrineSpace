from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
pack=json.loads((HERE/'manifest.json').read_text());hashes=json.loads((HERE/'frame-hashes.json').read_text());states={s['id']:s for s in pack['states']}
checks=0
for state in pack['states']:
    assert len(state['frameFiles'])==len(state['frameDurationsMs'])==6;checks+=1
    assert state['loop']==state['id'].startswith('weld-');checks+=1
    assert sum(state['frameDurationsMs'])==(960 if state['loop'] else 520);checks+=1
    for rel in state['frameFiles']:
        a=np.asarray(Image.open(HERE/rel).convert('RGBA'))
        assert a.shape==(256,256,4);checks+=1
        assert np.any(a[:,:,3]>180) and not a[[0,-1],:,3].any() and not a[:,[0,-1],3].any();checks+=1
        assert hashlib.sha256((HERE/rel).read_bytes()).hexdigest()==hashes[rel];checks+=1
def pixels(key,index):return Image.open(HERE/states[key]['frameFiles'][index]).tobytes()
for d,folder in [('east','idle-east-breathing-v1'),('west','idle-west-breathing-v1'),('south','idle-south-matte-v2'),('north','idle-north-transition-matte-v1')]:
    idle=Image.new('RGBA',(256,256));idle.alpha_composite(Image.open(HERE.parent/'crew-runtime-matte-v1/bill/frames'/folder/'000.png').convert('RGBA'),(36,52))
    assert pixels('torch-draw-'+d,0)==idle.tobytes();checks+=1
    assert pixels('torch-stow-'+d,5)==idle.tobytes();checks+=1
    assert pixels('torch-draw-'+d,5)==pixels('weld-'+d,0);checks+=1
    assert pixels('weld-'+d,5)==pixels('torch-stow-'+d,0);checks+=1
for d in ['south','north']:
    for rel in states['weld-'+d]['frameFiles']:
        a=np.asarray(Image.open(HERE/rel).convert('RGBA'));yy,xx=np.indices(a.shape[:2])
        region=(a[:,:,3]>180)&(((yy>60)&(yy<100)&(xx>135)) if d=='north' else ((yy>130)&(yy<190)))
        orange=region&(a[:,:,0]>210)&(a[:,:,1]>110)&(a[:,:,2]<150)
        blue=region&(a[:,:,2]>180)&(a[:,:,1]>130)&(a[:,:,0]<180)
        oy,ox=np.where(orange);by,bx=np.where(blue)
        assert len(oy)>0 and len(by)>0;checks+=1
        assert (oy.mean()>by.mean()) if d=='south' else (oy.mean()<by.mean());checks+=1
report={'checks':checks,'failures':0,'clips':12,'exportedFrameReferences':72,'sourcePoses':72,'axialFlameDirection':'south down / north up','ownerVisualAcceptance':'pending'}
(HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
