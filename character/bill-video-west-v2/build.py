from pathlib import Path
import json
import numpy as np
import imageio.v2 as iio
from PIL import Image, ImageDraw
from scipy import ndimage
P=Path(__file__).resolve().parent
def mask(a):
 v=a.astype(float); k=(v[:,:,1]>v[:,:,0]*1.3)&(v[:,:,1]>v[:,:,2]*1.3)&(v[:,:,1]>90)
 labels,_=ndimage.label(~k); n=np.bincount(labels.ravel());n[0]=0
 return labels==n.argmax()
ref=np.array(Image.open(P/'master-input.png').convert('RGB').resize((768,768)))
m=mask(ref);ys,xs=np.where(m);scale=148/(ys.max()-ys.min()+1)
offset=(92-round((xs.min()+xs.max())*.5*scale),172-round((ys.max()+1)*scale))
r=iio.get_reader(P/'source.mp4'); raw=[np.asarray(a) for a in r];fps=r.get_meta_data()['fps'];r.close()
frames=[];bounds=[]; mids=[]
for a in raw:
 m=mask(a);v=a.astype(float)/255
 # One fixed neutral-material correction for the entire clip; preserve chromatic hair/skin/patches.
 spread=np.ptp(v,axis=2);value=v.mean(axis=2)
 weight=np.clip((32/255-spread)/(12/255),0,1)*np.clip((140/255-value)/(35/255),0,1)
 v=v*(1+weight[:,:,None]*(np.array([58/68,57/63,58/68])-1))
 v=(v*.22+(np.minimum(v,.28)+np.maximum(v-.28,0)*.72)*.78)*.96
 im=Image.fromarray(np.dstack([np.rint(v*255).astype('uint8'),m.astype('uint8')*255]))
 f=Image.new('RGBA',(184,184));f.alpha_composite(im.resize((round(a.shape[1]*scale),round(a.shape[0]*scale)),Image.Resampling.LANCZOS),offset)
 frames.append(f);ar=np.array(f);yy,xx=np.where(ar[:,:,3]>127);bounds.append([int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)])
 neutral=(np.ptp(ar[:,:,:3].astype(float),axis=2)<24)&(ar[:,:,3]>250)&(ar[:,:,:3].mean(2)>25)&(ar[:,:,:3].mean(2)<120)
 mids.append(np.median(ar[:,:,:3][neutral],axis=0).tolist())
sheet=Image.new('RGB',(184*8,210*3),'#303b40');d=ImageDraw.Draw(sheet)
for j,n in enumerate(np.linspace(0,len(frames)-1,24).astype(int)):
 x=j%8*184;y=j//8*210;sheet.paste(frames[n],(x,y+20),frames[n]);d.text((x+8,y+3),str(n),fill='white')
sheet.save(P/'contact.png')
frames[0].save(P/'idle-west-candidate.png')
selection=P/'selection.json';cfg=json.loads(selection.read_text()) if selection.exists() else {'start':0,'end':len(frames),'cycles':0}
indices=list(range(cfg['start'],cfg['end']));preview=[]
for n in indices:
 bg=Image.new('RGB',(552,270),'#303b40');d=ImageDraw.Draw(bg)
 for height,x in [(148,0),(82,225),(54,355),(27,465)]:
  side=round(184*height/148);im=frames[n].resize((side,side),Image.Resampling.BILINEAR);bg.paste(im,(x,35),im)
 d.text((8,8),f'Bill west candidate / source frame {n}',fill='white');preview.append(bg)
ms=1500*cfg['cycles']/len(indices) if cfg['cycles'] else 1000/fps
preview[0].save(P/'review.gif',save_all=True,append_images=preview[1:],duration=[10*(round((i+1)*ms/10)-round(i*ms/10)) for i in range(len(indices))],loop=0)
dest=P/'frames/walk-west';dest.mkdir(parents=True,exist_ok=True)
for j,n in enumerate(indices):frames[n].save(dest/f'{j:03d}.png')
audit={'sourceFrames':len(raw),'fps':fps,'fixedScale':scale,'fixedOffset':offset,'bounds':bounds,'neutralMedians':mids,'selection':cfg,'processing':'Fixed registration and approved matte curve; no pose warping or per-frame resizing. One fixed feathered neutral-material gain across all frames; chromatic hair and skin excluded.'}
(P/'checks.json').write_text(json.dumps(audit,indent=2))
(P/'index.html').write_text('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#172226;color:#dbe4df;font:18px system-ui;max-width:1100px;margin:30px auto}img,video{max-width:100%}</style><h1>Bill west walk · revised proportions</h1><p>Candidate only. Matte finish, smooth sampling; source and extracted motion below. Runtime unchanged.</p><img src="review.gif"><h2>Original video</h2><video src="source.mp4" controls loop></video><h2>Motion contact sheet</h2><img src="contact.png">')
print(json.dumps({k:v for k,v in audit.items() if k not in ['bounds','neutralMedians']}))


if cfg['cycles']:
 durations=[round((i+1)*1500*cfg['cycles']/len(indices))-round(i*1500*cfg['cycles']/len(indices)) for i in range(len(indices))]
 manifest=dict(name='Bill revised west walk',status='candidate_not_installed',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,textureFilter='linear',precomposed=True,strideDistanceCells={'walk-west':cfg['cycles']*69/384},states=[dict(id='walk-west',frameCount=len(indices),frameFiles=[f'frames/walk-west/{i:03}.png' for i in range(len(indices))],frameDurationsMs=durations,gaitCycles=cfg['cycles'],loop=True,sourceFrames=indices,mirrored=False)])
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2))
