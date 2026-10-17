from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
from scipy.ndimage import label,binary_dilation
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;OLD=R/'character/krusher-cargo-family-v1';PREV=R/'character/krusher-cargo-family-v3';P=R/'character/krusher-cargo-family-v4';P.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
index=read(R/'character/krusher-animation-package-v3/package.json');BANK=R/'character/krusher-animation-package-v3';packed={}
for key,q in index['states'].items():
 g,sid=key.split(':',1);mp=BANK/q['manifest'];state=next(s for s in read(mp)['states'] if s['id']==sid)
 for old,new in zip(q['sourceFrames'],state['frameFiles']):packed[g,old]=(mp.parent/new).resolve()
originals=read(OLD/'provenance.json')['records'];prior={q['output']:q for q in read(PREV/'revision.json')['records']};paired={(q['state'],q['frame']):q for q in originals if q['gear']=='helmet'}
canonical={};oldidle={}
for g in ['bare','helmet']:
 mp=BANK/index['states'][g+':idle-south']['manifest'];m=read(mp);newm=read(R/'character/krusher-james-canonical-v7'/(g+'-manifest.json'))
 for d in ['south','east','north','west']:
  s=next(s for s in m['states'] if s['id']=='idle-'+d);a=arr(mp.parent/s['frameFiles'][0]);pad=np.zeros((256,256,4),np.uint8);pad[52:236,36:220]=a;oldidle[g,d]=pad
  s=next(s for s in newm['states'] if s['id']=='idle-'+d);a=arr(R/'character/krusher-james-canonical-v7'/s['frameFiles'][0]);pad=np.zeros((256,256,4),np.uint8);pad[52:236,36:220]=a;canonical[g,d]=pad

def axis(h):
 y,x=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=h.shape[0]-4));return round((int(x.min())+int(x.max()))/2)
