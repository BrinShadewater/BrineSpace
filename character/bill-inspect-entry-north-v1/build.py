from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent;B=P.parent/'bill-seated-north-coherent-v1';H=P.parent/'bill-seated-helmet-north-coherent-v1';L=P.parent/'bill-inspect-north-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 cfg=json.loads((P/'source-rulers.json').read_text())
 spec=importlib.util.spec_from_file_location('grade',B/'build.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 prepared={key:module.prepare(P/spec['source'],spec['heads'],spec['count'],spec['density']) for key,spec in cfg['sources'].items()}
 donors={'bare':[B/'frames/sit-down-north/000.png',L/'frames/bare/000.png'],'helmet':[H/'frames/sit-down-north/000.png',L/'frames/helmet/000.png']}
 packs={gear:[Image.open(paths[0]).convert('RGBA')] for gear,paths in donors.items()};a=np.array(packs['bare'][0]);y,x=np.where(a[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]))
 head=Image.open(H/'sources/canonical-head.png').convert('RGBA');yy,xx=np.indices((256,256));records=[];hashes={}
 for frame,(key,i) in enumerate(cfg['sequence'],1):
  source_spec=cfg['sources'][key];raw,labs,ids,grade,curve=prepared[key];heads=source_spec['heads'];sx,sy=source_spec['fixedRuler']
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];a=grade.copy();a[~mask]=0
  im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS);by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]));pos=(round(boot-front),ground-sole)
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);packs['bare'].append(plane);hx,hy=heads[i];hx=round(pos[0]+(hx-box[0])*sx);hy=round(pos[1]+(hy-box[1])*sy)
  a=np.array(plane);rgb=a[:,:,:3].astype(float);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+31)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);out=a.copy();out[erase]=0;helmet=Image.fromarray(out);helmet.alpha_composite(head,(hx-17,hy-6));out=np.array(helmet);out[hy+31:]=a[hy+31:];packs['helmet'].append(Image.fromarray(out))
  records.append({'frame':frame,'source':key,'sourcePose':i,'sourceBox':box,'fixedRuler':[sx,sy],'position':pos,'headAxis':[hx,hy],'protectedBodyFromY':hy+31,'targetFrontBoot':[boot,ground]})
 for gear,images in packs.items():
  images.append(Image.open(donors[gear][1]).convert('RGBA'));files=[]
  for i,im in enumerate(images):
   f=P/f'frames/{gear}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
  durations=[60,80,100,100,80,60];states=[]
  for action,sequence,timing in [('inspect-enter',files,durations),('inspect-exit',files[::-1],durations[::-1])]:states.append({'id':action+'-north','frameFiles':sequence,'frameDurationsMs':timing,'loop':False,'facings':['north']*6,'waterPoses':[False]*6,'waterKinds':[action]*6,'depthOffsets':[0]*6})
  m={'name':'Bill north reader transitions '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
  if gear=='helmet':m['equipment']='diving-helmet'
  (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 r={**cfg,'sourcesSha256':{key:sha(P/spec['source']) for key,spec in cfg['sources'].items()},'frames':records,'grades':{key:data[-1] for key,data in prepared.items()},'donors':{gear:[{'path':f.relative_to(P.parent).as_posix(),'sha256':sha(f)} for f in paths] for gear,paths in donors.items()},'helmetComponent':{'path':(H/'sources/canonical-head.png').relative_to(P.parent).as_posix(),'sha256':sha(H/'sources/canonical-head.png')},'scope':'authored standing reader draw/reversed stow; exact idle/held joins; actor selection/wiring pending'}
 for name,data in [('registration.json',r),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(34,52,62))
 for j,images in enumerate(packs.values()):
  for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
 board.save(P/'contact-sheet.png');print('Built standing north reader draw/stow:4gear states/24refs,480ms')
if __name__=='__main__':main()
