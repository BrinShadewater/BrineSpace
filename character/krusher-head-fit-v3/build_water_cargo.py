from pathlib import Path
import json,hashlib
from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes,distance_transform_edt

R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;OLD=R/'character/krusher-water-cargo-turns-v2';P=R/'character/krusher-water-cargo-turns-v3';P.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def ph(p):
 im=Image.open(p).convert('RGBA');return hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest()
seed={}
for old,new in [('krusher-water-family-v1','krusher-water-family-v3'),('krusher-recovery-salvage-v1','krusher-recovery-salvage-v2')]:
 for q in read(R/'character'/old/'provenance.json')['records']:
  if q['family'] not in ['water','salvage']:continue
  target=R/'character'/new/q['output'];assert target.exists();seed[(q['gear'],ph(R/q['source']))] = target
records=[];provenance=[]
for q in read(OLD/'provenance.json')['records']:
 g=q['gear'];v=q['view'];a=arr(OLD/q['output']);original=arr(R/q['source']);out=a.copy();yy,xx=np.indices(a.shape[:2]);details={};mask=np.zeros(a.shape[:2],bool)
 seedpath=seed.get((g,ph(R/q['source'])))
 if seedpath:
  out=arr(seedpath);mask=np.any(out!=a,2);details={'sharedCompletePose':'res://'+seedpath.relative_to(R).as_posix()}
 elif v!='north':
  name=v if v in ['se','sw','ne','nw','east','west'] else 'south-bowed';kind='bare' if g=='bare' else 'visor';hp=H/'sources'/f'{kind}-{name}-native.png'
  if not hp.exists() and g=='helmet' and v in ['ne','nw']:hp=H/'sources'/f'visor-{"east" if v=="ne" else "west"}-native.png'
  head=Image.open(hp).convert('RGBA');details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp)};x0,y0,x1,y1=q['headBox'];oldhead=Image.open(R/q['headSource']).convert('RGBA');ax,ay=q['headPaste'];allowed=np.array(Image.open(OLD/q['allowedMask']))>0
  foreground=((xx>=x1+5)&(yy<y1+7))|(xx>=x1+25) if v=='east' else ((xx<x0-5)&(yy<y1+7))|(xx<x0-25) if v=='west' else yy>=y1+4 if v=='south' else ((yy>=y1+5)|((xx>x1+12) if v=='se' else (xx<x0-12))) if v in ['se','sw'] else (yy<y0-18)|((xx>x1+8) if v=='ne' else (xx<x0-8))
  if g=='bare':
   oldlayer=Image.new('RGBA',(a.shape[1],a.shape[0]));oldlayer.paste(oldhead,(ax,ay));remove=(np.array(oldlayer)[:,:,3]>0)&allowed&~foreground;out[remove]=0
   paste=[ax-4 if v=='east' else ax+2 if v=='west' else ax-(head.width-oldhead.width)//2,ay if v in ['east','west'] else ay-3 if v=='south' else ay+oldhead.height-head.height]
   if q['state']=='swim-turn-north-south' and q['frame']==2:paste[1]+=1;details['observedNeckRegistration']=[0,1]
   layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.paste(head,tuple(paste));ha=np.array(layer);opaque=(ha[:,:,3]>0)&~foreground;out[opaque]=ha[opaque];mask=remove|opaque;details.update(paste=paste,oldPaste=[ax,ay],foregroundClippedPixels=int(((ha[:,:,3]>180)&foreground).sum()))
  else:
   rgb=a[:,:,:3].astype(float);cyan=(rgb[:,:,1]>rgb[:,:,0]*1.25)&(rgb[:,:,2]>rgb[:,:,0]*1.25)
   mask=binary_fill_holes(allowed&~cyan)&(xx>=x0-9)&(xx<x1+9)&(yy>=y0-9)&(yy<y1+8)&~foreground
   apertures={('swim-turn-south-west',1):[110,129,124,149],('swim-turn-south-west',2):[106,124,121,143],('swim-turn-north-east',1):[141,111,146,122],('swim-turn-north-south',1):[141,111,146,122],('swim-carry-turn-north-east',2):[140,110,147,123],('swim-carry-turn-north-west',3):[106,110,111,120],('swim-carry-turn-south-west',1):[111,137,129,150],('swim-carry-turn-south-west',2):[106,129,120,145]}
   if v in ['ne','nw','sw']:
    restoration=allowed&(xx>=x0-12)&(xx<x1+12)&(yy>=y0-15)&(yy<y1+1);out[restoration]=original[restoration]
    aperture=apertures.get((q['state'],q['frame']))
    if aperture:
     bx0,by0,bx1,by1=aperture;mask=binary_fill_holes(allowed)&(xx>=bx0)&(xx<bx1)&(yy>=by0)&(yy<by1)&~foreground
    else:mask=np.zeros_like(mask)
    details['observedVisorAperture']=aperture;details['originalShellRestored']=True
   if not mask.any():
    mask=restoration;details['noVisibleFace']=True
   else:
    faceMask=mask.copy()
    sy,sx=np.where(faceMask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)];part=np.array(head);near=distance_transform_edt(part[:,:,3]==0,return_distances=False,return_indices=True);part[:,:,:3]=part[near[0],near[1],:3];part[:,:,3]=255
    fitted=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.paste(fitted,(box[0],box[1]));out[faceMask,:3]=np.array(layer)[faceMask,:3];details['visorBox']=box
    if v in ['ne','nw','sw']:mask|=restoration
  out[foreground]=a[foreground];mask&=~foreground
 assert np.array_equal(a[~mask],out[~mask])
 if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
 target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
 records.append({'gear':g,'state':q['state'],'frame':q['frame'],'view':v,'output':q['output'],'source':'res://'+(OLD/q['output']).relative_to(R).as_posix(),'sourceHash':sha(OLD/q['output']),'outputHash':sha(target),'mask':mr,'details':details,'changedPixels':int(np.any(out!=a,2).sum())})
 combined=np.array(Image.open(OLD/q['allowedMask']))>0;combined|=mask;mp=P/q['allowedMask'];mp.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(combined.astype('uint8')*255).save(mp);n=q.copy();n['outputHash']=sha(target);provenance.append(n)