def primary_connected(out,head):
 labs,_=label(out[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;body=int(sizes.argmax());visible=(head[:,:,3]>180)&np.all(out==head,2);hl,_=label(visible,np.ones((3,3)));hs=np.bincount(hl.ravel());hs[0]=0
 return not hs.max() or np.all(labs[hl==hs.argmax()]==body)
records=[]
for q in originals:
 g,v=q['gear'],q['view'];prev=prior[q['output']];path=PREV/q['output'];base=packed.get((g,path.relative_to(R).as_posix()),path);a=arr(base);original=arr(R/q['source']);out=a.copy();yy,xx=np.indices(a.shape[:2]);mask=np.zeros(a.shape[:2],bool);details={};x0,y0,x1,y1=q['headBox']
 assert a.shape==(256,256,4) and original.shape==a.shape
 if g=='bare':
  bowed='repair-side-heads' in q['headSource'];hp=H/'sources'/f'clean-bare-{v}{"-bowed" if bowed else ""}-native.png';head=Image.open(hp).convert('RGBA');ha=np.array(head);old=arr(R/q['headSource']);ax,ay=q['headPaste'];paste=[ax+axis(old)-axis(ha),ay+old.shape[0]-head.height]
  if q['state']=='carry-turn-east-north' and q['frame'] in [0,2]:paste[1]+=4 if q['frame']==0 else 2
  pairedq=paired.get((q['state'],q['frame']));shared=np.zeros_like(mask)
  if pairedq:
   pa=arr(R/pairedq['source']);shared=(original[:,:,3]>180)&np.all(original==pa,2)
  rgb=original[:,:,:3].astype(float);r,gg,b=[rgb[:,:,i] for i in range(3)];skin=(r>b*1.15)&(gg>b*1.12)&(r>35)&(gg>r*.65)
  band=(xx>=x0-18)&(xx<x1+18)&(yy>=y0-3)&(yy<y1+10)
  collar=(shared&band)|((original[:,:,3]>180)&~skin&band&(yy>=y1))
  layer=Image.new('RGBA',(256,256));oldhp=prev['details'].get('headSource');oldpaste=prev['details'].get('paste')
  if oldhp and oldpaste:layer.paste(Image.open(R/oldhp.removeprefix('res://')).convert('RGBA'),tuple(oldpaste))
  else:layer.paste(Image.fromarray(old),(ax,ay))
  oldalpha=np.array(layer)[:,:,3]>0
  remove=(np.array(Image.open(PREV/prev['mask']).convert('L'))>0)|oldalpha
  remove&=~collar;clean=a.copy();clean[remove]=0;restore=collar&oldalpha;clean[restore]=original[restore]
  gold=restore&(r>gg*1.015)&(r<gg*1.8)&(gg>b*1.08)&(gg>35);lum=(r*.2126+gg*.7152+b*.0722)/145;colour=np.clip(lum[:,:,None]*np.array([82,124,128]),0,177).astype('uint8');clean[gold,:3]=colour[gold]
  def compose(at):
   layer=Image.new('RGBA',(256,256));layer.alpha_composite(head,tuple(at));n=np.array(layer);admitted=(n[:,:,3]>0)&(~collar|(yy<at[1]+head.height-6));o=clean.copy();o[admitted]=n[admitted];return o,n,admitted
  out,n,admit=compose(paste);offset=[0,0]
  if not primary_connected(out,n):
   offsets=sorted([(dx,dy) for dx in range(-6,7) for dy in range(-4,6)],key=lambda z:(abs(z[0])+abs(z[1]),abs(z[1]),abs(z[0]),z[0],z[1]));found=False
   necklocal=(ha[:,:,3]>180)&(np.indices(ha.shape[:2])[0]>=head.height-6)
   for dx,dy in offsets:
    at=[paste[0]+dx,paste[1]+dy];candidate,nc,ac=compose(at);neckimg=Image.new('L',(256,256));neckimg.paste(Image.fromarray(necklocal.astype('uint8')*255),tuple(at));neck=(np.array(neckimg)>0)&ac;contact=int((binary_dilation(neck,np.ones((3,3)))&(clean[:,:,3]>180)).sum())
    if contact>=2 and primary_connected(candidate,nc):out,n,admit=candidate,nc,ac;paste=at;offset=[dx,dy];found=True;break
   if not found:raise RuntimeError((q['state'],q['frame'],v,'no neck registration'))
  mask=remove|admit|restore;details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'paste':paste,'sourceHeadShapeUnscaled':True,'neckRegistrationOffset':offset,'collarRestoredPixels':int(restore.sum())}
 elif v!='north':
  mask=np.array(Image.open(PREV/prev['mask']).convert('L'))>0
  if 'restoredShellMask' in prev['details']:mask&=~(np.array(Image.open(PREV/prev['details']['restoredShellMask']).convert('L'))>0)
  sy,sx=np.where(mask);box=[int(sx.min()),int(sy.min()),int(sx.max()+1),int(sy.max()+1)]
  bowed='repair-side-heads' in q['headSource'];hp=H/'sources'/f'clean-bare-{v}{"-bowed" if bowed else ""}-native.png';head=Image.open(hp).convert('RGBA');px=box[2]+2-head.width if v in ['east','ne'] else box[0] if v in ['west','nw'] else round((box[0]+box[2]-head.width)/2);paste=[px,box[1]-5]
  layer=Image.new('RGBA',(256,256));layer.alpha_composite(head,tuple(paste));n=np.array(layer);opaque=n[:,:,3]>0;lining=arr(H/'sources/visor-lining-native.png');backdrop=lining[(yy-paste[1])%32,(xx-paste[0])%32,:3];out[mask,:3]=backdrop[mask];out[mask&opaque,:3]=n[mask&opaque,:3];details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'paste':paste,'sourceHeadShapeUnscaled':True,'visorBox':box,'oldPortraitPixelsRetainedInAperture':0,'liningPixels':int((mask&~opaque).sum()),'liningSource':'res://character/krusher-head-fit-v4/sources/visor-lining-native.png','restoredShellExcluded':prev['details'].get('restoredShellMask')}
 if len(v)>2:
  for d in [v]:
   ignore=(xx>=95)&(xx<165)&(yy<125)
   if np.array_equal(a[~ignore],oldidle[g,d][~ignore]):out=canonical[g,d].copy();mask|=np.any(a!=out,2);details={'canonicalEndpoint':d}
 assert np.array_equal(a[~mask],out[~mask]),(g,q['state'],q['frame'],'body protection')
 if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3]),(g,q['state'],q['frame'],'shell alpha')
 target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
 records.append({'gear':g,'state':q['state'],'frame':q['frame'],'view':v,'source':'res://'+base.relative_to(R).as_posix(),'sourceHash':sha(base),'originalBody':'res://'+q['source'],'output':q['output'],'outputHash':sha(target),'mask':mr,'changedPixels':int(np.any(a!=out,2).sum()),'details':details})
for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_bytes((PREV/(g+'-manifest.json')).read_bytes())
(P/'revision.json').write_text(json.dumps({'status':'unselected v4 repaired cargo candidate; full-bank and native review pending','records':records},indent=2)+'\n')
profile=R/'character/krusher-cargo-settle-profile-v4';profile.mkdir(exist_ok=True)
for g in ['bare','helmet']:
 m=read(R/'character/krusher-cargo-settle-profile-v3'/(g+'-manifest.json'))
 for s in m['states']:s['frameFiles']=[f.replace(PREV.name,P.name) for f in s['frameFiles']]
 (profile/(g+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({'outputs':len(records),'canonicalEndpoints':sum('canonicalEndpoint' in q['details'] for q in records),'translated':[(q['gear'],q['state'],q['frame'],q['details']['neckRegistrationOffset']) for q in records if q['details'].get('neckRegistrationOffset') not in [None,[0,0]]]}))
