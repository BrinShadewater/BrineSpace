from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-rest-family-v6';H=Path(__file__).resolve().parent;rows=json.loads((P/'revision.json').read_text())['records'];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),19);samples=[]
for g in ['bare','helmet']:
 for v in ['east','south','west','north']:
  group=[q for q in rows if q['gear']==g and q['view']==v and q['details'].get('tilt',0)==80];samples.append(group[0] if group else next(q for q in rows if q['gear']==g and q['view']==v))
 for v in ['east','south','west']:
  group=[q for q in rows if q['gear']==g and q['view']==v and 0<q['details'].get('tilt',0)<80];samples.append(group[len(group)//2])
board=Image.new('RGBA',(1000,880),'#252b2e');draw=ImageDraw.Draw(board)
for i,q in enumerate(samples):
 a=Image.open(P/q['output']).convert('RGBA');d=q['details'];at=d.get('paste',[110,80]);cx=at[0]+(Image.open(R/d['headSource'][6:]).width//2 if 'headSource' in d else 15);cy=at[1]+(Image.open(R/d['headSource'][6:]).height//2 if 'headSource' in d else 15);crop=a.crop((cx-32,cy-30,cx+32,cy+34)).resize((192,192),Image.Resampling.NEAREST);x=i%4*250+20;y=i//4*220;board.alpha_composite(crop,(x,y));draw.text((x,y+195),q['gear']+' '+q['view']+' '+str(d.get('tilt')),font=font,fill='white')
board.save(H/'rest-head-review.png')
board=Image.new('RGBA',(1000,1080),'#252b2e');draw=ImageDraw.Draw(board)
for i,q in enumerate(samples[:4]+samples[7:11]):
 a=Image.open(P/q['output']).convert('RGBA');x=i%2*500;y=i//2*270;board.alpha_composite(a.resize((384,384),Image.Resampling.NEAREST),(x+30,y-80));draw.text((x+10,y+240),q['gear']+' '+q['state'],font=font,fill='white')
board.save(H/'rest-body-review.png')
sequences={};review={}
for g in ['bare','helmet']:
 sm={s['id']:s for s in json.loads((P/(g+'-manifest.json')).read_text())['states']}
 for d in ['east','south','west','north']:
  names=['lie-down-'+d,'sleep-'+d,'get-up-'+d];entries=[];t=0
  for sid in names:
   for f,ms in zip(sm[sid]['frameFiles'],sm[sid]['frameDurationsMs']):entries.append((t,t+ms,f));t+=ms
  sequences[g,d]=(entries,t);review[g+':'+d]=names
frames=[];length=max(t for entries,t in sequences.values())
for i in range(math.ceil(length/50)+1):
 board=Image.new('RGBA',(1024,580),'#252b2e');draw=ImageDraw.Draw(board)
 for row,g in enumerate(['bare','helmet']):
  for col,d in enumerate(['east','south','west','north']):
   entries,t=sequences[g,d];at=min(i*50,t-.001);f=next(f for lo,hi,f in entries if lo<=at<hi);a=Image.open(P/f).convert('RGBA');board.alpha_composite(a,(col*256,row*290+25));draw.text((col*256+5,row*290+2),g+' '+d,font=font,fill='white')
 frames.append(board.convert('RGB'))
frames[0].save(H/'rest-motion-review.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
for frac in [.1,.5,.9]:frames[round((len(frames)-1)*frac)].save(H/f'rest-motion-phase-{round(frac*100):02}.png')
(H/'rest-motion-review.json').write_text(json.dumps({'sequences':review,'durationMs':length,'sampleStepMs':50,'scope':'Original lie-down,one sleep loop,get-up pergear/cardinal; source clocks20fps sampling atnative1x. Bunk-specific entry/exit separate.'},indent=2)+'\n');print('Rendered current rest bust/body and original-clock lie/sleep/rise review.')