for f in ['cargo','turn','cargo-turn']:
 for g in ['bare','helmet']:(P/f'{f}-{g}-manifest.json').write_bytes((OLD/f'{f}-{g}-manifest.json').read_bytes())
(P/'revision.json').write_text(json.dumps({'records':records},indent=2)+'\n');(P/'provenance.json').write_text(json.dumps({'records':provenance},indent=2)+'\n')
validator=(OLD/'validate.py').read_text().replace('krusher-water-family-v1','krusher-water-family-v3').replace('krusher-recovery-salvage-v1','krusher-recovery-salvage-v2');(P/'validate.py').write_text(validator)
(P/'native').mkdir(exist_ok=True);native=(OLD/'native/review.gd').read_text().replace(OLD.name,P.name).replace('res://character/krusher-complete-animation-v1/progress.json','res://character/krusher-water-cargo-turns-v3/pack-index.json');(P/'native/review.gd').write_text(native)
(P/'run_native.py').write_text((OLD/'run_native.py').read_text().replace(OLD.name,P.name));(P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://character/krusher-water-family-v3/water-'+g+'-manifest.json','res://character/krusher-recovery-salvage-v2/salvage-'+g+'-manifest.json']+['res://character/'+P.name+'/'+f+'-'+g+'-manifest.json' for f in ['cargo','turn','cargo-turn']] for g in ['bare','helmet']}},indent=2)+'\n')
(P/'build_review.py').write_text((OLD/'build_review.py').read_text())
print(json.dumps({'unique':len(records),'revised':sum(q['changedPixels']>0 for q in records),'sharedPoses':sum('sharedCompletePose' in q['details'] for q in records)}))
