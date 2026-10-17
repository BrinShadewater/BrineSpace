from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,sys
p=Path(__file__).resolve().parent;r=p.parents[1];phase=int(sys.argv[1]);version=int(sys.argv[2]);out=p/f'master-detail-phase{phase}-v{version}';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
assert sha(out/'prompt.txt')==d['promptSha256']
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
whole=raw.resize((256,256),Image.Resampling.LANCZOS);whole.save(out/'bare-whole-candidate.png')
base_file=p/f'master-head-review-v16/bare-{phase:03d}.png';base=np.asarray(Image.open(base_file).convert('RGBA'));generated=np.asarray(whole)
by,bx=np.where(base[:,:,3]>=128);gy,gx=np.where(generated[:,:,3]>=128)
original_bounds=[int(bx.min()),int(by.min()),int(bx.max()+1),int(by.max()+1)]
generated_bounds=[int(gx.min()),int(gy.min()),int(gx.max()+1),int(gy.max()+1)]
if abs(original_bounds[1]-generated_bounds[1])>3 or abs(original_bounds[3]-generated_bounds[3])>3:
    rejection=dict(phase=phase,status='rejected_before_protected_derivative_packaging',reason='Same-pose generated crown/sole registration differs by more than3native pixels. Silhouette masking cannot repair internal anatomy.',originalBounds=original_bounds,generatedBounds=generated_bounds,sourceAcceptance=False,normalChanged=False)
    (out/'registration-rejection.json').write_text(json.dumps(rejection,indent=2)+'\n')
    print(json.dumps(rejection));raise SystemExit(2)
interior=base[:,:,3]>=250
for dy in range(-2,3):
    for dx in range(-2,3):interior &= np.roll(np.roll(base[:,:,3]>=250,dy,axis=0),dx,axis=1)
mask=interior & (generated[:,:,3]>=250);mask[:104]=False
body=base.copy();body[mask,:3]=generated[mask,:3]
assert np.array_equal(body[:,:,3],base[:,:,3]) and np.array_equal(body[~mask],base[~mask])
assert np.array_equal(body[:104],base[:104])
Image.fromarray(body).save(out/'bare-head-protected.png')
helmet=Image.fromarray(body);old_helmet=Image.open(p/f'master-head-review-v16/helmet-{phase:03d}.png').convert('RGBA')
helmet.paste(old_helmet.crop((102,62,155,110)),(102,62));helmet.save(out/'helmet-head-protected.png')
assert np.array_equal(np.asarray(helmet)[110:],body[110:])
paired=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(paired)
for row,mode in enumerate(['bare','helmet']):
    fs=[('actual before',p/f'master-head-review-v16/{mode}-{phase:03d}.png'),('protected detail',out/f'{mode}-head-protected.png'),('carry reference',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png' if mode=='bare' else r/'character/james-carry-authored-helmet-v1/frames/004.png')]
    for col,(label,f) in enumerate(fs):
        im=Image.open(f).convert('RGBA');paired.alpha_composite(im,(col*256,row*280+24));draw.text((col*256+5,row*280+5),f'{mode} phase{phase} {label}',fill='white')
        if col==0:
            before=Image.new('RGBA',(256,256),(47,58,63,255));before.alpha_composite(im)
            assert np.array_equal(np.asarray(before),np.asarray(paired.crop((0,row*280+24,256,row*280+280))))
paired.save(out/'paired-protected-review.png')
board=Image.new('RGBA',(1024,280),(47,58,63,255));draw=ImageDraw.Draw(board)
fs=[('original master',r/'character/james-west-master-carry-v1/registered-original-master.png'),('actual original stride',base_file),('whole generated detail',out/'bare-whole-candidate.png'),('protected detail',out/'bare-head-protected.png')]
metrics=[]
for col,(label,f) in enumerate(fs):
    im=Image.open(f).convert('RGBA');board.alpha_composite(im,(col*256,24));draw.text((col*256+5,5),label,fill='white')
    ys,xs=np.where(np.asarray(im)[:,:,3]>=128);metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),alpha128Bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
board.save(out/'master-comparison.png')
report=dict(phase=phase,rawSize=list(raw.size),metrics=metrics,normalization='Full square normalized once256. Authored RGB admitted inside original opaque silhouette; original alpha and outer two-pixel ring unchanged. No fitting/warp/regrade.',alphaPlaneExact=True,outerTwoPixelRingExact=True,headTop104Exact=True,pairedBodyBelow110Exact=True,admittedPixelCount=int(mask.sum()),changedPixels=int(np.any(body!=base,axis=2).sum()),outsideExactPixels=int((~mask).sum()),pairedBeforeColumnPhase=phase,pairedBeforeBaselinesPixelVerified=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
(out/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(phase=phase,admitted=report['admittedPixelCount'],bounds=[m['alpha128Bounds'] for m in metrics],alphaExact=True)))
