from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import label,binary_dilation
from scipy.spatial import ConvexHull
R=Path(__file__).resolve().parents[2];old=R/'character/krusher-cargo-family-v1';P=R/'character/krusher-cargo-family-v2';P.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
yy,xx=np.indices((256,256));records=[];checks=0
shifts={'east':(-2,2),'west':(2,2),'se':(-1,1),'sw':(1,1),'ne':(-1,1),'nw':(1,1)}
def shift(mask,dx,dy):
 out=np.zeros_like(mask);y,x=np.where(mask);nx,ny=x+dx,y+dy;v=(nx>=0)&(nx<256)&(ny>=0)&(ny<256);out[ny[v],nx[v]]=True;return out
for q in read(old/'provenance.json')['records']:
 a=rgba(R/q['source']);before=rgba(old/q['output']);out=before.copy();rgb=a[:,:,:3].astype(float);mask=np.zeros((256,256),bool)
 g=q['gear'];view=q['view'];x0,y0,x1,y1=q['headBox'];axis=round((x0+x1)/2);bottom=y1+3;head=Image.open(R/q['headSource']).convert('RGBA');detail={}
 if g=='bare' and view in shifts:
  ax,ay=q['headPaste'];region=(xx>=min(x0-5,ax-1))&(xx<max(x1+5,ax+head.width+1))&(yy>=min(y0-10,ay-1))&(yy<bottom)
  collar=(a[:,:,3]>0)&(yy>=y0-2)
  if view=='east':collar&=xx<x0
  elif view=='west':collar&=xx>=x1
  else:collar&=(yy>=bottom-5)&(abs(xx-axis)>8)
  region&=~collar;dx,dy=shifts[view]
  marking=np.any(a!=before,axis=2)&~region&(before[:,:,3]>0)
  cool=(a[:,:,3]>0)&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2)
  mask=(region|shift(region,dx,dy))&~collar&~marking&~cool
  layer=Image.new('RGBA',(256,256));layer.paste(head,(ax+dx,ay+dy));out[mask]=np.array(layer)[mask]
  detail={'oldPaste':[ax,ay],'newPaste':[ax+dx,ay+dy],'collarProtected':True,'markingsProtected':True,'quarterShift':'One pixel toward side fit' if len(view)==2 else None}
 elif g=='helmet' and view!='north':
  skin=(a[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)&(xx>=x0-6)&(xx<x1+8)&(yy>=y0-5)&(yy<y1+8)
  labs,n=label(skin);sizes=np.bincount(labs.ravel())
  if view in ['ne','nw']:
   # Rear-facing hardware has warm bronze shading too. Use the actual narrow
   # visible visor aperture, never the largest warm component on the shell.
   aperture={('carry-turn-east-north',2):[142,82,151,100],('carry-turn-east-north',3):[143,84,146,98],('carry-turn-north-west',2):[115,80,120,94],('carry-turn-north-west',3):[113,82,125,98]}[q['state'],q['frame']]
   side='east' if view=='ne' else 'west'
   face_source=R/f'character/krusher-bill-base-test-v2/sources/{side}-head-native.png';head=Image.open(face_source).convert('RGBA')
  else:idx=int(sizes[1:].argmax())+1;side=view;face_source=R/q['headSource']
  if view in ['ne','nw']:
   face=skin&(xx>=aperture[0])&(xx<aperture[2])&(yy>=aperture[1])&(yy<aperture[3])
  else:
   y,x=np.where(labs==idx);points=np.column_stack([x,y]);hull=ConvexHull(points)
   image=Image.new('L',(256,256));ImageDraw.Draw(image).polygon([tuple(map(int,points[k])) for k in hull.vertices],fill=255);face=np.array(image)>0
  cool=(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2);face&=~cool;y,x=np.where(face)
  fb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];margin=2 if view=='south' else 1;box=[fb[0]-margin,fb[1]-3,fb[2]+margin,fb[3]]
  crop=[round(head.width*.3) if side=='east' else 0,round(head.height*.18),round(head.width*.7) if side=='west' else head.width,head.height]
  fit=head.crop(crop).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS);layer=Image.new('RGBA',(256,256));layer.paste(fit,(box[0],box[1]));h=np.array(layer)
  mask=binary_dilation(face,iterations=2)&(xx>=box[0])&(xx<box[2])&(yy>=box[1])&(yy<box[3])&(a[:,:,3]>0)&~cool&(h[:,:,3]>60)
  if view in ['ne','nw']:mask&=(xx>=aperture[0])&(xx<aperture[2])&(yy>=aperture[1])&(yy<aperture[3])&skin
  out[mask,:3]=h[mask,:3];detail={'oldFaceBox':fb,'newFaceBox':box,'crop':crop,'faceSource':'res://'+face_source.relative_to(R).as_posix(),'faceSourceHash':sha(face_source),'rearQuarterVisibleFace':view in ['ne','nw']}
  if view in ['ne','nw']:detail['protectedVisorAperture']=aperture
 assert np.array_equal(before[~mask],out[~mask]);checks+=1
 if g=='helmet':assert np.array_equal(before[:,:,3],out[:,:,3]);checks+=1
 # Cargo, hands, hips and boots lie below this per-pose head envelope.
 protected=min(256,y1+14);assert np.array_equal(before[protected:],out[protected:]);checks+=1
 path=P/q['output'];path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(path)
 mr='head-fit-masks/'+g+'/'+path.name;mp=P/mr;mp.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(mp)
 records.append({'gear':g,'state':q['state'],'frame':q['frame'],'view':view,'source':'res://'+(old/q['output']).relative_to(R).as_posix(),'sourceHash':sha(old/q['output']),'output':q['output'],'outputHash':sha(path),'mask':mr,'changedPixels':int(np.any(before!=out,axis=2).sum()),'protectedFromRow':protected,'details':detail})
