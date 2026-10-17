from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
from grade import prepare,IDLE
P=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    primary_heads=[(295,44),(814,75),(1290,126),(309,601),(773,600),(1255,592)]
    middle_heads=[(478,72),(1120,144)]
    primary=prepare(P/'sources/sit-v1.png',primary_heads,6)
    middle=prepare(P/'sources/interiors-v2.png',middle_heads,2,2.12)
    idle=Image.open(IDLE).convert('RGBA');plane=Image.new('RGBA',(256,256));plane.paste(idle,(36,52));frames=[plane]
    a=np.array(plane);y,x=np.where(a[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]));records=[]
    choices=[(primary,primary_heads,1,.27,.3058,'sources/sit-v1.png',5),(middle,middle_heads,0,.125,.1426,'sources/interiors-v2.png',8),(middle,middle_heads,1,.125,.1426,'sources/interiors-v2.png',5),(primary,primary_heads,4,.27,.3058,'sources/sit-v1.png',0),(primary,primary_heads,5,.27,.3058,'sources/sit-v1.png',0)]
    for frame,(data,heads,i,sx,sy,source,angle) in enumerate(choices,1):
        raw,labs,ids,grade,curve=data;mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0)
        y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
        a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box)
        im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
        by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]));pos=(round(boot-front),ground-sole)
        plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane)
        hx,hy=heads[i];records.append({'frame':frame,'source':source,'sourcePose':i,'sourceBox':box,'scaleX':sx,'scaleY':sy,'position':pos,'targetFrontBoot':[boot,ground],'headAxis':[round(pos[0]+(hx-box[0])*sx),round(pos[1]+(hy-box[1])*sy)],'headTiltDegrees':angle})
    hashes={};files=[]
    for i,im in enumerate(frames):
        file=P/f'frames/sit-down-east/{i:03}.png';file.parent.mkdir(parents=True,exist_ok=True);im.save(file);files.append(file.relative_to(P).as_posix());hashes[files[-1]]=sha(file)
    states=[]
    for action,sequence,timing,depth in [('sit-down',files,[100,120,140,160,160,120],[0,8,16,24,32,40]),('sit-rise',files[::-1],[120,160,160,140,120,100],[40,32,24,16,8,0])]:
        states.append({'id':action+'-east','frameFiles':sequence,'frameDurationsMs':timing,'loop':False,'facings':['east']*6,'waterKinds':[action]*6,'waterPoses':[False]*6,'depthOffsets':depth})
    manifest={'name':'Bill east sitting transition candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
    registration={'idleAuthority':IDLE.relative_to(P.parent).as_posix(),'idleSha256':sha(IDLE),'idlePadding':[36,52],'sources':{name:sha(P/name) for name in ['sources/sit-v1.png','sources/interiors-v2.png']},'primaryGeneration':'exec-bda2c1e2-1b68-4de7-a56b-2bfb9766bc3f','interiorGeneration':'exec-6617bcb3-aa9c-483f-aaa6-363c47abcfc6','primaryRuler':[.27,.3058],'interiorRuler':[.125,.1426],'frames':records,'excludedPrimaryPoses':[0,2,3],'scope':'authored lowering;exact selected standing;post-resize boot registration;real furniture/loop/selection pending'}
    for name,data in [('manifest.json',manifest),('registration.json',registration),('frame-hashes.json',hashes),('material-grade.json',{'primary':primary[-1],'interiors':middle[-1]})]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,512),(34,52,62))
    for i,im in enumerate(frames):board.paste(im,(i*256,0),im);board.paste(frames[0],(i*256,256),frames[0])
    board.save(P/'contact-sheet.png');print('Built east sitting: five authored interiors, reversed rise, exact idle')
if __name__=='__main__':main()
