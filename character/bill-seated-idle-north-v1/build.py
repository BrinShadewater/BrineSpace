from pathlib import Path
import importlib.util,json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent
B=P.parent/'bill-seated-north-coherent-v1'
H=P.parent/'bill-seated-helmet-north-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 spec=importlib.util.spec_from_file_location('transition',B/'build.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 source=P/'sources/seated-breathing-v1.png';heads=[(272,17),(768,16),(1264,16),(272,523),(768,525),(1264,524)]
 raw,labs,ids,grade,curve=module.prepare(source,heads,6,1.4)
 endpoint=Image.open(B/'frames/sit-down-north/005.png').convert('RGBA');ref=np.array(endpoint);y,x=np.where(ref[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]));frames=[endpoint];records=[]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];sole=float(y.max());front=float(np.median(x[(y>=sole-10)&(x>np.median(x))]));a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);sx,sy=.214,.251;im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS);position=(round(boot-(front-box[0])*sx),round(ground-(sole-box[1])*sy));plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,position);frames.append(plane);hx,hy=heads[i];records.append({'frame':len(frames)-1,'sourcePose':i,'sourceBox':box,'scaleX':sx,'scaleY':sy,'position':position,'headAxis':[round(position[0]+(hx-box[0])*sx),round(position[1]+(hy-box[1])*sy)]})
 frames.append(endpoint.copy());helmet_endpoint=Image.open(H/'frames/sit-down-north/005.png').convert('RGBA');head=Image.open(H/'sources/canonical-head.png').convert('RGBA');helmet=[helmet_endpoint];yy,xx=np.indices((256,256))
 for frame,row in zip(frames[1:5],records):
  a=np.array(frame);hx,hy=row['headAxis'];rgb=a[:,:,:3].astype(float);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+31)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);out=a.copy();out[erase]=0;im=Image.fromarray(out);im.alpha_composite(head,(hx-17,hy-6));out=np.array(im);out[hy+31:]=a[hy+31:];helmet.append(Image.fromarray(out))
 helmet.append(helmet_endpoint.copy());hashes={};manifests={}
 for gear,images in [('bare',frames),('helmet',helmet)]:
  files=[]
  for i,im in enumerate(images):
   f=P/f'frames/{gear}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
  m={'name':'Bill north seated breathing candidate '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':[{'id':'sit-idle-north','frameFiles':files,'frameDurationsMs':[160]*6,'loop':True,'facings':['north']*6,'waterPoses':[False]*6,'waterKinds':['sit-idle']*6,'depthOffsets':[40]*6}]}
  (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');manifests[gear]=m
 board=Image.new('RGB',(1536,768),(34,52,62))
 for j,images in enumerate([frames,helmet,[endpoint]*6]):
  for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
 board.save(P/'contact-sheet.png')
 evidence={'source':sha(source),'fixedRuler':[.214,.251],'sourceDensity':1.4,'frames':records,'bareEndpoint':sha(B/'frames/sit-down-north/005.png'),'helmetEndpoint':sha(H/'frames/sit-down-north/005.png'),'helmetComponent':sha(H/'sources/canonical-head.png'),'grade':curve,'scope':'staged breathing source;exact transition joins;furniture and runtime selection pending'}
 for name,data in [('registration.json',evidence),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 print('Built staged north seated breathing pair;12 references;960ms loop')
if __name__=='__main__':main()
