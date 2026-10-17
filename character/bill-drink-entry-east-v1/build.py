from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg=json.loads((P/'source-rulers.json').read_text());spec=importlib.util.spec_from_file_location('grade',P.parent/'bill-seated-east-coherent-v1/grade.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
prepared={key:module.prepare(P/s['source'],s['heads'],s['count'],s['density']) for key,s in cfg['sources'].items()}
donors=[P.parent/'bill-seated-east-coherent-v1/frames/sit-down-east/000.png',P.parent/'bill-drink-east-coherent-v1/frames/drink-east/000.png']
images=[Image.open(donors[0]).convert('RGBA')];a=np.array(images[0]);y,x=np.where(a[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]));records=[]
for frame,(key,i) in enumerate(cfg['sequence'],1):
    source=cfg['sources'][key];raw,labs,ids,grade,curve=prepared[key];sx,sy=source['fixedRuler']
    mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];a=grade.copy();a[~mask]=0
    im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS);by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]));pos=(round(boot-front),ground-sole)
    plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);images.append(plane);hx,hy=source['heads'][i]
    records.append({'frame':frame,'source':key,'sourcePose':i,'sourceBox':box,'fixedRuler':[sx,sy],'position':pos,'headAxis':[round(pos[0]+(hx-box[0])*sx),round(pos[1]+(hy-box[1])*sy)],'targetFrontBoot':[boot,ground]})
images.append(Image.open(donors[1]).convert('RGBA'));files=[];hashes={}
for i,im in enumerate(images):
    f=P/f'frames/bare/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
states=[]
for action,sequence,timing in [('drink-enter',files,cfg['durations']),('drink-exit',files[::-1],cfg['durations'][::-1])]:
    states.append({'id':action+'-east','frameFiles':sequence,'frameDurationsMs':timing,'loop':False,'facings':['east']*len(files),'waterPoses':[False]*len(files),'waterKinds':[action]*len(files),'depthOffsets':[0]*len(files)})
manifest={'name':'Bill east bare cup pickup/return candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
r={**cfg,'sourcesSha256':{key:sha(P/s['source']) for key,s in cfg['sources'].items()},'frames':records,'grades':{key:data[-1] for key,data in prepared.items()},'donors':[{'path':f.relative_to(P.parent).as_posix(),'sha256':sha(f)} for f in donors],'scope':'authored cup pickup and reversed return; exact idle/drinking-held endpoints; normal service pending'}
for name,data in [('manifest.json',manifest),('registration.json',r),('frame-hashes.json',hashes)]:
    (P/name).write_text(json.dumps(data,indent=2)+'\n')
board=Image.new('RGB',(len(images)*256,512),(34,52,62))
for j,row in enumerate([images,images[::-1]]):
    for i,im in enumerate(row):board.paste(im,(i*256,j*256),im)
board.save(P/'contact-sheet.png');print('Built east cup pickup/reversed return; exact idle/held joins')