for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_text(json.dumps(read(old/(g+'-manifest.json')),indent=2)+'\n')
(P/'revision.json').write_text(json.dumps({'checks':checks,'errors':[],'records':records,'scope':'Staged head-fit revision; exact original cargo/hands/body outside recorded head masks and below per-pose head envelope; helmet alpha and all root/state fields retained.'},indent=2)+'\n')
profile=R/'character/krusher-cargo-settle-profile-v2';profile.mkdir(exist_ok=True)
for g in ['bare','helmet']:
 oldprofile=R/'character/krusher-cargo-settle-profile-v1'/(g+'-manifest.json')
 pm=read(oldprofile)
 for s in pm['states']:s['frameFiles']=[f.replace('krusher-cargo-family-v1','krusher-cargo-family-v2') for f in s['frameFiles']]
 (profile/(g+'-manifest.json')).write_text(json.dumps(pm,indent=2)+'\n')
(P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://'+(P/(g+'-manifest.json')).relative_to(R).as_posix(),'res://'+(profile/(g+'-manifest.json')).relative_to(R).as_posix()] for g in ['bare','helmet']}},indent=2)+'\n')
(P/'native').mkdir(exist_ok=True)
s=(old/'native/review.gd').read_text().replace(old.name,P.name).replace('res://character/krusher-complete-animation-v1/progress.json','res://character/krusher-cargo-family-v2/pack-index.json').replace('res://character/krusher-complete-animation-v1/native/review.gd.uid','res://character/krusher-cargo-family-v2/native/review.gd.uid')
s=s.replace('player.load_manifest(BARE,true)','player.load_manifest(BARE,true)\n player.load_manifest("res://character/krusher-cargo-settle-profile-v2/bare-manifest.json",true)')
s=s.replace('check(player.load_equipment_manifest("diving-helmet",HELMET),"repair equipment admission")','check(player.load_equipment_manifest("diving-helmet",HELMET),"cargo equipment admission")\n check(player.load_equipment_manifest("diving-helmet","res://character/krusher-cargo-settle-profile-v2/helmet-manifest.json"),"nearest settle equipment admission")')
s=s.replace('check(texture!=null,"texture")','check(texture!=null,"texture")\n    if s.id=="carry-settle-west":check(not texture is CanvasTexture,"original nearest settle filter")')
(P/'native/review.gd').write_text(s);(P/'run_native.py').write_text((old/'run_native.py').read_text().replace(old.name,P.name));(P/'build_review.py').write_text((old/'build_review.py').read_text())
font=ImageFont.truetype(str(R/'assets/fonts/BarlowSemiCondensed-Regular.ttf'),20)
for chunk in range(0,len(records),48):
 qs=records[chunk:chunk+48];board=Image.new('RGB',(1536,60+((len(qs)+5)//6)*280),'#252b2e');draw=ImageDraw.Draw(board);draw.text((15,12),'KRUSHER DOM / CARGO HEAD FIT / '+str(chunk//48),font=font,fill='white')
 for j,q in enumerate(qs):
  im=Image.open(P/q['output']).convert('RGBA');x=j%6*256;y=50+j//6*280;board.paste(im,(x,y),im);draw.text((x+5,y+245),q['gear']+' '+q['state']+' '+str(q['frame']),font=font,fill='#bed2d3')
 board.save(P/f'head-fit-sheet-{chunk//48:02}.png')
print(json.dumps({'uniquePoses':len(records),'changed':sum(q['changedPixels']>0 for q in records),'checks':checks,'errors':[]}))
