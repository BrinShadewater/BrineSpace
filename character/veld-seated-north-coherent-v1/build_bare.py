"""One source ruler/pooled material grade; exact selected standing, held seat/reverse."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
geometry=json.loads((P/'source-scale-review.json').read_text())
raw=np.array(Image.open(P/geometry['source']).convert('RGBA'))
master_path=R/geometry['master'];master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(master_path).convert('RGBA'),(36,52));ref=np.array(master)
yy,xx=np.indices(raw.shape[:2]);heads=[];head=np.zeros(raw.shape[:2],bool);ears=np.zeros_like(head)
for record in geometry['frames']:
    x0,y0,x1,y1=record['box'];hx=(x0+x1)*.5;hy=y0+39;heads.append([hx,hy])
    head|=(xx-hx)**2+(yy-hy)**2<55**2
    ears|=(abs(xx-hx)>27)&(abs(xx-hx)<46)&(yy>hy+5)&(yy<hy+28)
def masks(a,h):
    rgb=a[:,:,:3].astype(float);solid=a[:,:,3]>200
    warm=solid&h&(rgb[:,:,0]>1.10*rgb[:,:,1])&(rgb[:,:,1]>1.13*rgb[:,:,2])
    blue=solid&(rgb[:,:,2]>1.30*rgb[:,:,0])&(rgb[:,:,2]>1.10*rgb[:,:,1])
    return {'skin':warm.copy(),'hair':warm.copy(),'science':blue,'neutral':solid&~h&~blue&(np.ptp(rgb,axis=2)<45)}
ry,rx=np.indices(ref.shape[:2]);rh=(rx>=116)&(rx<=143)&(ry>=75)&(ry<=105)
sm=masks(raw,head);rm=masks(ref,rh)
sm['skin']&=ears;sm['hair']&=~ears
rear_ears=((rx>=116)&(rx<=119)&(ry>=89)&(ry<=94))|((rx>=137)&(rx<=140)&(ry>=89)&(ry<=94))
rm['skin']&=rear_ears;rm['hair']&=~rear_ears
graded=raw.copy();curves={};quantiles=[0,15,35,55,75,90,100]
for material,mask in sm.items():
    authority=rm[material];assert mask.sum()>30 and authority.sum()>5,(material,int(mask.sum()),int(authority.sum()))
    luminance=raw[:,:,:3][mask].mean(1);knots=np.percentile(luminance,quantiles);target=np.percentile(ref[:,:,:3][authority],quantiles,axis=0)
    for channel in range(3):graded[mask,channel]=np.interp(luminance,knots,target[:,channel]).clip(0,255).astype('uint8')
    curves[material]={'knots':knots.tolist(),'targets':target.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(authority.sum())}
labels,count=label(raw[:,:,3]>180);sizes=np.bincount(labels.ravel());sizes[0]=0
parts=sorted(np.argsort(sizes)[-6:],key=lambda k:(int(np.where(labels==k)[0].min())//512,int(np.where(labels==k)[1].mean())//512))
frames=[master];files=[]
for slot in range(1,6):
    record=geometry['frames'][slot];pixels=graded.copy();pixels[~(binary_dilation(labels==parts[slot],iterations=3)&(raw[:,:,3]>0))]=0
    crop=Image.fromarray(pixels).crop(record['box']).resize(tuple(record['size']),Image.Resampling.LANCZOS)
    frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop,tuple(record['position']));frames.append(frame)
for slot,frame in enumerate(frames):
    path=P/f'frames/bare/sit-down-north/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);frame.save(path);files.append(path.relative_to(P).as_posix())
durations=[80,100,140,160,160,160]
def state(key,paths,timing,loop):
    return {'id':key,'frameFiles':paths,'frameDurationsMs':timing,'loop':loop,'facings':['north']*len(paths),'waterPoses':[False]*len(paths),'waterKinds':['seated']*len(paths),'depthOffsets':[0]*len(paths),'seatContactDepth':True}
manifest={'name':'Veld north seated bare candidate','status':'staged_candidate','precomposed':True,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','states':[state('sit-down-north',files,durations,False),state('sit-rise-north',files[::-1],durations[::-1],False),state('sit-idle-north',[files[-1]],[1000],True)]}
(P/'bare-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
registration={'source':geometry['source'],'sourceSha256':sha(P/geometry['source']),'master':geometry['master'],'masterSha256':sha(master_path),'fixedRuler':geometry['fixedRuler'],'heads':heads,'frames':geometry['frames'],'grade':'one pooled clip-wide curve per semantic material applied once before extraction/resampling','curves':curves,'scope':'staged bare chair-height sitting; equipment/native/world/contact/interruption/Continue pending'}
(P/'bare-registration.json').write_text(json.dumps(registration,indent=2)+'\n')
board=Image.new('RGB',(1792,540),'#202a30');draw=ImageDraw.Draw(board)
for col,frame in enumerate([master]+frames):
    board.paste(frame,(col*256,20),frame);draw.text((col*256+5,3),'Master' if col==0 else f'Candidate {col-1}',fill='white')
    small=frame.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(col*256+57,360),small)
board.save(P/'bare-contact-sheet.png')
print(json.dumps({'bareStates':3,'exports':6,'references':13,'durationMs':sum(durations),'normalSelection':False}))
