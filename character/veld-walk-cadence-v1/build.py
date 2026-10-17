from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent
sources={'south':'veld-video-south-v1','north':'veld-video-north-v6','west':'veld-video-walk-v1','east':'veld-video-east-v1'}
cycle=1500
states=[];seqs={};timelines={};checks=[]
for direction,folder in sources.items():
 root=P.parent/folder;m=json.loads((root/'manifest.json').read_text());state=m['states'][0];paths=[];seq=[];hashes=[]
 dest=P/'frames'/('walk-'+direction);dest.mkdir(parents=True,exist_ok=True)
 for j,source in enumerate(state['frameFiles']):
  src=root/source;target=dest/f'{j:03d}.png';data=src.read_bytes();target.write_bytes(data)
  assert hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256(data).digest()
  paths.append(str(target.relative_to(P)).replace('\\','/'));seq.append(Image.open(target).convert('RGBA'));hashes.append(hashlib.sha256(data).hexdigest())
 n=len(paths);bounds=[round(j*cycle/n) for j in range(n+1)];dur=[b-a for a,b in zip(bounds,bounds[1:])]
 states.append({'id':'walk-'+direction,'frameFiles':paths,'frameCount':n,'frameDurationsMs':dur,'loop':True,'mirrored':False,'sourceManifest':str((root/'manifest.json').relative_to(P.parent)),'sourceDurationMs':sum(state['frameDurationsMs']),'sourceFrameHashes':hashes})
 seqs[direction]=seq;timelines[direction]=[10*round(t/10) for t in bounds]
 checks.append({'direction':direction,'count':n,'durationMs':sum(dur),'allFrameBytesPreserved':True})
manifest={'name':'Veld four-direction walk cadence candidate','frameWidth':184,'frameHeight':184,'pivot':[92,172],'standingHeight':148,'status':'timing_and_front_review_pending_not_installed','states':states}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2))
times=sorted(set(t for bounds in timelines.values() for t in bounds));out=[]
order=['south','north','west','east'];labels=['FRONT - REVIEW','REAR - ACCEPTED MOTION','WEST - ACCEPTED MOTION','EAST - ACCEPTED MOTION']
for t in times[:-1]:
 im=Image.new('RGB',(736,880),'#263139');dr=ImageDraw.Draw(im)
 for k,d in enumerate(order):
  i=max(j for j,b in enumerate(timelines[d][:-1]) if b<=t);f=seqs[d][i];x=k%2*368;y=k//2*420
  big=f.resize((368,368),Image.Resampling.NEAREST);im.paste(big,(x,y+25),big);dr.text((x+10,y+8),labels[k],fill='white')
  small=f.resize((56,56),Image.Resampling.LANCZOS);im.paste(small,(x+156,y+360),small)
 dr.text((12,853),'Timing candidate: every full stride cycle is 1.5 seconds.',fill='white');out.append(im)
out[0].save(P/'four-direction-cadence.gif',save_all=True,append_images=out[1:],duration=[b-a for a,b in zip(times,times[1:])],loop=0)
# A separate front/master comparison at this candidate cadence.
master=Image.open(P.parent/'veld-animation-pilot-v12/frames/idle-south/000.png').convert('RGBA');front=[]
for f in seqs['south']:
 im=Image.new('RGB',(736,410),'#263139');dr=ImageDraw.Draw(im)
 for x,img,label in [(0,master,'APPROVED FRONT MASTER'),(368,f,'FRONT WALK - REVIEW')]:
  b=img.resize((368,368),Image.Resampling.NEAREST);im.paste(b,(x,30),b);dr.text((x+10,10),label,fill='white')
 front.append(im)
ts=timelines['south'];front[0].save(P/'front-master-review.gif',save_all=True,append_images=front[1:],duration=[b-a for a,b in zip(ts,ts[1:])],loop=0)
(P/'checks.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks))
