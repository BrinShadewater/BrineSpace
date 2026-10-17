from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib,sys
p=Path(__file__).resolve().parent;r=p.parents[1];phase=int(sys.argv[1]);version=int(sys.argv[2]);out=p/f'lower-material-phase{phase}-v{version}';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes());baseversion=d['baseVersion'];basefolder=r/d['baseFolder'] if 'baseFolder' in d else p/f'local-material-phase{phase}-v{baseversion}'
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
assert sha(out/'prompt.txt')==d['promptSha256']
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width==raw.height
crop=raw.resize((96,96),Image.Resampling.LANCZOS);crop.save(out/'native-generated-crop.png')
base=np.asarray(Image.open(basefolder/'bare-head-protected.png').convert('RGBA'));source=base.copy();source[160:256,80:176]=np.asarray(crop)
interior=base[:,:,3]>=250
for dy in range(-1,2):
    for dx in range(-1,2):interior &= np.roll(np.roll(base[:,:,3]>=250,dy,axis=0),dx,axis=1)
requested=np.zeros((256,256),bool);requested[181:236,80:176]=True
for x0,y0,x1,y1 in d.get('protectedRectangles',[]):requested[y0:y1,x0:x1]=False
mask=requested & interior & (source[:,:,3]>=250)
body=base.copy();body[mask,:3]=source[mask,:3]
assert np.array_equal(body[~mask],base[~mask]) and np.array_equal(body[:,:,3],base[:,:,3]) and np.array_equal(body[:181],base[:181])
Image.fromarray(body).save(out/'bare-head-protected.png')
helmet_base=np.asarray(Image.open(basefolder/'helmet-head-protected.png').convert('RGBA'));helmet=helmet_base.copy();helmet[mask,:3]=source[mask,:3]
assert np.array_equal(helmet[~mask],helmet_base[~mask]) and np.array_equal(helmet[110:],body[110:])
for x0,y0,x1,y1 in d.get('protectedRectangles',[]):
    assert np.array_equal(body[y0:y1,x0:x1],base[y0:y1,x0:x1]) and np.array_equal(helmet[y0:y1,x0:x1],helmet_base[y0:y1,x0:x1])
Image.fromarray(helmet).save(out/'helmet-head-protected.png')
board=Image.new('RGBA',(768,408),(47,58,63,255));draw=ImageDraw.Draw(board)
for col,(label,im) in enumerate([('before lower crop',Image.fromarray(base).crop((80,160,176,256))),('generated lower crop',crop),('protected lower crop',Image.fromarray(body).crop((80,160,176,256)))]):
    board.alpha_composite(im.resize((256,256),Image.Resampling.NEAREST),(col*256,24));draw.text((col*256+5,5),label,fill='white')
board.save(out/'lower-detail-review.png')
paired=Image.new('RGBA',(768,560),(47,58,63,255));draw=ImageDraw.Draw(paired)
neighbor_folder=(r/d['neighborSource']).parent if 'neighborSource' in d else p/('lower-material-phase5-v98' if version>=99 else 'textile-detail-phase3-v83')
neighbor_label=d.get('neighborLabel','phase5 provisional finish' if version>=99 else 'phase3 provisional finish')
for row,mode in enumerate(['bare','helmet']):
    for col,(label,f) in enumerate([('before lower repair',basefolder/f'{mode}-head-protected.png'),('protected lower repair',out/f'{mode}-head-protected.png'),(neighbor_label,neighbor_folder/f'{mode}-head-protected.png')]):
        paired.alpha_composite(Image.open(f).convert('RGBA'),(col*256,row*280+24));draw.text((col*256+5,row*280+5),mode+' '+label,fill='white')
paired.save(out/'paired-lower-review.png')
ys,xs=np.where(body[:,:,3]>=128);luma=lambda a:a[:,:,:3]@[.2126,.7152,.0722]
metrics={label:[round(float(v),2) for v in np.percentile(luma(a)[mask],[25,50,75,95])] for label,a in [('before',base),('after',body)]}
report=dict(rawSize=list(raw.size),cropNormalization='Full square normalized once to96crop at original coordinates; no fit/warp/regrade.',admittedPixelCount=int(mask.sum()),outsideExactPixels=int((~mask).sum()),changedPixels=int(np.any(body!=base,axis=2).sum()),alphaExact=True,outerOnePixelRingExact=True,allRowsAbove181Exact=True,pairedBodyBelow110Exact=True,alpha128Bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],localLumaQuartilesAnd95=metrics,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False)
report.update(protectedRectangles=d.get('protectedRectangles',[]),protectedRectanglesExact=True)
(out/'package-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
