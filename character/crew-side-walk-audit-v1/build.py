"""Read-only review of runtime catalog walks against owner-locked turnarounds."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;C=P.parent
specs=[('Bill','major-bill-v3','bill',{'east':(506,45,643,469),'west':(1247,45,1385,469)}),('Branforth','chief-engineer-branforth-v2','branforth',{'east':(573,15,706,454),'west':(1100,15,1239,454)})]
rows=[];report=[]
for name,folder,actor,crops in specs:
 root=C/folder;catalog=json.loads((root/'catalog.json').read_text());states={}
 for rel in catalog['body']:
  path=root/rel;m=json.loads(path.read_text())
  for e in m['states']:states[e['id']]=(path,m,e)
 for direction,box in crops.items():
  path,m,e=states['walk-'+direction];frames=[Image.open(path.parent/f).convert('RGBA') for f in e['frameFiles']]
  masterpath=C/'crew-turnarounds-v4'/f'{actor}-turnaround-01.png';master=Image.open(masterpath).crop(box);master=master.resize((round(master.width*148/master.height),148),Image.Resampling.LANCZOS)
  ref=Image.new('RGBA',(184,184),'#263139');ref.paste(master,(92-master.width//2,172-148))
  bounds=[]
  for f in frames:
   a=np.asarray(f);ys,xs=np.where(a[:,:,3]>=128);bounds.append([int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)])
  rows.append((name,direction,ref,frames,e['frameDurationsMs']))
  report.append(dict(actor=actor,direction=direction,manifest=path.relative_to(C).as_posix(),frameCount=len(frames),durationMs=sum(e['frameDurationsMs']),bounds=bounds,sourceHashes=[hashlib.sha256((path.parent/f).read_bytes()).hexdigest() for f in e['frameFiles']],masterCrop=box,masterSha256=hashlib.sha256(masterpath.read_bytes()).hexdigest()))
contact=Image.new('RGB',(7*184,4*210),'#263139');draw=ImageDraw.Draw(contact)
for r,(name,d,ref,frames,durations) in enumerate(rows):
 for j,im in enumerate([ref]+frames):
  contact.paste(im,(j*184,r*210+20),im);draw.text((j*184+4,r*210+4),f'{name} {d} '+('MASTER' if j==0 else str(j-1)),fill='white')
contact.save(P/'contact.png')
review=[]
for tick in range(96):
 bg=Image.new('RGB',(736,4*390),'#263139');draw=ImageDraw.Draw(bg)
 for row,(name,d,ref,frames,durations) in enumerate(rows):
  t=(tick*1000/24)%sum(durations);n=0
  while n<len(durations)-1 and t>=durations[n]:t-=durations[n];n+=1
  for col,im in enumerate([ref,frames[n]]):
   big=im.resize((368,368),Image.Resampling.NEAREST);bg.paste(big,(col*368,row*390+22),big)
  draw.text((8,row*390+5),f'{name} {d} / LOCKED MASTER',fill='white');draw.text((376,row*390+5),'CURRENT WALK / original timing',fill='white')
 review.append(bg)
review[0].save(P/'comparison.gif',save_all=True,append_images=review[1:],duration=[40,40,50]*32,loop=0,optimize=False)
(P/'audit.json').write_text(json.dumps({'scope':'Catalog-selected bare side walks only; static source inspection, not live-game capture. Master crops retain background and are scaled once to declared148px standing height.','rows':report,'creditsSpent':0},indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['actor','direction','frameCount','durationMs','bounds']} for r in report]))
