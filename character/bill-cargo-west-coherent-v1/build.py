"""Independent west cargo figures, calibrated to selected west idle."""
import copy,hashlib,json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'bill-cargo-east-coherent-v1'))
from matte_grade import calibrate,grade
IDLE='crew-runtime-matte-v1/bill/frames/idle-west-breathing-v1/000.png'

def extract(source,idle,walk_row=False):
    raw=np.array(Image.open(source).convert('RGBA'));labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());figures=[]
    for ident in np.where(counts>7000)[0]:
        if ident==0:continue
        y,x=np.where(labs==ident);figures.append((int(y.min()),int(x.min()),int(ident)))
    assert len(figures)==12,(source,len(figures))
    figures.sort();ordered=[]
    for row in range(2):ordered.extend(sorted(figures[row*6:(row+1)*6],key=lambda t:t[1]))
    masks=[labs==ident for _,_,ident in ordered];detached=[]
    for ident in np.where((counts>100)&(counts<7000))[0]:
        y,x=np.where(labs==ident);slot=min(1,int(y.mean()/(raw.shape[0]/2)))*6+min(5,int(x.mean()/(raw.shape[1]/6)))
        masks[slot]|=labs==ident;detached.append({'cell':slot,'pixels':int(counts[ident])})
    a=np.array(idle);iy,ix=np.where(a[:,:,3]>180);neutral=labs==ordered[0][2]
    yy,xx=np.indices(neutral.shape)
    # The first source case touches the boot silhouette and is in the same
    # connected component. Explicit inspected crop preserves the detached prop.
    ground_case=(xx>=35)&(xx<119)&(yy>=430)&(yy<500)&masks[0] if not walk_row else np.zeros_like(neutral)
    neutral=neutral&~ground_case;sy,sx=np.where(neutral)
    scale_y=(iy.max()-iy.min()+1)/(sy.max()-sy.min()+1);ratios=[]
    for offset in range(100,127,2):
        tx=np.where(a[int(iy.min()+offset),:,3]>180)[0];rx=np.where(neutral[round(sy.min()+offset/scale_y)])[0]
        if len(rx):ratios.append((tx.max()-tx.min()+1)/(rx.max()-rx.min()+1))
    scale_x=float(np.median(ratios));boot=float(np.median(ix[(iy>=iy.max()-6)&(ix<np.median(ix))]))
    settings=calibrate(raw,neutral,idle,IDLE,'west');frames=[];records=[];ground=None
    for i,mask in enumerate(masks):
        body=(labs==ordered[i][2])&(~ground_case if i==0 else True);by,bx=np.where(body);y,x=np.where(mask)
        p=raw.copy();p[~binary_dilation(mask,iterations=2)]=0;p,diagnostic=grade(p,body,settings)
        x0,y0,x1,y1=max(0,int(x.min()-3)),max(0,int(y.min()-3)),int(x.max()+4),int(y.max()+4)
        source_boot=float(np.median(bx[(by>=by.max()-10)&(bx<np.median(bx))]))
        if walk_row and i>=6:
            yy=np.indices(body.shape)[0];hy,hx=np.where(body&(yy<by.min()+18));ny,nx=np.where(neutral&(yy<sy.min()+18))
            source_boot=(hx.min()+hx.max())/2-(nx.min()+nx.max())/2+float(np.median(sx[(sy>=sy.max()-10)&(sx<np.median(sx))]))
        pos=(round(boot+36-(source_boot-x0)*scale_x),round(iy.max()+52-(by.max()-y0)*scale_y))
        im=Image.fromarray(p).crop((x0,y0,x1,y1)).resize((round((x1-x0)*scale_x),round((y1-y0)*scale_y)),Image.Resampling.LANCZOS)
        assert pos[0]>=0 and pos[1]>=0 and pos[0]+im.width<=256 and pos[1]+im.height<=256
        canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(im,pos);frames.append(canvas)
        if i==0 and not walk_row:
            case=p.copy();case[~binary_dilation(ground_case,iterations=2)]=0
            ci=Image.fromarray(case).crop((x0,y0,x1,y1)).resize(im.size,Image.Resampling.LANCZOS)
            ground=Image.new('RGBA',(256,256));ground.alpha_composite(idle,(36,52));ground.alpha_composite(ci,pos)
        if i in [1,5,8]:
            dest=HERE/'grade-masks'/f'{source.stem}-{i:02d}.png';dest.parent.mkdir(exist_ok=True);Image.fromarray(diagnostic).crop((x0,y0,x1,y1)).save(dest)
        records.append({'cell':i,'position':list(pos),'sourceBox':[x0,y0,x1,y1]})
    return frames,ground,{'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scaleX':scale_x,'scaleY':scale_y,'materialGrade':settings,'groundCaseBox':[35,430,119,500] if not walk_row else None,'detachedCases':detached,'frames':records}

def main():
    idle=Image.open(ROOT/IDLE).convert('RGBA');pickup,ground,preg=extract(HERE/'sources/pickup-detail-v2.png',idle)
    actions,_,areg=extract(HERE/'sources/carry-unload-detail-v2.png',idle,True)
    pickup[0]=ground
    chains={'pickup-west':pickup,'carry-west':actions[6:12],'unload-west':list(reversed(pickup))}
    legacy=json.loads((ROOT/'major-bill-v3/packs/bare-256x256-p128-224/manifest.json').read_text());states={s['id']:s for s in legacy['states']}
    pack={k:v for k,v in legacy.items() if k!='states'};pack.update(name='Bill bare west cargo candidate',status='owner_visual_accepted_staged_2026_09_30_detail_v2',textureFilter='linear',states=[]);hashes={}
    for key,images in chains.items():
        state=copy.deepcopy(states[key]);state['frameFiles']=[]
        if key!='carry-west':
            state['frameDurationsMs']=[half for d in state['frameDurationsMs'] for half in [d/2,d/2]]
            for field in ['facings','waterKinds','waterPoses','depthOffsets']:state[field]=[v for v in state[field] for _ in range(2)]
        state['provenance']='independent west source;fixed anatomy/material scale;unload reverses authored pickup with its own timing'
        for i,im in enumerate(images):
            p=HERE/'frames'/key/f'{i:03d}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);rel=p.relative_to(HERE).as_posix();state['frameFiles'].append(rel);hashes[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
        pack['states'].append(state)
    pack['strideDistanceCells']={'carry':0.12}
    for name,data in [('manifest.json',pack),('frame-hashes.json',hashes),('source-registration.json',{'pickup':preg,'carry':areg,'unloadDerivation':'reverse12 pickup images;distinct retained unload timing','unusedSourceCells':'carry-unload top row is reference/proposed alternative;not runtime-selected'})]:
        (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
    out=Image.new('RGB',(3072,768),(34,48,56));draw=ImageDraw.Draw(out)
    for row,(key,images) in enumerate(chains.items()):
        for i,im in enumerate(images):out.paste(im,(256*i,256*row),im);draw.text((256*i+4,256*row+4),key+' '+str(i),fill='white')
    out.save(HERE/'contact-sheet.png')
    assert len({im.tobytes() for im in chains['carry-west']})==6
    print('West cargo:3 clips/30 references;12 authored pickup/reversed unload;6 distinct carry poses')

if __name__=='__main__':main()
