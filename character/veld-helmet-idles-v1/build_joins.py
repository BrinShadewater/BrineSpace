from pathlib import Path
import json,shutil,hashlib,os
from PIL import Image,ImageDraw
import numpy as np
P=Path(__file__).resolve().parent;W=P.parent/'veld-helmet-walks-v1';OUT=P/'joined-pack';OUT.mkdir(exist_ok=True)
idles=json.loads((P/'manifest.json').read_text());walks=json.loads((W/'manifest.json').read_text());manifest={k:v for k,v in idles.items() if k!='states'};manifest.update(name='Veld helmet idle and walk staged joins',states=[],strideDistanceCells=walks['strideDistanceCells']);clips={};joinchecks={}
for direction in ['south','east','north','west']:
 idle=next(e for e in idles['states'] if e['id']=='idle-'+direction);walk=next(e for e in walks['states'] if e['id']=='walk-'+direction)
 reference=Image.open(P/idle['frameFiles'][0]).convert('RGBA');a=np.asarray(reference).astype(float)/255;a[:,:,:3]*=a[:,:,3:4];scores=[]
 for file in walk['frameFiles']:
  im=Image.open(W/file).convert('RGBA');b=np.asarray(im).astype(float)/255;b[:,:,:3]*=b[:,:,3:4]
  scores.append(float(np.mean(np.abs(a-b))))
 shift=int(np.argmin(scores));order=list(range(shift,len(scores)))+list(range(shift))
 joinchecks[direction]={'walkStartIndex':shift,'joinDifferenceBefore':scores[0],'joinDifferenceAfter':scores[shift],'worstPossibleStopDifference':max(scores),'rotationOnly':True}
 for entry,root,indices in [(idle,P,list(range(idle['frameCount']))),(walk,W,order)]:
  e=dict(entry);e['frameFiles']=[];e['frameDurationsMs']=[];e['sourceFrameOrder']=[];dest=OUT/'frames'/entry['id'];dest.mkdir(parents=True,exist_ok=True);frames=[]
  for j,i in enumerate(indices):
   source=root/entry['frameFiles'][i];target=dest/f'{j:03d}.png';shutil.copyfile(source,target);assert source.read_bytes()==target.read_bytes();e['frameFiles'].append(target.relative_to(OUT).as_posix());e['frameDurationsMs'].append(entry['frameDurationsMs'][i]);e['sourceFrameOrder'].append(i);frames.append(Image.open(target).convert('RGBA'))
  e['sourceFrames']=[entry['sourceFrames'][i] for i in indices];e['sourceVideo']=os.path.relpath(root/entry['sourceVideo'],OUT).replace('\\','/');e['sourceManifest']='../../veld-helmet-walks-v1/manifest.json' if root==W else '../manifest.json';manifest['states'].append(e);clips[entry['id']]={'frames':frames,'durations':e['frameDurationsMs']}
def at(key,t):
 clip=clips[key];t%=sum(clip['durations'])
 for im,duration in zip(clip['frames'],clip['durations']):
  if t<duration:return im
  t-=duration
 return clip['frames'][-1]
# 1s idle, 2.2s walk, 1s idle: includes a mid-stride stop, not a disguised complete-cycle stop.
review=[]
for i in range(126):
 t=i*1000/30;state='idle' if t<1000 or t>=3200 else 'walk';elapsed=t if t<1000 else t-1000 if t<3200 else t-3200
 canvas=Image.new('RGB',(736,880),'#263139');draw=ImageDraw.Draw(canvas)
 for j,d in enumerate(['south','east','north','west']):
  im=at(state+'-'+d,elapsed);x=j%2*368;y=j//2*440;draw.text((x+12,y+8),d.upper()+' / '+state.upper(),fill='white');big=im.resize((368,368),Image.Resampling.NEAREST);canvas.paste(big,(x,y+25),big);small=im.resize((64,64),Image.Resampling.LANCZOS);canvas.paste(small,(x+152,y+374),small)
 review.append(canvas)
review[0].save(P/'idle-walk-idle-review.gif',save_all=True,append_images=review[1:],duration=[30,40,30]*42,loop=0,optimize=False)
contact=Image.new('RGB',(184*4,210*4),'#263139');draw=ImageDraw.Draw(contact)
for row,d in enumerate(['south','east','north','west']):
 for col,(key,t,label) in enumerate([('idle-'+d,900,'idle'),('walk-'+d,0,'walk start'),('walk-'+d,2200,'walk stop'),('idle-'+d,0,'idle return')]):
  im=at(key,t);contact.paste(im,(col*184,row*210+22),im);draw.text((col*184+5,row*210+5),d+' '+label,fill='white')
contact.save(P/'joins-contact.png')
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');(P/'join-checks.json').write_text(json.dumps(joinchecks,indent=2)+'\n',encoding='utf-8')
# Foot-aligned endpoint comparison: legacy action geometry is preserved, not rescaled to hide the mismatch.
oldpath=P.parent/'dr-veld-v2/packs/bare-184x208-p92.0-196.0/manifest.json';old=json.loads(oldpath.read_text());equip=next(e for e in old['states'] if e['id']=='equip-helmet-east');bare=Image.open(P.parent/'veld-runtime-walk-v1/frames/idle-east/000.png').convert('RGBA');oldfirst=Image.open(oldpath.parent/equip['frameFiles'][0]).convert('RGBA');oldlast=Image.open(oldpath.parent/equip['frameFiles'][-1]).convert('RGBA');new=at('idle-east',0)
canvas=Image.new('RGB',(1472,470),'#263139');draw=ImageDraw.Draw(canvas)
for i,(im,title,pivot) in enumerate([(bare,'CURRENT BARE IDLE',(92,172)),(oldfirst,'OLD FITTING START',(92,196)),(oldlast,'OLD FITTING END',(92,196)),(new,'NEW HELMET IDLE',(92,172))]):
 big=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);canvas.paste(big,(i*368+184-pivot[0]*2,430-pivot[1]*2),big);draw.text((i*368+8,8),title,fill='white')
canvas.save(P/'fitting-joins.png');print(json.dumps(joinchecks,indent=2));print('Staged frames',sum(e['frameCount'] for e in manifest['states']))
