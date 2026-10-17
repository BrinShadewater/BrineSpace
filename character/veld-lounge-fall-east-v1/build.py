"""Staged authored seated lounge fall; fixed anatomical ruler and pooled grade."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
RAW=P/'sources/fall-v1.png'
IDLE=R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'
HEADS=[(326,87),(856,213),(450,811),(1077,894)]
NECKS=[(321,145),(852,271),(408,876),(1024,948)]
CONTACTS=[(340,674),(999,680),(390,1211),(750,1195)]
TARGETS=[(144,223),(144,223),(144,223),(105,223)]
ANGLES=[0,0,40,45]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pad(im):
 out=Image.new('RGBA',(256,272));out.alpha_composite(im,(0,0));return out
raw=np.array(Image.open(RAW).convert('RGBA'))
labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-4:],key=lambda k:(np.where(labs==k)[0].mean()//640,np.where(labs==k)[1].mean()))
y,x=np.where(labs==ids[0]);height=int(y.max()-y.min()+1);scale=148/height
assert height==649 and min(sizes[ids])>70000
yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
for hx,hy in HEADS:head|=(xx-hx)**2+(yy-hy)**2<75**2
master=Image.new('RGBA',(256,272));master.alpha_composite(Image.open(IDLE).convert('RGBA'),(36,52))
ref=np.array(master);ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<155)&(ry>=74)&(ry<107)
def masks(a,h):
 r,g,b=[a[:,:,c].astype(float) for c in range(3)];solid=a[:,:,3]>200;warm=(r>g*1.12)&(g>b*1.2)
 blue=solid&(b>r*1.3)&(b>g*1.1);skin=solid&h&warm&(r>150)&(g>90)
 return {'skin':skin,'hair':solid&h&warm&~skin,'science':blue,'neutral':solid&~h&~blue&(np.ptp(a[:,:,:3],axis=2)<45)}
graded=raw.copy();curves={};sm=masks(raw,head);rm=masks(ref,rh);q=[0,15,35,55,75,90,100]
for kind,mask in sm.items():
 assert mask.sum()>30 and rm[kind].sum()>5
 intensity=raw[:,:,:3][mask].mean(1);knots=np.percentile(intensity,q);target=np.percentile(ref[:,:,:3][rm[kind]],q,axis=0)
 for c in range(3):graded[mask,c]=np.interp(intensity,knots,target[:,c]).clip(0,255).astype('uint8')
 curves[kind]={'input':knots.tolist(),'master':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(rm[kind].sum())}
native=Image.open(R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head.png').convert('RGBA')
closed=Image.open(R/'character/veld-death-ground-east-coherent-v1/sources/canonical-head-closed.png').convert('RGBA')
frames={};records=[];checks=0
for gear in ['bare','helmet']:
 first=pad(Image.open(R/f'character/veld-seated-east-coherent-v1/frames/{gear}/sit-down-east/005.png').convert('RGBA'))
 terminal=pad(Image.open(R/f'character/veld-death-ground-east-coherent-v1/frames/{gear}/death-ground-east/005.png').convert('RGBA'))
 frames[gear]=[first]
 for i in [2,3]:
  k=ids[i];y,x=np.where(labs==k);box=(int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4)
  keep=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);a=graded.copy();a[~keep]=0
  cut=Image.fromarray(a).crop(box).resize((round((box[2]-box[0])*scale),round((box[3]-box[1])*scale)),Image.Resampling.LANCZOS)
  pos=tuple(round(TARGETS[i][j]-(CONTACTS[i][j]-box[j])*scale) for j in range(2))
  out=Image.new('RGBA',(256,272));out.alpha_composite(cut,pos)
  center=[pos[j]+(HEADS[i][j]-box[j])*scale for j in range(2)]
  neck=[pos[j]+(NECKS[i][j]-box[j])*scale for j in range(2)]
  assert min(pos)>=0 and pos[0]+cut.width<256 and pos[1]+cut.height<272;checks+=1
  protected=None;helmet_pos=None
  if gear=='helmet':
   component=closed if i==4 else native;rot=component.rotate(-ANGLES[i],resample=Image.Resampling.BICUBIC,expand=True)
   rad=math.radians(ANGLES[i]);dx,dy=19-component.width/2,36-component.height/2
   anchor=[rot.width/2+math.cos(rad)*dx-math.sin(rad)*dy,rot.height/2+math.sin(rad)*dx+math.cos(rad)*dy]
   helmet_pos=tuple(round(neck[j]-anchor[j]) for j in range(2))
   b=np.array(out);cy,cx=np.indices(b.shape[:2]);local=(cx-center[0])**2+(cy-center[1])**2<20**2
   warm=(b[:,:,0].astype(float)>b[:,:,1]*1.12)&(b[:,:,1].astype(float)>b[:,:,2]*1.14)
   erase=local&warm
   skin=masks(b,local)['skin'];sy,sx=np.where(skin);assert len(sy)>0
   erase|=local&(cy<=sy.min()+3)&(b[:,:,3]>0)
   protected=erase.copy();hx,hy=helmet_pos;protected[hy:hy+rot.height,hx:hx+rot.width]=True
   original=b.copy();b[erase]=0;out=Image.fromarray(b);out.alpha_composite(rot,helmet_pos)
   assert np.array_equal(np.array(out)[~protected],original[~protected]);checks+=1
   np.save(P/f'helmet-protected-pose-{i}.npy',protected)
  a=np.array(out);a[a[:,:,3]<8]=0;out=Image.fromarray(a);frames[gear].append(out)
  records.append({'gear':gear,'pose':i,'box':box,'position':pos,'sourceContact':CONTACTS[i],'targetContact':TARGETS[i],'headCenter':center,'neck':neck,'helmetPosition':helmet_pos,'helmetNativeScale':1 if gear=='helmet' else None,'tiltDegrees':ANGLES[i]})
 for source_index in [2,3,4]:frames[gear].append(Image.open(R/f'character/veld-bunk-early-fall-v1/frames/{gear}/death-bunk-crouch-east/{source_index:03}.png').convert('RGBA'))
 for i,im in enumerate(frames[gear]):
  path=P/f'frames/{gear}/death-lounge-seated-east/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
  assert im.getbbox()[0]>0 and im.getbbox()[1]>0 and im.getbbox()[2]<256 and im.getbbox()[3]<272;checks+=1
 states=[]
 for key,count,timing in [('death-lounge-seated-east',6,[180,180,180,180,220,500])]:
  states.append({'id':key,'frameFiles':[f'res://character/veld-lounge-fall-east-v1/frames/{gear}/{key}/{i:03}.png' for i in range(count)],'frameDurationsMs':timing,'loop':False,'terminalFrame':count-1,'furnitureFrames':['']*count,'depthOffsets':[0]*count})
 manifest={'name':'Veld seated lounge floor fall candidate','equipment':'diving-helmet' if gear=='helmet' else '', 'canvas':[256,272],'frameWidth':256,'frameHeight':272,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_source_only_native_entry_contact_pending','states':states}
 (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 assert frames[gear][0].tobytes()==first.tobytes() and frames[gear][-1].tobytes()==terminal.tobytes();checks+=2
(P/'material-grade.json').write_text(json.dumps(curves,indent=2)+'\n')
(P/'registration.json').write_text(json.dumps({'sourceSha256':sha(RAW),'standingSourceOpaqueHeight':height,'fixedRuler':scale,'nativeMasterHeight':148,'records':records,'checks':checks,'failures':0,'generatedSourcePoses':[2,3],'exactEntry':'staged master-aligned East seated pose5','exactTerminal':'current ground pose5 with transparent bottom16 padding','scope':'staged artwork only; selector/native furniture and temporal validation pending'},indent=2)+'\n')
board=Image.new('RGB',(1536,850),'#202a30');draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
 for i,im in enumerate(frames[gear]):
  board.paste(im,(i*256,row*280+20),im);draw.text((i*256+8,row*280+4),f'{gear} seated fall {i}',fill='white')
for i in range(6):
 im=master;board.paste(im,(i*256,580),im);draw.text((i*256+8,564),'Standing master / H148',fill='white')
board.save(P/'paired-source-review.png')
print(f'{checks} source/entry/terminal/helmet-body checks,0failures; fixed148/{height} ruler')
