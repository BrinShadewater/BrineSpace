"""Revise existing Krusher poses; preserve the previous suit and source clocks."""
from pathlib import Path
import copy, hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import label, binary_dilation
from scipy.spatial import ConvexHull

P=Path(__file__).resolve().parent
R=P.parent.parent
def read(p): return json.loads(p.read_text())
def rgba(p): return np.array(Image.open(p).convert('RGBA'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(base,p): return R/p[6:] if p.startswith('res://') else base/p
canonical=R/'character/krusher-james-canonical-v5'
oldcanonical=R/'character/krusher-james-canonical-v4'
idle={}
for gear in ['bare','helmet']:
 for d in ['south','east','north','west']:
  s=next(s for s in read(canonical/(gear+'-manifest.json'))['states'] if s['id']=='idle-'+d)
  idle[gear,d]=rgba(resolve(canonical,s['frameFiles'][0]))

for family in ['repair','torch','seated']:
 old=R/f'character/krusher-{family}-family-v1'
 new=R/f'character/krusher-{family}-family-v2';new.mkdir(exist_ok=True)
 tracking={(q['state'],q['frame']):q['headSkinBox'] for q in read(old/'head-tracking.json')}
 records=read(old/'provenance.json')['records'];mapped={};proof=[];checks=0
 for q in records:
  gear=q['gear'];state=q['state'];d=state.rsplit('-',1)[1]
  before=rgba(old/q['output']);a=rgba(R/q['source']);out=before.copy()
  height,width=before.shape[:2];yy,xx=np.indices((height,width));mask=np.zeros((height,width),bool)
  detail={};anchor=q['headPaste']
  if q['method'].startswith('Exact complete'):
   out=np.pad(idle[gear,d],((0,height-184),(0,0),(0,0)))
   mask=np.any(out!=before,axis=2);detail={'canonicalEndpoint':d}
  elif gear=='bare' and d in ['east','west']:
   x0,y0,x1,y1=q['headBox'];bottom=y1+3
   head=Image.open(R/q['headSource']).convert('RGBA');ax,ay=anchor
   if d=='east':
    region=(xx>=min(x0-4,ax-1))&(xx<x1+8);collar=(yy>=y0-2)&(xx<x0)&(a[:,:,3]>0)
   else:
    region=(xx>=x0-8)&(xx<max(x1+4,ax+head.width+1));collar=(yy>=y0-2)&(xx>=x1)&(a[:,:,3]>0)
   region&=(yy>=min(y0-9,ay-1))&(yy<bottom)
   dx=-2 if d=='east' else 2;dy=2
   moved=np.zeros_like(region)
   sy,sx=np.where(region);ny,nx=sy+dy,sx+dx;valid=(nx>=0)&(nx<width)&(ny<height)
   moved[ny[valid],nx[valid]]=True
   mask=(region|moved)&~collar
   rgb=a[:,:,:3].astype(float)
   cool=(a[:,:,3]>0)&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2)
   mask&=~cool
   # Recoloured department pixels are never overwritten by neck fitting.
   oldallowed=np.array(Image.open(old/q['allowedMask']))>0
   marking=oldallowed&~region&np.any(a!=before,axis=2)&(before[:,:,3]>0)
   mask&=~marking
   layer=Image.new('RGBA',(width,height));layer.paste(head,(ax+dx,ay+dy));h=np.array(layer)
   out[mask]=h[mask];detail={'oldPaste':anchor,'newPaste':[ax+dx,ay+dy],'collarProtected':int(collar.sum()),'markingProtected':int(marking.sum())}
  elif gear=='helmet' and d!='north':
   rgb=a[:,:,:3].astype(float);t=tracking[state,q['frame']]
   warm=(a[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)
   warm&=(xx>=t[0]-10)&(xx<t[2]+15)&(yy>=t[1]-10)&(yy<t[3]+15)
   labs,n=label(warm);sizes=np.bincount(labs.ravel());k=int(sizes[1:].argmax())+1
   sy,sx=np.where(labs==k);points=np.column_stack([sx,sy]);hull=ConvexHull(points)
   faceimage=Image.new('L',(width,height));ImageDraw.Draw(faceimage).polygon([tuple(map(int,points[v])) for v in hull.vertices],fill=255)
   face=np.array(faceimage)>0
   cool=(a[:,:,3]>0)&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2)
   if family=='seated':face&=~cool
   x0,y0,x1,y1=q['headBox'];margin=2 if d=='south' else 1
   box=[x0-margin,y0-3,x1+margin,y1]
   mask=binary_dilation(face,iterations=2)&(xx>=box[0])&(xx<box[2])&(yy>=box[1])&(yy<box[3])&(a[:,:,3]>0)&~cool
   head=Image.open(R/q['headSource']).convert('RGBA')
   crop=[round(head.width*.30) if d=='east' else 0,round(head.height*.18),head.width if d in ['east','south'] else round(head.width*.70),head.height]
   fit=head.crop(crop).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
   layer=Image.new('RGBA',(width,height));layer.paste(fit,(box[0],box[1]));h=np.array(layer)
   mask&=h[:,:,3]>60;out[mask,:3]=h[mask,:3]
   detail={'oldFaceBox':q['headBox'],'newFaceBox':box,'sourceCrop':crop,'coolForegroundProtected':True}
  assert np.array_equal(before[~mask],out[~mask]);checks+=1
  if gear=='helmet':assert np.array_equal(before[:,:,3],out[:,:,3]);checks+=1
  rel=q['output'];target=new/rel;target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target)
  maskrel='head-fit-masks/'+gear+'/'+Path(rel).name;(new/maskrel).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(new/maskrel)
  mapped[gear,rel]=rel
  proof.append({'gear':gear,'state':state,'frame':q['frame'],'source':'res://'+(old/rel).relative_to(R).as_posix(),'sourceHash':digest(old/rel),'output':rel,'outputHash':digest(target),'mask':maskrel,'changedPixels':int(np.any(out!=before,axis=2).sum()),'details':detail})
 for gear in ['bare','helmet']:
  m=read(old/(gear+'-manifest.json'));mnew=copy.deepcopy(m)
  for s in mnew['states']:
   s['frameFiles']=[mapped[gear,p] for p in s['frameFiles']]
  (new/(gear+'-manifest.json')).write_text(json.dumps(mnew,indent=2)+'\n')
  assert {k:v for k,v in m.items() if k!='states'}=={k:v for k,v in mnew.items() if k!='states'};checks+=1
  for a,b in zip(m['states'],mnew['states']):
   assert {k:v for k,v in a.items() if k!='frameFiles'}=={k:v for k,v in b.items() if k!='frameFiles'};checks+=1
 (new/'revision.json').write_text(json.dumps({'checks':checks,'errors':[],'records':proof,'scope':'Head fit only against previous Krusher output; exact suit outside recorded mask, helmet alpha, root/state fields. Staged candidate, not station acceptance.'},indent=2)+'\n')
 (new/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://'+(new/(g+'-manifest.json')).relative_to(R).as_posix()] for g in ['bare','helmet']}},indent=2)+'\n')
 native=new/'native';native.mkdir(exist_ok=True)
 source=R/'character/krusher-inspection-family-v2'
 (native/'verify.gd').write_text((source/'native/verify.gd').read_text().replace('krusher-inspection-family-v2',new.name).replace('Corrected inspection family: every1146source slot','Corrected '+family+' family: every source slot'))
 (new/'run_native_verify.py').write_text((source/'run_native_verify.py').read_text().replace('krusher-inspection-family-v2',new.name))
 font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22)
 board=Image.new('RGB',(1600,960),'#252b2e');draw=ImageDraw.Draw(board)
 draw.text((20,10),'KRUSHER DOM / '+family.upper()+' HEAD FIT / BARE ABOVE, HELMET BELOW',font=font,fill='white')
 for row,g in enumerate(['bare','helmet']):
  m=read(new/(g+'-manifest.json'))
  action={'repair':'repair','torch':'torch-weld','seated':'sit-idle'}[family]
  for col,d in enumerate(['south','east','north','west']):
   candidates=[s for s in m['states'] if s['id']==action+'-'+d]
   if not candidates:candidates=[s for s in m['states'] if s['id'].endswith('-'+d)]
   s=candidates[0];im=Image.open(new/s['frameFiles'][len(s['frameFiles'])//2]).convert('RGBA');im=im.resize((width*2,height*2),Image.Resampling.NEAREST)
   x=col*400+10;y=55+row*440;board.paste(im,(x,y),im);draw.text((x,y+height*2+8),s['id'],font=font,fill='#bed2d3')
 board.save(new/'head-fit-sheet.png')
 print(json.dumps({'family':family,'uniquePoses':len(proof),'changed':sum(q['changedPixels']>0 for q in proof),'checks':checks,'errors':[]}))
