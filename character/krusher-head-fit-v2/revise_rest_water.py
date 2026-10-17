"""Retain registered rest anatomy; fit water side heads and zoom visor identity."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,distance_transform_edt
from scipy.spatial import ConvexHull
R=Path(__file__).resolve().parents[2];inv=json.loads((R/'character/krusher-complete-animation-v1/source-coverage.json').read_text())
def read(p):return json.loads(p.read_text())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
def shift(mask,dx,dy):
 out=np.zeros_like(mask);y,x=np.where(mask);nx,ny=x+dx,y+dy;h,w=mask.shape;v=(nx>=0)&(nx<w)&(ny>=0)&(ny<h);out[ny[v],nx[v]]=True;return out
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),20)
for family,oldversion,newversion,names in [('rest-family',2,3,['bare-manifest.json','helmet-manifest.json']),('water-family',1,2,['water-bare-manifest.json','water-helmet-manifest.json'])]:
 old=R/f'character/krusher-{family}-v{oldversion}';P=R/f'character/krusher-{family}-v{newversion}';P.mkdir(exist_ok=True);proof=[];checks=0
 for q in read(old/'provenance.json')['records']:
  a=rgba(R/q['source']);before=rgba(old/q['output']);out=before.copy();h,w=a.shape[:2];yy,xx=np.indices((h,w));rgb=a[:,:,:3].astype(float)
  mask=np.zeros((h,w),bool);g=q['gear'];d=q.get('view',q['state'].rsplit('-',1)[1]);x0,y0,x1,y1=q['headBox'];details={}
  if g=='bare' and family=='water-family' and d in ['east','west']:
   original=inv['resolved']['helmet'][q['state']];mp=R/original['manifest'][6:];paired=rgba(resolve(mp,original['state']['frameFiles'][q['frame']]))
   axis=(x0+x1)/2;bottom=y1+2;cy=(y0+y1)/2-2;oldhead=(((xx-axis)/((x1-x0)/2+3))**2+((yy-cy)/((y1-y0)/2+5))**2)<1
   head=Image.open(R/q['headSource']).convert('RGBA');ax,ay=q['headPaste'];layer=Image.new('RGBA',(w,h));layer.paste(head,(ax,ay));ha=np.array(layer)
   common=(a[:,:,3]>0)&np.all(a==paired,2)&~oldhead;region=(oldhead|(ha[:,:,3]>0))&~common
   foreground=(a[:,:,3]>0)&np.all(a==paired,2)&(rgb.mean(2)<65)&(yy>=y1-4)
   collar=(a[:,:,3]>180)&(yy>=y0-2)&((xx<x0) if d=='east' else (xx>=x1));region&=~foreground&~collar
   marking=np.any(a!=before,axis=2)&~region&(before[:,:,3]>0);dx=-2 if d=='east' else 2;dy=2
   mask=(region|shift(region,dx,dy))&~foreground&~collar&~marking
   layer=Image.new('RGBA',(w,h));layer.paste(head,(ax+dx,ay+dy));out[mask]=np.array(layer)[mask]
   details={'oldPaste':[ax,ay],'newPaste':[ax+dx,ay+dy],'collarProtected':True,'foregroundProtected':True,'headSource':'res://'+q['headSource'],'headSourceHash':q['headHash']}
  elif g=='helmet' and d!='north':
   # Reconstruct the exact original face window. Keep its glass glints, rim,
   # shell and alpha intact; enlarge existing Krusher features inside that window.
   skin=(a[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)
   skin&=(xx>=x0-(6 if family=='rest-family' else 8))&(xx<x1+8)&(yy>=y0-(5 if family=='rest-family' else 8))&(yy<y1+8)
   labs,n=label(skin);sizes=np.bincount(labs.ravel());idx=int(sizes[1:].argmax())+1;sy,sx=np.where(labs==idx);points=np.column_stack([sx,sy]);hull=ConvexHull(points)
   image=Image.new('L',(w,h));ImageDraw.Draw(image).polygon([tuple(map(int,points[k])) for k in hull.vertices],fill=255)
   mask=(np.array(image)>0)&~((rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2))
   # Match the original fit masks before taking any colour samples.
   assert int(mask.sum())==q['facePixels'],(family,q['state'],q['frame'],int(mask.sum()),q['facePixels'])
   sy,sx=np.where(mask);bx=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)]
   part=before[bx[1]:bx[3],bx[0]:bx[2]].copy();pm=mask[bx[1]:bx[3],bx[0]:bx[2]];nearest=distance_transform_edt(~pm,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255
   cw,ch=bx[2]-bx[0],bx[3]-bx[1];size=(max(cw+2,round(cw*1.12)),max(ch+2,round(ch*1.12)))
   fit=Image.fromarray(part).resize(size,Image.Resampling.LANCZOS);paste=[bx[0]-(size[0]-cw)//2,bx[1]-(size[1]-ch)//2]
   layer=Image.new('RGBA',(w,h));layer.paste(fit,tuple(paste));zoom=np.array(layer);out[mask,:3]=zoom[mask,:3]
   details={'originalFaceBox':bx,'zoomSize':list(size),'zoomPaste':paste,'originalFacePixels':int(mask.sum()),'helmetApertureUnchanged':True,'method':'12 percent existing identity feature enlargement, clipped to original face window'}
  else:details={'method':'Existing manually registered rest neck or bowed/rear identity retained exactly'}
  assert np.array_equal(before[~mask],out[~mask]);checks+=1
  if g=='helmet':assert np.array_equal(before[:,:,3],out[:,:,3]);checks+=1
  protected=min(h,y1+12);assert np.array_equal(before[protected:],out[protected:]);checks+=1
  rel=q['output'];target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target)
  mr='head-fit-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
  proof.append({'gear':g,'state':q['state'],'frame':q['frame'],'source':'res://'+(old/rel).relative_to(R).as_posix(),'sourceHash':sha(old/rel),'output':rel,'outputHash':sha(target),'mask':mr,'protectedFromRow':protected,'changedPixels':int(np.any(before!=out,axis=2).sum()),'details':details})
 for name in names:(P/name).write_text(json.dumps(read(old/name),indent=2)+'\n')
 (P/'revision.json').write_text(json.dumps({'checks':checks,'errors':[],'records':proof,'scope':'Existing registered rest bare necks retained; water side heads back2/down2; helmet identity features enlarged inside original face window. Exact old body outside head mask, helmet alpha, root/state metadata and source clocks. Staged candidate.'},indent=2)+'\n')
 (P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://'+(P/(('water-' if family=='water-family' else '')+g+'-manifest.json')).relative_to(R).as_posix()] for g in ['bare','helmet']}},indent=2)+'\n')
 (P/'native').mkdir(exist_ok=True);s=(old/'native/review.gd').read_text().replace(old.name,P.name).replace('res://character/krusher-complete-animation-v1/progress.json','res://'+P.relative_to(R).as_posix()+'/pack-index.json')
 (P/'native/review.gd').write_text(s);(P/'run_native.py').write_text((old/'run_native.py').read_text().replace(old.name,P.name));(P/'build_review.py').write_text((old/'build_review.py').read_text())
 for chunk in range(0,len(proof),24):
  entries=proof[chunk:chunk+24];board=Image.new('RGB',(1536,60+((len(entries)+5)//6)*(h+30)),'#252b2e');draw=ImageDraw.Draw(board);draw.text((15,12),'KRUSHER / '+family+' / HEAD FIT',font=font,fill='white')
  for j,q in enumerate(entries):
   im=Image.open(P/q['output']).convert('RGBA');x=j%6*256;y=50+j//6*(h+30);board.paste(im,(x,y),im);draw.text((x+5,y+h-3),q['gear']+' '+q['state']+' '+str(q['frame']),font=font,fill='#bed2d3')
  board.save(P/f'head-fit-sheet-{chunk//24:02}.png')
 print(json.dumps({'family':family,'uniquePoses':len(proof),'changed':sum(q['changedPixels']>0 for q in proof),'checks':checks,'errors':[]}))
