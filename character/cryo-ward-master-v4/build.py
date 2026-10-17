"""Extract the reviewed ward masters at one frozen scale per chassis family."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy.ndimage import label, binary_dilation
from PIL import Image, ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
NAMES=['broken-human-a','broken-human-b','pet-closed-occupied','pet-closed-empty','pet-open-empty']
raw=np.asarray(Image.open(HERE/'sources/master-v4.png').convert('RGBA'))
labels,count=label(raw[:,:,3]>128)
objects=[]
for value in range(1,count+1):
    y,x=np.where(labels==value)
    if len(x)>8000:objects.append((x.mean(),value,(x.min(),y.min(),x.max()+1,y.max()+1)))
objects.sort()
assert len(objects)==5,len(objects)
human_scale=264/max(box[3]-box[1] for _,_,box in objects[:2])
pet_scale=160/(objects[3][2][3]-objects[3][2][1])
(HERE/'masters').mkdir(exist_ok=True)
(HERE/'frames').mkdir(exist_ok=True)
records=[];frames=[]
for index,(name,(_,value,box)) in enumerate(zip(NAMES,objects)):
    box=tuple(int(v) for v in box)
    pixels=raw.copy();pixels[~binary_dilation(labels==value,iterations=2)]=0
    master=Image.fromarray(pixels).crop(box)
    master.save(HERE/'masters'/f'{name}.png')
    scale=human_scale if index<2 else pet_scale
    small=master.resize((round(master.width*scale),round(master.height*scale)),Image.Resampling.LANCZOS)
    frame=Image.new('RGBA',(512,512));at=(256-small.width//2,448-small.height)
    assert at[0]>0 and at[1]>0
    frame.alpha_composite(small,at);frame.save(HERE/'frames'/f'{name}.png');frames.append(frame)
    records.append(dict(id=name,bounds=list(box),scale=scale,size=list(small.size),position=list(at),sha256=hashlib.sha256((HERE/'frames'/f'{name}.png').read_bytes()).hexdigest()))
manifest=dict(status='staged-master-review',standingHeight=148,pivot=[256,448],textureFilter='linear',frameWidth=512,frameHeight=512,
    sourceSha256=hashlib.sha256((HERE/'sources/master-v4.png').read_bytes()).hexdigest(),humanScale=human_scale,petScale=pet_scale,objects=records)
(HERE/'registration.json').write_text(json.dumps(manifest,indent=2)+'\n')
review=Image.new('RGBA',(1100,380),(35,43,49,255));draw=ImageDraw.Draw(review)
for i,(name,frame) in enumerate(zip(NAMES,frames)):
    sprite=frame.crop(frame.getbbox());review.alpha_composite(sprite,(i*210+40,330-sprite.height))
    draw.text((i*210+10,345),name,fill='white')
review.convert('RGB').save(HERE/'master-review.png')
# Same source-pixel scale: all three share the 148px world denominator.
scale_review=Image.new('RGBA',(720,390),(43,50,57,255))
for frame,x in [(frames[0],40),(frames[2],300),(frames[4],460)]:
    sprite=frame.crop(frame.getbbox());scale_review.alpha_composite(sprite,(x,340-sprite.height))
bill=Image.open(ROOT/'character/crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png').convert('RGBA')
margot=Image.open(ROOT/'character/margot-polish-v1/frames/idle-south/000.png').convert('RGBA')
scale_review.alpha_composite(bill,(185,340-172));scale_review.alpha_composite(margot,(370,340-172))
ImageDraw.Draw(scale_review).text((15,360),'STATIC SCALE REVIEW / shared 148px calibration / not a gameplay capture',fill='white')
scale_review.convert('RGB').save(HERE/'scale-review.png')
assert all(Image.open(HERE/'frames'/f'{name}.png').getpixel((0,0))[3]==0 for name in NAMES)
print('Five masters packaged; true alpha; fixed human/pet scales; matching floor pivots.')
