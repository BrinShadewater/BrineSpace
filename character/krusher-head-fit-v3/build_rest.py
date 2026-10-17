from pathlib import Path
from PIL import Image
from scipy.ndimage import binary_dilation,distance_transform_edt
import json,numpy as np,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;OLD=R/'character/krusher-rest-family-v2';PREV=R/'character/krusher-rest-family-v3';P=R/'character/krusher-rest-family-v4';P.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
previous={q['output']:q for q in read(PREV/'revision.json')['records']};yy,xx=np.indices((256,256));records=[];derived={}
for q in read(OLD/'provenance.json')['records']:
 g,v,tilt=q['gear'],q['view'],q['tilt'];a=arr(OLD/q['output']);out=a.copy();mask=np.zeros((256,256),bool);details={};kind='bare' if g=='bare' else 'visor'
 if v!='north':
  name=f'rest-{v}-closed' if v in ['east','west'] and tilt==80 else 'rest-south-raised-closed' if v=='south' and tilt==80 else 'rest-south-raised-open' if v=='south' and tilt>=30 else v
  hp=H/'sources'/f'{kind}-{name}-native.png';head=Image.open(hp).convert('RGBA');source=hp
  if v in ['east','west'] and tilt:
   hp=P/'sources'/f'{kind}-{name}-tilt-{tilt}.png';hp.parent.mkdir(exist_ok=True);angle=tilt if v=='east' else -tilt;head=head.rotate(angle,resample=Image.Resampling.NEAREST,expand=True);head.save(hp);derived[hp.relative_to(P).as_posix()]={'source':'res://'+source.relative_to(R).as_posix(),'sourceHash':sha(source),'angle':angle,'resample':'nearest','outputHash':sha(hp)}
  details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'tilt':tilt,'sourceKind':name}
  if g=='bare':
   oldhead=Image.open(R/q['headSource']).convert('RGBA');oldlayer=Image.new('RGBA',(256,256));oldlayer.paste(oldhead,tuple(q['headPaste']));remove=(np.array(oldlayer)[:,:,3]>0)&(np.array(Image.open(OLD/q['allowedMask']))>0);out[remove]=0
   body=np.array(q['bodyAxis']);hy,hx=np.where(np.array(head)[:,:,3]>180);projection=hx*body[0]+hy*body[1];near=projection>projection.max()-2;native_neck=np.array([hx[near].mean(),hy[near].mean()]);paste=np.rint(np.array(q['neck'])-native_neck).astype(int).tolist()
   layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(paste));ha=np.array(layer);opaque=ha[:,:,3]>0;out[opaque]=ha[opaque];mask=remove|opaque;details.update(paste=paste,bodyAxis=q['bodyAxis'],neck=q['neck'],nativeNeck=native_neck.tolist(),oldPaste=q['headPaste'])
  else:
   base=np.array(Image.open(PREV/previous[q['output']]['mask']))>0;original=arr(R/q['source']);rgb=original[:,:,:3].astype(float);by,bx=np.where(base);box=[int(bx.min()),int(by.min()),int(bx.max()+1),int(by.max()+1)]
   # Keep the recorded original visor aperture. Full hair/face identity fills
   # its finite window; original glass, shell and alpha remain untouched.
   mask=base.copy();part=np.array(head);nearest=distance_transform_edt(part[:,:,3]==0,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;fit=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(256,256));layer.paste(fit,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];details['visorBox']=box
 assert np.array_equal(a[~mask],out[~mask])
 if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
 target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
 records.append({'gear':g,'state':q['state'],'frame':q['frame'],'view':v,'source':'res://'+(OLD/q['output']).relative_to(R).as_posix(),'sourceHash':sha(OLD/q['output']),'output':q['output'],'outputHash':sha(target),'mask':mr,'changedPixels':int(np.any(a!=out,2).sum()),'details':details})
for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_bytes((OLD/(g+'-manifest.json')).read_bytes())
(P/'revision.json').write_text(json.dumps({'records':records,'derivedSources':derived,'scope':'Complete H3 head-neck and closed-eye/raised-chin identity on original resting bodies. Whole original manifest bytes/pivots/clocks/furniture flags exact; original shell alpha unchanged. Rear retained. Partial full-library candidate.'},indent=2)+'\n')
(P/'pack-index.json').write_text(json.dumps({'candidatePacks':{g:['res://'+(P/(g+'-manifest.json')).relative_to(R).as_posix()] for g in ['bare','helmet']}},indent=2)+'\n')
(P/'native').mkdir(exist_ok=True);(P/'native/review.gd').write_text((PREV/'native/review.gd').read_text().replace(PREV.name,P.name))
for name in ['run_native.py','build_review.py']:(P/name).write_text((PREV/name).read_text().replace(PREV.name,P.name))
print(json.dumps({'unique':len(records),'changed':sum(q['changedPixels']>0 for q in records),'derivedSources':len(derived)}))
