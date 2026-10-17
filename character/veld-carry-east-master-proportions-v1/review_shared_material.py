"""One existing master-derived grade; never normalizes each frame separately."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];S=P/'whole-pose-join-v4';O=S/'material-review';O.mkdir(exist_ok=True)
recipepath=R/'character/veld-carry-west-master-proportions-v1/package-registration.json'
recipe=json.loads(recipepath.read_text(encoding='utf-8'));knots=np.array(recipe['clothKnots']);target=np.array(recipe['clothTargetRGB'])
frames=[];records=[];checks=0
for i in range(6):
 source=S/f'{i:03}.png';original=np.array(Image.open(source).convert('RGBA'));a=original.copy();rgb=a[:,:,:3].astype(float)
 ys,xs=np.where(a[:,:,3]>200);top=int(ys.min())
 warm=(a[:,:,3]>200)&(rgb[:,:,0]-rgb[:,:,1]>8)&(rgb[:,:,0]-rgb[:,:,2]>15);warm[top+28:]=False
 cloth=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<24)&(rgb.mean(2)>15)&(rgb.mean(2)<125);cloth[:top+28]=False;cloth[110:160]=False
 for ch in range(3):a[cloth,ch]=np.interp(rgb[cloth].mean(1),knots,target[:,ch]).clip(0,255).astype('uint8')
 changed=cloth.copy()
 for name,mask in [('skin',warm&(rgb.mean(2)>85)),('hair',warm&(rgb.mean(2)<=85))]:
  a[mask,:3]=(rgb[mask]+np.array(recipe['skinHairFixedRGBOffsets'][name])).clip(0,255).astype('uint8');changed|=mask
 assert np.array_equal(a[:,:,3],original[:,:,3]);checks+=1
 assert np.array_equal(a[110:160],original[110:160]);checks+=1
 assert np.array_equal(a[~changed],original[~changed]);checks+=1
 im=Image.fromarray(a);im.save(O/f'{i:03}.png');frames.append(im)
 _,hx=np.where(a[ys.min():ys.min()+20,:,3]>128)
 records.append({'phase':i,'sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'gradedSHA256':hashlib.sha256((O/f'{i:03}.png').read_bytes()).hexdigest(),'headTop20Width':int(hx.max()-hx.min()+1),'clothPixels':int(cloth.sum()),'headWarmPixels':int(warm.sum())})
originalpath=R/'character/veld-side-foundation-v1/east-standing.png';heldpath=R/'character/veld-cargo-turns-master-family-v1/north-east-candidate-v5/frames/bare/005.png'
originalmaster=Image.open(originalpath).convert('RGBA');padded=Image.new('RGBA',(256,256));padded.alpha_composite(originalmaster,(36,52))
items=[('Original East master',padded),('Repaired held master',Image.open(heldpath).convert('RGBA'))]+[(f'Graded phase{i}',f) for i,f in enumerate(frames)]
board=Image.new('RGB',(2048,640),'#202a30');d=ImageDraw.Draw(board)
d.text((8,6),'SHARED MASTER MATERIAL STUDY: original alpha, one pooled cloth curve/fixed skin-hair offsets; case/grip protected.',fill='white')
for i,(name,f) in enumerate(items):
 d.text((i*256+5,32),name,fill='white');board.paste(f,(i*256,42),f)
 detail=f.crop((50,65,225,165)).resize((256,146),Image.Resampling.NEAREST);board.paste(detail,(i*256,320),detail)
 legs=f.crop((45,156,225,233)).resize((256,109),Image.Resampling.NEAREST);board.paste(legs,(i*256,500),legs)
board.save(O/'master-comparison.png')
preview=[]
for f in frames:
 bg=Image.new('RGBA',(256,256),'#202a30');bg.alpha_composite(f);preview.append(bg)
preview[0].save(O/'cycle.png',save_all=True,append_images=preview[1:],duration=140,loop=0,disposal=0,blend=0)
decoded=Image.open(O/'cycle.png');assert decoded.n_frames==6;checks+=1
for i,f in enumerate(preview):
 decoded.seek(i);assert np.array_equal(np.array(decoded.convert('RGBA')),np.array(f));checks+=1
 assert decoded.info['duration']==140;checks+=1
reg=json.loads((S/'registration.json').read_text());crowns=[r['registeredCrown'] for r in reg['rows']]
record={'scope':'Source material/ruler study only, not native/cadence/helmet/production acceptance.','materialRecipe':recipepath.relative_to(R).as_posix(),'materialRecipeSHA256':hashlib.sha256(recipepath.read_bytes()).hexdigest(),'canonicalReferences':[{'path':p.relative_to(R).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [originalpath,heldpath]],'checks':checks,'failures':0,'crownSpread':max(crowns)-min(crowns),'rows':records,'visualReview':'pending'}
(O/'review-evidence.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Veld East carry material review</title><style>body{background:#202a30;color:#dce5e8;font:18px system-ui;margin:28px}img{max-width:100%}.motion{width:512px;image-rendering:pixelated}</style><h1>Veld East carry — master comparison</h1><p>Shared color grade and reduced body rise. Motion, equipment joins and final material consistency remain under review.</p><img class="motion" src="cycle.png"><img src="master-comparison.png">''',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'headWidths':[r['headTop20Width'] for r in records],'crownSpread':record['crownSpread'],'canonicalReferences':2,'scope':'source-only shared grade'}))
