from pathlib import Path
import json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent
original=np.asarray(Image.open(P/'registered-reference.png').convert('RGBA'));control=np.asarray(Image.open(P/'input-alpha-control.png').convert('RGBA'))
frames=[np.asarray(Image.open(p).convert('RGBA')) for p in sorted((P/'full-clip-frames-v2').glob('*.png'))]
rgb=original[:,:,:3].astype(int);region=np.zeros((256,256),bool);region[150:175,110:135]=True
mask=region&(original[:,:,3]>200)&(control[:,:,3]>200)&(np.ptp(rgb,axis=2)<25)&(rgb[:,:,0]<110)&(rgb.mean(2)>20)
for a in frames:mask&=a[:,:,3]>200
assert mask.sum()>100
def sample(a):return dict(median=np.median(a[:,:,:3][mask],axis=0).tolist(),mean=np.mean(a[:,:,:3][mask],axis=0).tolist(),originalMAE=float(np.abs(a[:,:,:3].astype(float)[mask]-rgb[mask]).mean()))
rows=[dict(frame=n,**sample(a)) for n,a in enumerate(frames)]
out=dict(commonPixelCount=int(mask.sum()),original=sample(original),inputAlphaControl=sample(control),rows=rows,medianRanges=[[min(r['median'][i] for r in rows),max(r['median'][i] for r in rows)] for i in range(3)],scope='Identical fixed original spatial cloth pixels common-opaque in all142source frames and extraction control, below arms. No per-frame mask coverage change. Not proof of anatomical pixel correspondence or full material acceptance; no art edits.')
(P/'common-cloth-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(pixels=out['commonPixelCount'],original=out['original'],control=out['inputAlphaControl'],samples=[rows[n] for n in [0,71,141]],range=out['medianRanges'])))
