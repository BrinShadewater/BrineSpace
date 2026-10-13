"""Package authored cryostasis fall/recovery poses at a frozen idle scale."""
from pathlib import Path
import json
import hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'character/cryo-fall-recovery-v1'
ACTORS={
    'bill':'character/crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png',
    'veld':'character/crew-runtime-matte-v1/veld/frames/idle-south-breathing-v1/000.png',
    'branforth':'character/crew-runtime-matte-v1/branforth/frames/idle-south-matte-v2/000.png',
}

def build(actor,idle_path):
    here=PACK/actor
    source=here/'sources/fall-recovery.png'
    raw=np.asarray(Image.open(source).convert('RGBA')).copy()
    labels,count=label(raw[:,:,3]>180)
    components=[]
    for value in range(1,count+1):
        y,x=np.where(labels==value)
        if len(x)>3000:components.append((float(y.mean()),float(x.mean()),value))
    assert len(components)==8,(actor,len(components))
    top=sorted(components,key=lambda row:row[0])[:4]
    bottom=sorted(components,key=lambda row:row[0])[4:]
    ordered=sorted(top,key=lambda row:row[1])+sorted(bottom,key=lambda row:row[1])
    masks=[labels==value for _,_,value in ordered]
    first_y,first_x=np.where(masks[0])
    idle=Image.open(ROOT/idle_path).convert('RGBA')
    authority=np.asarray(idle)
    iy,ix=np.where(authority[:,:,3]>180)
    scale=(iy.max()-iy.min()+1)/(first_y.max()-first_y.min()+1)
    # One neutral-material calibration, frozen for the entire sheet. Coloured
    # patches, skin and hair are excluded from neutral cloth/metal transfer.
    rgb=raw[:,:,:3].astype(float)
    spread=rgb.max(2)-rgb.min(2)
    neutral=masks[0]&(spread<24)&(rgb.mean(2)>20)
    ar=authority[:,:,:3].astype(float)
    target=(authority[:,:,3]>220)&((ar.max(2)-ar.min(2))<24)&(ar.mean(2)>20)
    quantiles=[0,.1,.25,.5,.75,.9,.98,1]
    src=np.quantile(rgb.mean(2)[neutral],quantiles)
    dest=np.quantile(ar.mean(2)[target],quantiles)
    src,indices=np.unique(src,return_index=True);dest=dest[indices]
    weight=np.clip(1-(spread-12)/16,0,1)
    mapped=np.interp(rgb.mean(2),src,dest)
    graded=rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None]
    r,g,b=rgb.transpose(2,0,1)
    warm=(r>g+12)&(g>b+5)&(r<g*1.7)
    graded[warm]=rgb[warm]*np.array([.84,.90,.96])
    if actor=='bill':
        patches=(r>g*1.7)&(r>b*1.7)
        graded[patches]=rgb[patches]*np.array([.68,.74,.82])
    raw[:,:,:3]=np.clip(graded,0,255).astype('uint8')
    frames=[];records=[]
    for index,mask in enumerate(masks):
        y,x=np.where(mask)
        bounds=[max(0,int(x.min())-3),max(0,int(y.min())-3),min(raw.shape[1],int(x.max())+4),min(raw.shape[0],int(y.max())+4)]
        rgba=raw.copy();rgba[~binary_dilation(mask,iterations=2)]=0
        crop=Image.fromarray(rgba).crop(bounds)
        size=(round(crop.width*scale),round(crop.height*scale))
        image=crop.resize(size,Image.Resampling.LANCZOS)
        floor=224-round((int(y.max())-bounds[1])*scale)
        position=(128-round(((int(x.min())+int(x.max()))/2-bounds[0])*scale),floor)
        canvas=Image.new('RGBA',(256,256))
        assert position[0]>=0 and position[1]>=0 and position[0]+image.width<=256 and position[1]+image.height<=256
        canvas.alpha_composite(image,position)
        if index in [0,7]:
            canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(idle,(36,52))
        path=here/'frames'/f'{index:03d}.png';path.parent.mkdir(parents=True,exist_ok=True);canvas.save(path)
        frames.append(canvas)
        records.append({'pose':index,'sourceBounds':bounds,'position':list(position),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest={'name':actor+' cryostasis fall and recovery','frameWidth':256,'frameHeight':256,'pivot':[128,224],
        'standingHeight':148,'textureFilter':'linear','states':[
            {'id':'cryo-fall','frameFiles':['frames/000.png','frames/001.png','frames/002.png','frames/003.png'],'frameDurationsMs':[80,200,200,220],'loop':False},
            {'id':'cryo-rise','frameFiles':['frames/003.png','frames/004.png','frames/005.png','frames/006.png','frames/007.png'],'frameDurationsMs':[80,150,400,400,220],'loop':False}]}
    (here/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (here/'registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'idleAuthority':idle_path,
        'uniformScale':scale,'neutralInput':src.tolist(),'neutralOutput':dest.tolist(),'frames':records},indent=2)+'\n')
    contact=Image.new('RGBA',(2048,256),(25,32,38,255))
    for index,frame in enumerate(frames):contact.alpha_composite(frame,(index*256,0))
    contact.convert('RGB').save(here/'contact.png')
    print(actor+': 8 authored poses registered; exact selected-idle endpoints; frozen scale '+str(round(scale,4)))

if __name__=='__main__':
    for actor,idle in ACTORS.items():
        if (PACK/actor/'sources/fall-recovery.png').exists():build(actor,idle)
