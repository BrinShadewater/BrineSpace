"""One frozen source ruler, pooled semantic grade, exact selected standing joins."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
geometry=json.loads((P/'source-review.json').read_text());raw_path=P/geometry['source'];raw=np.array(Image.open(raw_path).convert('RGBA'))
master_path=R/geometry['master'];master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(master_path).convert('RGBA'),(36,52));reference=np.array(master)
yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool);face=np.zeros_like(head);heads=[];necks=[]
for r in geometry['frames']:
 x0,y0,x1,y1=r['rawBox'];cx=(x0+x1)/2;top=y0+3
 head|=((xx-cx)/46)**2+((yy-top-45)/51)**2<1
 face|=((xx-cx)/28)**2+((yy-top-59)/26)**2<1
 heads.append([cx,top+45]);necks.append([cx,top+99])
def masks(a,h,f):
 rgb=a[:,:,:3].astype(float);solid=a[:,:,3]>200;warm=solid&h&(rgb[:,:,0]>1.10*rgb[:,:,1])&(rgb[:,:,1]>1.08*rgb[:,:,2])
 cyan=solid&~h&(rgb[:,:,1]>1.4*rgb[:,:,0])&(rgb[:,:,2]>1.3*rgb[:,:,0])&(rgb[:,:,1]>.72*rgb[:,:,2])
 science=solid&~h&~cyan&(rgb[:,:,2]>1.3*rgb[:,:,0])&(rgb[:,:,2]>1.10*rgb[:,:,1])
 neutral=solid&~h&~cyan&~science&(np.ptp(rgb,axis=2)<45)
 return {'skin':warm&f,'hair':warm&~f,'cloth':neutral&(rgb.mean(2)<=95),'metal':neutral&(rgb.mean(2)>95),'science':science,'cyan':cyan}
ry,rx=np.indices(reference.shape[:2]);rh=(rx>=111)&(rx<=146)&(ry>=74)&(ry<=105)
# Master face is turned slightly within its south view. A centered ellipse sampled
# lower jaw shadows and misclassified its brighter outer cheek as hair.
rf=(rx>=124)&(rx<=143)&(ry>=83)&(ry<=101)
sm=masks(raw,head,face);rm=masks(reference,rh,rf);graded=raw.copy();curves={};palette={'skin':(230,135,85),'hair':(123,75,45),'cloth':(85,90,94),'metal':(205,195,180),'science':(50,110,220),'cyan':(20,195,205)}
mask_board=np.zeros_like(raw)
for name,mask in sm.items():
 authority=rm[name];assert mask.sum()>30 and authority.sum()>3,(name,int(mask.sum()),int(authority.sum()))
 lum=raw[:,:,:3][mask].mean(1);knots=np.percentile(lum,[0,15,35,55,75,90,100]);target=np.percentile(reference[:,:,:3][authority],[0,15,35,55,75,90,100],axis=0)
 for c in range(3):graded[mask,c]=np.interp(lum,knots,target[:,c]).clip(0,255).astype('uint8')
 curves[name]={'knots':knots.tolist(),'targets':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(authority.sum())}
 mask_board[mask,:3]=palette[name];mask_board[mask,3]=255
Image.fromarray(mask_board).save(P/'semantic-masks.png')
labs,n=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;parts=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].mean())//512,int(np.where(labs==k)[1].mean())//512))
frames=[master];files=[]
for slot in range(1,6):
 r=geometry['frames'][slot];pixels=graded.copy();pixels[~(binary_dilation(labs==parts[slot],iterations=3)&(raw[:,:,3]>0))]=0
 crop=Image.fromarray(pixels).crop(r['rawBox']).resize(r['size'],Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop,r['position']);frames.append(frame)
for slot,frame in enumerate(frames):
 path=P/f'frames/bare/sit-down-south/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);frame.save(path);files.append(path.relative_to(P).as_posix())
durations=[80,100,140,160,160,160]
def state(key,paths,times,loop):return {'id':key,'frameFiles':paths,'frameDurationsMs':times,'loop':loop,'facings':['south']*len(paths),'waterPoses':[False]*len(paths),'waterKinds':['seated']*len(paths),'depthOffsets':[0]*len(paths),'seatContactDepth':True}
manifest={'name':'Veld south seated bare candidate','status':'staged_candidate','precomposed':True,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':[state('sit-down-south',files,durations,False),state('sit-rise-south',files[::-1],durations[::-1],False),state('sit-idle-south',[files[-1]],[1000],True)]}
(P/'bare-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
registration={'source':geometry['source'],'sourceSha256':hashlib.sha256(raw_path.read_bytes()).hexdigest(),'master':geometry['master'],'masterSha256':hashlib.sha256(master_path.read_bytes()).hexdigest(),'fixedRuler':geometry['fixedRuler'],'frames':geometry['frames'],'heads':heads,'necks':necks,'grade':'one pooled curve per semantic region from all six raw figures to selected front master, once before extraction/resampling','curves':curves,'scope':'staged source fit; no helmet/native/furniture/motion/acceptance claim'}
(P/'bare-registration.json').write_text(json.dumps(registration,indent=2)+'\n')
board=Image.new('RGB',(1792,540),'#202a30');d=ImageDraw.Draw(board)
for col,frame in enumerate([master]+frames):
 board.paste(frame,(col*256,20),frame);d.text((col*256+5,3),'Selected master' if col==0 else f'Fitted {col-1}',fill='white')
 detail=frame.crop((90,70,168,230)).resize((117,240),Image.Resampling.NEAREST);board.paste(detail,(col*256+68,280),detail)
board.save(P/'bare-contact.png')
print(json.dumps({'exports':6,'states':3,'references':13,'durationMs':800,'normalSelection':False}))
