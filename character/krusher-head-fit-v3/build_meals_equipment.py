from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
from scipy.ndimage import binary_dilation,distance_transform_edt
R=Path.cwd();H=R/'character/krusher-head-fit-v3';C=R/'character/krusher-james-canonical-v6'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def pad(a):
 im=Image.new('RGBA',(256,256));im.alpha_composite(Image.fromarray(a),(36,52));return np.array(im)
cm={g:{s['id']:s for s in read(C/(g+'-manifest.json'))['states']} for g in ['bare','helmet']}
def canonical(g,key,i=0):return pad(arr(C/cm[g][key]['frameFiles'][i]))
def insert(before,oldhead,oldpaste,head,paste,allowed,foreground=None):
 oldlayer=Image.new('RGBA',(256,256));oldlayer.paste(oldhead,tuple(oldpaste));remove=(np.array(oldlayer)[:,:,3]>0)&allowed;out=before.copy();out[remove]=0
 layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(paste));ha=np.array(layer);opaque=ha[:,:,3]>0;out[opaque]=ha[opaque];mask=remove|opaque
 if foreground is not None:out[foreground]=before[foreground];mask&=~foreground
 return out,mask
def save(P,OLD,rel,out,mask,details,proof):
 a=arr(OLD/rel);assert np.array_equal(a[~mask],out[~mask]);target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+rel;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr);proof.append({'source':'res://'+(OLD/rel).relative_to(R).as_posix(),'sourceHash':sha(OLD/rel),'output':rel,'outputHash':sha(target),'mask':mr,'changedPixels':int(np.any(a!=out,2).sum()),'details':details})
def finish(P,OLD,names,proof):
 for name in names:(P/name).write_bytes((OLD/name).read_bytes())
 (P/'revision.json').write_text(json.dumps({'records':proof,'scope':'Complete head/neck revision on original body; original full manifest bytes, original foreground utensils and equipment preserved. Partial staged all-library candidate.'},indent=2)+'\n');(P/'native').mkdir(exist_ok=True)
 for name in ['review.gd']:(P/'native'/name).write_text((OLD/'native'/name).read_text().replace(OLD.name,P.name))
 for name in ['run_native.py','build_review.py']:(P/name).write_text((OLD/name).read_text().replace(OLD.name,P.name))
 print(json.dumps({'pack':P.name,'uniqueRecords':len(proof),'changed':sum(q['changedPixels']>0 for q in proof)}))
OLD=R/'character/krusher-meal-family-v1';P=R/'character/krusher-meal-family-v3';P.mkdir(exist_ok=True);proof=[]
for q in read(OLD/'provenance.json')['records']:
 g=q['gear'];d=q['state'].rsplit('-',1)[1];a=arr(OLD/q['output']);out=a.copy();mask=np.zeros((256,256),bool);detail={'gear':g,'state':q['state'],'frame':q['frame'],'protectedFromRow':141}
 if g=='helmet':out=canonical(g,'interact-'+d,q['canonicalTabletPose']);mask=np.any(a!=out,2);detail['canonicalTabletPose']=q['canonicalTabletPose'];assert np.array_equal(a[:,:,3],out[:,:,3])
 elif d!='north':
  hp=H/'sources'/f'bare-{d}-native.png';head=Image.open(hp).convert('RGBA');oldhead=Image.open(R/q['headSource']).convert('RGBA');ax,ay=q['headPaste'];paste=[ax-4 if d=='east' else ax+2 if d=='west' else ax-(head.width-oldhead.width)//2,ay];foreground=np.array(Image.open(OLD/q['foregroundMask']))>0;allowed=np.array(Image.open(OLD/q['allowedMask']))>0;out,mask=insert(a,oldhead,[ax,ay],head,paste,allowed,foreground);detail.update(headSource='res://'+hp.relative_to(R).as_posix(),headHash=sha(hp),paste=paste,foregroundMask='res://'+(OLD/q['foregroundMask']).relative_to(R).as_posix());assert np.array_equal(a[foreground],out[foreground])
 assert np.array_equal(a[141:],out[141:]);save(P,OLD,q['output'],out,mask,detail,proof)
finish(P,OLD,['bare-manifest.json','helmet-manifest.json'],proof)

OLD=R/'character/krusher-helmet-transition-v1';P=R/'character/krusher-helmet-transition-v3';P.mkdir(exist_ok=True);proof=[];m=read(OLD/'manifest.json');outputs={};yy,xx=np.indices((256,256))
for q in read(OLD/'provenance.json')['records']:
 i=q['pose'];rel=m['states'][0]['frameFiles'][i];a=arr(OLD/rel);out=a.copy();mask=np.zeros((256,256),bool);detail={'pose':i,'protectedFromRow':138}
 if i in [0,11]:g='bare' if i==0 else 'helmet';out=canonical(g,'idle-east');mask=np.any(a!=out,2);detail['canonicalEndpoint']=g
 elif q['faceBox'] is None:
  hp=H/'sources/bare-east-native.png';head=Image.open(hp).convert('RGBA');oldhead=Image.open(R/'character/krusher-bill-base-test-v2/sources/east-head-native.png').convert('RGBA');ax,ay=q['headPaste'];paste=[ax-4,ay];allowed=np.array(Image.open(OLD/f'masks/{i:03}-head.png'))>0;out,mask=insert(a,oldhead,[ax,ay],head,paste,allowed);detail.update(headSource='res://'+hp.relative_to(R).as_posix(),headHash=sha(hp),paste=paste)
 else:
  hp=H/'sources/visor-east-native.png';head=Image.open(hp).convert('RGBA');x0,y0,x1,y1=q['faceBox'];original=arr(R/q['source']);rgb=original[:,:,:3].astype(float);base=np.array(Image.open(OLD/f'masks/{i:03}-head.png'))>0;mask=binary_dilation(base,iterations=2)
  for dy in range(1,5):mask[:-dy]|=base[dy:]
  glass=(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2);metal=(rgb.max(2)-rgb.min(2)<12)&(rgb.mean(2)>75)&(yy<y0);mask&=(xx>=x0-1)&(xx<x1+1)&(yy>=y0-4)&(yy<y1+1)&~glass&~metal&(a[:,:,3]>180)
  if i==5:mask&=xx>=120
  sy,sx=np.where(mask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)];part=np.array(head);nearest=distance_transform_edt(part[:,:,3]==0,return_distances=False,return_indices=True);part[:,:,:3]=part[nearest[0],nearest[1],:3];part[:,:,3]=255;fit=Image.fromarray(part).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST);layer=Image.new('RGBA',(256,256));layer.paste(fit,(box[0],box[1]));out[mask,:3]=np.array(layer)[mask,:3];detail.update(headSource='res://'+hp.relative_to(R).as_posix(),headHash=sha(hp),visorBox=box,partialFaceForegroundProtected=i==5);assert np.array_equal(a[:,:,3],out[:,:,3])
 assert np.array_equal(a[138:],out[138:]);save(P,OLD,rel,out,mask,detail,proof);outputs[i]=out
