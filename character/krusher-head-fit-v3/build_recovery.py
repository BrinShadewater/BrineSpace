from pathlib import Path
from PIL import Image
from scipy.ndimage import distance_transform_edt,binary_fill_holes
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;OLD=R/'character/krusher-recovery-salvage-v1';P=R/'character/krusher-recovery-salvage-v2';C=R/'character/krusher-james-canonical-v6';P.mkdir(exist_ok=True);read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
records=[]
for q in read(OLD/'provenance.json')['records']:
 g=q['gear'];v=q['state'].rsplit('-',1)[1];a=arr(OLD/q['output']);out=a.copy();hh,ww=a.shape[:2];yy,xx=np.indices((hh,ww));mask=np.zeros((hh,ww),bool);details={}
 if 'canonical idle' in q['method']:
  m=read(C/(g+'-manifest.json'));s=next(s for s in m['states'] if s['id']=='idle-'+v);im=Image.new('RGBA',(ww,hh));im.alpha_composite(Image.open(C/s['frameFiles'][0]).convert('RGBA'),(36,52));out=np.array(im);mask=np.any(a!=out,2);details={'canonicalEndpoint':v}
 elif v!='north':
  bowed='bow-heads' in q['headSource'];name='south-fully-bowed' if v=='south' and q['family']=='salvage' else 'south-bowed' if bowed else v;kind='bare' if g=='bare' else 'visor'
  hp=H/'sources'/f'{kind}-{name}-native.png'
  # The deep South authored visor is the full identity excluding the final
  # neck ring, derived from its transparent full head, not a new shell.
  if not hp.exists() and g=='helmet' and name=='south-fully-bowed':
   source=H/'sources/bare-south-fully-bowed-native.png';head=Image.open(source).convert('RGBA');head.crop((0,0,head.width,head.height-3)).save(hp)
  head=Image.open(hp).convert('RGBA');details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'sourceKind':name}
  if g=='helmet' and name=='south-fully-bowed':
   source=H/'sources/bare-south-fully-bowed-native.png';im=Image.open(source).convert('RGBA');crop=[0,0,im.width,im.height-3];assert np.array_equal(np.array(head),np.array(im.crop(crop)));details['derivedVisorSource']={'source':'res://'+source.relative_to(R).as_posix(),'sourceHash':sha(source),'nativeCrop':crop}
  foreground=np.zeros_like(mask)
  if q['family']=='salvage':foreground=((xx>=158)&(yy>=133)&(yy<153)) if v=='east' else ((xx<=105)&(yy>=133)&(yy<153)) if v=='west' else yy>=157
  if g=='bare':
   oldhead=Image.open(R/q['headSource']).convert('RGBA');ax,ay=q['headPaste'];oldlayer=Image.new('RGBA',(ww,hh));oldlayer.paste(oldhead,(ax,ay));remove=(np.array(oldlayer)[:,:,3]>0)&(np.array(Image.open(OLD/q['allowedMask']))>0)&~foreground;out[remove]=0
   paste=[ax-(head.width-oldhead.width)//2,ay+oldhead.height-head.height] if bowed else [ax-4 if v=='east' else ax+2 if v=='west' else ax-(head.width-oldhead.width)//2,ay]
   if q['family']=='salvage' and v=='south':paste[1]-=3;details['projectedBackCollarRegistration']=[0,-3]
   layer=Image.new('RGBA',(ww,hh));layer.paste(head,tuple(paste));ha=np.array(layer);opaque=(ha[:,:,3]>0)&~foreground;out[opaque]=ha[opaque];mask=remove|opaque;details.update(paste=paste,oldPaste=[ax,ay])
  else:
   allowed=np.array(Image.open(OLD/q['allowedMask']))>0;rgb=a[:,:,:3].astype(float);recoloured=(rgb[:,:,1]>rgb[:,:,0]*1.25)&(rgb[:,:,2]>rgb[:,:,0]*1.25);base=binary_fill_holes(allowed&~recoloured);x0,y0,x1,y1=q['headBox'];mask=base&(xx>=x0-9)&(xx<x1+9)&(yy>=y0-9)&(yy<y1+8)&~foreground
   sy,sx=np.where(mask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)];part=np.array(head);nearest=distance_transform_edt(part[:,:,3]==0,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;fit=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(ww,hh));layer.paste(fit,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];details['visorBox']=box
  out[foreground]=a[foreground];mask&=~foreground;details['originalToolForegroundProtected']=q['family']=='salvage'
 assert np.array_equal(a[~mask],out[~mask])
 if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
 target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
 records.append({'gear':g,'family':q['family'],'state':q['state'],'frame':q['frame'],'source':'res://'+(OLD/q['output']).relative_to(R).as_posix(),'sourceHash':sha(OLD/q['output']),'output':q['output'],'outputHash':sha(target),'mask':mr,'changedPixels':int(np.any(a!=out,2).sum()),'details':details})
for family in ['recovery','salvage']:
 for g in ['bare','helmet']:(P/f'{family}-{g}-manifest.json').write_bytes((OLD/f'{family}-{g}-manifest.json').read_bytes())
(P/'revision.json').write_text(json.dumps({'records':records,'scope':'Complete H3 head/neck and full visor identity on original recovery/salvage bodies and tools. Full original manifests exact, canonical-v6 recovery endings. Rear source retained; partial full-library candidate.'},indent=2)+'\n')
(P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://'+(P/f'{f}-{g}-manifest.json').relative_to(R).as_posix() for f in ['recovery','salvage']] for g in ['bare','helmet']}},indent=2)+'\n');(P/'native').mkdir(exist_ok=True)
native=(OLD/'native/review.gd').read_text().replace(OLD.name,P.name).replace('res://character/krusher-complete-animation-v1/progress.json','res://character/krusher-recovery-salvage-v2/pack-index.json');(P/'native/review.gd').write_text(native)
for name in ['run_native.py','build_review.py']:(P/name).write_text((OLD/name).read_text().replace(OLD.name,P.name))
media=(P/'build_review.py').read_text().replace("\\nduration {hold/1000:.9f}","\\noption framerate 1000\\nduration {hold/1000:.9f}").replace("file 'video-frames/{name}'\\n\")","file 'video-frames/{name}'\\noption framerate 1000\\n\")").replace("'-vf','fps=60'","'-t',str(clock),'-vf','fps=60'");(P/'build_review.py').write_text(media)
print(json.dumps({'unique':len(records),'changed':sum(q['changedPixels']>0 for q in records)}))
