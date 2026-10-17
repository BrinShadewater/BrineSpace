"""Extract generated foundation views and compare with untouched accepted front."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
R=Path(__file__).resolve().parent
source=R/'side-master-01.png'
im=Image.open(source).convert('RGBA');a=np.array(im)
assert (a[:,:,3]<8).mean()>.1,'Source lacks true transparency'
lab,n=ndimage.label(a[:,:,3]>=128);sizes=np.bincount(lab.ravel())
objects=ndimage.find_objects(lab)
parts=[(i+1,b) for i,b in enumerate(objects) if b and sizes[i+1]>2000]
assert len(parts)==2,f'Expected two isolated figures, got {len(parts)}'
parts.sort(key=lambda p:p[1][1].start)
frames=[];records=[]
for name,(label,(ys,xs)) in zip(['east','west'],parts):
    box=(xs.start,ys.start,xs.stop,ys.stop);crop=im.crop(box)
    crop.putalpha(Image.fromarray(np.where(lab[ys,xs]==label,255,0).astype('uint8')))
    scale=148/crop.height
    size=(round(crop.width*scale),148)
    small=crop.resize(size,Image.Resampling.LANCZOS)
    frame=Image.new('RGBA',(184,184));frame.alpha_composite(small,((184-size[0])//2,24))
    frame.save(R/f'{name}-standing.png');frames.append(frame)
    records.append({'direction':name,'sourceBox':box,'standingHeight':148,'mirrored':False})
front_path=R.parent/'veld-animation-pilot-v12/frames/idle-south/000.png'
front=Image.open(front_path).convert('RGBA')
sheet=Image.new('RGB',(1104,600),'#263139');d=ImageDraw.Draw(sheet)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
for i,(label,f) in enumerate(zip(['A - Approved front','B - New east master','C - New west master'],[front,*frames])):
    large=f.resize((368,368),Image.Resampling.NEAREST);sheet.paste(large,(i*368,45),large)
    d.text((i*368+20,15),label,font=font,fill='white')
    small=f.resize((56,56),Image.Resampling.LANCZOS);sheet.paste(small,(i*368+155,455),small)
d.text((20,555),'Static foundation study / 148px standing, enlarged above; approximately 45px below',font=font,fill='white')
sheet.save(R/'comparison.png')
(R/'extraction.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'front_sha256':hashlib.sha256(front_path.read_bytes()).hexdigest(),'figures':records,'status':'static_candidate_not_animation_or_owner_accepted'},indent=2),encoding='utf-8')
print('Two independent side masters extracted; front comparison unchanged.')
