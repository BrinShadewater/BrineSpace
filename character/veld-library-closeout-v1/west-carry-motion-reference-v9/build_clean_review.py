"""Deterministic background removal and one full consecutive gait audition."""
from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
frames=[];rows=[]
F=P/'clean-frames';F.mkdir(exist_ok=True)
for i,p in enumerate(sorted((P/'raw-review').glob('raw-*.png'))):
 rgb=np.asarray(Image.open(p).convert('RGB'))
 # Fixed brightness separates dark background/shadow. Fill enclosed costume darks.
 labels,_=ndimage.label(rgb.max(axis=2)>28);counts=np.bincount(labels.ravel());counts[0]=0
 region=np.zeros(labels.shape,dtype=bool);region[250:870,200:760]=True
 major=(labels>0)&(counts[labels]>=500)&region
 distances=ndimage.distance_transform_edt(~major)
 near=ndimage.minimum(distances,labels,index=np.arange(len(counts)))<12
 seed=ndimage.binary_fill_holes((labels>0)&(counts[labels]>=20)&((counts[labels]>=500)|near[labels])&region)
 mask=ndimage.binary_fill_holes(ndimage.binary_dilation(seed,iterations=2)&(np.max(np.abs(rgb.astype(int)-[12,18,24]),axis=2)>8)&region)
 arr=np.dstack([rgb,mask.astype('uint8')*255]);arr[~mask]=0
 im=Image.fromarray(arr).resize((256,256),Image.Resampling.LANCZOS);im.save(F/f'{i:03}.png');frames.append(im)
 ys,xs=np.where(np.asarray(im)[:,:,3]>200);top=int(ys.min());hx=np.where(np.asarray(im)[top:top+16,:,3]>128)[1]
 rows.append(dict(frame=i,height=int(ys.max()-top+1),top=top,floor=int(ys.max()),headWidth=int(hx.max()-hx.min()+1),headAxis=float((hx.min()+hx.max())/2)))
chosen=list(range(24,48));loop=[frames[i] for i in chosen]
dur=[round((i+1)*1000/24)-round(i*1000/24) for i in range(24)]
loop[0].save(P/'clean-walk-loop.png',save_all=True,append_images=loop[1:],duration=dur,loop=0,disposal=0,blend=0)
ap=Image.open(P/'clean-walk-loop.png');assert ap.n_frames==24
for i,(im,hold) in enumerate(zip(loop,dur)):
 ap.seek(i);assert ap.convert('RGBA').tobytes()==im.tobytes();assert round(ap.info['duration'])==hold
board=Image.new('RGB',(1536,1152),'#263238');dr=ImageDraw.Draw(board)
for j,im in enumerate(loop):
 x=j%6*256;y=j//6*288;board.paste(im,(x,y+24),im);dr.text((x+4,y+4),f'Source {chosen[j]}',fill='white')
board.save(P/'clean-loop-chronology.png')
detail=Image.new('RGB',(1792,560),'#263238');dd=ImageDraw.Draw(detail)
for j,i in enumerate([24,28,32,36,40,44,47]):
 im=frames[i].resize((512,512),Image.Resampling.NEAREST);detail.paste(im,(j*256-128,32),im);dd.text((j*256+8,8),str(i),fill='white')
detail.save(P/'clean-phase-detail.png')
report=dict(status='Clean full-cycle review candidate only; no runtime/helmet admission',sourceIndices=chosen,frameCount=24,loopMs=sum(dur),replayChecks=48,allSourceFramesCleaned=len(frames),alpha='Fixed RGB max>28 major components>=500 plus nearby components>=20 within12 source pixels, fixed generous subject region x200..760/y250..870, enclosed-hole fill and2px edge recovery constrained by background distance>8; RGB unchanged; fixed960-to256 canvas. Initial largest-only extraction dropped disconnected suit sections, later small-component filtering dropped bun; corrected before visual delivery.',ranges={k:[min(r[k] for r in rows),max(r[k] for r in rows)] for k in ['height','top','floor','headWidth','headAxis']},rows=rows,remaining=['Detailed identity/case construction drift','Loop seam review','Physical foot contact and original helmet fitting','Cargo/turn joins and actual NPC lifecycle'],normalAdmission=False)
(P/'CLEAN_REVIEW.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['frameCount','loopMs','replayChecks','allSourceFramesCleaned','ranges']}))
