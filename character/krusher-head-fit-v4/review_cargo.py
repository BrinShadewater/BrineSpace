from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-cargo-family-v4';rows=json.loads((P/'revision.json').read_text())['records'];font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),19);samples=[]
for g in ['bare','helmet']:
 for v in ['south','se','east','ne','north','nw','west','sw']:samples.append(next(q for q in rows if q['gear']==g and q['view']==v))
 for sid,frame in [('carry-turn-east-north',2),('carry-turn-north-west',4)]:samples.append(next(q for q in rows if q['gear']==g and q['state']==sid and q['frame']==frame))
board=Image.new('RGBA',(1000,1000),'#252b2e');draw=ImageDraw.Draw(board)
for i,q in enumerate(samples):
 d=q['details'];a=Image.open(P/q['output']).convert('RGBA');box=a.getbbox();cx=round(sum(d['visorBox'][::2])/2) if 'visorBox' in d else d.get('paste',[round((box[0]+box[2])/2)-12,box[1]])[0]+12;cy=d.get('paste',[0,box[1]])[1];crop=a.crop((cx-28,cy-3,cx+28,cy+44)).resize((224,188),Image.Resampling.NEAREST);x=i%4*250;y=i//4*200;board.alpha_composite(crop,(x,y));draw.text((x+3,y+170),f"{q['gear']} / {q['view']} / {q['frame']}",font=font,fill='white')
board.save(H/'cargo-head-review.png')
samples=[]
for g in ['bare','helmet']:
 for sid in ['carry-east','carry-south','carry-west','carry-turn-north-west']:
  group=[q for q in rows if q['gear']==g and q['state']==sid];samples.append(group[len(group)//2])
board=Image.new('RGBA',(1000,650),'#252b2e');draw=ImageDraw.Draw(board)
for i,q in enumerate(samples):
 a=Image.open(P/q['output']).convert('RGBA');crop=a.crop((48,40,208,240)).resize((240,300),Image.Resampling.NEAREST);x=i%4*250;y=i//4*325;board.alpha_composite(crop,(x,y));draw.text((x+3,y+305),q['gear']+' '+q['state'],font=font,fill='white')
board.save(H/'cargo-body-review.png')
lanes=['east','north','west','south'];sequences={};review={}
for g in ['bare','helmet']:
 sm={s['id']:s for s in json.loads((P/(g+'-manifest.json')).read_text())['states']}
 for d in lanes:
  states=[sm['carry-turn-'+d+'-'+target] for target in lanes if target!=d];entries=[];t=0
  for s in states:
   for f,ms in zip(s['frameFiles'],s['frameDurationsMs']):entries.append((t,t+ms,f));t+=ms
  sequences[g,d]=(entries,t);review[g+':'+d]=[s['id'] for s in states]
length=max(t for entries,t in sequences.values());frames=[]
for i in range(math.ceil(length/50)+1):
 board=Image.new('RGBA',(1000,820),'#252b2e');draw=ImageDraw.Draw(board)
 for row,g in enumerate(['bare','helmet']):
  for col,d in enumerate(lanes):
   entries,t=sequences[g,d];at=min(i*50,t-.001);f=next(f for lo,hi,f in entries if lo<=at<hi);a=Image.open(P/f).convert('RGBA');crop=a.crop((68,45,188,231)).resize((240,372),Image.Resampling.NEAREST);x=col*250;y=row*410;board.alpha_composite(crop,(x,y+25));draw.text((x+5,y+2),g+' turns from '+d,font=font,fill='white')
 frames.append(board.convert('RGB'))
frames[0].save(H/'cargo-turn-review.gif',save_all=True,append_images=frames[1:],duration=50,loop=0)
for frac in [.25,.5,.75]:frames[round((len(frames)-1)*frac)].save(H/f'cargo-turn-phase-{round(frac*100):02}.png')
(H/'cargo-motion-review.json').write_text(json.dumps({'states':review,'durationMs':length,'captureStepMs':50,'scope':'All12original turns per gear, authored frames/clocks sampled20fps at2xnearest; shorter lanes hold final source. Separate sequences concatenate without inventing connecting motion.'},indent=2)+'\n')
print('Rendered20cargo busts,8full-body poses and all12turns per gear.')
