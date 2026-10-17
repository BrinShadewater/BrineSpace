from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-material-keys-v50'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
atlas=raw.resize((768,768),Image.Resampling.LANCZOS);atlas.save(out/'normalized-atlas.png')
metrics=[];master=Image.open(r/'character/james-west-master-carry-v1/registered-original-master.png').convert('RGBA')
for group in range(3):
    board=Image.new('RGBA',(768,840),(47,58,63,255));draw=ImageDraw.Draw(board)
    for row,cell in enumerate(range(group*3,group*3+3)):
        index=d['indices'][cell];before=Image.open(p/'master-head-review-v16'/('bare-%03d.png'%index)).convert('RGBA')
        after=atlas.crop((cell%3*256,cell//3*256,cell%3*256+256,cell//3*256+256));after.save(out/('raw-cell-%03d.png'%index))
        for col,(label,im) in enumerate([('original master',master),('before'+str(index),before),('atlas edit'+str(index),after)]):
            board.alpha_composite(im,(col*256,row*280+24));draw.text((col*256+5,row*280+5),label,fill='white')
        bounds=[]
        for im in [before,after]:
            ys,xs=np.where(np.asarray(im)[:,:,3]>=128);bounds.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
        metrics.append(dict(slot=index,beforeBounds=bounds[0],afterBounds=bounds[1]))
    board.save(out/('native-review-%d.png'%group))
(out/'review.json').write_text(json.dumps(dict(rawSize=list(raw.size),metrics=metrics,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,disposition='reject_atlas_geometry_drift',visualReviewPending=True),indent=2)+'\n')
print(json.dumps(dict(rawSize=list(raw.size),metrics=metrics)))
