from pathlib import Path
import json,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage
R=Path(__file__).resolve().parent
OLD=R.with_name('veld-side-walk-v1')
source=R/'sources/west-opposite-01.png'
im=Image.open(source).convert('RGBA');a=np.array(im)[:,:,3]
assert (a<8).mean()>.1
lab,_=ndimage.label(a>=128);sizes=np.bincount(lab.ravel())
parts=[(i+1,b) for i,b in enumerate(ndimage.find_objects(lab)) if b and sizes[i+1]>1000]
assert len(parts)==3,len(parts)
parts.sort(key=lambda p:p[1][1].start)
scale=148/float(np.median([b[0].stop-b[0].start for _,b in parts]))
folder=R/'frames/walk-west';folder.mkdir(parents=True,exist_ok=True)
for i,old_index in enumerate([2,0,1]):
    (folder/f'{i:03}.png').write_bytes((OLD/f'frames/walk-west/{old_index:03}.png').read_bytes())
for i,(label,(ys,xs)) in enumerate(parts,3):
    crop=im.crop((xs.start,ys.start,xs.stop,ys.stop))
    crop.putalpha(Image.fromarray(np.where(lab[ys,xs]==label,255,0).astype('uint8')))
    small=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
    _,xx=np.nonzero(np.array(crop)[:,:,3][int(crop.height*.05):int(crop.height*.14)]>=128)
    left=84-round(float(np.median(xx))*scale)
    assert left>=2 and left+small.width<=182
    frame=Image.new('RGBA',(184,184));frame.alpha_composite(small,(left,172-small.height));frame.save(folder/f'{i:03}.png')
m=json.loads((OLD/'manifest.json').read_text())
west=next(s for s in m['states'] if s['id']=='walk-west')
west['frameDurationsMs']=[150]*6
west['derivations']={'0':'v1/west/2','1':'v1/west/0','2':'v1/west/1','3':'opposite/0','4':'opposite/1','5':'opposite/2'}
m['status']='west_motion_review_candidate_east_owner_accepted'
(R/'manifest.json').write_text(json.dumps(m,indent=2))
for state in m['states']:
    frames=[Image.open(R/p).convert('RGBA') for p in state['frameFiles']]
    frames[0].save(R/(state['id']+'.webp'),save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,lossless=True)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
oldm=json.loads((OLD/'manifest.json').read_text());oldstate=next(s for s in oldm['states'] if s['id']=='walk-west')
review=[]
for t in range(0,900,30):
    canvas=Image.new('RGB',(736,480),'#263139');d=ImageDraw.Draw(canvas)
    for col,(base,state,label) in enumerate([(OLD,oldstate,'Previous west'),(R,west,'Opposite-step repair')]):
        phase=t
        for i,duration in enumerate(state['frameDurationsMs']):
            if phase<duration:break
            phase-=duration
        f=Image.open(base/state['frameFiles'][i]).convert('RGBA')
        big=f.resize((368,368),Image.Resampling.NEAREST);canvas.paste(big,(col*368,30),big)
        d.text((col*368+12,8),label+f' / {i+1}',font=font,fill='white')
        small=f.resize((56,56),Image.Resampling.LANCZOS);canvas.paste(small,(col*368+156,405),small)
    review.append(canvas)
review[0].save(R/'west-before-after.gif',save_all=True,append_images=review[1:],duration=30,loop=0)
sheet=Image.new('RGB',(1104,210),'#263139');d=ImageDraw.Draw(sheet)
for i,p in enumerate(west['frameFiles']):
    f=Image.open(R/p);sheet.paste(f,(i*184,0),f);d.text((i*184+10,188),str(i+1),fill='white')
sheet.save(R/'west-contact-sheet.png')
east=next(s for s in m['states'] if s['id']=='walk-east')
assert all((R/p).read_bytes()==(OLD/p).read_bytes() for p in east['frameFiles'])
print('West opposite-step candidate built; all six accepted east frames unchanged.')
