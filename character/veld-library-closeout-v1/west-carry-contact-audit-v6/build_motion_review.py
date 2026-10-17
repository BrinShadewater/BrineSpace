from pathlib import Path
import json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;V5=P.parent/'west-carry-master-match-v5'
stride=.07351351351351351
frames=[];visited=set()
cache={}
for gear in ['bare','helmet']:
 for i in range(6):
  im=Image.open(V5/f'frames/{gear}/{i:03}.png').convert('RGBA')
  for h in [47,93,148]:
   s=h/148;cache[gear,i,h]=im.resize((round(256*s),round(256*s)),Image.Resampling.LANCZOS)
for tick in range(101):
 t=tick/60;slot=min(5,int((t%0.84)/.14));visited.add(slot)
 im=Image.new('RGB',(850,690),'#202a30');d=ImageDraw.Draw(im)
 d.text((16,14),'Veld West: fixed floor / preserved walking speed',fill='white')
 d.text((16,36),f'Pose {slot}; two cycles. Geometry replay, not native NPC capture.',fill='white')
 for h,y in [(47,165),(93,365),(148,625)]:
  s=h/148;cell=h/.17;root_x=-stride*t/.84*cell
  d.line((20,y,830,y),fill='#728792');d.text((20,y-20),f'{h}px',fill='white')
  for x in range(60,831,20):d.line((x,y-4,x,y+4),fill='#728792')
  for gear,x in [('bare',280),('helmet',660)]:
   img=cache[gear,slot,h];im.paste(img,(round(x+root_x-128*s),round(y-224*s)),img)
   d.text((x-50,y+18),gear,fill='white')
 frames.append(im)
assert visited==set(range(6))
frames[0].save(P/'world-motion.png',save_all=True,append_images=frames[1:],duration=[1000/60]*len(frames),loop=0,disposal=0,blend=0)
ap=Image.open(P/'world-motion.png');assert ap.n_frames==101
for i,im in enumerate(frames):ap.seek(i);assert ap.convert('RGB').tobytes()==im.tobytes()
(P/'MOTION_REVIEW.json').write_text(json.dumps({'scope':'Software geometric replay of V5 source holds against fixed floor; not native/controller evidence','ticks':101,'rateHz':60,'sourceSlotsVisited':sorted(visited),'cycleMs':840,'strideDistanceCells':stride,'pixelChecks':101,'failures':0,'runtimeScale':'cell_size*0.17/148','normalAdmission':False},indent=2)+'\n',encoding='utf8')
print('Built 101-frame two-cycle floor replay, exact decoded pixels')
