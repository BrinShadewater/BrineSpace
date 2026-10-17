from pathlib import Path
import json,numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parent.parent;inv=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text());records=[]
for action in ['kneel','repair','stand']:
 for face in ['south','east','north','west']:
  v=inv['resolved']['bare'][action+'-'+face];s=v['state'];mp=R/v['manifest'].removeprefix('res://')
  for i,relative in enumerate(s['frameFiles']):
   q=R/relative.removeprefix('res://') if relative.startswith('res://') else mp.parent/relative;a=np.array(Image.open(q).convert('RGBA'));yy,xx=np.indices(a.shape[:2]);r=a[:,:,:3].astype(float)
   mask=(a[:,:,3]>180)&(yy<145)&(xx>50)&(xx<150)&(r[:,:,0]>r[:,:,1]*1.025)&(r[:,:,0]>r[:,:,2]*1.035)&(r[:,:,2]>r[:,:,1]*.65)&(r.mean(2)>40)
   labs,n=label(mask);candidates=[]
   for k in range(1,n+1):
    y,x=np.where(labs==k)
    if len(x)>=35 and x.max()-x.min()<40 and y.max()-y.min()<40:candidates.append((len(x),k))
   k=max(candidates)[1];y,x=np.where(labs==k);bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];records.append({'state':s['id'],'frame':i,'source':q.relative_to(R).as_posix(),'headSkinBox':bbox,'skinPixels':len(x)})
(P/'head-tracking.json').write_text(json.dumps(records,indent=2));print(json.dumps({'trackedBareFrames':len(records)}))
