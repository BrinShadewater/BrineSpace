"""Rigid whole-pose registration study; no anatomical fragments or engine admission."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
from scipy.ndimage import label,find_objects,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
version=sys.argv[1] if len(sys.argv)>1 else '1';assert version in ['1','2','3','4']
O=P/('whole-pose-join-v'+version);O.mkdir(exist_ok=True)
target=65.20902255639098
atlas=P/'raw-v11.png';replacement=P/'raw-opposite-contact-v14.png'
def components(path):
 im=Image.open(path).convert('RGBA');a=np.array(im);ids,_=label(a[:,:,3]>200);sizes=np.bincount(ids.ravel());sizes[0]=0
 rows=[]
 for n,sl in enumerate(find_objects(ids),1):
  if sl and sizes[n]>10000:
   y,x=sl;rows.append((x.start,n,sl))
 return im,a,ids,sorted(rows)
im,a,ids,cs=components(atlas);assert len(cs)==6
scale=target/(335-48)
board=Image.new('RGB',(1536,630),'#202a30');d=ImageDraw.Draw(board)
d.text((8,7),'WHOLE-POSE JOIN STUDY v'+version+': shared anatomy ruler, complete authored poses, original grade. Gait NOT accepted.',fill='white')
frames=[];records=[]
for i in range(6):
 path=atlas;sa=a;labels=ids;_,n,sl=cs[i];s=scale;cy=335
 if i==3 or (version in ['2','3','4'] and i==4) or (version in ['3','4'] and i==2):
  path=replacement if i==3 else P/'raw-passing-v16.png' if i==4 else P/('raw-far-swing-v20.png' if version=='4' else 'raw-far-swing-v18.png')
  rim,sa,labels,rcs=components(path);_,n,sl=max(rcs,key=lambda v:np.count_nonzero(labels[v[2]]==v[1]))
  cy=768 if i==3 else 689 if i==4 else 678 if version=='4' else 676;s=target/(cy-sl[0].start)
 y,x=sl;keep=binary_dilation(labels==n,iterations=2);clean=sa.copy();clean[~keep]=0
 bounds=(max(0,x.start-2),max(0,y.start-2),min(sa.shape[1],x.stop+2),min(sa.shape[0],y.stop+2))
 sample=round(cy+12/s);_,px=np.where(clean[sample-2:sample+3,:,3]>200);axis=(px.min()+px.max())/2
 crop=Image.fromarray(clean).crop(bounds);crop=crop.resize((round(crop.width*s),round(crop.height*s)),Image.Resampling.LANCZOS)
 offset=(round(128-(axis-bounds[0])*s),round(224-((y.stop-1)-bounds[1])*s))
 frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop,offset);frames.append(frame);frame.save(O/f'{i:03}.png')
 d.text((i*256+8,32),f'Phase{i}: '+path.name,fill='white');board.paste(frame,(i*256,40),frame)
 upper=frame.crop((50,65,220,164)).resize((256,149),Image.Resampling.NEAREST);board.paste(upper,(i*256,320),upper)
 lower=frame.crop((45,156,225,233)).resize((256,109),Image.Resampling.NEAREST);board.paste(lower,(i*256,500),lower)
 records.append({'phase':i,'source':path.name,'sourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourceBox':[x.start,y.start,x.stop,y.stop],'cylinderBottomY':cy,'scale':s,'registeredCrown':224-((y.stop-1)-y.start)*s,'upperThighAxisSampleY':sample,'position':offset,'outputSHA256':hashlib.sha256((O/f'{i:03}.png').read_bytes()).hexdigest()})
board.save(O/'comparison.png')
preview=[]
for frame in frames:
 bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(frame);preview.append(bg)
preview[0].save(O/'cycle.png',save_all=True,append_images=preview[1:],duration=140,loop=0,disposal=0,blend=0)
decoded=Image.open(O/'cycle.png');assert decoded.n_frames==6
for i,frame in enumerate(preview):
 decoded.seek(i);assert decoded.info['duration']==140;assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(frame))
(O/'registration.json').write_text(json.dumps({'scope':'Whole-pose rigid registration diagnostic only. No engine manifest/selection. Opposing contact and V2passing corrected; far swing/support-side phases, source margins and materials need review.','version':version,'targetCrownToCylinderSpan':target,'atlasCrown':48,'atlasCylinderBottom':335,'root':[128,224],'durationsMs':[140]*6,'apngDecodedExactFrames':6,'rows':records},indent=2)+'\n',encoding='utf-8')
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld East carry whole-pose study</title><style>body{background:#202a30;color:#dce5e8;font:18px system-ui;margin:30px}img{max-width:100%}.motion{width:512px;image-rendering:pixelated}</style><h1>Veld East carry — whole-pose study</h1><p>Repaired poses joined for review. Full stride, body movement and material matching remain provisional.</p><img class="motion" src="cycle.png"><p>One anatomical ruler; entire authored poses; no body strips.</p><img src="comparison.png">''',encoding='utf-8')
print(json.dumps({'wholePoses':6,'decodedExactFrames':6,'cycleMs':840,'atlasScale':scale,'oppositeScale':records[3]['scale'],'scope':'source diagnostic only'}))
