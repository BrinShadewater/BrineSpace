from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import distance_transform_edt,binary_fill_holes,label,binary_dilation
from scipy.spatial import ConvexHull
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;OLD=R/'character/krusher-death-family-v1';P=R/'character/krusher-death-family-v2';C=R/'character/krusher-james-canonical-v6';P.mkdir(exist_ok=True);read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();arr=lambda p:np.array(Image.open(p).convert('RGBA'))
records=[];provenance=[]
for q in read(OLD/'provenance.json')['records']:
 g=q['gear'];v=q['state'].rsplit('-',1)[1];j=q['frame'];a=arr(OLD/q['output']);out=a.copy();yy,xx=np.indices(a.shape[:2]);mask=np.zeros(a.shape[:2],bool);details={}
 if q['family']=='ground' and j==0:
  m=read(C/(g+'-manifest.json'));s=next(s for s in m['states'] if s['id']=='idle-'+v);im=Image.new('RGBA',(256,360));im.alpha_composite(Image.open(C/s['frameFiles'][0]).convert('RGBA'),(36,52));out=np.array(im);mask=np.any(a!=out,2);details={'canonicalIdle':'res://'+(C/s['frameFiles'][0]).relative_to(R).as_posix(),'padding':[36,52]}
 elif v!='north':
  name='death-'+v+'-closed' if j>=3 and v in ['east','west'] else v+'-bowed' if q['family']=='ground' and v in ['east','west'] else 'death-south-bowed-closed' if v=='south' and j>=3 else 'south-bowed' if v=='south' else v
  kind='bare' if g=='bare' else 'visor';hp=H/'sources'/f'{kind}-{name}-native.png';head=Image.open(hp).convert('RGBA');details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'sourceKind':name}
  if q['family']=='ground' and v=='south' and j>=3 and g=='bare':
   source=hp;head=head.rotate(35,resample=Image.Resampling.NEAREST,expand=True);hp=H/'sources/bare-death-south-rolled-native.png';head.save(hp);details.update(headSource='res://'+hp.relative_to(R).as_posix(),headHash=sha(hp),rigidSource='res://'+source.relative_to(R).as_posix(),rigidSourceHash=sha(source),rotationDegrees=35)
  x0,y0,x1,y1=q['headBox'];ax,ay=q['headPaste'];allowed=np.array(Image.open(OLD/q['allowedMask']))>0
  if g=='bare':
   oldhead=Image.open(R/q['headSource']).convert('RGBA');layer=Image.new('RGBA',(256,360));layer.paste(oldhead,(ax,ay));remove=(np.array(layer)[:,:,3]>0)&allowed;out[remove]=0
   paste=[ax-(head.width-oldhead.width)//2,ay+oldhead.height-head.height]
   if q['family']=='water' and v in ['east','west'] and j<3:paste=[ax-4 if v=='east' else ax+2,ay]
   if q['family']=='water' and v=='south':paste[1]=ay-3
   adjustments={('death-ground-east',2):[0,2],('death-ground-south',1):[0,1],('death-ground-south',2):[0,1],('death-ground-west',1):[3,0],('death-ground-west',2):[3,0],('death-ground-south',4):[2,0],('death-ground-south',5):[3,0]}
   adjustment=adjustments.get((q['state'],j),[0,0]);paste=[paste[0]+adjustment[0],paste[1]+adjustment[1]];details['neckRegistrationAdjustment']=adjustment
   layer=Image.new('RGBA',(256,360));layer.paste(head,tuple(paste));ha=np.array(layer);opaque=ha[:,:,3]>0;out[opaque]=ha[opaque];mask=remove|opaque;details['paste']=paste
  else:
   rgb=a[:,:,:3].astype(float);cyan=(rgb[:,:,1]>rgb[:,:,0]*1.25)&(rgb[:,:,2]>rgb[:,:,0]*1.25);mask=binary_fill_holes(allowed&~cyan)&(xx>=x0-9)&(xx<x1+9)&(yy>=y0-9)&(yy<y1+8)
   original=arr(R/q['source']);rgb=original[:,:,:3].astype(float);skin=(original[:,:,3]>180)&(rgb[:,:,0]>rgb[:,:,1]*1.1)&(rgb[:,:,0]>rgb[:,:,2]*1.12)&(rgb[:,:,2]>rgb[:,:,1]*.55)&(rgb.mean(2)>45)&(xx>=x0-8)&(xx<x1+8)&(yy>=y0-8)&(yy<y1+16)
   labs,count=label(skin);sizes=np.bincount(labs.ravel());main=sizes[1:].argmax()+1;sy,sx=np.where(labs==main);points=np.column_stack([sx,sy]);hull=ConvexHull(points);face=Image.new('L',(256,360));polygon=[list(map(int,points[k])) for k in hull.vertices];ImageDraw.Draw(face).polygon(polygon,fill=255);mask=np.array(face)>0;details['originalSkinVisorPolygon']=polygon
   originalCyan=(rgb[:,:,1]>rgb[:,:,0]*1.25)&(rgb[:,:,2]>rgb[:,:,0]*1.25);leak=allowed&cyan&~originalCyan&binary_dilation(mask,iterations=3)&~mask;out[leak]=original[leak];details['restoredOriginalFaceEdgePixels']=int(leak.sum())
   sy,sx=np.where(mask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)];part=np.array(head);near=distance_transform_edt(part[:,:,3]==0,return_distances=False,return_indices=True);part[:,:,:3]=part[near[0],near[1],:3];part[:,:,3]=255;fit=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(256,360));layer.paste(fit,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];details['visorBox']=box
   mask|=leak
 assert np.array_equal(a[~mask],out[~mask])
 if g=='helmet' and 'canonicalIdle' not in details:assert np.array_equal(a[:,:,3],out[:,:,3])
 target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
 records.append({'gear':g,'state':q['state'],'frame':j,'view':v,'output':q['output'],'source':'res://'+(OLD/q['output']).relative_to(R).as_posix(),'sourceHash':sha(OLD/q['output']),'outputHash':sha(target),'mask':mr,'details':details,'changedPixels':int(np.any(out!=a,2).sum())})
 combined=(np.array(Image.open(OLD/q['allowedMask']))>0)|mask;mp=P/q['allowedMask'];mp.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(combined.astype('uint8')*255).save(mp);n=q.copy();n['outputHash']=sha(target);provenance.append(n)
