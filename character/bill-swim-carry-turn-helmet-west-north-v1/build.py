"""Fit authored prone-yaw components; preserve exact cargo bodies and endpoints."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
BARE=HERE.parent/'bill-swim-carry-turn-west-north-v1'
SOURCE=HERE/'sources/helmet-shell-v1.png'
SCALE=.09
ENDPOINTS=[('bill-swim-carry-helmet-west-coherent-v1/frames/swim-carry-west/000.png',(42,40)),('bill-swim-carry-helmet-north-coherent-v1/frames/swim-carry-north/000.png',(24,56))]
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));rgb=raw[:,:,:3].astype(float);labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.median(np.where(labs==k)[0]))//512,int(np.where(labs==k)[1].min())))
 references=[]
 for path in ['bill-swim-carry-helmet-west-coherent-v1/sources/canonical-head.png','bill-swim-carry-helmet-north-coherent-v1/sources/canonical-head.png']:
  a=np.array(Image.open(HERE.parent/path).convert('RGBA'));ar=a[:,:,:3].astype(float);references.extend(ar.mean(2)[(a[:,:,3]>180)&(np.ptp(ar,axis=2)<22)].tolist())
 q=[0,.05,.2,.4,.5,.7,.85,.95,1];neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22);src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(references,q)
 weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0);mapped=np.interp(rgb.mean(2),src,dst);graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8')
 components=[];component_records=[];(HERE/'components').mkdir(exist_ok=True)
 for i,k in enumerate(ids):
  mask=binary_dilation(labs==k,iterations=2)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];pix=graded.copy();pix[~mask]=0
  im=Image.fromarray(pix).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS);path=HERE/'components'/f'{i:03}.png';im.save(path);components.append(im);component_records.append({'file':path.relative_to(HERE).as_posix(),'sourceBox':box,'scale':SCALE,'size':list(im.size),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
 p=json.loads((BARE/'manifest.json').read_text(encoding='utf-8'));r=json.loads((BARE/'registration.json').read_text(encoding='utf-8'));images=[];records=[]
 for i,(path,pad) in enumerate(ENDPOINTS):
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(HERE.parent/path).convert('RGBA'),pad);images.append(plane)
 start,end=images;images=[start];yy,xx=np.indices((256,256))
 case_boxes=[(77,118,105,144),(80,108,110,134),(86,88,115,113),(107,85,135,104)]
 for i,registration in enumerate(r['frames'],1):
  bare=Image.open(BARE/p['states'][0]['frameFiles'][i]).convert('RGBA');b=np.array(bare);hx,hy=map(round,registration['targetCrownAxis']);head=components[i];pos=(hx-head.width//2,hy-3)
  br=b[:,:,:3].astype(float);warm_head=(br[:,:,0]>1.13*br[:,:,1])&(br[:,:,1]>1.14*br[:,:,2])
  erase=(abs(xx-hx)<=24)&(yy>=hy-2)&(yy<hy+31)&warm_head;out=b.copy();out[erase]=0;plane=Image.fromarray(out);plane.alpha_composite(head,pos);a=np.array(plane)
  x0,y0,x1,y1=case_boxes[i-1];case=(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)
  foreground=(b[:,:,3]>0)&(case|((abs(xx-hx)>20)&(yy>=hy+20)));a[foreground]=b[foreground];plane=Image.fromarray(a);images.append(plane)
  records.append({'sourcePose':i,'file':p['states'][0]['frameFiles'][i],'component':component_records[i]['file'],'position':pos,'crownAxis':[hx,hy],'eraseBox':[hx-24,hy-2,hx+25,hy+31],'eraseMethod':'bounded warm hair/skin support;neutral collar/quilt remains intact','protectedCaseBox':[x0,y0,x1,y1],'protectedBodyFromY':max(hy+31,pos[1]+head.height),'bareSha256':hashlib.sha256((BARE/p['states'][0]['frameFiles'][i]).read_bytes()).hexdigest()})
 images.append(end);manifest=copy.deepcopy(p);manifest.update(name='Bill west/north pitched helmet water cargo turn candidate',equipment='diving-helmet');hashes={}
 for state,frames in zip(manifest['states'],[images,images[::-1]]):
  for file,im in zip(state['frameFiles'],frames):
   path=HERE/file;path.parent.mkdir(parents=True,exist_ok=True);im.save(path);hashes[file]=hashlib.sha256(path.read_bytes()).hexdigest()
  state['provenance']='exact helmet carrying endpoints;four authored prone-yaw shell components at one fixed scale/grade;protected body/foreground case;reverse derived'
 reg={'source':'sources/helmet-shell-v1.png','sourceGeneration':'exec-98e5fcbf-abe0-4a8c-ab72-9ea8cc43a36e','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'scale':SCALE,'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'unusedSourcePoses':[0,5],'components':component_records,'endpointAuthorities':[{'path':path,'padding':pad} for path,pad in ENDPOINTS],'frames':records}
 for file,data in [('manifest.json',manifest),('helmet-registration.json',reg),('frame-hashes.json',hashes)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51))
 for i,im in enumerate(images):board.paste(im,(256*i,0),im);bare=Image.open(BARE/p['states'][0]['frameFiles'][i]);board.paste(bare,(256*i,256),bare)
 board.save(HERE/'contact-sheet.png');print('Built two helmet water cargo turns;one.09 shell ruler;exact endpoint bodies')
if __name__=='__main__':main()
