from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'master-material-v49'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:
    assert all(sha(r/f)==v for f,v in d[group].items())
assert sha(out/'prompt.txt')==d['promptSha256']
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
candidate=raw.resize((256,256),Image.Resampling.LANCZOS);candidate.save(out/'bare-candidate.png')
target=Image.open(p/'master-head-review-v16/bare-000.png').convert('RGBA')
guarded=candidate.copy();guarded.paste(target.crop((0,0,256,104)),(0,0));guarded.save(out/'bare-head-protected.png')
helmet=guarded.copy();helmet_source=Image.open(p/'master-head-review-v16/helmet-000.png').convert('RGBA')
helmet.paste(helmet_source.crop((102,62,155,110)),(102,62));helmet.save(out/'helmet-head-protected.png')
assert np.array_equal(np.asarray(guarded)[:104],np.asarray(target)[:104])
assert np.array_equal(np.asarray(helmet)[110:],np.asarray(guarded)[110:])
paired=Image.new('RGBA',(768,560),(47,58,63,255));pd=ImageDraw.Draw(paired)
for row,mode in enumerate(['bare','helmet']):
    for col,(label,f) in enumerate([('before',p/'master-head-review-v16'/(mode+'-000.png')),('protected material',out/(mode+'-head-protected.png')),('carrying reference',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png' if mode=='bare' else r/'character/james-carry-authored-helmet-v1/frames/004.png')]):
        paired.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));pd.text((col*256+6,row*280+6),mode+' '+label,fill='white')
paired.save(out/'paired-protected-review.png')
files=[r/'character/james-west-master-carry-v1/registered-original-master.png',p/'master-head-review-v16/bare-000.png',out/'bare-candidate.png',r/'character/james-west-master-carry-v1/local-v3-carry-pose.png']
labels=['original master','before walking entry','material candidate','carrying case reference']
board=Image.new('RGBA',(1024,280),(47,58,63,255));draw=ImageDraw.Draw(board)
metrics=[]
for col,(f,label) in enumerate(zip(files,labels)):
    im=Image.open(f).convert('RGBA');assert im.size==(256,256)
    board.alpha_composite(im,(col*256,24));draw.text((col*256+6,6),label,fill='white')
    a=np.asarray(im);ys,xs=np.where(a[:,:,3]>=128)
    hy,hx=np.where(a[62:104,:,3]>=128)
    metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),alpha128Bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],headRegion62to104Bounds=[int(hx.min()),int(hy.min()+62),int(hx.max()+1),int(hy.max()+63)]))
board.save(out/'native-material-comparison.png')
board.resize((2048,560),Image.Resampling.NEAREST).save(out/'enlarged-material-comparison.png')
before=np.asarray(Image.open(files[1]).convert('RGBA'));after=np.asarray(candidate)
report=dict(rawSize=list(raw.size),normalization='Full square canvas resampled once to256; no bbox fitting or color grading.',sourceMetrics=metrics,headPixelsExact=bool(np.array_equal(before[62:104],after[62:104])),visualReviewPending=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
(out/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
rasters=[f.relative_to(r).as_posix() for f in out.glob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(report))
