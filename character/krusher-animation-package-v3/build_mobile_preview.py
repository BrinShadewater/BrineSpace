from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,bisect
P=Path(__file__).resolve().parent;R=P.parents[1]
index=json.loads((P/'package.json').read_text());clips=[]
for gear in ['bare','helmet']:
 for key in ['walk-east','inspect-south','repair-east']:
  mp=P/index['states'][gear+':'+key]['manifest'];m=json.loads(mp.read_text());s=next(s for s in m['states'] if s['id']==key)
  ims=[Image.open(mp.parent/f).convert('RGBA') for f in s['frameFiles']];pivot=s.get('pivot',m['pivot']);times=[];total=0
  for duration in s['frameDurationsMs']:total+=duration;times.append(total)
  xmin=min((im.getbbox()[0]-pivot[0])*2 for im in ims);xmax=max((im.getbbox()[2]-pivot[0])*2 for im in ims)
  assert xmax-xmin<=300
  anchor=int((300-(xmax-xmin))/2-xmin)
  clips.append((gear,key,ims,pivot,times,anchor))
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22);frames=[]
for tick in range(100):
 out=Image.new('RGBA',(900,940),'#252b2e');draw=ImageDraw.Draw(out);draw.text((18,12),'KRUSHER DOM / SYSTEM ADMINISTRATOR',font=font,fill='white')
 for i,(gear,key,ims,pivot,times,anchor) in enumerate(clips):
  im=ims[min(bisect.bisect_right(times,(tick*50)%times[-1]),len(ims)-1)];box=im.getbbox();crop=im.crop(box);crop=crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST)
  x=i%3*300+anchor+int((box[0]-pivot[0])*2);y=i//3*450+420+int((box[1]-pivot[1])*2)
  assert i%3*300<=x and x+crop.width<=(i%3+1)*300 and i//3*450+95<=y and y+crop.height<=(i//3+1)*450
  out.alpha_composite(crop,(x,y));draw.text((i%3*300+18,i//3*450+65),gear+' / '+key,font=font,fill='#afd1d3')
 frames.append(out.convert('RGB'))
frames[0].save(P/'references/animation-preview-mobile.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,optimize=True);frames[40].save(P/'references/animation-preview-mobile.png')
print('Mobile source preview:100frames,5seconds,20fps,both gears,2x nearest; every tile bounds check passed.')
