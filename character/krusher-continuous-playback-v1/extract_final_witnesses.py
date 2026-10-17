from pathlib import Path
import json,av
from PIL import Image,ImageDraw,ImageFont
R=Path.cwd();H=R/'character/krusher-continuous-playback-v1';L=json.loads((H/'playback-v11-final/contract.json').read_text());O=H/'playback-v11-final';T=H/'motion-witnesses-v11';T.mkdir(exist_ok=True);font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),16);witnesses=[]
for bp in sorted(O.glob('batch-*.json')):
 report=json.loads(bp.read_text());batch=report['batch'];video=bp.with_suffix('.webm');retry=H/'playback-v11-retry'/video.name;video=retry if retry.exists() else video
 if not video.exists():continue
 targets=[]
 for j,plan in enumerate(L['plans'][batch*6:batch*6+6]):
  if len(plan['segments'])==3:
   a,b,c=plan['segments'];start=a['duration'];span=b['duration'];times=[start-30,start+20,start+span*.33,start+span*.66,start+span-20,start+span+20,plan['duration']-550]
  else:
   s=L['states'][plan['key']];duration=sum(s['durations']);times=[duration*q for q in ([0,.2,.4,.6,.8,.99,1.01] if s['loop'] else [0,.16,.33,.5,.67,.84,.98])]
  targets.extend((float(t/1000),j,k,plan['key']) for k,t in enumerate(times))
 targets.sort();pos=0;images={}
 with av.open(str(video)) as cont:
  for frame in cont.decode(video=0):
   tm=float(frame.time or 0)
   if pos>=len(targets):break
   if tm+1/60<targets[pos][0]:continue
   im=frame.to_image().convert("RGBA")
   while pos<len(targets) and targets[pos][0]<=tm+1/60:
    _,j,k,key=targets[pos];x=j%3*400+276;y=j//3*360+184;crop=im.crop((x,y,x+112,y+120)).resize((84,90),Image.Resampling.LANCZOS);images[(j,k)]=crop;pos+=1
 for j,plan in enumerate(L['plans'][batch*6:batch*6+6]):
  if not all((j,k) in images for k in range(7)):continue
  strip=Image.new('RGBA',(600,115),'#27323a');d=ImageDraw.Draw(strip);d.text((4,1),plan['key'],font=font,fill='white')
  for k in range(7):strip.alpha_composite(images[(j,k)],(k*85,23))
  dest=T/(str(batch*6+j).zfill(3)+'.png');strip.save(dest);witnesses.append({'key':plan['key'],'batch':batch,'strip':dest.name})
for page in range((len(witnesses)+15)//16):
 board=Image.new('RGBA',(1200,920),'#27323a')
 for j,q in enumerate(witnesses[page*16:page*16+16]):board.alpha_composite(Image.open(T/q['strip']),(j%2*600,j//2*115))
 board.save(T/('review-%02d.png'%page))
(H/'motion-witness-index-v11.json').write_text(json.dumps(witnesses,indent=2));print({'continuousVideos':len(list(O.glob('*.webm'))),'witnessedStates':len(witnesses),'reviewSheets':(len(witnesses)+15)//16})
