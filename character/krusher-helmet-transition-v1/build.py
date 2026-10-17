"""Deterministic selected James suit reuse; no generated or redrawn body motion."""
import copy, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label, distance_transform_edt
from scipy.spatial import ConvexHull

P=Path(__file__).resolve().parent; R=P.parent.parent
SOURCE=R/'character/james-helmet-fitting-east-v1'
CANON=R/'character/krusher-james-canonical-v4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((SOURCE/'manifest.json').read_text())
headpath=CANON/'sources/east-head-native.png'
if not headpath.exists():headpath=R/'character/krusher-bill-base-test-v2/sources/east-head-native.png'
head=Image.open(headpath).convert('RGBA'); face_head=head.crop((8,5,head.width,head.height))
yy,xx=np.indices((256,256)); target=np.array([82.,124.,128.]); luma=np.array([.2126,.7152,.0722])
out_frames=[]; records=[]; checks=0
# Masks follow visible head/collar/foreground equipment, not the whole upper body.
bare_regions={1:(108,70,140,100),2:(107,70,137,101),3:(108,70,136,101),4:(106,70,132,102)}
for i,relative in enumerate(manifest['states'][0]['frameFiles']):
 source=SOURCE/relative; a=np.array(Image.open(source).convert('RGBA')); rgb=a[:,:,:3].astype(float)
 suit_region=(yy>=95)&(yy<138)
 if i==5:suit_region|=(xx<120)&(yy>=80)&(yy<95)
 marking=(a[:,:,3]>0)&suit_region&(rgb[:,:,0]>rgb[:,:,2]*1.15)&(rgb[:,:,1]>rgb[:,:,2]*1.12)&(rgb[:,:,0]>35)&(rgb[:,:,1]>rgb[:,:,0]*.65)
 edit=np.zeros((256,256),bool); out=a.copy(); gain=np.minimum(1.15,(rgb@luma)/(target@luma)); colours=np.rint(gain[:,:,None]*target).astype('uint8');out[marking,:3]=colours[marking]
 facebox=None; anchor=None
 if i in (0,11):
  gear='bare' if i==0 else 'helmet'; cm=json.loads((CANON/(gear+'-manifest.json')).read_text()); row=next(s for s in cm['states'] if s['id']=='idle-east')
  endpoint=Image.open(CANON/row['frameFiles'][0]).convert('RGBA'); layer=Image.new('RGBA',(256,256));layer.alpha_composite(endpoint,(36,52));out=np.array(layer);edit=np.any(out!=a,axis=2);marking[:]=False
 elif i in bare_regions:
  x0,y0,x1,y1=bare_regions[i]; axis=round((x0+x1)/2)
  edit=(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1)
  # Keep the original raised rear collar while clearing all exposed James hair.
  collar=(yy>=y1-5)&(xx<axis-3)&(a[:,:,3]>0);edit&=~collar
  anchor=[x1-head.width,y1-head.height];layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(anchor)); h=np.array(layer)
  out[edit]=h[edit]
 else:
  warm=(a[:,:,3]>180)&(xx>=110)&(xx<149)&(yy<110)&(rgb[:,:,0]>rgb[:,:,1]*1.10)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb.mean(2)>40)
  labs,n=label(warm); sizes=np.bincount(labs.ravel()); k=int(np.argmax(sizes[1:]))+1
  visible=labs==k
  if i==5:visible=warm&(xx>=120)&(xx<137)&(yy>=78)&(yy<100)
  sy,sx=np.where(visible);points=np.column_stack([sx,sy]);hull=ConvexHull(points)
  mask=Image.new('L',(256,256));ImageDraw.Draw(mask).polygon([tuple(map(int,points[q])) for q in hull.vertices],fill=255);edit=np.array(mask)>0
  fy,fx=np.where(edit);facebox=[int(fx.min()),int(fy.min()),int(fx.max()+1),int(fy.max()+1)]
  identity_head=face_head
  scale=max((facebox[2]-facebox[0])/identity_head.width,(facebox[3]-facebox[1])/identity_head.height)
  fit=identity_head.resize((max(1,round(identity_head.width*scale)),max(1,round(identity_head.height*scale))),Image.Resampling.LANCZOS)
  anchor=[facebox[2]-fit.width,facebox[3]-fit.height];layer=Image.new('RGBA',(256,256));layer.paste(fit,tuple(anchor));h=np.array(layer)
  # Source face silhouette can exceed the crop's alpha edge. Extend nearest
  # existing identity RGB within that silhouette rather than retain old goggles.
  nearest=distance_transform_edt(h[:,:,3]<=60,return_distances=False,return_indices=True)
  fitted_rgb=h[nearest[0],nearest[1],:3];out[edit,:3]=fitted_rgb[edit]
 allowed=marking|edit
 assert np.array_equal(a[~allowed],out[~allowed]);checks+=1
 assert np.array_equal(a[138:],out[138:]);checks+=1
 if i not in bare_regions and i not in (0,11):assert np.array_equal(a[:,:,3],out[:,:,3]);checks+=1
 (P/'masks').mkdir(exist_ok=True)
 for kind,mask in [('allowed',allowed),('head',edit),('marking',marking)]:Image.fromarray(mask.astype('uint8')*255).save(P/'masks'/f'{i:03}-{kind}.png')
 image=Image.fromarray(out);out_frames.append(image)
 records.append({'pose':i,'source':source.relative_to(R).as_posix(),'sourceHash':sha(source),'allowedMask':f'masks/{i:03}-allowed.png','faceBox':facebox,'headPaste':anchor,'changedPixels':int(np.any(a!=out,axis=2).sum())})
