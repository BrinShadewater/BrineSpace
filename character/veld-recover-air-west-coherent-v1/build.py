"""Extract authored recovery with a shared ruler, grade and planted boot anchor."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
SOURCE=P/'sources/recovery-v1.png'
IDLE=ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-west-transition-matte-v1/000.png'
SX=.29
SY=148/488
HEADS=[(220,16,310,100),(643,46,736,132),(1132,69,1233,158),(169,590,274,681),(687,539,791,629),(1222,523,1320,612)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));rgb=raw[:,:,:3].astype(float)
 labs,_=label(raw[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0
 ids=sorted(np.argsort(n)[-6:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
 assert all(n[k]>35000 for k in ids)
 ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
 head=np.zeros(raw.shape[:2],bool)
 for x0,y0,x1,y1 in HEADS:head[y0:y1,x0:x1]=True
 neutral=(raw[:,:,3]>200)&(~head)&(np.ptp(rgb,axis=2)<22)
 rn=(ref[:,:,3]>200)&(ry>50)&(np.ptp(rr,axis=2)<22)
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1]
 src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[rn],q)
 mapped=np.interp(rgb.mean(2),src,dst)
 w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)*(~head)
 grade=raw.copy();grade[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8')
 warm=(rgb[:,:,0]>1.15*rgb[:,:,1])&(rgb[:,:,1]>1.15*rgb[:,:,2])&(raw[:,:,3]>200)&head
 # Separate the dark chestnut hair from exposed skin; bounds follow authored heads.
 hair=warm&(rgb.mean(2)<72);face=warm&(rgb.mean(2)>85)
 rh=(ref[:,:,3]>200)&(ry>=24)&(ry<37)&(rr.mean(2)<72)&(rr[:,:,0]>1.15*rr[:,:,1])
 rf=(ref[:,:,3]>200)&(rx<85)&(ry>=32)&(ry<48)&(rr.mean(2)>85)&(rr[:,:,0]>1.15*rr[:,:,1])
 blue=(raw[:,:,3]>200)&(rgb[:,:,2]>1.35*rgb[:,:,0])&(rgb[:,:,1]>1.12*rgb[:,:,0])
 rb=(ref[:,:,3]>200)&(ry>50)&(rr[:,:,2]>1.35*rr[:,:,0])&(rr[:,:,1]>1.12*rr[:,:,0])
 gains={}
 for name,mask,target in [('hair',hair,rh),('skin',face,rf),('blue',blue,rb)]:
  assert mask.sum()>0 and target.sum()>0,name
  gain=np.median(rr[target],axis=0)/np.median(rgb[mask],axis=0);gains[name]=gain.tolist()
  grade[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8')
 by,bx=np.where(ref[:,:,3]>180);ground=int(by.max()+52)
 boot=float(np.median(bx[(by>=by.max()-6)&(bx<np.median(bx))]))+36
 idle=Image.new('RGBA',(256,256));idle.paste(Image.fromarray(ref),(36,52))
 frames=[idle];records=[]
 for i in [1,2,3,4]:
  component=labs==ids[i];mask=binary_dilation(component,iterations=3)&(raw[:,:,3]>0)
  y,x=np.where(component);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
  sole=float(y.max());front=float(np.median(x[(y>=y.max()-10)&(x<np.median(x))]))
  a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box)
  im=im.resize((round(im.width*SX),round(im.height*SY)),Image.Resampling.LANCZOS)
  pos=(round(boot-(front-box[0])*SX),round(ground-(sole-box[1])*SY))
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane)
  hx=(HEADS[i][0]+HEADS[i][2])/2;hy=HEADS[i][1]
  records.append({'sourcePose':i,'sourceBox':box,'scale':[SX,SY],'frontBootSource':[front,sole],'frontBootTarget':[boot,ground],'position':pos,'headCrown':[round(pos[0]+(hx-box[0])*SX),round(pos[1]+(hy-box[1])*SY)],'headTiltDegrees':[0,5,12,15,6,0][i]})
 frames.append(idle.copy());files=[]
 for i,im in enumerate(frames):
  f=P/'frames/recover-air-west'/f'{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P).as_posix())
 manifest={'name':'Veld west authored dry breathing recovery','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','states':[{'id':'recover-air-west','frameFiles':files,'frameDurationsMs':[500]*6,'loop':False,'facings':['west']*6,'waterKinds':['recover']*6,'waterPoses':[False]*6,'depthOffsets':[0]*6}]}
 registration={'source':'sources/recovery-v1.png','sourceSha256':sha(SOURCE),'provider':'exec-e058d4d6-7cd7-47a3-87af-b12d40768b6b','idleAuthority':IDLE.relative_to(ROOT).as_posix(),'idleSha256':sha(IDLE),'scale':[SX,SY],'ruler':'upright authored 488px maps to148px;142px body width maps to41px;frozen across all interiors','unusedSourcePoses':[0,5],'idlePadding':[36,52],'haloRemoval':'connected opaque figure plus3pixel source edge;discard distant translucent halo','frames':records}
 data={'manifest.json':manifest,'registration.json':registration,'material-grade.json':{'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'gains':gains,'scope':'pooled atlas grade;bounded hair/skin and blue markings'},'frame-hashes.json':{f:sha(P/f) for f in files}}
 for file,value in data.items():(P/file).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51));d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):
  board.paste(im,(i*256,0),im);board.paste(idle,(i*256,256),idle);d.text((i*256+4,4),f'recovery {i}',fill='white');d.text((i*256+4,260),'selected idle',fill='white')
 board.save(P/'contact-sheet.png')
 print('6 recovery poses packaged; shared ruler and grade; exact selected idle endpoints')
if __name__=='__main__':main()
