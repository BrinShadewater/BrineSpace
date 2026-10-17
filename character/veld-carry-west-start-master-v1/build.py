from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=Image.open(P/'raw-start-v1.png').convert('RGBA');a=np.array(raw);occupied=(a[:,:,3]>200).any(0);bounds=[0]
for i in range(1,4):
 nominal=round(i*raw.width/4);poss=np.where(~occupied[nominal-70:nominal+71])[0]+nominal-70;assert len(poss);bounds.append(int(poss[np.argmin(abs(poss-nominal))]))
bounds.append(raw.width);cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(4)];ys,xs=np.where(cells[0][:,:,3]>200);scale=148/(ys.max()-ys.min()+1)
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json';recipe=json.loads(recipepath.read_text(encoding='utf-8'));target=np.array(recipe['clothTargetRGB'])
shellpath=R/'character/veld-shared-helmet-v1/frames/idle-west/000.png';head=Image.open(shellpath).convert('RGBA').crop((64,14,108,60));ha=np.array(head);_,hx=np.where(ha[-5:,:,3]>160);gasketCenter=(hx.min()+hx.max())/2
new={'bare':[],'helmet':[]};rows=[];checks=0
for i,cell in enumerate(cells):
 lab,n=label(cell[:,:,3]>200);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==int(sizes.argmax());yy,xx=np.where(mask);floor=int(yy.max());_,bx=np.where(mask[floor-7:floor+1]);center=(bx.min()+bx.max())/2
 clean=cell.copy();clean[~binary_dilation(mask,iterations=2)]=0;source_rgb=clean[:,:,:3].astype(float);source_top=int(yy.min());head_mask=(clean[:,:,3]>200)&(source_rgb[:,:,0]-source_rgb[:,:,1]>8)&(source_rgb[:,:,0]-source_rgb[:,:,2]>15);head_mask[source_top+round(28/scale):]=False;_,head_x=np.where(head_mask);source_head_axis=(head_x.min()+head_x.max())/2;frame=Image.new('RGBA',(256,256));offset=(round(134-source_head_axis*scale),round(224-floor*scale));frame.alpha_composite(Image.fromarray(clean).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS),offset)
 old=np.array(frame);ar=old.copy();rgb=ar[:,:,:3].astype(float);fy,fx=np.where(ar[:,:,3]>200);top=int(fy.min())
 warm=(ar[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
 cloth=(ar[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False
 # Preserve equipment/grip surface rather than normalize visible area per pose.
 cloth[107:157,82:128]=False
 for ch in range(3):ar[cloth,ch]=np.interp(rgb[cloth].mean(1),recipe['clothKnots'],target[:,ch]).clip(0,255).astype('uint8')
 for material,select in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:ar[select,:3]=(rgb[select]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8')
 assert np.array_equal(ar[:,:,3],old[:,:,3]);assert np.array_equal(ar[107:157,82:128],old[107:157,82:128]);checks+=2
 b=Image.fromarray(ar);wy,wx=np.where(warm);htop=int(wy.min());axis=round((wx.min()+wx.max())/2);pos=(axis-23,htop-10);clear=(int(wx.min())-3,htop,int(wx.max())+4,htop+32)
 e=b.copy();e.paste((0,0,0,0),clear);e.alpha_composite(head,pos);ea=np.array(e);protected=np.ones(ar.shape[:2],bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+head.height),min(clear[0],pos[0]):max(clear[2],pos[0]+head.width)]=False
 assert np.array_equal(ea[protected],ar[protected]);checks+=1
 new['bare'].append(b);new['helmet'].append(e);(P/'ungraded').mkdir(exist_ok=True);frame.save(P/f'ungraded/{i:03}.png')
 _,headx=np.where(ar[top:top+20,:,3]>128);rows.append({'phase':i,'floor':floor,'bootCenter':float(center),'sourceHeadAxis':float(source_head_axis),'registration':'whole body translated to canonical held head axis134, physical boot floor224; leg swing width preserved','offset':offset,'nativeHeight':int(fy.max()-fy.min()+1),'headTop':top,'headWidthTop20':int(headx.max()-headx.min()+1),'shellPosition':pos,'edgePixels':int((cell[:,-1,3]>200).sum())})
durations=[80,80,80,80];board=Image.new('RGB',(1024,900),'#202a30');draw=ImageDraw.Draw(board);bindings={}
for row,gear in enumerate(['bare','helmet']):
 heldpath=R/f'character/veld-cargo-turns-master-family-v1/north-west-candidate-v4/frames/{gear}/005.png';stridepath=R/f'character/veld-carry-west-master-proportions-v1/frames/{gear}/000.png'
 frames=[Image.open(heldpath).convert('RGBA'),new[gear][1],new[gear][2],Image.open(stridepath).convert('RGBA')];refs=[]
 for i,f in enumerate(frames):
  dest=P/f'frames/{gear}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest);refs.append('res://'+dest.relative_to(R).as_posix());bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest();board.paste(f,(i*256,row*300+24),f);draw.text((i*256+3,row*300+4),gear+' / start '+str(i),fill='white')
 assert frames[0].tobytes()==Image.open(heldpath).convert('RGBA').tobytes();assert frames[3].tobytes()==Image.open(stridepath).convert('RGBA').tobytes();checks+=2
 # Whole generated first/final drawings are retained diagnostics; endpoint aliases rule.
 diagnostic=new[gear][0] if gear=='bare' else new[gear][3];board.paste(diagnostic,(row*256,624),diagnostic)
 data=json.loads((R/f'character/veld-carry-west-master-proportions-v1/{gear}-manifest.json').read_text(encoding='utf-8'));states=[]
 for st in data['states']:st['frameFiles']=['res://'+(R/f'character/veld-carry-west-master-proportions-v1/frames/{gear}/{i:03}.png').relative_to(R).as_posix() for i in range(st['frameCount'])]
 for action in ['start','stop']:
  states.append({'id':'carry-'+action+'-west','frameFiles':refs if action=='start' else refs[::-1],'frameDurationsMs':durations,'frameCount':4,'loop':False,'facings':['west']*4,'waterKinds':['carry']*4,'waterPoses':[False]*4,'depthOffsets':[0.0]*4})
 data.update(name='Veld West master carry start/stop '+gear,status='staged_no_controller_adoption',states=states+data['states']);(P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 for action,order in [('start',range(4)),('stop',reversed(range(4)))]:
  previews=[]
  for i in order:bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(frames[i]);previews.append(bg)
  out=P/f'{gear}-carry-{action}-west.apng';previews[0].save(out,format='PNG',save_all=True,append_images=previews[1:],duration=durations,loop=1,disposal=0,blend=0)
  with Image.open(out) as decoded:
   assert decoded.n_frames==4;checks+=1
   for i,f in enumerate(previews):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==f.tobytes();assert decoded.info['duration']==80;checks+=2
board.save(P/'paired-start-stop.png')
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceDimensions':raw.size,'scale':scale,'ruler':'one first standing148 source ruler, no pose height normalization','rows':rows,'gutters':bounds,'bindings':bindings,'caseGripProtectedBox':[82,107,128,157],'recipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'shellSource':shellpath.relative_to(R).as_posix(),'shellCrop':[64,14,108,60],'shellScale':1,'sourceSHA256':hashlib.sha256((P/'raw-start-v1.png').read_bytes()).hexdigest(),'scope':'Whole authored small steps, exact held and carry0 endpoints, staged finite320start/reversed stop. No controller travel/phase/adoption/full cadence or original-master complete-library acceptance.'},indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0,'scale':scale,'rows':rows}))
