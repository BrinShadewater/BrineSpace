from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2]
master=np.array(Image.open(R/'character/veld-east-held-original-master-v1/frames/bare/000.png').convert('RGBA')).astype(float)
candidate=np.array(Image.open(P/'frames/bare/000.png').convert('RGBA')).astype(float)
x0,y0,x1,y1=103,202,133,224
t=master[y0:y1,x0:x1,:3];alpha=master[y0:y1,x0:x1,3]
mask=(alpha>200)&(t[:,:,0]>t[:,:,1]+3)&(t[:,:,0]>t[:,:,2]+3)&(t.mean(2)>40)&(t.mean(2)<220)
assert mask.sum()>10
v=t[mask];v-=v.mean(0);den=np.sqrt((v*v).sum());best=None
for dy in range(-3,4):
 for dx in range(-6,7):
  w=candidate[y0+dy:y1+dy,x0+dx:x1+dx,:3][mask];w-=w.mean(0)
  score=float((v*w).sum()/max(1e-8,den*np.sqrt((w*w).sum())))
  if best is None or score>best[0]:best=(score,dx,dy)
rows=[]
for name,a in [('original',master),('candidate',candidate)]:
 # The screen-right far boot is separately visible at the distal end.
 # x134 overlaps the planted near toe in the candidate; x138 excludes it.
 y,x=np.where(a[202:224,138:172,3]>200)
 rows.append({'source':name,'screenRightDistalBootBottom':int(y.max()+202),'distalOpaquePixels':int(len(y))})
N=R/'output/veld-east-guided-lift-v1'
before=json.loads((N/'inputs-after.json').read_text(encoding='utf-8'))
assert all(hashlib.sha256((R/p).read_bytes()).hexdigest()==s for p,s in before.items())
report={'nearBootMaterialProxy':{'box':[x0,y0,x1,y1],'maskPixels':int(mask.sum()),'NCC':round(best[0],4),'dx':best[1],'dy':best[2]},'farBootExtent':rows,'farBootBox':[138,202,172,224],'supersedes':'native-review-v0-overlapping-boot-roi.json: x134 included planted near toe; its far-floor221 result invalid','nativeReview':{'bareComplete47_93_148':'viewed','helmetComplete47_93_148':'viewed','nativeInputsStillStable':len(before)},'scope':'Two-source diagnostic only. Independent near-boot warm-material correspondence can reveal a join displacement but does not prove rigid sole contact, anatomy identity through occlusion or final moving-root gait. Distal alpha floor is a silhouette extent, not a physical contact point. No artwork or frozen native inputs changed.'}
(P/'native-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
