from pathlib import Path
from PIL import Image
from scipy.ndimage import label,binary_dilation
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;OLD=R/'character/krusher-rest-family-v2';PREV=R/'character/krusher-rest-family-v4';P=R/'character/krusher-rest-family-v5';P.mkdir(exist_ok=True);BANK=R/'character/krusher-animation-package-v3';read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();index=read(BANK/'package.json');packed={}
for key,q in index['states'].items():
 g,sid=key.split(':',1);mp=BANK/q['manifest'];s=next(s for s in read(mp)['states'] if s['id']==sid)
 for old,new in zip(q['sourceFrames'],s['frameFiles']):packed[g,old]=(mp.parent/new).resolve()
previous={q['output']:q for q in read(PREV/'revision.json')['records']};records=[];derived={}
def connected(out,head):
 visible=(head[:,:,3]>180)&np.all(out==head,2);hl,_=label(visible,np.ones((3,3)));hs=np.bincount(hl.ravel());hs[0]=0;labs,_=label(out[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;return hs.max()>0 and np.all(labs[hl==int(hs.argmax())]==int(sizes.argmax()))
for q in read(OLD/'provenance.json')['records']:
 g,v,tilt=q['gear'],q['view'],q['tilt'];oldpath=PREV/q['output'];base=packed.get((g,oldpath.relative_to(R).as_posix()),oldpath);a=arr(base);original=arr(R/q['source']);out=a.copy();yy,xx=np.indices(a.shape[:2]);mask=np.zeros(a.shape[:2],bool);details={};prev=previous[q['output']]
 if g=='bare' or v!='north':
  name=(v+'-closed') if v in ['east','west'] and tilt==80 else 'south-raised-closed' if v=='south' and tilt==80 else 'south-raised-open' if v=='south' and tilt>=30 else 'north-bowed' if v=='north' and 'rear-bow' in q['headSource'] else v
  if v=='north' and 'rear-bow' in q['headSource']:name='north-bow'+str({0:45,1:65,2:90}[int(Path(q['headSource']).stem.split('-')[-1])])
  hp=H/'sources'/('clean-bare-'+name+'-native.png');head=Image.open(hp).convert('RGBA');source=hp;angle=0
  if v in ['east','west'] and tilt:
   angle=tilt if v=='east' else -tilt;head=head.rotate(angle,resample=Image.Resampling.NEAREST,expand=True);hp=P/'sources'/('clean-'+name+'-tilt-'+str(tilt)+'.png');hp.parent.mkdir(exist_ok=True);head.save(hp);derived[hp.relative_to(P).as_posix()]={'source':'res://'+source.relative_to(R).as_posix(),'sourceHash':sha(source),'rotationDegrees':angle,'resample':'nearest','outputHash':sha(hp)}
  h=np.array(head);body=np.array(q['bodyAxis']);hy,hx=np.where(h[:,:,3]>180);projection=hx*body[0]+hy*body[1];near=projection>projection.max()-2;neck=np.array([hx[near].mean(),hy[near].mean()]);paste=np.rint(np.array(q['neck'])-neck).astype(int).tolist()
  details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'sourceKind':name,'tilt':tilt,'paste':paste,'bodyAxis':q['bodyAxis'],'neck':q['neck'],'nativeNeck':neck.tolist(),'sourceHeadShapeUnscaled':True,'rotationDegrees':angle}
  if g=='bare':
   oldlayer=Image.new('RGBA',(256,256));oldhp=prev['details'].get('headSource');oldat=prev['details'].get('paste');oldlayer.paste(Image.open(R/oldhp[6:]).convert('RGBA') if oldhp else Image.open(R/q['headSource']).convert('RGBA'),tuple(oldat or q['headPaste']));oldalpha=np.array(oldlayer)[:,:,3]>0
   r,gg,b=[original[:,:,i].astype(float) for i in range(3)];skin=(r>b*1.15)&(gg>b*1.12)&(r>35)&(gg>r*.65);neckGlobal=np.array(q['neck']);depth=(xx-neckGlobal[0])*body[0]+(yy-neckGlobal[1])*body[1];side=(xx-neckGlobal[0])*body[1]-(yy-neckGlobal[1])*body[0];collar=(original[:,:,3]>180)&~skin&(depth>=-4)&(depth<8)&(np.abs(side)<18)
   remove=((np.array(Image.open(PREV/prev['mask']).convert('L'))>0)|oldalpha)&~collar;clean=a.copy();clean[remove]=0;restore=collar&oldalpha;clean[restore]=original[restore];gold=restore&(r>gg*1.015)&(r<gg*1.8)&(gg>b*1.08)&(gg>35);lum=(r*.2126+gg*.7152+b*.0722)/145;colour=np.clip(lum[:,:,None]*np.array([82,124,128]),0,177).astype('uint8');clean[gold,:3]=colour[gold]
   def compose(at):
    layer=Image.new('RGBA',(256,256));layer.alpha_composite(head,tuple(at));n=np.array(layer);nativeDepth=(xx-at[0]-neck[0])*body[0]+(yy-at[1]-neck[1])*body[1];admit=(n[:,:,3]>0)&(~collar|(nativeDepth<-5));candidate=clean.copy();candidate[admit]=n[admit];return candidate,n,admit
   out,n,admit=compose(paste);offset=[0,0]
   if not connected(out,n):
    offsets=sorted([(dx,dy) for dx in range(-5,6) for dy in range(-5,6)],key=lambda z:(abs(z[0])+abs(z[1]),abs(z[1]),abs(z[0]),z[0],z[1]));found=False;npix=np.indices(h.shape[:2]);necklocal=(h[:,:,3]>180)&((npix[1]-neck[0])*body[0]+(npix[0]-neck[1])*body[1]>-6)
    for dx,dy in offsets:
     at=[paste[0]+dx,paste[1]+dy];candidate,nc,ac=compose(at);neckimg=Image.new('L',(256,256));neckimg.paste(Image.fromarray(necklocal.astype('uint8')*255),tuple(at));contact=int((binary_dilation((np.array(neckimg)>0)&ac,np.ones((3,3)))&(clean[:,:,3]>180)).sum())
     if contact>=2 and connected(candidate,nc):out,n,admit=candidate,nc,ac;paste=at;offset=[dx,dy];found=True;break
    if not found:raise RuntimeError((q['state'],q['frame'],'no neck registration'))
   mask=remove|restore|admit;details.update(paste=paste,neckRegistrationOffset=offset,collarRestoredPixels=int(restore.sum()))
  else:
   # Helmet provenance's projected endpoint is the original face/chin,
   # not a bare skin neck. Register a face landmark to the observed aperture
   # while retaining the complete head's physical size and rigid rotation.
   mask=np.array(Image.open(PREV/prev['mask']).convert('L'))>0;sy,sx=np.where(mask);sourceImage=Image.open(source);face=np.array([sourceImage.width*(.72 if v=='east' else .28 if v=='west' else .5),sourceImage.height*.46]);theta=np.radians(angle);delta=face-np.array(sourceImage.size)/2;rotation=np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]]);landmark=rotation@delta+np.array(head.size)/2;targetFace=np.array([sx.mean(),sy.mean()]);paste=np.rint(targetFace-landmark).astype(int).tolist();details.update(paste=paste,nativeFaceLandmark=landmark.tolist(),apertureFaceCenter=targetFace.tolist())
   layer=Image.new('RGBA',(256,256));layer.alpha_composite(head,tuple(paste));n=np.array(layer);opaque=n[:,:,3]>0;lining=arr(H/'sources/visor-lining-native.png');backdrop=lining[(yy-paste[1])%32,(xx-paste[0])%32,:3];out[mask,:3]=backdrop[mask];out[mask&opaque,:3]=n[mask&opaque,:3];details.update(liningSource='res://character/krusher-head-fit-v4/sources/visor-lining-native.png',liningPixels=int((mask&~opaque).sum()))
 assert np.array_equal(a[~mask],out[~mask]),(g,q['state'],q['frame'],'body protection')
 if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
 target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
 records.append({'gear':g,'state':q['state'],'frame':q['frame'],'view':v,'source':'res://'+base.relative_to(R).as_posix(),'sourceHash':sha(base),'originalBody':'res://'+q['source'],'output':q['output'],'outputHash':sha(target),'mask':mr,'details':details})
for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_bytes((PREV/(g+'-manifest.json')).read_bytes())
(P/'revision.json').write_text(json.dumps({'status':'unselected v4 identity on rest-v5; full bank and station review pending','records':records,'derivedSources':derived},indent=2)+'\n');print(json.dumps({'outputs':len(records),'derivedSources':len(derived),'translations':[(q['state'],q['frame'],q['details'].get('neckRegistrationOffset')) for q in records if q['details'].get('neckRegistrationOffset') not in [None,[0,0]]]}))
