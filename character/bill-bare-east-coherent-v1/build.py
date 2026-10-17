"""Register independent front-facing whole figures against selected east idle."""
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = HERE/'sources/actions.png'
IDLE = ROOT/'crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png'


def main():
    raw = np.asarray(Image.open(SOURCE).convert('RGBA'))
    labs,_ = label(raw[:,:,3]>180)
    counts = np.bincount(labs.ravel())
    poses=[]
    for ident in range(1,len(counts)):
        if counts[ident]>10000:
            y,x=np.where(labs==ident)
            poses.append((int(y.min()),int(x.min()),ident))
    assert len(poses)==18,len(poses)
    poses.sort()
    ordered=[]
    for row in range(3): ordered.extend(sorted(poses[row*6:(row+1)*6],key=lambda a:a[1]))
    idle=Image.open(IDLE).convert('RGBA')
    a=np.asarray(idle)
    iy,ix=np.where(a[:,:,3]>180)
    sy,sx=np.where(labs==ordered[0][2])
    scale_y=(iy.max()-iy.min()+1)/(sy.max()-sy.min()+1)
    hy,hx=np.where((a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<iy.min()+25))
    shy,shx=np.where((labs==ordered[0][2])&(np.indices(labs.shape)[0]<sy.min()+50))
    scale_x=(hx.max()-hx.min()+1)/(shx.max()-shx.min()+1)
    boot=float(np.median(ix[(iy>=iy.max()-6)&(ix>np.median(ix))]))
    frames=[];records=[]
    yy,xx=np.indices(labs.shape)
    for n,(_,_,ident) in enumerate(ordered):
        mask=labs==ident;y,x=np.where(mask)
        p=raw.copy();p[~binary_dilation(mask,iterations=2)]=0
        rgb=p[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1)
        luma=rgb.mean(2);valid=p[:,:,3]>0
        top=int(y.min())
        head_y,head_x=np.where(mask&(yy<top+50))
        center=(head_x.min()+head_x.max())/2;half=(head_x.max()-head_x.min())*.30
        face=(xx>head_x.min()+(head_x.max()-head_x.min())*.48)&(yy>=top+15)&(yy<top+85)
        warm=np.clip((r-g-7)/16,0,1)*np.clip((r-b-9)/18,0,1)
        skin=valid*face*warm*np.clip((luma-50)/30,0,1)
        patch=valid*(~face)*(yy>=top+55)*warm
        neutral=valid*(1-np.clip((rgb.max(2)-rgb.min(2)-10)/18,0,1))
        metal=neutral*np.clip((luma-80)/30,0,1)
        lamp=(yy<top+22)&(luma>175)
        metal*=~lamp
        shell=neutral*(yy<top+78)*(1-metal)*(1-skin)*(1-patch)*(~lamp)
        cloth=neutral*(yy>=top+78)*(1-metal)*(1-patch)
        graded=rgb.copy()
        for weight,target in [(cloth,rgb*.90+np.array([1,0,0])),(shell,rgb+np.array([-2,-2,-1])),(metal,luma[:,:,None]+np.array([2,1,0])),(patch,rgb*np.array([.93,.97,1.02])),(skin,rgb*np.array([.94,.97,1.0]))]:
            graded=graded*(1-weight[:,:,None])+target*weight[:,:,None]
        p[:,:,:3]=np.clip(graded,0,255).astype('uint8');p[~valid]=0
        x0,y0,x1,y1=int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)
        source_boot=float(np.median(x[(y>=y.max()-10)&(x>np.median(x))]))
        im=Image.fromarray(p).crop((x0,y0,x1,y1))
        im=im.resize((round(im.width*scale_x),round(im.height*scale_y)),Image.Resampling.LANCZOS)
        position=(round(boot-(source_boot-x0)*scale_x),round(iy.max()-(y.max()-y0)*scale_y))
        assert position[0]>=0 and position[1]>=0
        assert position[0]+im.width<=184 and position[1]+im.height<=184
        canvas=Image.new('RGBA',(184,184));canvas.alpha_composite(im,position)
        frames.append(canvas)
        records.append({'cell':n,'sourceBox':[x0,y0,x1,y1],'bootX':source_boot,'position':list(position)})
        if n in (0,2,8,12):
            diagnostic=np.zeros_like(p);diagnostic[:,:,:3]=np.clip(np.stack((patch*255+neutral*45,skin*255+neutral*45,metal*255+neutral*45),2),0,255).astype('uint8');diagnostic[:,:,3]=p[:,:,3]
            dest=HERE/'review-masks'/f'{n:02d}.png';dest.parent.mkdir(exist_ok=True)
            Image.fromarray(diagnostic).crop((x0,y0,x1,y1)).save(dest)
    chains={'interact-east':[idle,*frames[1:5],idle], 'kneel-east':[idle,*frames[7:11],frames[12]], 'repair-east':frames[12:18], 'stand-east':[frames[17],*reversed(frames[7:11]),idle]}
    base=json.loads((ROOT/'major-bill-v3/packs/bare-184x184-p92-172/manifest.json').read_text())
    result={k:v for k,v in base.items() if k!='states'}
    result.update(name='Bill coherent bare east action candidate',status='owner_review_pending',states=[])
    selected={s['id']:s for s in base['states']}
    timing=json.loads((HERE/'build-settings.json').read_text())['frameDurationsMs']
    hashes={}
    for key,images in chains.items():
        state=copy.deepcopy(selected[key]);state['frameFiles']=[];state['frameDurationsMs']=timing[key]
        state['provenance']='independent front whole figures; fixed source scale; planted anatomical left boot; reverse descent for stand'
        for i,im in enumerate(images):
            padded=im.copy()
            dest=HERE/'frames'/key/f'{i:03d}.png';dest.parent.mkdir(parents=True,exist_ok=True);padded.save(dest)
            rel=dest.relative_to(HERE).as_posix();state['frameFiles'].append(rel);hashes[rel]=hashlib.sha256(dest.read_bytes()).hexdigest()
        result['states'].append(state)
    for name,data in [('manifest.json',result),('frame-hashes.json',hashes),('source-registration.json',{'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scaleX':scale_x,'scaleY':scale_y,'plantedLeftBoot':boot,'profilePadding':[0,0],'frames':records})]:
        (HERE/name).write_text(json.dumps(data,indent=2)+'\n')
    contact=Image.new('RGB',(1104,736),(34,48,56));draw=ImageDraw.Draw(contact)
    for row,(key,images) in enumerate(chains.items()):
        for i,im in enumerate(images):
            contact.paste(im,(i*184,row*184),im);draw.text((i*184+3,row*184+3),key+' '+str(i),fill='white')
    contact.save(HERE/'contact-sheet.png')
    assert chains['kneel-east'][5].tobytes()==chains['repair-east'][0].tobytes()
    assert chains['repair-east'][5].tobytes()==chains['stand-east'][0].tobytes()
    print('Bare east: 18 source poses, 24 frames, no clipping, fixed scale, exact action joins')


if __name__=='__main__': main()
