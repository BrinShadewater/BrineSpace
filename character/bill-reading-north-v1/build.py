from pathlib import Path
import importlib.util, json, hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent
B=P.parent/'bill-seated-north-coherent-v1'
H=P.parent/'bill-seated-helmet-north-coherent-v1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    spec=importlib.util.spec_from_file_location('north_grade',B/'build.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    source=P/'sources/reading-v1.png'
    heads=[(272,17),(768,35),(1268,16),(272,542),(768,525),(1264,525)]
    raw,labs,ids,grade,curve=module.prepare(source,heads,6,1.4)
    endpoint=Image.open(B/'frames/sit-down-north/005.png').convert('RGBA')
    ref=np.array(endpoint);y,x=np.where(ref[:,:,3]>180);ground=int(y.max())
    boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]))
    sx,sy=.214,.251;bare=[];helmet=[];records=[]
    head=Image.open(H/'sources/canonical-head.png').convert('RGBA')
    yy,xx=np.indices((256,256))
    for i in range(6):
        mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0)
        y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
        a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box)
        im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
        by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max())
        front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]))
        pos=(round(boot-front),ground-sole)
        plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos)
        hx,hy=heads[i];hx=round(pos[0]+(hx-box[0])*sx);hy=round(pos[1]+(hy-box[1])*sy)
        bare.append(plane);a=np.array(plane);rgb=a[:,:,:3].astype(float)
        erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+31)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2])
        out=a.copy();out[erase]=0;equipped=Image.fromarray(out)
        equipped.alpha_composite(head,(hx-17,hy-6));out=np.array(equipped);out[hy+31:]=a[hy+31:]
        helmet.append(Image.fromarray(out))
        records.append({'frame':i,'sourcePose':i,'sourceBox':box,'position':pos,'headAxis':[hx,hy],'protectedBodyFromY':hy+31})
    hashes={}
    for gear,images in [('bare',bare),('helmet',helmet)]:
        files=[]
        for i,im in enumerate(images):
            path=P/f'frames/{gear}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
            files.append(path.relative_to(P).as_posix());hashes[files[-1]]=sha(path)
        state={'id':'read-seated-north','frameFiles':files,'frameDurationsMs':[160]*6,'loop':True,'facings':['north']*6,'waterPoses':[False]*6,'waterKinds':['read-seated']*6,'depthOffsets':[40]*6}
        manifest={'name':'Bill north reading candidate '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':[state]}
        if gear=='helmet':manifest['equipment']='diving-helmet'
        (P/(gear+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
    registration={'generation':'exec-9c0c7e0c-65af-4f5b-af52-0e637ef899a1','source':sha(source),'fixedRuler':[sx,sy],'sourceDensity':1.4,'frames':records,'grade':curve,'bareSeat':sha(B/'frames/sit-down-north/005.png'),'helmetComponent':sha(H/'sources/canonical-head.png'),'scope':'staged loop;tablet is occluded in front;actual furniture and entry/exit joins pending'}
    for name,data in [('registration.json',registration),('frame-hashes.json',hashes)]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,768),(34,52,62))
    for j,images in enumerate([bare,helmet,[endpoint]*6]):
        for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
    board.save(P/'contact-sheet.png')
    print('Built north reading: two gear states/12 references; fixed master ruler and native helmet')
if __name__=='__main__':main()
