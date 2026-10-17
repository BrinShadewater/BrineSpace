from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
from scipy.ndimage import label
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
raw=OUT/'sources/walk-028-calibrated-v1.png';source=Image.open(raw).convert('RGBA');a=np.array(source)
oldpath=ROOT/'character/bill-walk-west-material-v1/frames/bare/walk-west/028.png';old=Image.open(oldpath).convert('RGBA');old_a=np.array(old)
scale=148/938
rows=[]
def extract(roi):
 x,y,x1,y1=roi;b=a[y:y1,x:x1].copy();labels,n=label(b[:,:,3]>0);sizes=np.bincount(labels.ravel());chosen=int(sizes[1:].argmax()+1);removed=int(((b[:,:,3]>0)&(labels!=chosen)).sum());b[labels!=chosen]=0
 out=np.zeros_like(a);out[y:y1,x:x1]=b;return Image.fromarray(out),removed
def sole(array,threshold=180):
 mask=array[:,:,3]>=threshold;ys,xs=np.where(mask);last=int(ys.max());band=mask&(np.indices(mask.shape)[0]>=last-11);by,bx=np.where(band);return [(int(bx.min())+int(bx.max()))/2,last], [int(bx.min()),int(by.min()),int(bx.max()+1),int(by.max()+1)]
old_anchor,old_band=sole(old_a)
for name,roi,target in [('neutral',(100,0,650,1024),[128,224]),('walk028',(700,0,1536,1024),old_anchor)]:
 whole,removed=extract(roi);anchor,band=sole(np.array(whole));resized=whole.resize((round(source.width*scale),round(source.height*scale)),Image.Resampling.LANCZOS)
 offset=[round(target[i]-anchor[i]*scale) for i in [0,1]]
 canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(resized,tuple(offset));ys,xs=np.where(np.array(canvas)[:,:,3]>0);assert min(xs)>0 and max(xs)<255 and min(ys)>0 and max(ys)<255
 if name=='walk028':dest=OUT/'frames/bare/walk-west/028.png'
 else:dest=OUT/'neutral-calibration.png'
 dest.parent.mkdir(parents=True,exist_ok=True);canvas.save(dest)
 rows.append({'pose':name,'actionROI':list(roi),'wholeSourceScale':scale,'registrationTranslation':offset,'sourceSoleBand':band,'sourcePaintedSoleAnchor':anchor,'targetPaintedSoleAnchor':target,'detachedAlphaPixelsRemoved':removed,'physicalContactAccepted':False,'scope':'Whole figure painted sole-band proxy only; no separate body/head/limb fitting. Neutral standing denominator938 independent of posed height.'})
master=Image.open(ROOT/'character/bill-water-exit-west-master-v8/sources/master-west-reference.png').convert('RGBA');master=master.resize((round(master.width*148/956),round(master.height*148/956)),Image.Resampling.LANCZOS);mc=Image.new('RGBA',(256,256));mc.alpha_composite(master,(128-master.width//2,224-master.height))
items=[('Original West master',mc),('Generated neutral / ruler',Image.open(OUT/'neutral-calibration.png').convert('RGBA')),('Selected walk028',old),('New whole walk028 candidate',Image.open(OUT/'frames/bare/walk-west/028.png').convert('RGBA'))]
board=Image.new('RGB',(1024,600),(23,42,51));draw=ImageDraw.Draw(board)
for i,(name,im) in enumerate(items):
 draw.text((256*i+5,5),name,fill='white');board.paste(im,(256*i,25),im)
 crop=im.crop((85,55,165,155)).resize((200,250),Image.Resampling.NEAREST);board.paste(crop,(256*i+25,325),crop)
board.save(OUT/'master-review.png')
job=json.loads((OUT/'generation-provenance-v1.json').read_text());assert hashlib.sha256(raw.read_bytes()).hexdigest()==job['sha256'];assert hashlib.sha256(Path(job['originalPath']).read_bytes()).hexdigest()==job['sha256'];assert hashlib.sha256((OUT/job['promptPath']).read_bytes()).hexdigest()==job['promptSHA256']==job['submittedPromptSHA256']
for r in job['references']:assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
(OUT/'review.json').write_text(json.dumps({'status':'representative_whole_source_candidate_unselected','generationId':job['generationId'],'standingOpaqueHeight':938,'neutralHeadProxySize':[142,161],'walkingHeadProxySize':[145,152],'frames':rows,'oldSoleBand':old_band,'canvas':[256,256],'pivot':[128,224],'standingHeight':148,'sourceAlphaMax':int(a[:,:,3].max()),'normalSelected':False,'nativeAcceptance':False,'authoredCandidateWalkingPoses':1,'fullTarget':{'bare':48,'helmet':48},'remainingCandidateCoverage':{'bare':47,'helmet':48},'scope':'One whole bare pose and neutral ruler. No runtime clip clock or normal source edit; full48phase gait retained in existing selection. Body identity/pose/contact/grade remain visual/provisional.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'standing':938,'scale':scale,'oldPaintedSupport':old_anchor,'rows':rows,'provenance':'pass'}))
