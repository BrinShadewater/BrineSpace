"""Authored partial North seat fall: one 148/592 ruler, pooled anatomical grade."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation
P=Path(__file__).resolve().parent; R=P.parents[1]
RAW=P/'sources/fall-v1.png'
HEADS=[(351,95),(860,225),(361,805),(858,930)]
NECKS=[(351,140),(860,273),(361,832),(858,950)]
CONTACTS=[(351,638),(860,638),(363,1202),(860,1221)]
EARS=[(303,104,321,132),(383,104,402,132),(811,237,829,266),(893,237,910,266),(309,810,327,836),(397,810,414,836),(806,935,825,955),(895,935,911,955)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def padded(path):
 out=Image.new('RGBA',(256,272)); out.alpha_composite(Image.open(path).convert('RGBA')); return out
raw=np.array(Image.open(RAW).convert('RGBA')); labs,n=label(raw[:,:,3]>180)
sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-4:],key=lambda k:(np.where(labs==k)[0].mean()//643,np.where(labs==k)[1].mean()))
y,x=np.where(labs==ids[0]); height=int(y.max()-y.min()+1); assert height==592 and min(sizes[ids])>58000
scale=148/height
yy,xx=np.indices(raw.shape[:2]); head=np.zeros(raw.shape[:2],bool); ear=np.zeros_like(head)
for hx,hy in HEADS:head|=(xx-hx)**2+(yy-hy)**2<57**2
for x0,y0,x1,y1 in EARS:ear[y0:y1,x0:x1]=True
master=Image.new('RGBA',(256,272)); master.alpha_composite(Image.open(R/'character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png').convert('RGBA'),(36,52))
ref=np.array(master);ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<144)&(ry>=76)&(ry<104)
re=(((rx>=116)&(rx<=119)&(ry>=89)&(ry<=94))|((rx>=137)&(rx<=140)&(ry>=89)&(ry<=94)))
def masks(a,h,e):
 v=a[:,:,:3].astype(float); solid=a[:,:,3]>200
 warm=(v[:,:,0]>v[:,:,1]*1.10)&(v[:,:,1]>v[:,:,2]*1.10)
 blue=solid&(v[:,:,2]>v[:,:,0]*1.30)&(v[:,:,2]>v[:,:,1]*1.10)
 skin=solid&e&warm
 return {'skin':skin,'hair':solid&h&warm&~skin,'science':blue,'neutral':solid&~h&~blue&(np.ptp(v,axis=2)<45)}
sm=masks(raw,head,ear);rm=masks(ref,rh,re);graded=raw.copy();curves={};q=[0,15,35,55,75,90,100]
for kind,mask in sm.items():
 assert mask.sum()>30 and rm[kind].sum()>5,(kind,mask.sum(),rm[kind].sum())
 intensity=raw[:,:,:3][mask].mean(1);knots=np.percentile(intensity,q);target=np.percentile(ref[:,:,:3][rm[kind]],q,axis=0)
 for c in range(3):graded[mask,c]=np.interp(intensity,knots,target[:,c]).clip(0,255).astype('uint8')
 curves[kind]={'input':knots.tolist(),'master':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(rm[kind].sum()),'authority':'explicit anatomical rear ear windows' if kind=='skin' else 'selected North idle material'}
records=[];frames={};checks=0;bindings={}
for gear in ['bare','helmet']:
 first=R/f'character/veld-seated-north-coherent-v1/frames/{gear}/sit-down-north/002.png'
 frames[gear]=[padded(first)];bindings[first.relative_to(R).as_posix()]=sha(first)
 for i in [2,3]:
  k=ids[i];y,x=np.where(labs==k);box=(int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4)
  keep=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);a=graded.copy();a[~keep]=0
  cut=Image.fromarray(a).crop(box).resize((round((box[2]-box[0])*scale),round((box[3]-box[1])*scale)),Image.Resampling.LANCZOS)
  pos=(round(128-(CONTACTS[i][0]-box[0])*scale),round(223-(CONTACTS[i][1]-box[1])*scale))
  out=Image.new('RGBA',(256,272));out.alpha_composite(cut,pos)
  center=[pos[j]+(HEADS[i][j]-box[j])*scale for j in range(2)];neck=[pos[j]+(NECKS[i][j]-box[j])*scale for j in range(2)]
  assert min(pos)>=0 and pos[0]+cut.width<256 and pos[1]+cut.height<272;checks+=1
  helmet_pos=None;component_path=None
  if gear=='helmet':
   component_path=R/f'character/veld-death-ground-north-coherent-v1/sources/fitted-pitch-{i-1:02}.png'
   component=Image.open(component_path).convert('RGBA');bindings[component_path.relative_to(R).as_posix()]=sha(component_path)
   b=np.array(out);cy,cx=np.indices(b.shape[:2]);local=(cx-center[0])**2+(cy-center[1])**2<18**2
   v=b[:,:,:3].astype(float);warm=(v[:,:,0]>v[:,:,1]*1.10)&(v[:,:,1]>v[:,:,2]*1.10)
   erase=local&warm;erase|=local&(cy<neck[1]-4)&(b[:,:,3]>0)
   helmet_pos=(round(neck[0]-component.width/2),round(neck[1]-(component.height-3)));hx,hy=helmet_pos
   protected=erase.copy();protected[hy:hy+component.height,hx:hx+component.width]=True
   original=b.copy();b[erase]=0;out=Image.fromarray(b);out.alpha_composite(component,helmet_pos)
   assert np.array_equal(np.array(out)[~protected],original[~protected]);checks+=1
   np.save(P/f'helmet-protected-pose-{i}.npy',protected)
  a=np.array(out);a[a[:,:,3]<8]=0;out=Image.fromarray(a);frames[gear].append(out)
  records.append({'gear':gear,'sourcePose':i,'box':box,'position':pos,'sourceContact':CONTACTS[i],'targetContact':[128,223],'headCenter':center,'neck':neck,'helmetPosition':helmet_pos,'helmetNativeScale':1 if gear=='helmet' else None,'helmetPitchDegrees':([15,40][i-2] if gear=='helmet' else None),'helmetComponent':component_path.relative_to(R).as_posix() if component_path else None})
 for index in [3,4,5]:
  path=R/f'character/veld-death-ground-north-coherent-v1/frames/{gear}/death-ground-north/{index:03}.png'
  frames[gear].append(padded(path));bindings[path.relative_to(R).as_posix()]=sha(path)
 for index,im in enumerate(frames[gear]):
  path=P/f'frames/{gear}/death-lounge-partial-north/{index:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
  box=im.getbbox();assert box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272;checks+=1
 state={'id':'death-lounge-partial-north','frameFiles':[f'res://character/veld-lounge-partial-fall-north-v1/frames/{gear}/death-lounge-partial-north/{index:03}.png' for index in range(6)],'frameDurationsMs':[180,160,180,180,220,500],'loop':False,'terminalFrame':5,'furnitureFrames':['']*6,'depthOffsets':[0]*6}
 manifest={'name':'Veld partial North lounge floor fall source candidate','equipment':'diving-helmet' if gear=='helmet' else '', 'canvas':[256,272],'frameWidth':256,'frameHeight':272,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'loungeFallDeathMode':'partial-north-v1','status':'installed_locally_owner_motion_review_open','states':[state]}
 (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(P/'material-grade.json').write_text(json.dumps(curves,indent=2)+'\n',encoding='utf-8')
(P/'registration.json').write_text(json.dumps({'sourceSha256':sha(RAW),'generation':'exec-774892bf-42da-4a9b-adeb-1f1ced7eaeda','standingSourceOpaqueHeight':height,'fixedRuler':scale,'nativeMasterHeight':148,'records':records,'checks':checks,'failures':0,'newInteriorSourcePoses':[2,3],'bindings':bindings,'scope':'source artwork only; not proof of all earlier seat entrances or furniture contact'},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,850),'#202a30');draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
 for index,im in enumerate(frames[gear]):board.paste(im,(index*256,row*280+20),im);draw.text((index*256+8,row*280+4),f'{gear} partial North fall {index}',fill='white')
for index in range(6):board.paste(master,(index*256,580),master);draw.text((index*256+8,564),'Standing master / H148',fill='white')
board.save(P/'paired-source-review.png');print(f'{checks} builder checks,0failures; fixed148/{height} ruler')
