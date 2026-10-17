from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
P=Path(__file__).resolve().parent;L=P.parent/'bill-seated-loops-east-v1';B=P.parent/'bill-seated-east-coherent-v1';H=P.parent/'bill-seated-helmet-east-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 spec=importlib.util.spec_from_file_location('grade',B/'grade.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);heads=[(248,48),(762,47),(1293,48),(251,540),(763,540),(1291,540)];source=P/'sources/entry-v1.png';raw,labs,ids,grade,curve=module.prepare(source,heads,6,1.1);sx,sy=.235,.263
 seat=Image.open(B/'frames/sit-down-east/005.png').convert('RGBA');ar=np.array(seat);y,x=np.where(ar[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]));bare=[seat];helmet=[Image.open(H/'frames/sit-down-east/005.png').convert('RGBA')];head=Image.open(H/'sources/canonical-head.png').convert('RGBA');yy,xx=np.indices((256,256));records=[]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS);by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]));pos=(round(boot-front),ground-sole);plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);bare.append(plane);hx,hy=heads[i];hx=round(pos[0]+(hx-box[0])*sx);hy=round(pos[1]+(hy-box[1])*sy)
  a=np.array(plane);rgb=a[:,:,:3].astype(float);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+31)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);out=a.copy();out[erase]=0;im=Image.fromarray(out);im.alpha_composite(head,(hx-19,hy-4));out=np.array(im);out[hy+31:]=a[hy+31:];helmet.append(Image.fromarray(out));records.append({'frame':i,'sourcePose':i,'sourceBox':box,'position':pos,'headAxis':[hx,hy],'protectedBodyFromY':hy+31})
 for gear,images in [('bare',bare),('helmet',helmet)]:
  images.append(Image.open(L/f'frames/{gear}/read-seated-east/000.png').convert('RGBA'))
 hashes={}
 for gear,images in [('bare',bare),('helmet',helmet)]:
  files=[]
  for i,im in enumerate(images):
   f=P/f'frames/{gear}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);file=f.relative_to(P).as_posix();files.append(file);hashes[file]=sha(f)
  durations=[60,80,100,100,80,60];states=[]
  for action,sequence,timing in [('read-seated-enter',files,durations),('read-seated-exit',files[::-1],durations[::-1])]:states.append({'id':action+'-east','frameFiles':sequence,'frameDurationsMs':timing,'loop':False,'facings':['east']*6,'waterPoses':[False]*6,'waterKinds':[action]*6,'depthOffsets':[40]*6})
  m={'name':'Bill east tablet transition '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
  if gear=='helmet':m['equipment']='diving-helmet'
  (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(34,52,62))
 for j,images in enumerate([bare,helmet]):
  for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
 board.save(P/'contact-sheet.png')
 reg={'sourceSha256':sha(source),'fixedRuler':[sx,sy],'density':1.1,'sourcePoses':[1,2,3,4],'generation':'exec-70d56942-f3f2-4c43-8b18-243981209ed4','frames':records,'grade':curve,'scope':'authored tablet entry/reversed exit;exact neutral/reading joins;runtime stage wiring pending'}
 for name,data in [('registration.json',reg),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 print('Built east tablet entry/exit candidates;4gear states/24refs;480ms')
if __name__=='__main__':main()