for s in m['states']:
 for rel,i in zip(s['frameFiles'],s['sourcePoseIndices']):target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(outputs[i]).save(target)
finish(P,OLD,['manifest.json'],proof)

# Indexed meal service/cancel poses reuse exact corrected meal drawings. Deep
# South source heads follow the original pitch family; rear poses stay intact.
OLD=R/'character/krusher-meal-service-v1';P=R/'character/krusher-meal-service-v3';P.mkdir(exist_ok=True);proof=[];replace={};mealold=R/'character/krusher-meal-family-v1';mealnew=R/'character/krusher-meal-family-v3'
for q in read(mealnew/'revision.json')['records']:
 if q['details']['gear']=='bare':replace[arr(mealold/q['output']).tobytes()]=arr(mealnew/q['output'])
oldcan=R/'character/krusher-james-canonical-v4'
for d in ['south','east','north','west']:
 s=next(s for s in read(oldcan/'bare-manifest.json')['states'] if s['id']=='idle-'+d);replace[pad(arr(oldcan/s['frameFiles'][0])).tobytes()]=canonical('bare','idle-'+d)
for q in read(OLD/'provenance.json')['records']:
 a=arr(OLD/q['output']);out=a.copy();mask=np.zeros((256,256),bool);detail={'protectedFromRow':q['protectedFromRow'],'newSourceIndex':q['newSourceIndex'],'method':'Rear source retained'}
 if a.tobytes() in replace:out=replace[a.tobytes()].copy();mask=np.any(a!=out,2);detail['method']='Exact corrected shared meal or standing endpoint'
 elif q['headSource'] and 'bow-heads' in q['headSource']:
  oldhead=Image.open(R/q['headSource']).convert('RGBA');pitch=int(Path(q['headSource']).stem.split('-')[-1]);name={0:'bare-south-bowed',1:'bare-south-deep',2:'bare-south-fully-bowed'}[pitch];hp=H/'sources'/f'{name}-native.png';head=Image.open(hp).convert('RGBA');ax,ay=q['headPaste'];paste=[ax-(head.width-oldhead.width)//2,ay+oldhead.height-head.height];allowed=np.array(Image.open(OLD/q['allowedMask']))>0;out,mask=insert(a,oldhead,[ax,ay],head,paste,allowed);detail.update(method='Complete pitched South identity on original pickup body',headSource='res://'+hp.relative_to(R).as_posix(),headHash=sha(hp),paste=paste,pitch=pitch)
 assert np.array_equal(a[q['protectedFromRow']:],out[q['protectedFromRow']:]);save(P,OLD,q['output'],out,mask,detail,proof)
finish(P,OLD,['bare-manifest.json'],proof)
