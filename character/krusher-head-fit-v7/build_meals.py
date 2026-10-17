from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
from scipy.ndimage import label,binary_dilation
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;BANK=R/'character/krusher-animation-package-v3';read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();index=read(BANK/'package.json');packed={}
for key,q in index['states'].items():
 g,sid=key.split(':',1);mp=BANK/q['manifest'];s=next(s for s in read(mp)['states'] if s['id']==sid)
 for old,new in zip(q['sourceFrames'],s['frameFiles']):packed[g,old]=(mp.parent/new).resolve()
def pad(a):
 out=np.zeros((256,256,4),np.uint8);out[52:52+a.shape[0],36:36+a.shape[1]]=a;return out
C=R/'character/krusher-james-canonical-v9';cm={g:{s['id']:s for s in read(C/(g+'-manifest.json'))['states']} for g in ['bare','helmet']}
def canonical(g,key,i=0):return pad(arr(C/cm[g][key]['frameFiles'][i]))
def axis(h):
 y,x=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=h.shape[0]-4));return round((int(x.min())+int(x.max()))/2)
def attached(o,n):
 labs,_=label(o[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;body=int(sizes.argmax());visible=(n[:,:,3]>180)&np.all(o==n,2);hl,_=label(visible,np.ones((3,3)));hs=np.bincount(hl.ravel());hs[0]=0;return hs.max()>0 and np.all(labs[hl==hs.argmax()]==body)
def barefit(a,original,q,prev,oldroot,hp,foreground=None):
 head=Image.open(hp).convert('RGBA');h=np.array(head);old=arr(R/q['headSource']);ax,ay=q['headPaste'];paste=[ax+axis(old)-axis(h),ay+old.shape[0]-head.height];yy,xx=np.indices(a.shape[:2]);foreground=np.zeros(a.shape[:2],bool) if foreground is None else foreground
 layer=Image.new('RGBA',(256,256));source=prev['details'].get('headSource');at=prev['details'].get('paste');layer.paste(Image.open(R/source.removeprefix('res://')).convert('RGBA') if source else Image.fromarray(old),tuple(at) if at else (ax,ay));oldalpha=np.array(layer)[:,:,3]>0
 rgb=original[:,:,:3].astype(float);r,g,b=[rgb[:,:,i] for i in range(3)];skin=(r>b*1.15)&(g>b*1.12)&(r>35)&(g>r*.65);collar=(original[:,:,3]>180)&~skin&(yy>=ay+old.shape[0]-5)&(yy<ay+old.shape[0]+8)&(xx>=ax-12)&(xx<ax+old.shape[1]+12)
 remove=((np.array(Image.open(oldroot/prev['mask']).convert('L'))>0)|oldalpha)&~collar&~foreground;clean=a.copy();clean[remove]=0;restore=collar&oldalpha&~foreground;clean[restore]=original[restore];gold=restore&(r>g*1.015)&(r<g*1.8)&(g>b*1.08)&(g>35);lum=(r*.2126+g*.7152+b*.0722)/145;colour=np.clip(lum[:,:,None]*np.array([82,124,128]),0,177).astype('uint8');clean[gold,:3]=colour[gold]
 def compose(at):
  layer=Image.new('RGBA',(256,256));layer.alpha_composite(head,tuple(at));n=np.array(layer);admit=(n[:,:,3]>0)&~foreground&(~collar|(yy<at[1]+head.height-6));out=clean.copy();out[admit]=n[admit];return out,n,admit
 out,n,admit=compose(paste);offset=[0,0]
 if not attached(out,n):
  offsets=sorted([(dx,dy) for dx in range(-6,7) for dy in range(-4,6)],key=lambda z:(abs(z[0])+abs(z[1]),abs(z[1]),abs(z[0]),z[0],z[1]));found=False;necklocal=(h[:,:,3]>180)&(np.indices(h.shape[:2])[0]>=head.height-6)
  for dx,dy in offsets:
   at=[paste[0]+dx,paste[1]+dy];o,hn,an=compose(at);nl=Image.new('L',(256,256));nl.paste(Image.fromarray(necklocal.astype('uint8')*255),tuple(at));neck=(np.array(nl)>0)&an;contact=int((binary_dilation(neck,np.ones((3,3)))&(clean[:,:,3]>180)).sum())
   if contact>=2 and attached(o,hn):out,n,admit=o,hn,an;paste=at;offset=[dx,dy];found=True;break
  if not found:raise RuntimeError((q.get('state'),q.get('newSourceIndex'),'neck'))
 return out,remove|restore|admit,{'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'paste':paste,'neckRegistrationOffset':offset,'sourceHeadShapeUnscaled':True,'collarRestoredPixels':int(restore.sum())}
def save(P,base,rel,out,mask,details,records):
 a=arr(base);assert np.array_equal(a[~mask],out[~mask]);target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+rel;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr);records.append({'gear':details['gear'],'state':details.get('state','service-'+str(details.get('newSourceIndex'))),'frame':details.get('frame',details.get('newSourceIndex',0)),'source':'res://'+base.relative_to(R).as_posix(),'sourceHash':sha(base),'output':rel,'outputHash':sha(target),'mask':mr,'details':details})
OLD=R/'character/krusher-meal-family-v1';PREV=R/'character/krusher-meal-family-v3';P=R/'character/krusher-meal-family-v5';P.mkdir(exist_ok=True);prior={q['output']:q for q in read(PREV/'revision.json')['records']};records=[];replace={}
for q in read(OLD/'provenance.json')['records']:
 g=q['gear'];d=q['state'].rsplit('-',1)[1];oldpath=PREV/q['output'];base=packed.get((g,oldpath.relative_to(R).as_posix()),oldpath);a=arr(base);detail={'gear':g,'state':q['state'],'frame':q['frame']}
 if g=='helmet':out=canonical(g,'interact-'+d,q['canonicalTabletPose']);mask=np.any(a!=out,2);detail['canonicalTabletPose']=q['canonicalTabletPose'];assert np.array_equal(a[:,:,3],out[:,:,3])
 else:
  original=arr(R/q['source']);original=pad(original) if original.shape[:2]!=(256,256) else original;hp=H/'sources'/f'clean-bare-{d}-native.png';foreground=np.array(Image.open(OLD/q['foregroundMask']).convert('L'))>0;out,mask,fit=barefit(a,original,q,prior[q['output']],PREV,hp,foreground);detail.update(fit);detail['foregroundMask']='res://'+(OLD/q['foregroundMask']).relative_to(R).as_posix();assert np.array_equal(a[foreground],out[foreground]);replace[a.tobytes()]=out
 assert np.array_equal(a[141:],out[141:]) if g=='bare' else np.array_equal(a[141:,:,3],out[141:,:,3]);save(P,base,q['output'],out,mask,detail,records)
for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_bytes((PREV/(g+'-manifest.json')).read_bytes())
(P/'revision.json').write_text(json.dumps({'status':'unselected v4 meal candidate; full-bank native review pending','records':records},indent=2)+'\n');print('meal',len(records))
for d in ['south','east','north','west']:
 mp=BANK/index['states']['bare:idle-'+d]['manifest'];s=next(s for s in read(mp)['states'] if s['id']=='idle-'+d);replace[pad(arr(mp.parent/s['frameFiles'][0])).tobytes()]=canonical('bare','idle-'+d)
OLD=R/'character/krusher-meal-service-v1';PREV=R/'character/krusher-meal-service-v3';P=R/'character/krusher-meal-service-v5';P.mkdir(exist_ok=True);prior={q['output']:q for q in read(PREV/'revision.json')['records']};records=[]
for q in read(OLD/'provenance.json')['records']:
 oldpath=PREV/q['output'];base=packed.get(('bare',oldpath.relative_to(R).as_posix()),oldpath);a=arr(base);detail={'gear':'bare','newSourceIndex':q['newSourceIndex'],'protectedFromRow':q['protectedFromRow']}
 if q['method']=='Exact canonical-v4 bare idle endpoint':
  d='north' if 'north' in q['source'] else 'south';out=canonical('bare','idle-'+d);mask=np.any(a!=out,2);detail['method']='Exact repaired canonical endpoint';detail['canonicalEndpoint']=d
 elif a.tobytes() in replace:out=replace[a.tobytes()].copy();mask=np.any(a!=out,2);detail['method']='Exact repaired meal or standing drawing'
 else:
  if not q['headSource']:raise RuntimeError(('unresolved alias',q['output']))
  d='north' if 'north' in q['headSource'] else 'south';pitch=int(Path(q['headSource']).stem.split('-')[-1]) if 'bow-heads' in q['headSource'] else None;name='clean-bare-'+d if pitch is None else {0:'clean-bare-south-bowed',1:'clean-bare-south-deep',2:'clean-bare-south-fully-bowed'}[pitch];hp=H/'sources'/(name+'-native.png');original=arr(R/q['source']);original=pad(original) if original.shape[:2]!=(256,256) else original;out,mask,fit=barefit(a,original,q,prior[q['output']],PREV,hp);detail.update(fit);detail['method']='Complete anatomical pickup head'
 assert np.array_equal(a[q['protectedFromRow']:,:,3],out[q['protectedFromRow']:,:,3]) if 'canonicalEndpoint' in detail else np.array_equal(a[q['protectedFromRow']:],out[q['protectedFromRow']:]);save(P,base,q['output'],out,mask,detail,records)
(P/'bare-manifest.json').write_bytes((PREV/'bare-manifest.json').read_bytes());(P/'revision.json').write_text(json.dumps({'status':'unselected v4 meal-service candidate; full-bank native review pending','records':records},indent=2)+'\n');print('meal service',len(records))



