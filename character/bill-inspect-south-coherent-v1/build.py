from pathlib import Path
import importlib.util,json,hashlib,math
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent;B=P.parent/'bill-seated-loops-south-v1';H=P.parent/'bill-seated-helmet-south-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    spec=importlib.util.spec_from_file_location('south_grade',B/'build.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    cfg=json.loads((P/'source-rulers.json').read_text());source=P/cfg.get('source','sources/inspect-v1.png')
    heads=cfg['heads'];sx,sy=cfg['fixedRuler'];raw,labs,ids,grade,curve=module.prepare(source,heads,cfg['density'])
    idle=Image.new('RGBA',(256,256));idle.paste(Image.open(module.IDLE).convert('RGBA'),(36,52));a=np.array(idle);y,x=np.where(a[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]))
    head=Image.open(H/'sources/canonical-head.png').convert('RGBA');yy,xx=np.indices((256,256));packs={'bare':[],'helmet':[]};records=[];hashes={}
    for frame,i in enumerate(cfg['sourcePoses']):
        mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
        a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
        by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]));pos=(round(boot-front),ground-sole)
        plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);packs['bare'].append(plane)
        hx,hy=heads[i];hx=round(pos[0]+(hx-box[0])*sx);hy=round(pos[1]+(hy-box[1])*sy);angle=cfg['tilts'][i]
        tilted=head.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True);radians=math.radians(angle);dx=18-head.width/2;dy=8-head.height/2
        anchor=(tilted.width/2+math.cos(radians)*dx-math.sin(radians)*dy,tilted.height/2+math.sin(radians)*dx+math.cos(radians)*dy);head_pos=(round(hx-anchor[0]),round(hy-anchor[1]))
        a=np.array(plane);rgb=a[:,:,:3].astype(float);warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+35)&warm
        out=a.copy();out[erase]=0;equipped=Image.fromarray(out);equipped.alpha_composite(tilted,head_pos);out=np.array(equipped);out[hy+35:]=a[hy+35:];packs['helmet'].append(Image.fromarray(out))
        records.append({'frame':frame,'sourcePose':i,'sourceBox':box,'position':pos,'headAxis':[hx,hy],'tiltDegrees':angle,'protectedBodyFromY':hy+35,'targetFrontBoot':[boot,ground]})
    # Preserve exact neutral loop closure at one fixed source scale.
    for images in packs.values():images.append(images[0].copy())
    for gear,images in packs.items():
        files=[]
        for i,im in enumerate(images):
            path=P/f'frames/{gear}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);files.append(path.relative_to(P).as_posix());hashes[files[-1]]=sha(path)
        state={'id':'inspect-south','frameFiles':files,'frameDurationsMs':[160]*6,'loop':True,'facings':['south']*6,'waterPoses':[False]*6,'waterKinds':['inspect']*6,'depthOffsets':[0]*6}
        manifest={'name':'Bill south inspection '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':[state]}
        if gear=='helmet':manifest['equipment']='diving-helmet'
        (P/(gear+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
    for name,data in [('registration.json',{'sourceSha256':sha(source),'source':source.relative_to(P).as_posix(),**cfg,'frames':records,'excludedSourcePoses':sorted(set(range(6))-set(cfg['sourcePoses'])),'closure':'explicit authored source sequence;slot5 copies exact slot0;no per-pose scaling','idleAuthority':module.IDLE.relative_to(P.parent).as_posix(),'idleSha256':sha(module.IDLE)}),('material-grade.json',curve),('frame-hashes.json',hashes)]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,768),(34,52,62))
    for j,images in enumerate([packs['bare'],packs['helmet'],[idle]*6]):
        for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
    board.save(P/'contact-sheet.png');print('Built south inspection:2gear states/12refs;fixed ruler/native helmet')
if __name__=='__main__':main()
