from pathlib import Path
import importlib.util,json,hashlib,math
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent;B=P.parent/'bill-seated-west-coherent-v1';H=P.parent/'bill-seated-helmet-west-coherent-v1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    spec=importlib.util.spec_from_file_location('west_grade',B/'grade.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    endpoint=Image.open(B/'frames/sit-down-west/005.png').convert('RGBA');helmet_endpoint=Image.open(H/'frames/sit-down-west/005.png').convert('RGBA')
    a=np.array(endpoint);y,x=np.where(a[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x<np.median(x))]))
    head=Image.open(H/'sources/canonical-head.png').convert('RGBA');yy,xx=np.indices((256,256))
    packs={'bare':[],'helmet':[]};records={};grades={};hashes={};reviews=[]
    specs=json.loads((P/'source-rulers.json').read_text())
    for action,name,heads,sx,sy,density,poses,angles,generation in specs:
        raw,labs,ids,grade,curve=module.prepare(P/'sources'/name,heads,6,density)
        bare=[endpoint.copy()] if action=='sit-idle' else [];helmet=[helmet_endpoint.copy()] if action=='sit-idle' else [];rows=[]
        for i in poses:
            mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
            a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
            by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx<np.median(bx))]));position=(round(boot-front),ground-sole)
            plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,position);bare.append(plane)
            hx,hy=heads[i];hx=round(position[0]+(hx-box[0])*sx);hy=round(position[1]+(hy-box[1])*sy)
            angle=angles[i];tilted=head.rotate(-angle,resample=Image.Resampling.BICUBIC,expand=True)
            radians=math.radians(angle);dx=20-head.width/2;dy=4-head.height/2
            anchor=(tilted.width/2+math.cos(radians)*dx-math.sin(radians)*dy,tilted.height/2+math.sin(radians)*dx+math.cos(radians)*dy)
            head_position=(round(hx-anchor[0]),round(hy-anchor[1]))
            a=np.array(plane);rgb=a[:,:,:3].astype(float);warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+31)&warm
            out=a.copy();out[erase]=0;equipped=Image.fromarray(out);equipped.alpha_composite(tilted,head_position);out=np.array(equipped);out[hy+31:]=a[hy+31:];helmet.append(Image.fromarray(out))
            rows.append({'frame':len(bare)-1,'sourcePose':i,'sourceBox':box,'position':position,'headAxis':[hx,hy],'tiltDegrees':angle,'protectedBodyFromY':hy+31,'scaleX':sx,'scaleY':sy})
        if action=='sit-idle':bare.append(endpoint.copy());helmet.append(helmet_endpoint.copy())
        for gear,images in [('bare',bare),('helmet',helmet)]:
            files=[]
            for i,im in enumerate(images):
                path=P/f'frames/{gear}/{action}-west/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path);files.append(path.relative_to(P).as_posix());hashes[files[-1]]=sha(path)
            packs[gear].append({'id':action+'-west','frameFiles':files,'frameDurationsMs':[160]*6,'loop':True,'facings':['west']*6,'waterPoses':[False]*6,'waterKinds':[action]*6,'depthOffsets':[40]*6})
        records[action]={'source':name,'sourceSha256':sha(P/'sources'/name),'generation':generation,'fixedRuler':[sx,sy],'density':density,'frames':rows};grades[action]=curve;reviews.extend([bare,helmet])
    for gear,states in packs.items():
        manifest={'name':'Bill west seated loops '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
        if gear=='helmet':manifest['equipment']='diving-helmet'
        (P/(gear+'-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
    for name,data in [('registration.json',records),('material-grade.json',grades),('frame-hashes.json',hashes)]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,1024),(34,52,62))
    for j,images in enumerate(reviews):
        for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
    board.save(P/'contact-sheet.png');print('Built west seated breathing/reading: four gear states/24refs;960ms loops')
if __name__=='__main__':main()
