"""Pool the east materials once before extraction; exact selected standing join."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent; R=P.parents[1]
g=json.loads((P/'source-review.json').read_text()); source=P/g['source']; raw=np.array(Image.open(source).convert('RGBA'))
master_path=R/g['master']; master=Image.new('RGBA',(256,256)); master.alpha_composite(Image.open(master_path).convert('RGBA'),(36,52)); ref=np.array(master)
yy,xx=np.indices(raw.shape[:2]); head=np.zeros(raw.shape[:2],bool); face=np.zeros_like(head)
head_boxes=[(264,14,370,103),(701,47,816,138),(1141,93,1257,188),(249,589,359,682),(702,592,812,686),(1136,590,1248,684)]
head_boxes=[(g['frames'][i]['rawBox'][0]+3,*box[1:]) for i,box in enumerate(head_boxes)]
face_boxes=[(318,43,368,103),(768,79,815,136),(1207,124,1255,186),(307,620,357,680),(760,623,810,684),(1196,621,1246,682)]
for h,f in zip(head_boxes,face_boxes):
 head|=(xx>=h[0])&(xx<h[2])&(yy>=h[1])&(yy<h[3]); face|=(xx>=f[0])&(xx<f[2])&(yy>=f[1])&(yy<f[3])
def masks(a,h,f):
 rgb=a[:,:,:3].astype(float); solid=a[:,:,3]>200
 warm=solid&h&(rgb[:,:,0]>1.10*rgb[:,:,1])&(rgb[:,:,1]>1.08*rgb[:,:,2])
 cyan=solid&~h&(rgb[:,:,1]>1.4*rgb[:,:,0])&(rgb[:,:,2]>1.3*rgb[:,:,0])&(rgb[:,:,1]>.72*rgb[:,:,2])
 science=solid&~h&~cyan&(rgb[:,:,2]>1.3*rgb[:,:,0])&(rgb[:,:,2]>1.10*rgb[:,:,1])
 neutral=solid&~h&~cyan&~science&(np.ptp(rgb,axis=2)<45)
 return {'skin':warm&f,'hair':warm&~f,'cloth':neutral&(rgb.mean(2)<=95),'metal':neutral&(rgb.mean(2)>95),'science':science,'cyan':cyan}
ry,rx=np.indices(ref.shape[:2]); rh=(rx>=118)&(rx<153)&(ry>=73)&(ry<105); rf=(rx>=135)&(rx<153)&(ry>=82)&(ry<105)
sm=masks(raw,head,face); rm=masks(ref,rh,rf); graded=raw.copy(); curves={}; mask_board=np.zeros_like(raw)
palette={'skin':(230,135,85),'hair':(123,75,45),'cloth':(85,90,94),'metal':(205,195,180),'science':(50,110,220),'cyan':(20,195,205)}
for name,mask in sm.items():
 authority=rm[name]; assert mask.sum()>10 and authority.sum()>0,(name,int(mask.sum()),int(authority.sum()))
 lum=raw[:,:,:3][mask].mean(1); knots=np.percentile(lum,[0,15,35,55,75,90,100]); target=np.percentile(ref[:,:,:3][authority],[0,15,35,55,75,90,100],axis=0)
 for c in range(3): graded[mask,c]=np.interp(lum,knots,target[:,c]).clip(0,255).astype('uint8')
 curves[name]={'knots':knots.tolist(),'targets':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(authority.sum())}
 mask_board[mask,:3]=palette[name]; mask_board[mask,3]=255
assert np.array_equal(graded[:,:,3],raw[:,:,3]); Image.fromarray(mask_board).save(P/'semantic-masks.png')
labs,n=label(raw[:,:,3]>180); counts=np.bincount(labs.ravel()); counts[0]=0
parts=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.where(labs==k)[0].mean())//512,int(np.where(labs==k)[1].mean())//512))
frames=[master]; files=[]
for slot in range(1,6):
 r=g['frames'][slot]; pixels=graded.copy(); pixels[~(binary_dilation(labs==parts[slot],iterations=3)&(raw[:,:,3]>0))]=0
 crop=Image.fromarray(pixels).crop(r['rawBox']).resize(r['size'],Image.Resampling.LANCZOS)
 frame=Image.new('RGBA',(256,256)); frame.alpha_composite(crop,r['position']); frames.append(frame)
for slot,frame in enumerate(frames):
 path=P/f'frames/bare/sit-down-east/{slot:03}.png'; path.parent.mkdir(parents=True,exist_ok=True); frame.save(path); files.append(path.relative_to(P).as_posix())
durations=[80,100,140,160,160,160]
def state(key,paths,times,loop): return {'id':key,'frameFiles':paths,'frameDurationsMs':times,'loop':loop,'facings':['east']*len(paths),'waterPoses':[False]*len(paths),'waterKinds':['seated']*len(paths),'depthOffsets':[0]*len(paths),'seatContactDepth':True}
manifest={'name':'Veld east seated bare candidate','status':'staged_candidate','precomposed':True,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':[state('sit-down-east',files,durations,False),state('sit-rise-east',files[::-1],durations[::-1],False),state('sit-idle-east',[files[-1]],[1000],True)]}
(P/'bare-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(P/'bare-registration.json').write_text(json.dumps({'source':g['source'],'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'master':g['master'],'masterSha256':hashlib.sha256(master_path.read_bytes()).hexdigest(),'fixedRuler':g['fixedRuler'],'frames':g['frames'],'headBoxes':head_boxes,'faceBoxes':face_boxes,'grade':'one pooled curve per material across six raw poses; applied once before extraction/resampling','curves':curves,'scope':'staged bare source fit; no helmet/native/furniture/acceptance claim'},indent=2)+'\n')
board=Image.new('RGB',(1792,540),'#202a30'); d=ImageDraw.Draw(board)
for col,frame in enumerate([master]+frames):
 board.paste(frame,(col*256,20),frame); d.text((col*256+5,3),'Selected east master' if col==0 else f'Fitted {col-1}',fill='white')
 detail=frame.crop((75,65,180,230)).resize((153,240),Image.Resampling.NEAREST); board.paste(detail,(col*256+50,280),detail)
board.save(P/'bare-contact.png')
print(json.dumps({'exports':6,'states':3,'references':13,'durationMs':800,'materialPixels':{k:v['masterPixels'] for k,v in curves.items()},'normalSelection':False}))
