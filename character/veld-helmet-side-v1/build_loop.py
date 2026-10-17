"""Package the helmet west trial without recolouring or per-frame scaling."""
from pathlib import Path
import json, hashlib
import imageio.v2 as iio
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
START,COUNT=52,45
SCALE=148/911*763/778/.75
SIZE=round(768*SCALE)
OFFSET=(92-round(384*SCALE),172-round(747*SCALE))
r=iio.get_reader(P/'source.mp4');raw=[np.asarray(a) for a in r];r.close()
frames=[]; paths=[]; bounds=[]; levels=[]
dest=P/'frames/walk-west';dest.mkdir(parents=True,exist_ok=True)
for j,a in enumerate(raw[START:START+COUNT]):
 v=a.astype(float);key=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
 lab,n=ndimage.label(~key);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax()
 im=Image.fromarray(np.dstack([a,mask.astype('uint8')*255]));frame=Image.new('RGBA',(184,184));frame.alpha_composite(im.resize((SIZE,SIZE),Image.Resampling.LANCZOS),OFFSET)
 frame.save(dest/f'{j:03d}.png');frames.append(frame);paths.append(f'frames/walk-west/{j:03d}.png')
 arr=np.asarray(frame);ys,xs=np.where(arr[:,:,3]>=128);bounds.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
 # Head-region diagnostic only; anatomy/art variation makes it an indicator, not acceptance.
 roi=arr[15:45];mask=roi[:,:,3]>220;rgb=roi[:,:,:3][mask];levels.append(float(np.median(rgb@np.array([.2126,.7152,.0722]))))
durations=[round((j+1)*1500/COUNT)-round(j*1500/COUNT) for j in range(COUNT)]
manifest={'name':'Veld helmet west walk pilot','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'precomposed':True,'status':'candidate_not_installed','sourceFrames':list(range(START,START+COUNT)),'sharedScale':SCALE,'sharedOffset':OFFSET,'strideDistanceCells':{'walk-west':69/384},'states':[{'id':'walk-west','frameCount':COUNT,'frameFiles':paths,'frameDurationsMs':durations,'loop':True}]}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
source=Image.open(P/'side-master-01.png').convert('RGBA');a=np.array(source);a[:,:,3]=np.where(a[:,:,3]>=128,255,0);source=Image.fromarray(a).crop((878,16,1164,984))
helmet=Image.new('RGBA',(184,184));size=(round(source.width*SCALE*.75),round(source.height*SCALE*.75));helmet.alpha_composite(source.resize(size,Image.Resampling.LANCZOS),(92-size[0]//2,172-size[1]))
helmet.save(P/'west-standing.png')
bare=Image.open(P.parent/'veld-side-foundation-v1/west-standing.png').convert('RGBA')
reviews=[]
for frame in frames:
 bg=Image.new('RGB',(1104,470),'#263139');draw=ImageDraw.Draw(bg)
 for col,(im,title) in enumerate([(bare,'APPROVED BARE MASTER'),(helmet,'HELMET MASTER CANDIDATE'),(frame,'HELMET WALK / MATCHED CADENCE')]):
  draw.text((col*368+10,10),title,fill='white');big=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(col*368,30),big)
  small=im.resize((81,81),Image.Resampling.LANCZOS);bg.paste(small,(col*368+144,385),small)
 reviews.append(bg)
gifdur=[10*(round((j+1)*150/COUNT)-round(j*150/COUNT)) for j in range(COUNT)]
reviews[0].save(P/'west-helmet-review.gif',save_all=True,append_images=reviews[1:],duration=gifdur,loop=0,optimize=False)
originaldur=[10*(round((j+1)*100/24)-round(j*100/24)) for j in range(COUNT)]
reviews[0].save(P/'west-original-speed.gif',save_all=True,append_images=reviews[1:],duration=originaldur,loop=0,optimize=False)
contact=Image.new('RGB',(184*9,210),'#263139');draw=ImageDraw.Draw(contact)
for j,i in enumerate(range(0,COUNT,5)):
 contact.paste(frames[i],(184*j,20),frames[i]);draw.text((184*j+4,3),str(START+i),fill='white')
contact.save(P/'loop-contact.png')
a=[np.array(x).astype(float)/255 for x in frames];diff=[float(np.mean(np.abs(a[j]-a[(j+1)%COUNT]))) for j in range(COUNT)]
audit={'sourceSha256':hashlib.sha256((P/'source.mp4').read_bytes()).hexdigest(),'frames':COUNT,'sourceRangeInclusive':[START,START+COUNT-1],'originalDurationMs':1875,'previewDurationMs':1500,'seamMeanAbsoluteDifference':diff[-1],'internalMedianDifference':float(np.median(diff[:-1])),'clippedFrames':sum(b[0]<=0 or b[1]<=0 or b[2]>=184 or b[3]>=184 for b in bounds),'opaqueHeightRange':[min(b[3]-b[1] for b in bounds),max(b[3]-b[1] for b in bounds)],'headMedianLuminanceRange':[min(levels),max(levels)],'processing':'Largest-component green key, constant body-calibrated scale and placement, unchanged source RGB. Helmet naturally extends above bare crown. No per-frame size or brightness normalization.','status':'candidate_not_installed'}
assert audit['clippedFrames']==0
(P/'loop-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(audit)
