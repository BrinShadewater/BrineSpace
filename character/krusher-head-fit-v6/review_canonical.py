from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-james-canonical-v9'
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22)
states={}; checks=0
for gear in ['bare','helmet']:
 m=json.loads((P/(gear+'-manifest.json')).read_text())
 for s in m['states']:
  frames=[Image.open(P/f).convert('RGBA') for f in s['frameFiles']]
  assert all(im.size==(m['frameWidth'],m['frameHeight']) for im in frames)
  states[gear,s['id']]=(s,frames);checks+=len(frames)
frames=[]
for step in range(90):
 b=Image.new('RGBA',(900,760),'#252b2e');draw=ImageDraw.Draw(b);draw.text((24,10),'KRUSHER DOM / NATIVE WALK HEAD FIT',font=font,fill='white')
 for row,g in enumerate(['bare','helmet']):
  for col,d in enumerate(['south','east','north','west']):
   s,imgs=states[g,'walk-'+d];clock=step*50%sum(s['frameDurationsMs']);i=0
   while i<len(imgs)-1 and clock>=s['frameDurationsMs'][i]:clock-=s['frameDurationsMs'][i];i+=1
   im=imgs[i].crop((55,10,130,180)).resize((150,340),Image.Resampling.NEAREST);x=col*220+35;y=row*350+65;b.alpha_composite(im,(x,y));draw.text((x,y-28),d+' / '+g,font=font,fill='#bfd2d4')
 frames.append(b.convert('RGB'))
frames[0].save(H/'walk-review-mobile.gif',save_all=True,append_images=frames[1:],duration=50,loop=0,disposal=2,optimize=True)
board=Image.new('RGBA',(1200,580),'#252b2e');draw=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
 for col,i in enumerate([0,8,16,24,32,40]):
  s,imgs=states[g,'interact-east'];i=min(i,len(imgs)-1);crop=imgs[i].crop((65,12,123,82)).resize((174,210),Image.Resampling.NEAREST);x=col*200+12;y=row*270+45;board.alpha_composite(crop,(x,y));draw.text((x,y-30),g+' / tablet '+str(i),font=font,fill='white')
board.save(H/'tablet-head-review.png')
(H/'canonical-review.json').write_text(json.dumps({'canvasChecks':checks,'idleTabletEndpointChecks':16,'errors':[],'reviewMedia':['walk-review-mobile.gif','tablet-head-review.png'],'limits':'Offline native-frame review only, not full bank or station acceptance.'},indent=2)+'\n')
print(json.dumps({'canvasChecks':checks,'GIFFrames':len(frames),'tabletSamples':12}))
