from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np,sys
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),23)
families={'repair':['kneel','repair','stand'],'torch':['torch-draw','weld','torch-stow'],'seated':['sit-down','sit-idle','sit-rise']};reports={}
for family,actions in families.items():
 if sys.argv[1:] and family not in sys.argv[1:]:continue
 P=R/f'character/krusher-{family}-family-v4';players={};maxduration=0
 for gear in ['bare','helmet']:
  m=json.loads((P/(gear+'-manifest.json')).read_text());sm={s['id']:s for s in m['states']}
  for direction in ['south','east','north','west']:
   slots=[]
   for action in actions:
    s=sm[action+'-'+direction];slots.extend([(Image.open(P/f).convert('RGBA'),t,action,i) for i,(f,t) in enumerate(zip(s['frameFiles'],s['frameDurationsMs']))])
   duration=sum(s[1] for s in slots);maxduration=max(maxduration,duration);players[gear,direction]=(slots,duration)
 frames=[]
 for clock in range(0,int(maxduration)+50,50):
  b=Image.new('RGBA',(1000,885),'#252b2e');draw=ImageDraw.Draw(b);draw.text((25,12),'KRUSHER DOM / '+family.upper()+' / ORIGINAL POSE CLOCKS',font=font,fill='white')
  for row,g in enumerate(['bare','helmet']):
   for col,d in enumerate(['south','east','north','west']):
    slots,duration=players[g,d];time=min(clock,duration-0.001);j=0
    while j<len(slots)-1 and time>=slots[j][1]:time-=slots[j][1];j+=1
    im,hold,action,index=slots[j];crop=im.crop((43,0,141,192)).resize((196,384),Image.Resampling.NEAREST);x=col*245+25;y=row*410+78;b.alpha_composite(crop,(x,y));draw.text((x,y-30),d+' / '+g,font=font,fill='#bfd2d4')
  frames.append(b.convert('RGB'))
 path=H/(family+'-motion-review.gif');frames[0].save(path,save_all=True,append_images=frames[1:],duration=50,loop=0,disposal=2,optimize=True)
 sample=Image.new('RGB',(1500,885),'#252b2e')
 for col,f in enumerate([frames[len(frames)//3],frames[len(frames)//2],frames[len(frames)*2//3]]):sample.paste(f.resize((500,442),Image.Resampling.NEAREST),(col*500,0))
 # Separate native-size frames preserve source pixel density for visual review.
 picks=[]
 for step in [len(frames)//3,len(frames)//2,len(frames)*2//3]:
  p=H/(family+f'-motion-phase-{step:03}.png');frames[step].save(p);picks.append(p.name)
 reports[family]={'GIF':path.name,'reviewFrames':picks,'frames':len(frames),'durationMs':maxduration,'method':'Whole original-clock entry/work/exit sequence sampled at20fps, native2x nearest. Shorter direction sequences hold their exact final pose. Offline preview; not station integration.'}
old=json.loads((H/'action-motion-review.json').read_text()) if (H/'action-motion-review.json').exists() else {};old.update(reports)
(H/'action-motion-review.json').write_text(json.dumps(old,indent=2)+'\n');print(json.dumps({k:{'frames':q['frames'],'durationMs':q['durationMs']} for k,q in reports.items()}))
