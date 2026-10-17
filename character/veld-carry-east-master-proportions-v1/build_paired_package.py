"""Staged exact body sources and unchanged original East helmet component."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'whole-pose-join-v4/material-review/case-review-v2';O=P/'paired-package-v1';O.mkdir(exist_ok=True)
originalpath=R/'character/veld-carry-east-consistent-v1/bare-manifest.json';original=json.loads(originalpath.read_text());source=R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png'
componentBox=(82,17,116,55);head=Image.open(source).convert('RGBA').crop(componentBox);ha=np.array(head);_,hx=np.where(ha[-5:,:,3]>160);gasketCenter=(hx.min()+hx.max())/2
board=Image.new('RGB',(1536,820),'#202a30');d=ImageDraw.Draw(board);fits=[];bindings={};checks=0;gears={'bare':[],'helmet':[]}
for i in range(6):
 src=S/f'{i:03}.png';b=Image.open(src).convert('RGBA');a=np.array(b);rgb=a[:,:,:3].astype(float)
 warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[110:]=False;yy,xx=np.where(warm)
 top=int(yy.min());axis=round((xx.min()+xx.max())/2);gasket=top+27;pos=(round(axis-gasketCenter),gasket-head.height)
 clear=(int(xx.min())-3,top,int(xx.max())+4,top+25);body=b.copy();body.paste((0,0,0,0),clear);e=body.copy();e.alpha_composite(head,pos);ea=np.array(e)
 protected=np.ones(a.shape[:2],bool);protected[min(clear[1],pos[1]):max(clear[3],pos[1]+head.height),min(clear[0],pos[0]):max(clear[2],pos[0]+head.width)]=False
 assert np.array_equal(ea[protected],a[protected]);checks+=1
 assert np.array_equal(ea[110:],a[110:]);checks+=1
 # Exact original opaque helmet pixels; translucent edge blends with the preserved body where appropriate.
 patch=ea[pos[1]:pos[1]+head.height,pos[0]:pos[0]+head.width];assert np.array_equal(patch[ha[:,:,3]==255],ha[ha[:,:,3]==255]);checks+=1
 fits.append({'phase':i,'warmHeadTop':top,'warmHeadAxis':axis,'bodyClearBox':clear,'position':pos,'gasketBottom':gasket,'componentBox':componentBox,'componentScale':1,'componentGradeChanged':False,'sourceBareSHA256':hashlib.sha256(src.read_bytes()).hexdigest()})
 for row,(gear,f) in enumerate([('bare',b),('helmet',e)]):
  folder=O/'frames'/gear;folder.mkdir(parents=True,exist_ok=True);path=folder/f'{i:03}.png';f.save(path);gears[gear].append(f)
  bindings[path.relative_to(O).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest();fa=np.array(f)
  assert not np.any(np.concatenate([fa[0,:,3],fa[-1,:,3],fa[:,0,3],fa[:,-1,3]])>20);checks+=1
  if gear=='bare':assert np.array_equal(fa,a);checks+=1
  board.paste(f,(i*256,row*280+24),f);d.text((i*256+6,row*280+4),gear+' phase '+str(i),fill='white')
 detail=e.crop((94,65,162,116)).resize((240,180),Image.Resampling.NEAREST);board.paste(detail,(i*256+8,600),detail)
for gear,frames in gears.items():
 data=json.loads(json.dumps(original));data.update(name='Veld East master carry '+gear,status='staged_not_installed');data['states'][0]['frameFiles']=['res://'+(O/'frames'/gear/f'{i:03}.png').relative_to(R).as_posix() for i in range(6)]
 (O/f'{gear}-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 previews=[]
 for f in frames:
  bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(f);previews.append(bg)
 previews[0].save(O/f'{gear}-cycle.png',save_all=True,append_images=previews[1:],duration=data['states'][0]['frameDurationsMs'],loop=0,disposal=0,blend=0)
 decoded=Image.open(O/f'{gear}-cycle.png');assert decoded.n_frames==6;checks+=1
 for i,f in enumerate(previews):
  decoded.seek(i);assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(f));checks+=1
  assert decoded.info['duration']==140;checks+=1
board.save(O/'paired-master-contact.png')
(O/'package-registration.json').write_text(json.dumps({'status':'staged_not_installed','scope':'Exact revised body and unchanged shared East shell; original metadata retained. Source fitting only, no native/world/adoption acceptance.','originalManifest':originalpath.relative_to(R).as_posix(),'originalManifestSHA256':hashlib.sha256(originalpath.read_bytes()).hexdigest(),'bareSourceDirectory':S.relative_to(R).as_posix(),'helmetSource':source.relative_to(R).as_posix(),'helmetSourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'helmetComponentBox':componentBox,'helmetComponentScale':1,'helmetFits':fits,'sourceBindings':bindings,'checks':checks,'failures':0,'visualReview':'pending'},indent=2)+'\n',encoding='utf-8')
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld East paired master carry</title><style>body{background:#202a30;color:#dce5e8;font:18px system-ui;margin:28px}img{max-width:100%}.motion{width:512px;image-rendering:pixelated}</style><h1>Veld East carry — master helmet pairing</h1><p>Same body and case, original shared helmet. Alignment and native motion remain under review.</p><img class="motion" src="bare-cycle.png"><img class="motion" src="helmet-cycle.png"><img src="paired-master-contact.png">''',encoding='utf-8')
print(json.dumps({'pairedFrames':12,'checks':checks,'failures':0,'helmetPositions':[f['position'] for f in fits],'cycleMs':840,'standingHeight':data['standingHeight'],'stride':data['strideDistanceCells']}))
