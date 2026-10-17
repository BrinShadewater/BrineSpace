from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'detail-phase2-v75';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
assert sha(out/'prompt.txt')==d['promptSha256']
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
whole=raw.resize((256,256),Image.Resampling.LANCZOS);whole.save(out/'bare-whole-candidate.png')
base=Image.open(p/'master-material-phase2-v69/bare-head-protected.png').convert('RGBA')
bare=whole.copy();bare.paste(base.crop((0,0,256,104)),(0,0));bare.save(out/'bare-head-protected.png')
helmet=bare.copy();cap=Image.open(p/'master-material-phase2-v69/helmet-head-protected.png').convert('RGBA')
helmet.paste(cap.crop((102,62,155,110)),(102,62));helmet.save(out/'helmet-head-protected.png')
assert np.array_equal(np.asarray(bare)[:104],np.asarray(base)[:104])
assert np.array_equal(np.asarray(helmet)[110:],np.asarray(bare)[110:])
metrics=[]
fs=[('original master',r/'character/james-west-master-carry-v1/registered-original-master.png'),('before V69',p/'master-material-phase2-v69/bare-head-protected.png'),('detail candidate V75',out/'bare-head-protected.png'),('original stride2',p/'master-head-review-v16/bare-002.png'),('previous phase1',p/'master-material-phase1-v66/bare-head-protected.png'),('next phase3',p/'master-material-phase3-v70/bare-head-protected.png')]
board=Image.new('RGBA',(1536,280),(47,58,63,255));draw=ImageDraw.Draw(board)
for col,(label,f) in enumerate(fs):
    im=Image.open(f).convert('RGBA');board.alpha_composite(im,(col*256,24));draw.text((col*256+5,5),label,fill='white')
    ys,xs=np.where(np.asarray(im)[:,:,3]>=128)
    metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),alpha128Bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
board.save(out/'detail-and-neighbor-review.png')
paired=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(paired)
for row,mode in enumerate(['bare','helmet']):
    for col,(label,f) in enumerate([('before V69',p/f'master-material-phase2-v69/{mode}-head-protected.png'),('detail candidate V75',out/f'{mode}-head-protected.png'),('original stride2',p/f'master-head-review-v16/{mode}-002.png')]):
        paired.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));draw.text((col*256+5,row*280+5),mode+' '+label,fill='white')
paired.save(out/'paired-protected-review.png')
(out/'package-review.json').write_text(json.dumps(dict(rawSize=list(raw.size),metrics=metrics,normalization='Full canvas resampled once256, exact original head104rows/cap restored. No bbox fitting or grade.',headProtectedPixels=26624,pairedBodyBelow110Exact=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
print(json.dumps(dict(rawSize=list(raw.size),bounds=[x['alpha128Bounds'] for x in metrics],sourceAcceptance=False)))
