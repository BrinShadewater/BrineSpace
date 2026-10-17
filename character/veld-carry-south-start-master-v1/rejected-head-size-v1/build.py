from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=Image.open(P/'raw-start-v1.png').convert('RGBA');a=np.array(raw)
source_labels,n=label(a[:,:,3]>200);areas=np.bincount(source_labels.ravel());areas[0]=0;ids=np.argsort(areas)[-4:];boxes=[]
for identity in ids:
 yy,xx=np.where(source_labels==identity);assert len(yy)>10000;boxes.append((int(xx.min()),int(xx.max())))
boxes.sort();bounds=[0]+[round((boxes[i][1]+boxes[i+1][0])/2) for i in range(3)]+[raw.width]
cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(4)]
for cell in cells:assert not np.any(cell[:,[0,-1],3]>20),'Whole figures need alpha gutters'
ys,xs=np.where(cells[0][:,:,3]>200);scale=148/(ys.max()-ys.min()+1);floor=int(ys.max());offset_y=round(224-floor*scale)
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json';recipe=json.loads(recipepath.read_text(encoding='utf-8'));target=np.array(recipe['clothTargetRGB'])
shellpath=R/'character/veld-shared-helmet-south-v1/fitted-helmet.png';shell=Image.open(shellpath).convert('RGBA');ha=np.array(shell);_,hx=np.where(ha[-5:,:,3]>160);gasket=(hx.min()+hx.max())/2
images={'bare':[],'helmet':[]};rows=[];checks=0
for i,cell in enumerate(cells):
 lab,n=label(cell[:,:,3]>200);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==int(sizes.argmax());yy,xx=np.where(mask)
 clean=cell.copy();clean[~binary_dilation(mask,iterations=2)]=0;rgb=clean[:,:,:3].astype(float);top=int(yy.min());warm=(clean[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+round(28/scale):]=False;_,head_x=np.where(mask[top:top+round(20/scale)]);head_axis=(head_x.min()+head_x.max())/2
 frame=Image.new('RGBA',(256,256));offset=(round(128-head_axis*scale),offset_y);frame.alpha_composite(Image.fromarray(clean).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS),offset)
 old=np.array(frame);ar=old.copy();rgb=ar[:,:,:3].astype(float);fy,fx=np.where(ar[:,:,3]>200);top=int(fy.min())
 warm=(ar[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
 cloth=(ar[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False;cloth[110:166,95:162]=False
 for ch in range(3):ar[cloth,ch]=np.interp(rgb[cloth].mean(1),recipe['clothKnots'],target[:,ch]).clip(0,255).astype('uint8')
 for material,select in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:ar[select,:3]=(rgb[select]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8')
 assert np.array_equal(ar[:,:,3],old[:,:,3]);assert np.array_equal(ar[110:166,95:162],old[110:166,95:162]);checks+=2
 bare=Image.fromarray(ar);wy,wx=np.where(warm);htop=int(wy.min());_,skull_x=np.where(ar[top:top+20,:,3]>128);axis=(skull_x.min()+skull_x.max())/2;position=(111,top+31-shell.height);clear=(int(wx.min())-3,htop,int(wx.max())+4,htop+25)
 equipped=bare.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(shell,position);ea=np.array(equipped);protected=np.ones((256,256),bool);protected[min(clear[1],position[1]):max(clear[3],position[1]+shell.height),min(clear[0],position[0]):max(clear[2],position[0]+shell.width)]=False
 assert np.array_equal(ea[protected],ar[protected]);checks+=1
 for im in [bare,equipped]:
  v=np.array(im);assert not np.any(np.concatenate([v[0,:,3],v[-1,:,3],v[:,0,3],v[:,-1,3]])>20);checks+=1
 images['bare'].append(bare);images['helmet'].append(equipped);(P/'ungraded').mkdir(exist_ok=True);frame.save(P/f'ungraded/{i:03}.png')
 _,headx=np.where(ar[top:top+20,:,3]>128)
 rows.append({'phase':i,'offset':offset,'nativeHeight':int(fy.max()-fy.min()+1),'headTop':top,'headWidthTop20':int(headx.max()-headx.min()+1),'sourceHeadAxis':float(head_axis),'shellPosition':position,'gutterEdgeOpaque':int((cell[:,-1,3]>200).sum())})

durations=[80]*4
board=Image.new('RGB',(1024,900),'#202a30');draw=ImageDraw.Draw(board);bindings={}
for row,gear in enumerate(['bare','helmet']):
 heldpath=R/f'character/veld-cargo-turns-master-family-v1/candidate-v7/frames/{gear}/000.png';stridepath=R/f'character/veld-carry-south-master-proportions-v1/frames/{gear}/000.png'
 frames=[Image.open(heldpath).convert('RGBA'),images[gear][1],images[gear][2],Image.open(stridepath).convert('RGBA')];refs=[]
 for i,f in enumerate(frames):
  dest=P/f'frames/{gear}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);f.save(dest);refs.append('res://'+dest.relative_to(R).as_posix());bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest();board.paste(f,(i*256,row*300+24),f);draw.text((i*256+3,row*300+4),gear+' / start '+str(i),fill='white')
 assert frames[0].tobytes()==Image.open(heldpath).convert('RGBA').tobytes();assert frames[3].tobytes()==Image.open(stridepath).convert('RGBA').tobytes();checks+=2
 # Whole generated first/final drawings are retained diagnostics; endpoint aliases rule.
 diagnostic=images[gear][0] if gear=='bare' else images[gear][3];board.paste(diagnostic,(row*256,624),diagnostic)
 data=json.loads((R/f'character/veld-carry-south-master-proportions-v1/{gear}-manifest.json').read_text(encoding='utf-8'));states=[]
 for st in data['states']:st['frameFiles']=['res://'+(R/f'character/veld-carry-south-master-proportions-v1/frames/{gear}/{i:03}.png').relative_to(R).as_posix() for i in range(st['frameCount'])]
 for action in ['start','stop']:
  states.append({'id':'carry-'+action+'-south','frameFiles':refs if action=='start' else refs[::-1],'frameDurationsMs':durations,'frameCount':4,'loop':False,'facings':['south']*4,'waterKinds':['carry']*4,'waterPoses':[False]*4,'depthOffsets':[0.0]*4})
 data.update(name='Veld South master carry start/stop '+gear,status='staged_no_controller_adoption',states=states+data['states']);(P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 for action,order in [('start',range(4)),('stop',reversed(range(4)))]:
  previews=[]
  for i in order:bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(frames[i]);previews.append(bg)
  out=P/f'{gear}-carry-{action}-south.apng';previews[0].save(out,format='PNG',save_all=True,append_images=previews[1:],duration=durations,loop=1,disposal=0,blend=0)
  with Image.open(out) as decoded:
   assert decoded.n_frames==4;checks+=1
   for i,f in enumerate(previews):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==f.tobytes();assert decoded.info['duration']==80;checks+=2
board.save(P/'paired-start-stop.png')
(P/'registration.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceDimensions':raw.size,'scale':scale,'ruler':'one first standing148 source ruler/global source boot floor, skull axis128, no per-pose scale','rows':rows,'gutters':bounds,'bindings':bindings,'caseGripProtectedBox':[95,110,162,166],'recipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'shellSource':shellpath.relative_to(R).as_posix(),'shellDimensions':shell.size,'shellScale':1,'sourceSHA256':hashlib.sha256((P/'raw-start-v1.png').read_bytes()).hexdigest(),'scope':'Whole authored small steps, exact held and carry0 endpoints, staged finite320start/reversed stop. No controller travel/phase/adoption/full cadence or original-master complete-library acceptance.'},indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0,'scale':scale,'rows':rows}))
