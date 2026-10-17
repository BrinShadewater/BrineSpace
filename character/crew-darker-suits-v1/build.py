from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;C=P.parent
dirs=['south','east','north','west'];clips={};checks=[];hashes={}
for who in ['bill','veld','branforth']:
 root=C/'veld-runtime-walk-v1' if who=='veld' else C/'crew-walk-stage-v1'/who
 m=json.loads((root/'manifest.json').read_text());dst=P/who;dst.mkdir(parents=True,exist_ok=True)
 for s in m['states']:
  if not s['id'].startswith(('walk-','idle-')):continue
  before=[];after=[];files=[]
  for n,f in enumerate(s['frameFiles']):
   source=(root/f).resolve();hashes[str(source)]=hashlib.sha256(source.read_bytes()).hexdigest();im=Image.open(source).convert('RGBA');a=np.array(im);v=a[:,:,:3].astype(float)
   yy=np.indices(a.shape[:2])[0];ys,xs=np.where(a[:,:,3]>=128);headEnd=int(ys.min())+27
   # Fixed material approximation: protect head, bright silver and chromatic department accents.
   mean=v.mean(axis=2);weight=np.clip((32-np.ptp(v,axis=2))/16,0,1)*np.clip((140-mean)/40,0,1)*(yy>=headEnd)*(a[:,:,3]>0)
   b=a.copy();b[:,:,:3]=np.rint(v*(1-.14*weight[:,:,None])).clip(0,255).astype('uint8')
   assert np.array_equal(a[:,:,3],b[:,:,3]);assert np.array_equal(a[yy<headEnd],b[yy<headEnd]);assert np.all(b[:,:,:3]<=a[:,:,:3])
   out=dst/'frames'/s['id']/f'{n:03d}.png';out.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(b).save(out);files.append(out.relative_to(dst).as_posix());before.append(im);after.append(Image.fromarray(b))
  direction=s['id'].split('-',1)[1]
  if s['id'].startswith('walk-'):clips[(who,direction)]=(before,after,s['frameDurationsMs'])
  checks.append(dict(character=who,state=s['id'],frameCount=len(files),headPixelsUnchanged=True,alphaUnchanged=True,noPixelBrightened=True))
  s['frameFiles']=files
 m['name']=who+' darker suit comparison';m['status']='palette_review_candidate_not_installed';(dst/'manifest.json').write_text(json.dumps(m,indent=2))
def frame(frames,durations,t):
 t%=sum(durations);n=0
 while n<len(durations)-1 and t>=durations[n]:t-=durations[n];n+=1
 return frames[n]
out=[]
for tick in range(144):
 bg=Image.new('RGB',(828,1016),'#263139');draw=ImageDraw.Draw(bg)
 for col,who in enumerate(['bill','veld','branforth']):
  for row,direction in enumerate(dirs):
   before,after,durations=clips[(who,direction)];im=frame(after,durations,tick*1000/24);x=col*276;y=row*254
   draw.text((x+8,y+5),f'{who.upper()} {direction.upper()} / DARKER',fill='white');large=im.resize((230,230),Image.Resampling.NEAREST);bg.paste(large,(x+8,y+22),large)
   small=im.resize((64,64),Image.Resampling.LANCZOS);bg.paste(small,(x+208,y+176),small)
 out.append(bg)
out[0].save(P/'darker-cast-review.gif',save_all=True,append_images=out[1:],duration=[40,40,50]*48,loop=0,optimize=False)
sheet=Image.new('RGB',(1104,440),'#263139');d=ImageDraw.Draw(sheet)
for col,who in enumerate(['bill','veld','branforth']):
 before,after,_=clips[(who,'south')]
 for j,im in enumerate([before[0],after[0]]):
  x=col*368+j*184;d.text((x+5,8),f'{who.upper()} / '+('BEFORE' if j==0 else 'DARKER'),fill='white');sheet.paste(im,(x,30),im)
 # Inspect Bill hair at frame intervals, without changing it.
for j,n in enumerate([0,14,28,42,56,70]):
 im=clips[('bill','south')][0][n];a=np.array(im);ys,xs=np.where(a[:,:,3]>=128);top=int(ys.min());crop=im.crop((66,top,118,top+40)).resize((156,120),Image.Resampling.NEAREST);sheet.paste(crop,(j*184,280),crop);d.text((j*184+5,260),f'BILL FRONT frame {n}',fill='white')
sheet.save(P/'colour-and-hair-review.png')
for f,h in hashes.items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h
(P/'checks.json').write_text(json.dumps(dict(policy='14 percent maximum darkening in feathered neutral body mask; head and bright/chromatic pixels protected. Material approximation, not semantic segmentation.',states=checks,sourceFilesUnchanged=len(hashes)),indent=2))
print('Built 24 states; source frames unchanged, alpha/head protected, no pixel brightened.')
