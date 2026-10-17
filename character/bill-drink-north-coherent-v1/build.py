from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('north_grade',P.parent/'bill-seated-north-coherent-v1/build.py');grade=importlib.util.module_from_spec(spec);spec.loader.exec_module(grade)
cfg=json.loads((P/'source-rulers.json').read_text());source=P/cfg['source'];sx,sy=cfg['fixedRuler']
raw,labs,ids,graded,curve=grade.prepare(source,cfg['heads'],6,cfg['density'])
idle=Image.new('RGBA',(256,256));idle.paste(Image.open(grade.IDLE).convert('RGBA'),(36,52))
a=np.array(idle);y,x=np.where(a[:,:,3]>180);sole=int(y.max());boot=float(np.median(x[(y>=sole-4)&(x>np.median(x))]))
poses=[];records=[]
for i in range(6):
    mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
    a=graded.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
    by,bx=np.where(np.array(im)[:,:,3]>180);ground=int(by.max());front=float(np.median(bx[(by>=ground-4)&(bx>np.median(bx))]));pos=(round(boot-front),sole-ground)
    plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);poses.append(plane)
    hx,hy=cfg['heads'][i]
    records.append({'sourcePose':i,'sourceBox':box,'position':pos,'headAxis':[round(pos[0]+(hx-box[0])*sx),round(pos[1]+(hy-box[1])*sy)],'targetFrontBoot':[boot,sole]})
files=[];hashes={}
for i,source_pose in enumerate(cfg['sequence']):
    path=P/f'frames/drink-north/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);poses[source_pose].save(path);files.append(path.relative_to(P).as_posix());hashes[files[-1]]=sha(path)
state={'id':'drink-north','frameFiles':files,'frameDurationsMs':cfg['durations'],'loop':True,'facings':['north']*7,'waterPoses':[False]*7,'waterKinds':['drink']*7,'depthOffsets':[0]*7}
manifest={'name':'Bill north bare drink candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':[state]}
for name,data in [('manifest.json',manifest),('frame-hashes.json',hashes),('material-grade.json',curve),('registration.json',{'sourceSha256':sha(source),**cfg,'idleAuthority':grade.IDLE.relative_to(P.parent).as_posix(),'idleSha256':sha(grade.IDLE),'frames':records,'closure':'last slot copies exact first; one atlas ruler, no per-pose scaling'})]:
    (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1792,512),(34,52,62))
for i,source_pose in enumerate(cfg['sequence']):board.paste(poses[source_pose],(i*256,0),poses[source_pose]);board.paste(idle,(i*256,256),idle)
board.save(P/'contact-sheet.png')
print('Built north drinking candidate: one bare state/seven slots/six authored poses')
