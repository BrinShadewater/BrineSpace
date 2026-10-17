"""Extract the authored twelve-pose pickup with one frozen anatomy calibration."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
from matte_grade import calibrate,grade
HERE=Path(__file__).resolve().parent

def refine(start,end):
    source=HERE/'sources/pickup-smooth-v3.png';raw=np.array(Image.open(source).convert('RGBA'))
    labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());bodies=[]
    for ident in np.where(counts>10000)[0]:
        if ident==0:continue
        y,x=np.where(labs==ident);bodies.append((int(y.min()),int(x.min()),int(ident)))
    assert len(bodies)==12,len(bodies)
    bodies.sort();ordered=[]
    for row in range(2):ordered.extend(sorted(bodies[row*6:(row+1)*6],key=lambda b:b[1]))
    masks=[labs==ident for _,_,ident in ordered]
    for ident in np.where((counts>100)&(counts<10000))[0]:
        y,x=np.where(labs==ident)
        slot=min(1,int(y.mean()/(raw.shape[0]/2)))*6+min(5,int(x.mean()/(raw.shape[1]/6)))
        masks[slot]|=labs==ident
    idle=Image.open(HERE.parent/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png').convert('RGBA')
    a=np.array(idle);iy,ix=np.where(a[:,:,3]>180);sy,sx=np.where(labs==ordered[0][2])
    scale_y=(iy.max()-iy.min()+1)/(sy.max()-sy.min()+1)
    ratios=[]
    for offset in range(100,127,2):
        tx=np.where(a[int(iy.min()+offset),:,3]>180)[0]
        rx=np.where(labs[round(sy.min()+offset/scale_y)]==ordered[0][2])[0]
        if len(rx):ratios.append((tx.max()-tx.min()+1)/(rx.max()-rx.min()+1))
    scale_x=float(np.median(ratios));boot=float(np.median(ix[(iy>=iy.max()-6)&(ix>np.median(ix))]))
    material_grade=calibrate(raw,labs==ordered[0][2],idle)
    frames=[];records=[]
    for i,mask in enumerate(masks):
        body=labs==ordered[i][2];by,bx=np.where(body);y,x=np.where(mask)
        p=raw.copy();p[~binary_dilation(mask,iterations=2)]=0
        p,diagnostic=grade(p,body,material_grade)
        x0,y0,x1,y1=max(0,int(x.min()-3)),max(0,int(y.min()-3)),int(x.max()+4),int(y.max()+4)
        source_boot=float(np.median(bx[(by>=by.max()-10)&(bx>np.median(bx))]))
        pos=(round(boot+36-(source_boot-x0)*scale_x),round(iy.max()+52-(by.max()-y0)*scale_y))
        im=Image.fromarray(p).crop((x0,y0,x1,y1));im=im.resize((round(im.width*scale_x),round(im.height*scale_y)),Image.Resampling.LANCZOS)
        assert pos[0]>=0 and pos[1]>=0 and pos[0]+im.width<=256 and pos[1]+im.height<=256
        canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,pos);frames.append(canvas)
        if i in [1,5,8]:
            dest=HERE/'grade-masks'/f'{i:02d}.png';dest.parent.mkdir(exist_ok=True)
            Image.fromarray(diagnostic).crop((x0,y0,x1,y1)).save(dest)
        records.append({'cell':i,'sourceBox':[x0,y0,x1,y1],'position':list(pos),'crownY':int(by.min())})
    # Source pose10 overshoots the standing height. Stop at pose9, then join
    # the retained held-case endpoint; never shrink individual pose bounds.
    frames=[start,*frames[1:10],end]
    (HERE/'pickup-registration.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scaleX':scale_x,'scaleY':scale_y,'frames':records,'materialGrade':material_grade,'endpointDerivation':'exact existing idle-plus-case and held-case images'},indent=2)+'\n')
    return frames
