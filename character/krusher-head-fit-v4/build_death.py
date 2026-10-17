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
C=R/'character/krusher-james-canonical-v7';cm={g:{s['id']:s for s in read(C/(g+'-manifest.json'))['states']} for g in ['bare','helmet']}
def canonical(g,key,i=0):return pad(arr(C/cm[g][key]['frameFiles'][i]))
def axis(h):
 opaque=h[:,:,3]>150;last=int(np.where(opaque)[0].max());y,x=np.where(opaque&(np.indices(h.shape[:2])[0]>=last-3));return round((int(x.min())+int(x.max()))/2)
def attached(o,n):
 labs,_=label(o[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;body=int(sizes.argmax());visible=(n[:,:,3]>180)&np.all(o==n,2);hl,_=label(visible,np.ones((3,3)));hs=np.bincount(hl.ravel());hs[0]=0;return hs.max()>0 and np.all(labs[hl==hs.argmax()]==body)
def barefit(a,original,q,prev,oldroot,hp,foreground=None):
 head=Image.open(hp).convert('RGBA');h=np.array(head);old=arr(R/q['headSource']);ax,ay=q['headPaste'];paste=[ax+axis(old)-axis(h),ay+old.shape[0]-head.height];yy,xx=np.indices(a.shape[:2]);foreground=np.zeros(a.shape[:2],bool) if foreground is None else foreground
 layer=Image.new('RGBA',(a.shape[1],a.shape[0]));source=prev['details'].get('headSource');at=prev['details'].get('paste');layer.paste(Image.open(R/source.removeprefix('res://')).convert('RGBA') if source else Image.fromarray(old),tuple(at) if at else (ax,ay));oldalpha=np.array(layer)[:,:,3]>0
 rgb=original[:,:,:3].astype(float);r,g,b=[rgb[:,:,i] for i in range(3)];skin=(r>b*1.15)&(g>b*1.12)&(r>35)&(g>r*.65);collar=(original[:,:,3]>180)&~skin&(yy>=ay+old.shape[0]-5)&(yy<ay+old.shape[0]+8)&(xx>=ax-12)&(xx<ax+old.shape[1]+12)
 remove=((np.array(Image.open(oldroot/prev['mask']).convert('L'))>0)|oldalpha)&~collar&~foreground;clean=a.copy();clean[remove]=0;restore=collar&oldalpha&~foreground;clean[restore]=original[restore];gold=restore&(r>g*1.015)&(r<g*1.8)&(g>b*1.08)&(g>35);lum=(r*.2126+g*.7152+b*.0722)/145;colour=np.clip(lum[:,:,None]*np.array([82,124,128]),0,177).astype('uint8');clean[gold,:3]=colour[gold]
 def compose(at):
  layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.alpha_composite(head,tuple(at));n=np.array(layer);admit=(n[:,:,3]>0)&~foreground&(~collar|(yy<at[1]+head.height-6));out=clean.copy();out[admit]=n[admit];return out,n,admit
 out,n,admit=compose(paste);offset=[0,0]
 if not attached(out,n):
  offsets=sorted([(dx,dy) for dx in range(-6,7) for dy in range(-4,6)],key=lambda z:(abs(z[0])+abs(z[1]),abs(z[1]),abs(z[0]),z[0],z[1]));found=False;necklocal=(h[:,:,3]>180)&(np.indices(h.shape[:2])[0]>=head.height-6)
  for dx,dy in offsets:
   at=[paste[0]+dx,paste[1]+dy];o,hn,an=compose(at);nl=Image.new('L',(a.shape[1],a.shape[0]));nl.paste(Image.fromarray(necklocal.astype('uint8')*255),tuple(at));neck=(np.array(nl)>0)&an;contact=int((binary_dilation(neck,np.ones((3,3)))&(clean[:,:,3]>180)).sum())
   if contact>=2 and attached(o,hn):out,n,admit=o,hn,an;paste=at;offset=[dx,dy];found=True;break
  if not found:raise RuntimeError((q.get('state'),q.get('newSourceIndex'),'neck'))
 return out,remove|restore|admit,{'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'paste':paste,'neckRegistrationOffset':offset,'sourceHeadShapeUnscaled':True,'collarRestoredPixels':int(restore.sum())}
def save(P,base,rel,out,mask,details,records):
 a=arr(base);assert np.array_equal(a[~mask],out[~mask]);target=P/rel;target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+rel;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr);records.append({'gear':details['gear'],'state':details.get('state','service-'+str(details.get('newSourceIndex'))),'frame':details.get('frame',details.get('newSourceIndex',0)),'source':'res://'+base.relative_to(R).as_posix(),'sourceHash':sha(base),'output':rel,'outputHash':sha(target),'mask':mr,'details':details})
OLD=R/'character/krusher-death-family-v1';PREV=R/'character/krusher-death-family-v2';P=R/'character/krusher-death-family-v3';P.mkdir(exist_ok=True);prior={q['output']:q for q in read(PREV/'revision.json')['records']};records=[];derived={}
for q in read(OLD/'provenance.json')['records']:
 g=q['gear'];v=q['state'].rsplit('-',1)[1];j=q['frame'];oldpath=PREV/q['output'];base=packed.get((g,oldpath.relative_to(R).as_posix()),oldpath);a=arr(base);yy,xx=np.indices(a.shape[:2]);out=a.copy();mask=np.zeros(a.shape[:2],bool);detail={'gear':g,'state':q['state'],'frame':j,'family':q['family']}
 if q['family']=='ground' and j==0:
  out=np.zeros_like(a);out[:256,:256]=canonical(g,'idle-'+v);mask=np.any(a!=out,2);detail['canonicalEndpoint']=v
 elif g=='bare' or v!='north':
  name=v+'-closed' if j>=3 and v in ['east','west'] else v+'-bowed' if q['family']=='ground' and v in ['east','west'] else 'south-bowed-closed' if v=='south' and j>=3 else 'south-bowed' if v=='south' else v
  if v=='north':name='north-bow'+str({0:45,1:65,2:90}[int(Path(q['headSource']).stem.split('-')[-1])]) if 'rear-bow' in q['headSource'] else 'north-bow90'
  hp=H/'sources'/('clean-bare-'+name+'-native.png');head=Image.open(hp).convert('RGBA');source=hp
  if q['family']=='ground' and v=='south' and j>=3:
   head=head.rotate(35,resample=Image.Resampling.NEAREST,expand=True);hp=P/'sources'/'clean-south-rolled-closed.png';hp.parent.mkdir(exist_ok=True);head.save(hp);derived[hp.relative_to(P).as_posix()]={'source':'res://'+source.relative_to(R).as_posix(),'sourceHash':sha(source),'rotationDegrees':35,'outputHash':sha(hp)}
  if g=='bare':
   original=arr(R/q['source']);assert original.shape==a.shape;out,mask,fit=barefit(a,original,q,prior[q['output']],PREV,hp);detail.update(fit)
  else:
   mask=np.array(Image.open(PREV/prior[q['output']]['mask']).convert('L'))>0;sy,sx=np.where(mask);sourceImage=Image.open(source);face=np.array([sourceImage.width*(.72 if v=='east' else .28 if v=='west' else .5),sourceImage.height*(.62 if v=='south' else .46)]);angle=35 if q['family']=='ground' and v=='south' and j>=3 else 0;theta=np.radians(angle);delta=face-np.array(sourceImage.size)/2;rotation=np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]]);face=rotation@delta+np.array(head.size)/2;target=np.array([sx.mean(),sy.mean()]);paste=np.rint(target-face).astype(int).tolist();layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.alpha_composite(head,tuple(paste));n=np.array(layer);opaque=n[:,:,3]>0;lining=arr(H/'sources/visor-lining-native.png');backdrop=lining[(yy-paste[1])%32,(xx-paste[0])%32,:3];out[mask,:3]=backdrop[mask];out[mask&opaque,:3]=n[mask&opaque,:3];detail.update(headSource='res://'+hp.relative_to(R).as_posix(),headHash=sha(hp),paste=paste,liningSource='res://character/krusher-head-fit-v4/sources/visor-lining-native.png',sourceHeadShapeUnscaled=True,nativeFaceLandmark=face.tolist(),apertureFaceCenter=target.tolist())
 assert np.array_equal(a[~mask],out[~mask])
 if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
 save(P,base,q['output'],out,mask,detail,records)
for family in ['ground','water']:
 for g in ['bare','helmet']:(P/(family+'-'+g+'-manifest.json')).write_bytes((PREV/(family+'-'+g+'-manifest.json')).read_bytes())
(P/'revision.json').write_text(json.dumps({'status':'unselected v4 identity death-v3; full-bank/native review pending','records':records,'derivedSources':derived},indent=2)+'\n');print(json.dumps({'outputs':len(records),'translations':[(q['state'],q['frame'],q['details'].get('neckRegistrationOffset')) for q in records if q['details'].get('neckRegistrationOffset') not in [None,[0,0]]]}))
