"""Package whole authored figures; preserve detached cases and frozen anatomy scale."""
import copy, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
from matte_grade import calibrate,grade
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def main():
    source=HERE/'sources/actions-gait-v2.png'
    raw=np.array(Image.open(source).convert('RGBA'))
    labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel())
    figures=[]
    for ident in np.where(counts>10000)[0]:
        if ident==0:continue
        y,x=np.where(labs==ident)
        figures.append((int(y.min()),int(x.min()),int(ident)))
    assert len(figures)==18,len(figures)
    figures.sort();ordered=[]
    for row in range(3):ordered.extend(sorted(figures[row*6:(row+1)*6],key=lambda t:t[1]))
    centers=[]
    for _,_,ident in ordered:
        y,x=np.where(labs==ident);centers.append((float(x.mean()),float(y.mean())))
    masks=[labs==ident for _,_,ident in ordered]
    detached=[]
    for ident in np.where((counts>100)&(counts<10000))[0]:
        y,x=np.where(labs==ident)
        # Ground cases sit below the body: vertical proximity would steal them
        # into the neighboring crouched figure. Use authored six-column gutters.
        slot=min(2,int(y.mean()/(raw.shape[0]/3)))*6+min(5,int(x.mean()/(raw.shape[1]/6)))
        masks[slot]|=labs==ident;detached.append({'component':int(ident),'cell':slot,'pixels':int(counts[ident])})
    idle=Image.open(ROOT/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png').convert('RGBA')
    a=np.array(idle);iy,ix=np.where(a[:,:,3]>180)
    neutral=labs==ordered[0][2];sy,sx=np.where(neutral)
    scale_y=(iy.max()-iy.min()+1)/(sy.max()-sy.min()+1)
    ratios=[]
    for offset in range(100,127,2):
        target=np.where(a[int(iy.min()+offset),:,3]>180)[0]
        initial=np.where(neutral[round(sy.min()+offset/scale_y)])[0]
        if len(initial):ratios.append((target.max()-target.min()+1)/(initial.max()-initial.min()+1))
    scale_x=float(np.median(ratios))
    boot=float(np.median(ix[(iy>=iy.max()-6)&(ix>np.median(ix))]))
    material_grade=calibrate(raw,neutral,idle)
    frames=[];records=[];ground=None
    for i,mask in enumerate(masks):
        body=labs==ordered[i][2];by,bx=np.where(body);y,x=np.where(mask)
        p=raw.copy();p[~binary_dilation(mask,iterations=2)]=0
        p,diagnostic=grade(p,body,material_grade)
        x0,y0,x1,y1=max(0,int(x.min()-3)),max(0,int(y.min()-3)),int(x.max()+4),int(y.max()+4)
        source_boot=float(np.median(bx[(by>=by.max()-10)&(bx>np.median(bx))]))
        # Fixed head/torso registration through walking; planted boot for stationary bends.
        if 6<=i<12:
            ny,nx=np.where(neutral&(np.indices(neutral.shape)[0]<sy.min()+45))
            hy,hx=np.where(body&(np.indices(body.shape)[0]<by.min()+45))
            source_boot=float((hx.min()+hx.max())/2 - (nx.min()+nx.max())/2 + np.median(sx[(sy>=sy.max()-10)&(sx>np.median(sx))]))
        position=(round(boot+36-(source_boot-x0)*scale_x),round(iy.max()+52-(by.max()-y0)*scale_y))
        im=Image.fromarray(p).crop((x0,y0,x1,y1));im=im.resize((round(im.width*scale_x),round(im.height*scale_y)),Image.Resampling.LANCZOS)
        assert position[0]>=0 and position[1]>=0
        assert position[0]+im.width<=256 and position[1]+im.height<=256
        canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,position);frames.append(canvas)
        if i in [5,6,14]:
            dest=HERE/'grade-masks'/f'cargo-{i:02d}.png';dest.parent.mkdir(exist_ok=True)
            Image.fromarray(diagnostic).crop((x0,y0,x1,y1)).save(dest)
        if i==0:
            case=p.copy();case[body]=0;case[~binary_dilation(mask&~body,iterations=2)]=0
            ci=Image.fromarray(case).crop((x0,y0,x1,y1)).resize(im.size,Image.Resampling.LANCZOS)
            ground=Image.new('RGBA',(256,256));ground.alpha_composite(idle,(36,52));ground.alpha_composite(ci,position)
        records.append({'cell':i,'sourceBox':[x0,y0,x1,y1],'position':list(position)})
    chains={'pickup-east':[ground,*frames[1:6]],'carry-east':frames[6:12],'unload-east':[frames[5],*frames[13:17],ground]}
    from refine_pickup import refine
    chains['pickup-east']=refine(ground,frames[5])
    base=json.loads((ROOT/'major-bill-v3/packs/bare-256x256-p128-224/manifest.json').read_text())
    selected={s['id']:s for s in base['states']};pack={k:v for k,v in base.items() if k!='states'}
    pack.update(name='Bill bare east cargo candidate',status='owner_visual_accepted_staged_2026_09_29_detail_v6',textureFilter='linear',states=[])
    hashes={}
    for key,images in chains.items():
        state=copy.deepcopy(selected[key]);state['frameFiles']=[]
        if key=='pickup-east':
            state['frameDurationsMs']=[35,35,40,40,45,45,50,50,50,65,65]
            for field in ['facings','waterKinds','waterPoses','depthOffsets']:
                state[field]=[state[field][min(5,i*6//11)] for i in range(11)]
        state['provenance']='independent authored whole figures; one frozen anatomy calibration; current idle plus preserved ground case endpoints'
        for i,im in enumerate(images):
            p=HERE/'frames'/key/f'{i:03d}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
            rel=p.relative_to(HERE).as_posix();state['frameFiles'].append(rel);hashes[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
        pack['states'].append(state)
    pack['strideDistanceCells']={'carry':0.12}
    for name,value in [('manifest.json',pack),('frame-hashes.json',hashes),('source-registration.json',{'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scaleX':scale_x,'scaleY':scale_y,'materialGrade':material_grade,'detachedCases':detached,'frames':records})]:
        (HERE/name).write_text(json.dumps(value,indent=2)+'\n')
    out=Image.new('RGB',(3072,768),(34,48,56));draw=ImageDraw.Draw(out)
    for row,(key,images) in enumerate(chains.items()):
        for i,im in enumerate(images):out.paste(im,(256*i,256*row),im);draw.text((256*i+4,256*row+4),key+' '+str(i),fill='white')
    out.save(HERE/'contact-sheet.png')
    assert chains['pickup-east'][-1].tobytes()==chains['unload-east'][0].tobytes()
    assert chains['pickup-east'][0].tobytes()==chains['unload-east'][5].tobytes()
    assert len({im.tobytes() for im in chains['carry-east']})==6
    print('Cargo east:23 frame references;shared idle-calibrated matte materials;motion/timing preserved')

if __name__=='__main__':main()
