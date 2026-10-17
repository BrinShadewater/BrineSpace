from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
R=Path(__file__).resolve().parent
states=[];clips=[];audit=[];dur=[300,260,280,300,280,300]
for direction in ['east','west']:
 sid='idle-'+direction;im=Image.open(R/'sources'/f'{sid}-01.png').convert('RGBA');a=np.array(im)[:,:,3]
 assert (a<8).mean()>.1
 lab,_=ndimage.label(a>=128);sizes=np.bincount(lab.ravel());parts=[(i+1,b) for i,b in enumerate(ndimage.find_objects(lab)) if b and sizes[i+1]>1000]
 assert len(parts)==6,(sid,len(parts))
 parts.sort(key=lambda p:p[1][0].start);parts=sorted(parts[:3],key=lambda p:p[1][1].start)+sorted(parts[3:],key=lambda p:p[1][1].start)
 frames=[];files=[];boxes=[];folder=R/'frames'/sid;folder.mkdir(parents=True,exist_ok=True)
 for i,(label,(ys,xs)) in enumerate(parts):
  box=(xs.start,ys.start,xs.stop,ys.stop);boxes.append(box);crop=im.crop(box);crop.putalpha(Image.fromarray(np.where(lab[ys,xs]==label,255,0).astype('uint8')))
  scale=148/crop.height;small=crop.resize((round(crop.width*scale),148),Image.Resampling.LANCZOS)
  _,xx=np.nonzero(np.array(crop)[:,:,3][int(crop.height*.05):int(crop.height*.14)]>=128);left=(100 if direction=='east' else 84)-round(float(np.median(xx))*scale)
  assert 2<=left and left+small.width<=182
  frame=Image.new('RGBA',(184,184));frame.alpha_composite(small,(left,24));p=folder/f'{i:03}.png';frame.save(p);files.append(p.relative_to(R).as_posix());frames.append(frame)
 frames[0].save(R/f'{sid}.webp',save_all=True,append_images=frames[1:],duration=dur,loop=0,lossless=True)
 states.append(dict(id=sid,frameFiles=files,frameCount=6,frameDurationsMs=dur,loop=True,mirrored=False));clips.append(frames);audit.append(dict(state=sid,sourceBoxes=boxes))
(R/'manifest.json').write_text(json.dumps(dict(name='Veld approved-foundation side idle',frameWidth=184,frameHeight=184,pivot=[92,172],standingHeight=148,status='candidate_not_installed',states=states),indent=2))
(R/'extraction.json').write_text(json.dumps(audit,indent=2))
review=[]
for i in range(6):
 canvas=Image.new('RGB',(736,900),'#263139');d=ImageDraw.Draw(canvas)
 for row,direction in enumerate(['east','west']):
  master=Image.open(R.parent/'veld-side-foundation-v1'/f'{direction}-standing.png').convert('RGBA')
  for col,f in enumerate([master,clips[row][i]]):
   big=f.resize((368,368),Image.Resampling.NEAREST);canvas.paste(big,(col*368,row*450+25),big);d.text((col*368+20,row*450+10),direction+(' approved master' if col==0 else f' idle frame {i+1}/6'),fill='white')
   small=f.resize((56,56),Image.Resampling.LANCZOS);canvas.paste(small,(col*368+156,row*450+390),small)
 review.append(canvas)
review[0].save(R/'idle-review.gif',save_all=True,append_images=review[1:],duration=dur,loop=0)
review[0].save(R/'idle-review.png')
print('12 frames / two independent idle clips extracted; source colours preserved')
