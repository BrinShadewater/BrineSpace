from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'local-material-phase4-v90';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
assert sha(out/'prompt.txt')==d['promptSha256']
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
crop=raw.resize((96,96),Image.Resampling.LANCZOS);crop.save(out/'native-generated-crop.png')
base_file=p/'master-head-review-v16/bare-004.png';base=np.asarray(Image.open(base_file).convert('RGBA'));source=base.copy();source[104:200,80:176]=np.asarray(crop)
interior=base[:,:,3]>=250
for dy in range(-2,3):
    for dx in range(-2,3):interior &= np.roll(np.roll(base[:,:,3]>=250,dy,axis=0),dx,axis=1)
requested=np.zeros((256,256),bool);requested[110:200,80:176]=True
mask=requested & interior & (source[:,:,3]>=250)
body=base.copy();body[mask,:3]=source[mask,:3]
assert np.array_equal(body[~mask],base[~mask]) and np.array_equal(body[:,:,3],base[:,:,3])
assert np.array_equal(body[:110],base[:110]) and np.array_equal(body[200:],base[200:])
Image.fromarray(body).save(out/'bare-head-protected.png')
helmet_base=np.asarray(Image.open(p/'master-head-review-v16/helmet-004.png').convert('RGBA'));helmet=helmet_base.copy();helmet[mask,:3]=source[mask,:3]
assert np.array_equal(helmet[~mask],helmet_base[~mask]) and np.array_equal(helmet[110:],body[110:])
Image.fromarray(helmet).save(out/'helmet-head-protected.png')
paired=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(paired)
for row,mode in enumerate(['bare','helmet']):
    for col,(label,f) in enumerate([('actual original4',p/f'master-head-review-v16/{mode}-004.png'),('local material trial',out/f'{mode}-head-protected.png'),('previous phase3',p/f'textile-detail-phase3-v83/{mode}-head-protected.png')]):
        paired.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));draw.text((col*256+5,row*280+5),mode+' '+label,fill='white')
paired.save(out/'paired-local-review.png')
cropboard=Image.new('RGBA',(768,408),(47,58,63,255));draw=ImageDraw.Draw(cropboard)
for col,(label,im) in enumerate([('before crop',Image.fromarray(base).crop((80,104,176,200))),('generated crop',crop),('protected crop',Image.fromarray(body).crop((80,104,176,200)))]):
    cropboard.alpha_composite(im.resize((256,256),Image.Resampling.NEAREST),(col*256,24));draw.text((col*256+5,5),label,fill='white')
cropboard.save(out/'crop-detail-review.png')
ys,xs=np.where(body[:,:,3]>=128)
report=dict(sourceSha256={base_file.relative_to(r).as_posix():sha(base_file)},rawSize=list(raw.size),cropNormalization='Full raw square resampled once to original96crop; no fitting, translation or warp.',admittedPixelCount=int(mask.sum()),outsideExactPixels=int((~mask).sum()),changedPixels=int(np.any(body!=base,axis=2).sum()),alphaExact=True,outerTwoPixelRingExact=True,headTop110Exact=True,bootsBelow200Exact=True,pairedBodyBelow110Exact=True,alpha128Bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
(out/'package-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