for family in ['ground','water']:
 for g in ['bare','helmet']:(P/f'{family}-{g}-manifest.json').write_bytes((OLD/f'{family}-{g}-manifest.json').read_bytes())
(P/'revision.json').write_text(json.dumps({'records':records},indent=2)+'\n');(P/'provenance.json').write_text(json.dumps({'records':provenance},indent=2)+'\n')
(P/'validate.py').write_text((OLD/'validate.py').read_text().replace('krusher-james-canonical-v4','krusher-james-canonical-v6').replace('padded=np.pad(a,((52,124),(36,36),(0,0)))', "canvas=Image.new('RGBA',(256,360));canvas.alpha_composite(Image.fromarray(a),(36,52));padded=np.array(canvas)"))
(P/'native').mkdir(exist_ok=True);(P/'native/review.gd').write_text((OLD/'native/review.gd').read_text().replace(OLD.name,P.name).replace('res://character/krusher-complete-animation-v1/progress.json','res://character/krusher-death-family-v2/pack-index.json'))
(P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://character/'+P.name+'/'+f+'-'+g+'-manifest.json' for f in ['ground','water']] for g in ['bare','helmet']}},indent=2)+'\n')
for name in ['run_native.py','build_review.py']:(P/name).write_text((OLD/name).read_text().replace(OLD.name,P.name))
print(json.dumps({'unique':len(records),'revised':sum(q['changedPixels']>0 for q in records)}))
