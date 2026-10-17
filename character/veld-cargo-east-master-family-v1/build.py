"""Staged whole authored East actions, canonical endpoints and fixed-size original helmet."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];C=R/'character/veld-carry-east-master-proportions-v1/paired-package-v1';H=R/'character/veld-cargo-turns-master-family-v1/north-east-candidate-v5'
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json';recipe=json.loads(recipepath.read_text());knots=recipe['clothKnots'];targets=np.array(recipe['clothTargetRGB'])
headpath=R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png';head=Image.open(headpath).convert('RGBA').crop((82,17,116,55));ha=np.array(head);_,hx=np.where(ha[-5:,:,3]>160);gasketX=(hx.min()+hx.max())/2
bare=[Image.open(H/'frames/bare/005.png').convert('RGBA')];helmet=[Image.open(H/'frames/helmet/005.png').convert('RGBA')];fits=[{'phase':0,'wholeCanonicalHeldAlias':True}];grade=[];checks=0
# Conservative authored case/grip contexts; no generated anatomy fragments or per-pose grade normalization.
protectedBoxes={1:(132,130,180,171),2:(133,164,184,202),3:(137,190,189,230),4:(143,193,187,230)}
for i in range(1,5):
 path=P/f'ungraded-unload/{i:03}.png';a=np.array(Image.open(path).convert('RGBA'));old=a.copy();rgb=a[:,:,:3].astype(float);yy,xx=np.where(a[:,:,3]>200);top=int(yy.min())
 warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
 cloth=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False
 x0,y0,x1,y1=protectedBoxes[i];cloth[y0:y1,x0:x1]=False
 for ch in range(3):a[cloth,ch]=np.interp(rgb[cloth].mean(1),knots,targets[:,ch]).clip(0,255).astype('uint8')
 changed=cloth.copy()
 for material,mask in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:a[mask,:3]=(rgb[mask]+np.array(recipe['skinHairFixedRGBOffsets'][material])).clip(0,255).astype('uint8');changed|=mask
 assert np.array_equal(a[:,:,3],old[:,:,3]);checks+=1;assert np.array_equal(a[~changed],old[~changed]);checks+=1;assert np.array_equal(a[y0:y1,x0:x1],old[y0:y1,x0:x1]);checks+=1
 b=Image.fromarray(a);bare.append(b);wy,wx=np.where(warm);htop=int(wy.min());axis=round((wx.min()+wx.max())/2);angle={1:-6,2:-12,3:-16,4:-6}[i]
 component=head.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True);theta=math.radians(angle);dx=gasketX-head.width/2;dy=head.height-head.height/2
 anchor=(component.width/2+math.cos(theta)*dx+math.sin(theta)*dy,component.height/2-math.sin(theta)*dx+math.cos(theta)*dy)
 pos=(round(axis-anchor[0]),round(htop+27-anchor[1]));clear=(int(wx.min())-3,htop,int(wx.max())+4,htop+25)
 body=b.copy();body.paste((0,0,0,0),clear);e=body.copy();e.alpha_composite(component,pos);ea=np.array(e)
 protected=np.ones(a.shape[:2],bool);protected[min(pos[1],clear[1]):max(pos[1]+component.height,clear[3]),min(pos[0],clear[0]):max(pos[0]+component.width,clear[2])]=False
 assert np.array_equal(ea[protected],a[protected]);checks+=1;helmet.append(e)
 fits.append({'phase':i,'position':pos,'clearBox':clear,'rigidAngleDegrees':angle,'componentSize':component.size,'componentScale':1,'rotatedGasketAnchor':anchor,'bodyGasketAnchor':[axis,htop+27],'componentGradeChanged':False})
 grade.append({'phase':i,'sourceSHA256':hashlib.sha256(path.read_bytes()).hexdigest(),'protectedCaseGripBox':protectedBoxes[i],'clothPixels':int(cloth.sum()),'warmHeadPixels':int(warm.sum())})
casepath=P/'floor-case.png';case=Image.open(casepath).convert('RGBA');casepos=(149,200)
for frames in [bare,helmet]:frames[4].alpha_composite(case,casepos)
idlepaths={'bare':R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png','helmet':headpath}
for gear,frames in [('bare',bare),('helmet',helmet)]:
 final=Image.new('RGBA',(256,256));final.alpha_composite(Image.open(idlepaths[gear]).convert('RGBA'),(36,52));final.alpha_composite(case,casepos);frames.append(final)
fits.append({'phase':5,'exactOriginalIdleBodyUnderForegroundCase':True})
bindings={};board=Image.new('RGB',(1536,860),'#202a30');d=ImageDraw.Draw(board)
for row,(gear,frames) in enumerate([('bare',bare),('helmet',helmet)]):
 paths=[]
 for i,f in enumerate(frames):
  path=P/'frames'/gear/'unload-east'/f'{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);f.save(path);ref='res://'+path.relative_to(R).as_posix();paths.append(ref);bindings[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
  a=np.array(f);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1;board.paste(f,(i*256,row*290+24),f);d.text((i*256+5,row*290+5),gear+' unload '+str(i),fill='white')
  if gear=='helmet':detail=f.crop((80,65,179,168)).resize((248,230),Image.Resampling.NEAREST);board.paste(detail,(i*256+4,620),detail)
 data=json.loads((C/f'{gear}-manifest.json').read_text());carry=data['states'][0];unload=json.loads((R/'character/veld-unload-east-consistent-v1/original-state.json').read_text());unload.update(frameFiles=paths,frameCount=6)
 pickup=json.loads((R/'character/veld-pickup-east-consistent-v1/original-state.json').read_text());pickup.update(frameFiles=list(reversed(paths)),frameCount=6)
 data.update(name='Veld East master cargo family '+gear,status='staged_not_installed',states=[carry,unload,pickup]);(P/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 for state,images in [(unload,frames),(pickup,list(reversed(frames)))]:
  previews=[]
  for f in images:bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(f);previews.append(bg)
  previews[0].save(P/f"{gear}-{state['id']}.apng",format='PNG',save_all=True,append_images=previews[1:],duration=state['frameDurationsMs'],loop=1,disposal=0,blend=0)
  decoded=Image.open(P/f"{gear}-{state['id']}.apng");assert decoded.n_frames==6;checks+=1
  for i,f in enumerate(previews):decoded.seek(i);assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(f));assert decoded.info['duration']==state['frameDurationsMs'][i];checks+=2
board.save(P/'paired-unload-contact.png')
record={'status':'staged_not_installed','source':'raw-unload-v1.png','sourceSHA256':hashlib.sha256((P/'raw-unload-v1.png').read_bytes()).hexdigest(),'sharedMaterialRecipe':recipepath.relative_to(R).as_posix(),'sharedMaterialRecipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'grades':grade,'helmetSource':headpath.relative_to(R).as_posix(),'helmetSourceSHA256':hashlib.sha256(headpath.read_bytes()).hexdigest(),'helmetFits':fits,'floorCaseSource':casepath.name,'floorCasePosition':casepos,'fixedFloorCaseAfterRelease':[4,5],'heldAliasDirectory':H.relative_to(R).as_posix(),'exactOriginalIdleBodyUnderForegroundProp':True,'pickupReverseAliases':[5,4,3,2,1,0],'newFrameBindings':bindings,'checks':checks,'failures':0,'visualReview':'pending','scope':'Whole authored action interiors, exact canonical held/idle endpoints, common recipe and rigid existing helmet. Contact case geometry and full cadence/native/world ownership/normal adoption pending.'}
(P/'family-registration.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
(P/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld East master cargo actions</title><style>body{background:#202a30;color:#dce5e8;font:18px system-ui;margin:28px}img{max-width:100%}.motion{width:512px;image-rendering:pixelated}</style><h1>Veld East — matched cargo actions</h1><p>Staged pickup and unload with master identity and shared helmet. Contact, native motion and gameplay remain under review.</p><h2>Unload</h2><img class="motion" src="bare-unload-east.apng"><img class="motion" src="helmet-unload-east.apng"><h2>Pickup</h2><img class="motion" src="bare-pickup-east.apng"><img class="motion" src="helmet-pickup-east.apng"><h2>All poses</h2><img src="paired-unload-contact.png">''',encoding='utf-8')
print(json.dumps({'pairedStates':6,'newExports':12,'checks':checks,'failures':0,'casePosition':casepos,'helmetFits':fits,'scope':'staged source only'}))
