from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation
from correction import prepare as prepare_correction
P=Path(__file__).resolve().parent;L=P.parent/'bill-reading-north-v1';B=P.parent/'bill-seated-north-coherent-v1';H=P.parent/'bill-seated-helmet-north-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 spec=importlib.util.spec_from_file_location('grade',B/'build.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);heads=[(272,17),(768,17),(1264,17),(272,534),(768,538),(1264,535)];source=P/'sources/entry-v1.png';primary=module.prepare(source,heads,6,1.4);corrected=prepare_correction(P/'sources/entry-right-arm-v2.png',heads,primary[-1]);sx,sy=.214,.251
 seat=Image.open(B/'frames/sit-down-north/005.png').convert('RGBA');ar=np.array(seat);y,x=np.where(ar[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]));bare=[seat];helmet=[Image.open(H/'frames/sit-down-north/005.png').convert('RGBA')];head=Image.open(H/'sources/canonical-head.png').convert('RGBA');yy,xx=np.indices((256,256));records=[]
 for i in [1,2,3,4]:
  raw,labs,ids,grade,curve=corrected if i==1 else primary
  sx,sy=(.214,.2455) if i==1 else (.214,.251)
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS);by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]));pos=(round(boot-front),ground-sole);plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);bare.append(plane);hx,hy=heads[i];hx=round(pos[0]+(hx-box[0])*sx);hy=round(pos[1]+(hy-box[1])*sy)
  a=np.array(plane);rgb=a[:,:,:3].astype(float);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+31)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);out=a.copy();out[erase]=0;im=Image.fromarray(out);im.alpha_composite(head,(hx-17,hy-6));out=np.array(im);out[hy+31:]=a[hy+31:];helmet.append(Image.fromarray(out));records.append({'frame':i,'sourcePose':i,'sourceBox':box,'position':pos,'headAxis':[hx,hy],'protectedBodyFromY':hy+31,'fixedSourceRuler':[sx,sy],'source':'entry-right-arm-v2.png' if i==1 else 'entry-v1.png'})
 for gear,images in [('bare',bare),('helmet',helmet)]:
  images.append(Image.open(L/f'frames/{gear}/000.png').convert('RGBA'))
 hashes={}
 for gear,images in [('bare',bare),('helmet',helmet)]:
  files=[]
  for i,im in enumerate(images):
   f=P/f'frames/{gear}/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);file=f.relative_to(P).as_posix();files.append(file);hashes[file]=sha(f)
  durations=[60,80,100,100,80,60];states=[]
  for action,sequence,timing in [('read-seated-enter',files,durations),('read-seated-exit',files[::-1],durations[::-1])]:states.append({'id':action+'-north','frameFiles':sequence,'frameDurationsMs':timing,'loop':False,'facings':['north']*6,'waterPoses':[False]*6,'waterKinds':[action]*6,'depthOffsets':[40]*6})
  m={'name':'Bill north tablet transition '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
  if gear=='helmet':m['equipment']='diving-helmet'
  (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(34,52,62))
 for j,images in enumerate([bare,helmet]):
  for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
 board.save(P/'contact-sheet.png')
 reg={'sourceSha256':sha(source),'fixedRuler':[sx,sy],'density':1.4,'sourcePoses':[1,2,3,4],'generation':'exec-a6999412-1ee7-47c1-a98e-41476adfece3','correctedSourceSha256':sha(P/'sources/entry-right-arm-v2.png'),'correctedPose':1,'correctedGeneration':'exec-e66eb374-e924-4be9-8f4f-a905d3b27743','correctedOpaqueThreshold':240,'correctedRuler':[.214,.2455],'frames':records,'grade':{'primary':primary[-1],'corrected':corrected[-1]},'scope':'authored tablet entry/reversed exit;exact neutral/reading joins;runtime stage wiring pending'}
 for name,data in [('registration.json',reg),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 print('Built north tablet entry/exit candidates;4gear states/24refs;480ms')
if __name__=='__main__':main()
