from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-return-v272';d=json.loads((out/'inputs.json').read_bytes());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items());assert sha(out/'prompt.txt')==d['promptSha256']
raw=Image.open(out/'raw.png').convert('RGBA');assert raw.width*2==raw.height*3 and raw.width%3==0 and raw.height%2==0;half=raw.width//3
board=Image.new('RGBA',(1536,560),(47,59,63,255));draw=ImageDraw.Draw(board);details=Image.new('RGBA',(1536,480),(47,59,63,255));dd=ImageDraw.Draw(details);reports=[]
for i,source in enumerate(d['sources']):
 phase=source['phase'];folder=out/f'phase{phase}';folder.mkdir(exist_ok=True);box=source['cropBox'];tile=raw.crop(((i%3)*half,(i//3)*half,(i%3+1)*half,(i//3+1)*half)).resize((96,96),Image.Resampling.LANCZOS);g=np.asarray(tile)
 b=np.asarray(Image.open(r/source['files']['bare']['file']).convert('RGBA'));h=np.asarray(Image.open(r/source['files']['helmet']['file']).convert('RGBA'))
 assert all(sha(r/row['file'])==row['sha256'] for row in source['files'].values())
 admission=Image.new('L',(256,256));ImageDraw.Draw(admission).polygon([tuple(xy) for xy in source['admissionPolygon']],fill=255)
 mask=np.asarray(admission)>0;mask&=np.asarray(Image.fromarray(np.uint8(b[:,:,3]>=250)*255).filter(ImageFilter.MinFilter(3)))>0
 plate=np.zeros_like(b);plate[box[1]:box[3],box[0]:box[2]]=g;mask&=plate[:,:,3]>=250
 for x0,y0,x1,y1 in source['protectedRectangles']:mask[y0:y1,x0:x1]=False
 if not source['edit']:mask[:]=False
 bb=b.copy();hh=h.copy();bb[mask,:3]=plate[mask,:3];hh[mask,:3]=plate[mask,:3]
 assert np.array_equal(bb[~mask],b[~mask]) and np.array_equal(hh[~mask],h[~mask]) and np.array_equal(bb[:,:,3],b[:,:,3]) and np.array_equal(hh[:,:,3],h[:,:,3]) and np.array_equal(bb[110:],hh[110:])
 for gear,a,original in [('bare',bb,b),('helmet',hh,h)]:
  for x0,y0,x1,y1 in source['protectedRectangles']:assert np.array_equal(a[y0:y1,x0:x1],original[y0:y1,x0:x1])
  Image.fromarray(a).save(folder/f'{gear}-head-protected.png');board.alpha_composite(Image.fromarray(a),(i*256,20+(gear=='helmet')*280));draw.text((i*256+3,5+(gear=='helmet')*280),f'{gear} phase{phase}',fill='white')
 for row,a,label in [(0,b,'Before'),(1,bb,'Joint candidate')]:
  im=Image.fromarray(a).crop((120,140,168,176)).resize((240,180),Image.Resampling.NEAREST);details.alpha_composite(im,(i*256,20+row*240));dd.text((i*256+3,3+row*240),f'{label} phase{phase}',fill='white')
 luma=lambda a:a[:,:3]@np.array([.2126,.7152,.0722])
 reports.append(dict(phase=phase,admittedPixels=int(mask.sum()),outsideExact=int((~mask).sum()),alphaExact=True,silhouetteExact=True,kneeExactBothGears=True,sharedBodyExact=True,medianBefore=float(np.median(luma(b[mask]))) if mask.any() else None,medianAfter=float(np.median(luma(bb[mask]))) if mask.any() else None,p95Before=float(np.percentile(luma(b[mask]),95)) if mask.any() else None,p95After=float(np.percentile(luma(bb[mask]),95)) if mask.any() else None))
board.save(out/'paired-source-review.png');details.save(out/'thigh-detail-review.png');(out/'package-review.json').write_text(json.dumps(dict(rawSize=raw.size,tiles=reports,selected=False,normalChanged=False,sourceAcceptance=False),indent=2)+'\n',encoding='utf-8');print(json.dumps(reports))
