from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
raw=Image.open(P/'raw-v1.png').convert('RGBA');a=np.array(raw);occupied=(a[:,:,3]>200).any(0);bounds=[0]
for i in range(1,6):
 nominal=round(i*raw.width/6);poss=np.where(~occupied[nominal-40:nominal+41])[0]+nominal-40;assert len(poss);bounds.append(int(poss[np.argmin(abs(poss-nominal))]))
bounds.append(raw.width);cells=[a[:,bounds[i]:bounds[i+1]].copy() for i in range(6)];ys,xs=np.where(cells[0][:,:,3]>200);scale=148/(ys.max()-ys.min()+1);floor=int(ys.max());offset_y=round(224-floor*scale)
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json';recipe=json.loads(recipepath.read_text(encoding='utf-8'));target=np.array(recipe['clothTargetRGB'])
shellpath=R/'character/veld-shared-helmet-v1/fitted-north.png';shell=Image.open(shellpath).convert('RGBA');ha=np.array(shell);_,hx=np.where(ha[-5:,:,3]>160);gasket=(hx.min()+hx.max())/2
images={'bare':[],'helmet':[]};rows=[];checks=0
for i,cell in enumerate(cells):
 lab,n=label(cell[:,:,3]>200);sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==int(sizes.argmax());yy,xx=np.where(mask)
 clean=cell.copy();clean[~binary_dilation(mask,iterations=2)]=0;rgb=clean[:,:,:3].astype(float);top=int(yy.min());warm=(clean[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+round(28/scale):]=False;_,head_x=np.where(warm);head_axis=(head_x.min()+head_x.max())/2
 frame=Image.new('RGBA',(256,256));offset=(round(128-head_axis*scale),offset_y);frame.alpha_composite(Image.fromarray(clean).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS),offset)
 old=np.array(frame);ar=old.copy();rgb=ar[:,:,:3].astype(float);fy,fx=np.where(ar[:,:,3]>200);top=int(fy.min())
 warm=(ar[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
 cloth=(ar[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False;cloth[116:153,103:155]=False
 for ch in range(3):ar[cloth,ch]=np.interp(rgb[cloth].mean(1),recipe['clothKnots'],target[:,ch]).clip(0,255).astype('uint8')
 for material,select in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:ar[select,:3]=(rgb[select]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8')
 assert np.array_equal(ar[:,:,3],old[:,:,3]);assert np.array_equal(ar[116:153,103:155],old[116:153,103:155]);checks+=2
 bare=Image.fromarray(ar);wy,wx=np.where(warm);htop=int(wy.min());_,skull_x=np.where(ar[top:top+20,:,3]>128);axis=(skull_x.min()+skull_x.max())/2;position=(round(axis-gasket),top+27-shell.height);clear=(int(wx.min())-3,htop,int(wx.max())+4,htop+25)
 equipped=bare.copy();equipped.paste((0,0,0,0),clear);equipped.alpha_composite(shell,position);ea=np.array(equipped);protected=np.ones((256,256),bool);protected[min(clear[1],position[1]):max(clear[3],position[1]+shell.height),min(clear[0],position[0]):max(clear[2],position[0]+shell.width)]=False
 assert np.array_equal(ea[protected],ar[protected]);checks+=1
 for im in [bare,equipped]:
  v=np.array(im);assert not np.any(np.concatenate([v[0,:,3],v[-1,:,3],v[:,0,3],v[:,-1,3]])>20);checks+=1
 images['bare'].append(bare);images['helmet'].append(equipped);(P/'ungraded').mkdir(exist_ok=True);frame.save(P/f'ungraded/{i:03}.png')
 _,headx=np.where(ar[top:top+20,:,3]>128)
 rows.append({'phase':i,'offset':offset,'nativeHeight':int(fy.max()-fy.min()+1),'headTop':top,'headWidthTop20':int(headx.max()-headx.min()+1),'sourceHeadAxis':float(head_axis),'shellPosition':position,'gutterEdgeOpaque':int((cell[:,-1,3]>200).sum())})
board=Image.new('RGB',(1536,840),'#202a30');draw=ImageDraw.Draw(board);bindings={};durations=[140]*6
for row,gear in enumerate(['bare','helmet']):
 refs=[]
 for i,im in enumerate(images[gear]):
  dest=P/f'frames/{gear}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);im.save(dest);refs.append('res://'+dest.relative_to(R).as_posix());bindings[dest.relative_to(R).as_posix()]=hashlib.sha256(dest.read_bytes()).hexdigest();board.paste(im,(i*256,row*280+22),im);draw.text((i*256+4,row*280+3),gear+' North walk '+str(i+1),fill='white')
 data=json.loads((R/f'character/veld-carry-north-consistent-v1/{gear}-manifest.json').read_text(encoding='utf-8'));data.update(name='Veld North master proportions '+gear,status='staged_not_installed');data['states'][0].update(frameFiles=refs,frameCount=6,frameDurationsMs=durations,loop=True);(P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 previews=[]
 for im in images[gear]:bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(im);previews.append(bg)
 out=P/f'{gear}-carry-north.apng';previews[0].save(out,format='PNG',save_all=True,append_images=previews[1:],duration=durations,loop=0,disposal=0,blend=0)
 with Image.open(out) as decoded:
  assert decoded.n_frames==6;checks+=1
  for i,im in enumerate(previews):decoded.seek(i);assert decoded.convert('RGBA').tobytes()==im.tobytes();assert decoded.info['duration']==140;checks+=2
 master=Image.open(R/f'character/veld-cargo-turns-master-family-v1/north-west-candidate-v4/frames/{gear}/000.png').convert('RGBA')
 for i in range(3):board.paste(master,((i+row*3)*256,583),master);draw.text(((i+row*3)*256+3,562),'Canonical North held - '+gear,fill='white')
board.save(P/'paired-master-contact.png')
record={'checks':checks,'failures':0,'sourceDimensions':raw.size,'scale':scale,'ruler':'one first contact148 reference ruler; one scale/global boot floor for entire source row, no pose height forcing','globalSourceFloor':floor,'gutters':bounds,'rows':rows,'bindings':bindings,'sourceSHA256':hashlib.sha256((P/'raw-v1.png').read_bytes()).hexdigest(),'recipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'shellSource':shellpath.relative_to(R).as_posix(),'shellSHA256':hashlib.sha256(shellpath.read_bytes()).hexdigest(),'shellDimensions':shell.size,'shellScale':1,'cycleMs':840,'strideDistanceCells':data['strideDistanceCells'],'scope':'Whole authored straight North gait, unchanged original shell/shared material recipe; no starts/stops, normal adoption, room or full cadence acceptance.'}
(P/'registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps({'checks':checks,'failures':0,'scale':scale,'rows':rows}))
