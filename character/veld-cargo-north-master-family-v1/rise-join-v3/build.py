from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent; F=P.parent/'idle-join-v2';R=P.parents[2]
raw=Image.open(P/'raw-rise-v1.png').convert('RGBA');a=np.array(raw);occupied=(a[:,:,3]>200).any(0);bounds=[0]
for i in range(1,4):
 nominal=round(i*raw.width/4);possible=np.where(~occupied[nominal-60:nominal+61])[0]+nominal-60
 assert len(possible);bounds.append(int(possible[np.argmin(abs(possible-nominal))]))
bounds.append(raw.width);cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(4)]
ys,xs=np.where(cells[3][:,:,3]>200);scale=148/(ys.max()-ys.min()+1)
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json';recipe=json.loads(recipepath.read_text(encoding='utf-8'));targets=np.array(recipe['clothTargetRGB'])
shellpath=R/'character/veld-shared-helmet-v1/fitted-north.png';shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-5:,:,3]>160);axis=(sx.min()+sx.max())/2
rows=[];new={'bare':[],'helmet':[]};checks=0
for i,cell in enumerate(cells):
 lab,n=label(cell[:,:,3]>200);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==int(sizes.argmax());yy,xx=np.where(mask);floor=int(yy.max());_,bx=np.where(mask[floor-7:floor+1]);center=(bx.min()+bx.max())/2
 clean=cell.copy();clean[~binary_dilation(mask,iterations=2)]=0
 frame=Image.new('RGBA',(256,256));offset=(round(128-center*scale),round(224-floor*scale));frame.alpha_composite(Image.fromarray(clean).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS),offset)
 old=np.array(frame);ar=old.copy();rgb=ar[:,:,:3].astype(float);fy,fx=np.where(ar[:,:,3]>200);top=int(fy.min())
 warm=(ar[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
 cloth=(ar[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False
 for ch in range(3):ar[cloth,ch]=np.interp(rgb[cloth].mean(1),recipe['clothKnots'],targets[:,ch]).clip(0,255).astype('uint8')
 for material,select in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:ar[select,:3]=(rgb[select]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8')
 assert np.array_equal(ar[:,:,3],old[:,:,3]);checks+=1
 bare=Image.fromarray(ar);hy,hx=np.where(warm);htop=int(hy.min());bodyaxis=(hx.min()+hx.max())/2;pos=(round(bodyaxis-axis),htop+27-shell.height);clear=(int(hx.min())-3,htop,int(hx.max())+4,htop+25)
 helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(shell,pos)
 protected=np.ones((256,256),bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False
 assert np.array_equal(np.array(helmet)[protected],ar[protected]);checks+=1
 new['bare'].append(bare);new['helmet'].append(helmet)
 (P/'ungraded').mkdir(exist_ok=True);frame.save(P/f'ungraded/{i:03}.png')
 rows.append({'phase':i,'floor':floor,'bootCenter':float(center),'offset':offset,'nativeHeight':int(fy.max()-fy.min()+1),'headTop':top,'shellPosition':pos,'gutterEdgeOpaque':int((cell[:,-1,3]>200).sum())})
for name in ['floor-case.png','floor-case-canvas.png']:shutil.copy2(F/name,P/name)
case=Image.open(P/'floor-case-canvas.png').convert('RGBA');durations=[70,90,100,60,65,65,70];assert sum(durations)==520
board=Image.new('RGB',(7*256,600),'#202a30');draw=ImageDraw.Draw(board);bindings={}
for row,gear in enumerate(['bare','helmet']):
 frames=[Image.open(F/f'frames/{gear}/unload-north/{i:03}.png').convert('RGBA') for i in range(3)]+new[gear][:3]+[Image.open(F/f'frames/{gear}/unload-north/005.png').convert('RGBA')]
 refs=[]
 for i,frame in enumerate(frames):
  dest=P/f'frames/{gear}/unload-north/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);frame.save(dest);refs.append('res://'+dest.relative_to(R).as_posix());bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest()
  if i in [0,1,2,6]:assert frame.tobytes()==Image.open(F/f'frames/{gear}/unload-north/{i if i<3 else 5:03}.png').convert('RGBA').tobytes();checks+=1
  display=case.copy() if i>=3 else Image.new('RGBA',(256,256));display.alpha_composite(frame);board.paste(display,(i*256,row*300+25),display);draw.text((i*256+3,row*300+4),gear+' / '+str(i),fill='white')
 data=json.loads((F/f'{gear}-manifest.json').read_text(encoding='utf-8'))
 for state in data['states']:
  if state['id']=='idle-north':state['frameFiles']=[refs[-1]];continue
  reverse=state['id']=='pickup-north';state.update(frameFiles=refs[::-1] if reverse else refs,frameDurationsMs=durations[::-1] if reverse else durations,frameCount=7,facings=['north']*7,waterKinds=['pickup' if reverse else 'unload']*7,waterPoses=[False]*7,depthOffsets=[0.0]*7)
 data.update(status='staged_rise_join_not_complete_idle_or_lifecycle',floorPropStudy={'canvas':'res://'+(P/'floor-case-canvas.png').relative_to(R).as_posix(),'displayUnloadIndices':[3,4,5,6],'displayPickupIndices':[0,1,2,3],'handoffSeconds':.26,'scope':'separate fixed prop after contact; lifecycle pending'})
 (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 for action,order,holds in [('unload',list(range(7)),durations),('pickup',list(reversed(range(7))),durations[::-1])]:
  previews=[]
  for i in order:
   bg=Image.new('RGBA',(256,256),'#202a30')
   if i>=3:bg.alpha_composite(case)
   bg.alpha_composite(frames[i]);previews.append(bg)
  out=P/f'{gear}-{action}-north.apng';previews[0].save(out,format='PNG',save_all=True,append_images=previews[1:],duration=holds,loop=1,disposal=0,blend=0)
  with Image.open(out) as decoded:
   assert decoded.n_frames==7;checks+=1
   for i,im in enumerate(previews):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes();assert decoded.info['duration']==holds[i];checks+=2
board.save(P/'paired-rise-join.png')
record={'checks':checks,'failures':0,'sourceDimensions':raw.size,'scale':scale,'ruler':'last authored standing148; one scale for all poses; exact original-master terminal reused','gutters':bounds,'rows':rows,'sourceSHA256':hashlib.sha256((P/'raw-rise-v1.png').read_bytes()).hexdigest(),'recipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'shellSHA256':hashlib.sha256(shellpath.read_bytes()).hexdigest(),'bindings':bindings,'timing':durations,'floorProp':'same fixed case from idle-join-v2, behind body from source3 onward','scope':'Whole authored rises/master endpoint. First3 sources reused; no production ownership/controller/adoption/cadence or complete idle acceptance.'}
(P/'registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0,'scale':scale,'rows':rows}))