result=copy.deepcopy(manifest);result.update(name='Krusher Dom helmet fitting east',status='candidate-not-installed',runtimeInstalled=False,identity={'name':'Krusher Dom','title':'System Administrator','department':'AI & Robotics','accentTarget':'#527C80','baseFamily':'James / Branforth'})
for state in result['states']:
 indices=list(range(12)) if state['id'].startswith('equip') else list(reversed(range(12)));state['frameFiles']=[]
 state['provenance']='James authored body, tool and shell motion reused; Krusher identity and matte cyan markings; removal reverses fitting poses; exact canonical-v4 idle endpoints'
 for i,n in enumerate(indices):
  rel=f'frames/{state["id"]}/{i:03}.png';q=P/rel;q.parent.mkdir(parents=True,exist_ok=True);out_frames[n].save(q);state['frameFiles'].append(rel)
 state['sourcePoseIndices']=indices
(P/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
proof={'sourceManifest':SOURCE.relative_to(R).as_posix()+'/manifest.json','sourceManifestHash':sha(SOURCE/'manifest.json'),'headSource':headpath.relative_to(R).as_posix(),'headHash':sha(headpath),'records':records,'checks':checks,'errors':[],'scope':'East equipment transition only. Source whole-body motion/timing/feet/helmet preserved outside identity and marking masks. No normal equipment routing installed.'}
(P/'provenance.json').write_text(json.dumps(proof,indent=2)+'\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),24)
board=Image.new('RGB',(1200,1050),'#242c31');draw=ImageDraw.Draw(board);draw.text((20,12),'KRUSHER DOM / HELMET FITTING / JAMES UTILITY SUIT',font=font,fill='white')
for i,im in enumerate(out_frames):
 x=(i%4)*300;y=65+(i//4)*325;tile=im.resize((256,256),Image.Resampling.NEAREST);board.paste(tile,(x+20,y),tile);draw.text((x+20,y+260),f'Equip pose {i:02}',font=font,fill='#cadcde')
board.save(P/'contact-sheet.png')
print(json.dumps({'poses':12,'frameReferences':24,'checks':checks,'errors':[]}))
