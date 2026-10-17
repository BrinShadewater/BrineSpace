from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import distance_transform_edt
R=Path.cwd();H=R/'character/krusher-head-fit-v3';old=R/'character/krusher-water-family-v2';orig=R/'character/krusher-water-family-v1';P=R/'character/krusher-water-family-v3';P.mkdir(exist_ok=True);qs=json.loads((orig/'provenance.json').read_text())['records'];inv=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text());records=[]
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def polygon(shape,points):
 im=Image.new('L',(shape[1],shape[0]));ImageDraw.Draw(im).polygon([tuple(map(int,p)) for p in points],fill=255);return np.array(im)>0
for q in qs:
 d=q['state'].rsplit('-',1)[1];a=arr(old/q['output']);out=a.copy();h,w=a.shape[:2];mask=np.zeros((h,w),bool);details={'method':'Other directions retained pending coherent front/rear head review'};x0,y0,x1,y1=q['headBox'];yy,xx=np.indices((h,w))
 if d in ['east','west']:
  headpath=H/'sources'/f"{'bare' if q['gear']=='bare' else 'visor'}-{d}-native.png";head=Image.open(headpath).convert('RGBA');details={'headSource':'res://'+headpath.relative_to(R).as_posix(),'headHash':sha(headpath),'method':'Complete generated head and neck registration, original body retained'}
  if q['gear']=='bare':
   original=arr(R/q['source']);pairedspec=inv['resolved']['helmet'][q['state']];mp=R/pairedspec['manifest'][6:];paired=arr(resolve(mp,pairedspec['state']['frameFiles'][q['frame']]))
   ax,ay=q['headPaste'];oldhead=Image.open(R/q['headSource']).convert('RGBA');layer=Image.new('RGBA',(w,h));layer.paste(oldhead,(ax-2 if d=='east' else ax+2,ay+2));oldalpha=np.array(layer)[:,:,3]>0
   if d=='east':points=[[132,100],[138,96],[151,97],[157,104],[157,116],[155,122],[151,128],[141,128],[134,120],[130,109]];delta=(x0-138,y0-108);paste=(ax-4,ay)
   else:points=[[97,110],[102,104],[111,103],[120,108],[123,118],[120,127],[112,133],[102,133],[97,127],[94,118]];delta=(x0-100,y0-113);paste=(ax+2,ay)
   skull=polygon((h,w),[(x+delta[0],y+delta[1]) for x,y in points]);common=(original[:,:,3]>0)&np.all(original==paired,2);remove=(skull|oldalpha)&~common
   out[remove]=[0,0,0,0];base=Image.fromarray(out);layer=Image.new('RGBA',(w,h));layer.paste(head,paste);newalpha=np.array(layer)[:,:,3]>0;base.alpha_composite(layer);out=np.array(base);mask=remove|newalpha
   details.update(paste=list(paste),oldSkullPolygon=[[x+delta[0],y+delta[1]] for x,y in points],commonBodyProtectedUnlessOverlaidByActualHead=True,greyHairOverlapRemoved=True)
   assert np.array_equal(out[newalpha],np.array(layer)[newalpha])
  else:
   if d=='east':points=[[148,104],[153,105],[156,109],[157,115],[156,123],[151,128],[146,127],[141,120],[141,113],[143,108]];delta=(x0-138,y0-108)
   else:points=[[103,106],[108,106],[112,109],[114,116],[113,122],[109,127],[103,127],[98,123],[96,118],[97,112],[100,108]];delta=(x0-100,y0-113)
   mask=polygon((h,w),[(x+delta[0],y+delta[1]) for x,y in points]);rgb=arr(R/q['source'])[:,:,:3].astype(float);glass=(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2);mask&=~glass&(a[:,:,3]>180)
   y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];part=np.array(head);opaque=part[:,:,3]>0;nearest=distance_transform_edt(~opaque,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;face=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(w,h));layer.paste(face,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];details.update(visorPolygon=[[x+delta[0],y+delta[1]] for x,y in points],visorBox=box,glassGlintsProtected=True,helmetShellAlphaExact=True)
  assert np.array_equal(a[~mask],out[~mask]);assert np.array_equal(a[y1+18:],out[y1+18:])
  if q['gear']=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])

 if d=='south':
  step=q['frame'] if q['state'].startswith('swim-start-') else 5-q['frame'] if q['state'].startswith('swim-stop-') else 5 if q['state'].startswith('swim-') else 0
  bowed=step>0;hp=H/'sources'/f"{'bare' if q['gear']=='bare' else 'visor'}-south{'-bowed' if bowed else ''}-native.png";head=Image.open(hp).convert('RGBA');details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'method':'Generated complete front/bowed identity head-neck, original body and source foreground retained','bowed':bowed}
  if q['gear']=='bare':
   original=arr(R/q['source']);pairedspec=inv['resolved']['helmet'][q['state']];mp=R/pairedspec['manifest'][6:];paired=arr(resolve(mp,pairedspec['state']['frameFiles'][q['frame']]))
   ax,ay=q['headPaste'];oldhead=Image.open(R/q['headSource']).convert('RGBA');layer=Image.new('RGBA',(w,h));layer.paste(oldhead,(ax,ay));oldalpha=np.array(layer)[:,:,3]>0;axis=(x0+x1)/2
   skull=(((xx-axis)/((x1-x0)/2+5))**2+((yy-(y0+y1)/2+3)/((y1-y0)/2+10))**2)<1
   common=(original[:,:,3]>0)&np.all(original==paired,2);foreground=(yy>=y1+4) if step>=2 else np.zeros((h,w),bool);remove=oldalpha&~common&~foreground;out[remove]=[0,0,0,0];paste=(round(axis-head.width/2),ay-3 if step>=2 else ay);layer=Image.new('RGBA',(w,h));layer.paste(head,paste);ha=np.array(layer);newalpha=(ha[:,:,3]>0)&~foreground;out[newalpha]=ha[newalpha];mask=remove|newalpha;details.update(paste=list(paste),foregroundFromRow=y1+4 if step>=2 else None,greyHairOverlapRemoved=True)
  else:
   originalmask=np.array(Image.open(old/'head-fit-masks'/q['gear']/Path(q['output']).name))>0;mask=originalmask.copy()
   for dy in range(1,4):mask[:-dy]|=originalmask[dy:]
   mask[:,1:]|=originalmask[:,:-1];mask[:,:-1]|=originalmask[:,1:]
   rgb=arr(R/q['source'])[:,:,:3].astype(float);glass=(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2);y,x=np.where(originalmask);top=int(y.min());metal=(rgb.max(2)-rgb.min(2)<12)&(rgb.mean(2)>75)&(yy<top);mask&=~glass&~metal&(a[:,:,3]>180)
   y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];part=np.array(head);opaque=part[:,:,3]>0;nearest=distance_transform_edt(~opaque,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;fit=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(w,h));layer.paste(fit,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];details.update(visorBox=box,glassAndUpperMetalRimProtected=True)
  assert np.array_equal(a[~mask],out[~mask]);assert np.array_equal(a[y1+18:],out[y1+18:])
  if q['gear']=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
 target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+q['gear']+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
 records.append(dict(q,previousSource='res://'+(old/q['output']).relative_to(R).as_posix(),previousHash=sha(old/q['output']),outputHash=sha(target),mask=mr,details=details,changedPixels=int(np.any(a!=out,2).sum())))
