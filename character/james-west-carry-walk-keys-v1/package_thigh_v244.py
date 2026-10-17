from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-construction-phase0-v244';d=json.loads((out/'inputs.json').read_bytes());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(out/'prompt.txt')==d['promptSha256']
base=r/d['baseFolder'];box=d['cropBox'];raw=Image.open(out/'raw.png').convert('RGBA');generated=raw.resize((40,40),Image.Resampling.LANCZOS);g=np.array(generated)
b=np.array(Image.open(base/'bare-head-protected.png').convert('RGBA'));h=np.array(Image.open(base/'helmet-head-protected.png').convert('RGBA'))
opaque=Image.fromarray(np.uint8(b[:,:,3]>=250)*255).filter(ImageFilter.MinFilter(3));mask=np.zeros((256,256),bool);x0,y0,x1,y1=d['admissionRectangle'];mask[y0:y1,x0:x1]=True;mask&=np.array(opaque)>0
plate=np.zeros_like(b);plate[box[1]:box[3],box[0]:box[2]]=g;mask&=plate[:,:,3]>=250
bb=b.copy();hh=h.copy();bb[mask,:3]=plate[mask,:3];hh[mask,:3]=plate[mask,:3]
assert np.array_equal(bb[:,:,3],b[:,:,3]) and np.array_equal(hh[:,:,3],h[:,:,3])
assert np.array_equal(bb[~mask],b[~mask]) and np.array_equal(hh[~mask],h[~mask]) and np.array_equal(bb[110:],hh[110:])
for name,arr in [('bare',bb),('helmet',hh)]:Image.fromarray(arr).save(out/f'{name}-head-protected.png')
def luma(arr):return arr[:,:3]@np.array([.2126,.7152,.0722])
report=dict(rawSize=raw.size,admittedPixels=int(mask.sum()),outsidePixelsExact=int((~mask).sum()),alphaExact=True,outerOnePixelRingExact=True,outsideRectangleExact=True,pairedBodyBelow110Exact=True,medianBefore=float(np.median(luma(b[mask]))),medianAfter=float(np.median(luma(bb[mask]))),p95Before=float(np.percentile(luma(b[mask]),95)),p95After=float(np.percentile(luma(bb[mask]),95)),sourceAcceptance=False,normalChanged=False)
(out/'package-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGBA',(768,300),(47,59,63,255));draw=ImageDraw.Draw(board)
for i,(label,im) in enumerate([('Original thigh construction',Image.fromarray(b).crop(box)),('Generated candidate',generated),('Protected candidate',Image.fromarray(bb).crop(box))]):
 board.alpha_composite(im.resize((240,240),Image.Resampling.NEAREST),(i*256,30));draw.text((i*256+4,5),label,fill='white')
board.convert('RGB').save(out/'thigh-detail-review.png')
board=Image.new('RGBA',(1024,560),(47,59,63,255));draw=ImageDraw.Draw(board)
for i,phase in enumerate([48,0,1,2]):
 row=json.loads((p/'material-repair-progress.json').read_bytes())['states'][phase]
 for j,gear in enumerate(['bare','helmet']):
  f=out/f'{gear}-head-protected.png' if phase==0 else r/row['candidateSources'][gear]['file'];im=Image.open(f).convert('RGBA');board.alpha_composite(im,(i*256,j*280+20));draw.text((i*256+4,j*280+5),f'{gear} phase{phase}',fill='white')
board.convert('RGB').save(out/'paired-neighbor-review.png')
print(json.dumps(report))
