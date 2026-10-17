"""Inspect complete generated case edits; no replacement selection or anatomy compositing."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects,binary_dilation
P=Path(__file__).resolve().parent
v=sys.argv[1];assert v in ['21','22']
O=P/('case-source-v'+v);O.mkdir(exist_ok=True)
paths=[P/'raw-far-swing-v20.png',P/'raw-case-surface-v21.png']
if v=='22':paths.append(P/'raw-case-surface-v22.png')
board=Image.new('RGB',(512*len(paths),1020),'#202a30');d=ImageDraw.Draw(board)
records=[];original=np.array(Image.open(paths[0]).convert('RGBA'))
for i,path in enumerate(paths):
 a=np.array(Image.open(path).convert('RGBA'));ids,_=label(a[:,:,3]>200);sizes=np.bincount(ids.ravel());sizes[0]=0;n=int(sizes.argmax());y,x=find_objects(ids)[n-1]
 clean=a.copy();clean[~binary_dilation(ids==n,iterations=2)]=0
 # Same inspected source crown/cylinder ruler; changes require review, never fit each pose to total height.
 cy=678;scale=65.20902255639098/(cy-y.start)
 sample=round(cy+12/scale);_,px=np.where(clean[sample-2:sample+3,:,3]>200);axis=(px.min()+px.max())/2
 box=(max(0,x.start-2),max(0,y.start-2),min(a.shape[1],x.stop+2),min(a.shape[0],y.stop+2))
 crop=Image.fromarray(clean).crop(box);crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
 offset=(round(128-(axis-box[0])*scale),round(224-(y.stop-1-box[1])*scale))
 frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop,offset);frame.save(O/(path.stem+'-registered.png'))
 d.text((i*512+8,8),path.name,fill='white');shown=frame.resize((512,512),Image.Resampling.NEAREST);board.paste(shown,(i*512,30),shown)
 detail=Image.fromarray(a).crop((535,455,845,710)).resize((496,408),Image.Resampling.NEAREST);board.paste(detail,(i*512+8,580),detail)
 row={'source':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':[a.shape[1],a.shape[0]],'opaqueBounds':[x.start,y.start,x.stop,y.stop],'cylinderBottomManualY':cy,'scale':scale,'registeredCrown':224-(y.stop-1-y.start)*scale,'nativeOffset':offset}
 if a.shape==original.shape:
  changed=np.any(a!=original,axis=2);case=np.zeros(changed.shape,bool);case[455:710,535:845]=True
  row.update({'changedPixels':int(changed.sum()),'changedOutsideCaseContext':int((changed&~case).sum()),'exactOutsideCaseContext':not bool((changed&~case).any()),'alphaExact':bool(np.array_equal(a[:,:,3],original[:,:,3]))})
 records.append(row)
board.save(O/'comparison.png')
(O/'review.json').write_text(json.dumps({'scope':'Complete authored source edit diagnostic only; not selected, native, helmet or final motion accepted.','ruler':'Original source landmarks provisionally reused, visually verify before admission.','rows':records,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'candidate':v,'rows':records}))
