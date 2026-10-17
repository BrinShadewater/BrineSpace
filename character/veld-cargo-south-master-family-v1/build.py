from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1]
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json'
recipe=json.loads(recipepath.read_text(encoding='utf-8'));targets=np.array(recipe['clothTargetRGB'])
shellpath=R/'character/veld-shared-helmet-south-v1/fitted-helmet.png'
shell=Image.open(shellpath).convert('RGBA');sa=np.array(shell);_,sx=np.where(sa[-5:,:,3]>160);gasket=(sx.min()+sx.max())/2
checks=0;fits=[];grades=[]
def fit_helmet(body,slot):
 global checks
 a=np.array(body);y,x=np.where(a[:,:,3]>200);top=int(y.min());_,hx=np.where(a[top:top+16,:,3]>128);axis=(hx.min()+hx.max())/2
 pos=(round(axis-gasket),top+31-shell.height);clear=(int(hx.min())-3,top,int(hx.max())+4,top+24)
 e=body.copy();e.paste((0,0,0,0),clear);e.alpha_composite(shell,pos)
 protected=np.ones((256,256),bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+shell.height),min(clear[0],pos[0]):max(clear[2],pos[0]+shell.width)]=False
 assert np.array_equal(np.array(e)[protected],a[protected]);checks+=1
 fits.append({'phase':slot,'position':pos,'clearBox':clear,'headBand':16,'shellScale':1,'shellGradeChanged':False});return e
held=R/'character/veld-cargo-turns-master-family-v1/candidate-v7'
images={gear:[Image.open(held/f'frames/{gear}/000.png').convert('RGBA')] for gear in ['bare','helmet']}
protect_boxes={1:(95,165,161,195),2:(103,192,153,227)}
for slot in range(1,6):
 old=np.array(Image.open(P/f'ungraded-unload/{slot:03}.png').convert('RGBA'));a=old.copy();rgb=a[:,:,:3].astype(float);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min())
 warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+20:]=False
 cloth=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+24]=False
 protect=protect_boxes.get(slot);changed=cloth.copy()
 if protect:
  x0,y0,x1,y1=protect;cloth[y0:y1,x0:x1]=False;changed=cloth.copy()
 for ch in range(3):a[cloth,ch]=np.interp(rgb[cloth].mean(1),recipe['clothKnots'],targets[:,ch]).clip(0,255).astype('uint8')
 for material,mask in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:
  a[mask,:3]=(rgb[mask]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8');changed|=mask
 assert np.array_equal(a[:,:,3],old[:,:,3]);assert np.array_equal(a[~changed],old[~changed]);checks+=2
 if protect:assert np.array_equal(a[y0:y1,x0:x1],old[y0:y1,x0:x1]);checks+=1
 body=Image.fromarray(a);images['bare'].append(body);images['helmet'].append(fit_helmet(body,slot));grades.append({'phase':slot,'protectedCaseGripBox':protect,'clothPixels':int(cloth.sum())})
idle=Image.open(P/'original-master-idle.png').convert('RGBA');images['bare'].append(idle);images['helmet'].append(fit_helmet(idle,6))
case=Image.open(P/'floor-case.png').convert('RGBA');assert case.size==(33,24)
case_position=(112,199);canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(case,case_position);canvas.save(P/'floor-case-canvas.png')
durations=[70,90,100,60,65,65,70];assert sum(durations)==520
board=Image.new('RGB',(1792,600),'#202a30');draw=ImageDraw.Draw(board);bindings={}
for row,gear in enumerate(['bare','helmet']):
 refs=[]
 for slot,body in enumerate(images[gear]):
  path=P/f'frames/{gear}/unload-south/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);body.save(path);refs.append('res://'+path.relative_to(R).as_posix());bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
  a=np.array(body);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
  display=body.copy()
  if slot>=3:display.alpha_composite(canvas)
  board.paste(display,(slot*256,row*300+25),display);draw.text((slot*256+3,row*300+4),gear+' / unload '+str(slot),fill='white')
 assert images[gear][0].tobytes()==Image.open(held/f'frames/{gear}/000.png').convert('RGBA').tobytes();checks+=1
 if gear=='bare':assert images[gear][-1].tobytes()==idle.tobytes();checks+=1
 data=json.loads((R/f'character/veld-carry-south-master-proportions-v1/{gear}-manifest.json').read_text(encoding='utf-8'));states=[]
 for action in ['unload','pickup']:
  reverse=action=='pickup';states.append({'id':action+'-south','frameFiles':refs[::-1] if reverse else refs,'frameCount':7,'frameDurationsMs':durations[::-1] if reverse else durations,'loop':False,'facings':['south']*7,'waterKinds':[action]*7,'waterPoses':[False]*7,'depthOffsets':[0.0]*7})
 states.append({'id':'idle-south','frameFiles':[refs[-1]],'frameCount':1,'frameDurationsMs':[1000],'loop':False,'facings':['south'],'waterKinds':['idle'],'waterPoses':[False],'depthOffsets':[0.0]})
 data.update(name='Veld South master cargo family '+gear,status='staged_not_complete_idle_or_lifecycle',states=states+data['states'],floorPropStudy={'canvas':'res://'+(P/'floor-case-canvas.png').relative_to(R).as_posix(),'displayUnloadIndices':[3,4,5,6],'displayPickupIndices':[0,1,2,3],'handoffSeconds':.26,'scope':'fixed independent case in front of body after authored release, not production ownership/lifetime'})
 (P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 for action,order,holds in [('unload',list(range(7)),durations),('pickup',list(reversed(range(7))),durations[::-1])]:
  previews=[]
  for slot in order:
   bg=Image.new('RGBA',(256,256),'#202a30')
   bg.alpha_composite(images[gear][slot])
   if slot>=3:bg.alpha_composite(canvas)
   previews.append(bg)
  out=P/f'{gear}-{action}-south.apng';previews[0].save(out,format='PNG',save_all=True,append_images=previews[1:],duration=holds,loop=1,disposal=0,blend=0)
  with Image.open(out) as decoded:
   assert decoded.n_frames==7;checks+=1
   for i,frame in enumerate(previews):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==frame.tobytes();assert decoded.info['duration']==holds[i];checks+=2
board.save(P/'paired-master-cargo.png')
record={'checks':checks,'failures':0,'extraction':json.loads((P/'extraction.json').read_text(encoding='utf-8')),'fits':fits,'grade':grades,'shellSource':shellpath.relative_to(R).as_posix(),'shellDimensions':shell.size,'shellSHA256':hashlib.sha256(shellpath.read_bytes()).hexdigest(),'recipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'bindings':bindings,'casePosition':case_position,'caseDimensions':case.size,'timing':durations,'scope':'Whole authored unload/pickup, exact held and original bare idle endpoints, fixed independent case. No world/controller/normal adoption/ownership/save/full cadence or complete idle acceptance.'}
(P/'registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0,'fits':fits,'casePosition':case_position}))
