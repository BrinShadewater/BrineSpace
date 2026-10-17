"""Authored rear lounge fall; one body ruler, rear-ear grade, native depth-pitch helmet."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
RAW=P/'sources/fall-v1.png';IDLE=R/'character/crew-runtime-matte-v1/veld/frames/idle-north-breathing-v1/000.png'
HEADS=[(285,130),(780,248),(315,909),(790,1018)]
NECKS=[(285,202),(780,307),(295,950),(790,1054)]
CONTACTS=[(286,768),(780,712),(291,1308),(790,1385)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pad(im):
 out=Image.new('RGBA',(256,272));out.alpha_composite(im,(0,0));return out
def regions(a,head):
 v=a[:,:,:3].astype(float);solid=a[:,:,3]>200;warm=(v[:,:,0]>1.12*v[:,:,1])&(v[:,:,1]>1.20*v[:,:,2]);luma=v.mean(2)
 blue=solid&(v[:,:,2]>1.30*v[:,:,0])&(v[:,:,2]>1.10*v[:,:,1])
 return {'skin':solid&head&warm&(luma>=80),'hair':solid&head&warm&(luma<80),'science':blue,'neutral':solid&~head&~blue&(np.ptp(v,axis=2)<45)}
raw=np.array(Image.open(RAW).convert('RGBA'));labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-4:],key=lambda k:(np.where(labs==k)[0].mean()//(raw.shape[0]/2),np.where(labs==k)[1].mean()))
y,x=np.where(labs==ids[0]);height=int(y.max()-y.min()+1);scale=148/height
assert height==693 and min(sizes[ids])>80000
yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
for hx,hy in HEADS:head|=(xx-hx)**2+(yy-hy)**2<65**2
master=Image.new('RGBA',(256,272));master.alpha_composite(Image.open(IDLE).convert('RGBA'),(36,52));ref=np.array(master)
ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<144)&(ry>=76)&(ry<104)
sm=regions(raw,head);rm=regions(ref,rh);v=ref[:,:,:3].astype(float)
ears=(((rx>=116)&(rx<=119)&(ry>=89)&(ry<=94))|((rx>=137)&(rx<=140)&(ry>=89)&(ry<=94)))&(ref[:,:,3]>160)&(v[:,:,0]>v[:,:,1]*1.10)&(v[:,:,1]>v[:,:,2]*1.10)
rm['skin']=ears;rm['hair']&=~ears;graded=raw.copy();curves={};q=[0,15,35,55,75,90,100]
for kind,mask in sm.items():
 assert mask.sum()>30 and rm[kind].sum()>5,(kind,int(mask.sum()),int(rm[kind].sum()))
 intensity=raw[:,:,:3][mask].mean(1);knots=np.percentile(intensity,q);target=np.percentile(ref[:,:,:3][rm[kind]],q,axis=0)
 for c in range(3):graded[mask,c]=np.interp(intensity,knots,target[:,c]).clip(0,255).astype('uint8')
 curves[kind]={'input':knots.tolist(),'master':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(rm[kind].sum()),'authority':'spatial rear-ear strips' if kind=='skin' else 'selected North idle material'}
helmet_path=R/'character/veld-death-ground-north-coherent-v1/sources/fitted-pitch-02.png'
component=Image.open(helmet_path).convert('RGBA');assert component.size==(32,29)
frames={};records=[];checks=0
for gear in ['bare','helmet']:
 first=pad(Image.open(R/f'character/veld-seated-north-coherent-v1/frames/{gear}/sit-down-north/005.png').convert('RGBA'));frames[gear]=[first]
 for i in [2,3]:
  k=ids[i];y,x=np.where(labs==k);box=(int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4)
  keep=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);a=graded.copy();a[~keep]=0
  cut=Image.fromarray(a).crop(box).resize((round((box[2]-box[0])*scale),round((box[3]-box[1])*scale)),Image.Resampling.LANCZOS)
  pos=(round(128-(CONTACTS[i][0]-box[0])*scale),round(223-(CONTACTS[i][1]-box[1])*scale))
  out=Image.new('RGBA',(256,272));out.alpha_composite(cut,pos)
  center=[pos[j]+(HEADS[i][j]-box[j])*scale for j in range(2)];neck=[pos[j]+(NECKS[i][j]-box[j])*scale for j in range(2)]
  assert min(pos)>=0 and pos[0]+cut.width<256 and pos[1]+cut.height<272;checks+=1
  helmet_pos=None
  if gear=='helmet':
   b=np.array(out);cy,cx=np.indices(b.shape[:2]);local=(cx-center[0])**2+(cy-center[1])**2<18**2
   v=b[:,:,:3].astype(float);warm=(v[:,:,0]>v[:,:,1]*1.12)&(v[:,:,1]>v[:,:,2]*1.14)
   erase=local&warm;erase|=local&(cy<neck[1]-4)&(b[:,:,3]>0)
   helmet_pos=(round(neck[0]-16),round(neck[1]-26));hx,hy=helmet_pos
   protected=erase.copy();protected[hy:hy+component.height,hx:hx+component.width]=True
   original=b.copy();b[erase]=0;out=Image.fromarray(b);out.alpha_composite(component,helmet_pos)
   assert np.array_equal(np.array(out)[~protected],original[~protected]);checks+=1
   np.save(P/f'helmet-protected-pose-{i}.npy',protected)
  a=np.array(out);a[a[:,:,3]<8]=0;out=Image.fromarray(a);frames[gear].append(out)
  records.append({'gear':gear,'pose':i,'box':box,'position':pos,'sourceContact':CONTACTS[i],'targetContact':[128,223],'headCenter':center,'neck':neck,'helmetPosition':helmet_pos,'helmetNativeScale':1 if gear=='helmet' else None,'helmetPitchDegrees':40 if gear=='helmet' else None})
 for source_index in [3,4,5]:frames[gear].append(pad(Image.open(R/f'character/veld-death-ground-north-coherent-v1/frames/{gear}/death-ground-north/{source_index:03}.png').convert('RGBA')))
 for i,im in enumerate(frames[gear]):
  path=P/f'frames/{gear}/death-lounge-seated-north/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
  assert im.getbbox()[0]>0 and im.getbbox()[1]>0 and im.getbbox()[2]<256 and im.getbbox()[3]<272;checks+=1
 state={'id':'death-lounge-seated-north','frameFiles':[f'res://character/veld-lounge-fall-north-v1/frames/{gear}/death-lounge-seated-north/{i:03}.png' for i in range(6)],'frameDurationsMs':[180,180,180,180,220,500],'loop':False,'terminalFrame':5,'furnitureFrames':['']*6,'depthOffsets':[0]*6}
 manifest={'name':'Veld North seated lounge floor fall candidate','equipment':'diving-helmet' if gear=='helmet' else '','canvas':[256,272],'frameWidth':256,'frameHeight':272,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'installed_locally_owner_motion_review_open','loungeFallDeathMode':'seated-north-v1','states':[state]}
 (P/f'{gear}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
 assert frames[gear][0].tobytes()==first.tobytes();checks+=1
(P/'material-grade.json').write_text(json.dumps(curves,indent=2)+'\n',encoding='utf-8')
(P/'registration.json').write_text(json.dumps({'sourceSha256':sha(RAW),'standingSourceOpaqueHeight':height,'fixedRuler':scale,'nativeMasterHeight':148,'records':records,'checks':checks,'failures':0,'generatedSourcePoses':[2,3],'helmetComponent':helmet_path.relative_to(R).as_posix(),'helmetComponentSha256':sha(helmet_path),'scope':'staged source artwork; current real lounge facing North, native seat registration/selector/Continue pending'},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,850),'#202a30');draw=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
 for i,im in enumerate(frames[gear]):board.paste(im,(i*256,row*280+20),im);draw.text((i*256+8,row*280+4),f'{gear} North seated fall {i}',fill='white')
for i in range(6):board.paste(master,(i*256,580),master);draw.text((i*256+8,564),'Standing master / H148',fill='white')
board.save(P/'paired-source-review.png');print(f'{checks} builder source/helmet/clipping checks,0failures; fixed148/{height}')