for name in ['water-bare-manifest.json','water-helmet-manifest.json']:(P/name).write_bytes((old/name).read_bytes())
(P/'revision.json').write_text(json.dumps({'records':records,'scope':'East/West and front/bowed South whole-head-neck candidate. North retained. Not owner visually accepted. Original suit outside local head edit exact.'},indent=2)+'\n')
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),22);board=Image.new('RGB',(1200,760),'#252b2e');draw=ImageDraw.Draw(board);draw.text((20,12),'KRUSHER / ORIGINAL BODIES / NEW HEAD & NECK FIT',font=font,fill='white')
for i,(g,d) in enumerate([('bare','east'),('bare','west'),('helmet','east'),('helmet','west')]):
 q=next(q for q in records if q['gear']==g and q['state']=='swim-'+d and q['frame']==2);x=i%2*600;y=i//2*360+40
 for k,pack in enumerate([old,P]):
  im=Image.open(pack/q['output']).convert('RGBA').crop((70,70,185,180)).resize((345,330),Image.Resampling.NEAREST);# One full sprite comparison per cell; old head crop inset
  if k==1:board.paste(im,(x+170,y),im)
  else:
   crop=Image.open(pack/q['output']).convert('RGBA').crop((90,90,165,145)).resize((150,110),Image.Resampling.NEAREST);board.paste(crop,(x+10,y+95),crop)
 draw.text((x+10,y+5),g.upper()+' '+d.upper(),font=font,fill='white');draw.text((x+10,y+210),'OLD',font=font,fill='#b6c8cb');draw.text((x+180,y+295),'NEW / ORIGINAL SUIT',font=font,fill='#b6c8cb')
board.save(P/'fit-comparison.png');print(json.dumps({'unique':len(records),'changed':sum(q['changedPixels']>0 for q in records)}))
