"""Package painted layers once; every pet state shares this chassis and door."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
raw=np.asarray(Image.open(HERE/'sources/layers.png').convert('RGBA'))
labels,count=label(raw[:,:,3]>128)
objects=[]
for value in range(1,count+1):
    y,x=np.where(labels==value)
    if len(x)>8000:objects.append((x.mean(),value,tuple(int(v) for v in (x.min(),y.min(),x.max()+1,y.max()+1))))
objects.sort();assert len(objects)==4
names=['broken-human-a','broken-human-b','pet-chassis','pet-door']
human_scale=264/max(box[3]-box[1] for _,_,box in objects[:2])
pet_scale=160/(objects[2][2][3]-objects[2][2][1])
for folder in ['masters','frames']:(HERE/folder).mkdir(exist_ok=True)
records=[];frames=[]
for i,(name,(_,value,box)) in enumerate(zip(names,objects)):
    owned=raw.copy();owned[~binary_dilation(labels==value,iterations=2)]=0
    master=Image.fromarray(owned).crop(box);master.save(HERE/'masters'/f'{name}.png')
    scale=human_scale if i<2 else pet_scale
    small=master.resize((round(master.width*scale),round(master.height*scale)),Image.Resampling.LANCZOS)
    at=(256-small.width//2,292 if i==3 else 448-small.height)
    frame=Image.new('RGBA',(512,512));frame.alpha_composite(small,at)
    frame.save(HERE/'frames'/f'{name}.png');frames.append(frame)
    assert frame.getpixel((0,0))[3]==0 and frame.getbbox()[1]>0
    records.append(dict(id=name,sourceBounds=box,scale=scale,size=small.size,position=at,sha256=hashlib.sha256((HERE/'frames'/f'{name}.png').read_bytes()).hexdigest()))
assert frames[3].getpixel((256,355))[3]==0,'Door aperture must retain real alpha'
glass=Image.new('RGBA',(61,91),(150,184,201,50))
closed=frames[2].copy();closed.alpha_composite(glass,(226,311));closed.alpha_composite(frames[3])
opened=frames[2].copy();opened.alpha_composite(glass,(226,311-82));opened.alpha_composite(frames[3],(0,-82))
closed.save(HERE/'frames/pet-closed-empty.png');opened.save(HERE/'frames/pet-open-empty.png')
manifest=dict(status='layered-runtime',standingHeight=148,pivot=[256,448],glass=[226,311,61,91],doorTravel=82,glassOverlapPixels=9,frameSize=[512,512],runtimeFrameSize=[512,640],humanScale=human_scale,petScale=pet_scale,objects=records,sourceSha256=hashlib.sha256((HERE/'sources/layers.png').read_bytes()).hexdigest())
(HERE/'registration.json').write_text(json.dumps(manifest,indent=2)+'\n')
board=Image.new('RGBA',(1100,390),(35,43,49,255));draw=ImageDraw.Draw(board)
for i,(name,frame) in enumerate(zip(['broken A','broken B','closed / same layers','open / same layers'],[frames[0],frames[1],closed,opened])):
    sprite=frame.crop(frame.getbbox());board.alpha_composite(sprite,(i*245+40,350-sprite.height));draw.text((i*245+25,365),name,fill='white')
board.convert('RGB').save(HERE/'master-review.png')
print('PASS: four painted components, true door aperture, one chassis/door for both endpoints, frozen family scale.')
