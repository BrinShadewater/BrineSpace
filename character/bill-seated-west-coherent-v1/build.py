from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
from grade import prepare,IDLE
P=Path(__file__).resolve().parent
SX=.27;SY=148/456
HEADS=[(267,43),(711,76),(1196,116),(255,613),(778,616),(1267,614)]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    raw,labs,ids,grade,curve=prepare(P/'sources/sit-v1.png',HEADS,6)
    idle=Image.open(IDLE).convert('RGBA');plane=Image.new('RGBA',(256,256));plane.paste(idle,(36,52));frames=[plane]
    a=np.array(plane);y,x=np.where(a[:,:,3]>180);ground=int(y.max())
    boot=float(np.median(x[(y>=ground-4)&(x<np.median(x))]));records=[]
    for i in range(1,6):
        mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0)
        y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
        a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box)
        im=im.resize((round(im.width*SX),round(im.height*SY)),Image.Resampling.LANCZOS)
        by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx<np.median(bx))]))
        pos=(round(boot-front),ground-sole);plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane)
        hx,hy=HEADS[i];records.append({'frame':i,'source':'sources/sit-v1.png','sourcePose':i,'sourceBox':box,'scaleX':SX,'scaleY':SY,'position':pos,'targetFrontBoot':[boot,ground],'headAxis':[round(pos[0]+(hx-box[0])*SX),round(pos[1]+(hy-box[1])*SY)],'headTiltDegrees':[0,-5,-8,-4,0,0][i]})
    hashes={};files=[]
    for i,im in enumerate(frames):
        file=P/f'frames/sit-down-west/{i:03}.png';file.parent.mkdir(parents=True,exist_ok=True);im.save(file);files.append(file.relative_to(P).as_posix());hashes[files[-1]]=sha(file)
    states=[]
    for action,sequence,timing,depth in [('sit-down',files,[100,120,140,160,160,120],[0,8,16,24,32,40]),('sit-rise',files[::-1],[120,160,160,140,120,100],[40,32,24,16,8,0])]:
        states.append({'id':action+'-west','frameFiles':sequence,'frameDurationsMs':timing,'loop':False,'facings':['west']*6,'waterKinds':[action]*6,'waterPoses':[False]*6,'depthOffsets':depth})
    manifest={'name':'Bill west sitting transition candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
    registration={'idleAuthority':IDLE.relative_to(P.parent).as_posix(),'idleSha256':sha(IDLE),'idlePadding':[36,52],'sources':{'sources/sit-v1.png':sha(P/'sources/sit-v1.png')},'primaryGeneration':'exec-c51243ea-d2e4-4815-b545-afd67a643d71','primaryRuler':[SX,SY],'frames':records,'excludedPrimaryPoses':[0],'scope':'independent west sitting source;exact standing endpoint;candidate selection/furniture pending'}
    for name,data in [('manifest.json',manifest),('registration.json',registration),('frame-hashes.json',hashes),('material-grade.json',curve)]:
        (P/name).write_text(json.dumps(data,indent=2)+'\n')
    board=Image.new('RGB',(1536,512),(34,52,62))
    for i,im in enumerate(frames):board.paste(im,(i*256,0),im);board.paste(frames[0],(i*256,256),frames[0])
    board.save(P/'contact-sheet.png');print('Built west sitting and exact reversed rise')
if __name__=='__main__':main()
