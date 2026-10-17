from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
from scipy.ndimage import label,binary_dilation
from scipy.spatial import ConvexHull
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;BANK=R/'character/krusher-animation-package-v3';read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();index=read(BANK/'package.json');packed={}
for key,q in index['states'].items():
 g,sid=key.split(':',1);mp=BANK/q['manifest'];s=next(s for s in read(mp)['states'] if s['id']==sid)
 for old,new in zip(q['sourceFrames'],s['frameFiles']):packed[g,old]=(mp.parent/new).resolve()
def pad(a):
 out=np.zeros((256,256,4),np.uint8);out[52:52+a.shape[0],36:36+a.shape[1]]=a;return out
C=R/'character/krusher-james-canonical-v7';cm={g:{s['id']:s for s in read(C/(g+'-manifest.json'))['states']} for g in ['bare','helmet']}
def canonical(g,key,i=0):return pad(arr(C/cm[g][key]['frameFiles'][i]))
def axis(h):
 y,x=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=h.shape[0]-4));return round((int(x.min())+int(x.max()))/2)
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
def pixelkey(a):return hashlib.sha256(str((a.shape[1],a.shape[0])).encode()+a.tobytes()).hexdigest()
seed={}
for originalFolder,newFolder in [('krusher-recovery-salvage-v1','krusher-recovery-salvage-v3')]:
 newroot=R/'character'/newFolder;newrecords={q['output']:q for q in read(newroot/'revision.json')['records']}
 for q in read(R/'character'/originalFolder/'provenance.json')['records']:
  if q['family']!='salvage':continue
  nq=newrecords[q['output']];original=arr(R/q['source']);out=arr(newroot/q['output']);mask=np.array(Image.open(newroot/nq['mask']).convert('L'))>0;seed[q['gear'],pixelkey(original)]=(out,mask,nq['details'],'res://'+(newroot/q['output']).relative_to(R).as_posix(),mask.copy() if q['gear']=='helmet' and 'headSource' in nq['details'] else None)
for folder,oldVersion,prevVersion,newVersion,names in [('water-family',1,3,4,['water']),('water-cargo-turns',2,3,4,['cargo','turn','cargo-turn']),('water-interruptions',1,2,3,['cancel','distress'])]:
 OLD=R/f'character/krusher-{folder}-v{oldVersion}';PREV=R/f'character/krusher-{folder}-v{prevVersion}';P=R/f'character/krusher-{folder}-v{newVersion}';P.mkdir(exist_ok=True);prior={q['output']:q for q in read(PREV/'revision.json')['records']};records=[]
 if folder=='water-interruptions':
  additions={};originalLookup={}
  for sourcefolder in ['krusher-recovery-salvage-v1','krusher-water-cargo-turns-v2']:
   for oq in read(R/'character'/sourcefolder/'provenance.json')['records']:
    original=arr(R/oq['source'])
    if original.shape[:2]==(276,256):originalLookup[oq['gear'],pixelkey(original)]=original
  for (g,key),(out,mask,d,path,faceMask) in list(seed.items()):
   if out.shape[:2]!=(276,256):continue
   original=originalLookup.get((g,key))
   if original is None:continue
   assert not np.any(original[264:,:,3]);canvas=np.zeros((360,256,4),np.uint8);canvas[96:]=original[:264];newcanvas=np.zeros_like(canvas);newcanvas[96:]=out[:264];newmask=np.zeros((360,256),bool);newmask[96:]=mask[:264];nd=dict(d);newFace=None
   if faceMask is not None:newFace=np.zeros((360,256),bool);newFace[96:]=faceMask[:264]
   if 'paste' in nd:nd['paste']=[nd['paste'][0],nd['paste'][1]+96]
   nd.pop('foregroundMask',None);additions[g,pixelkey(canvas)]=(newcanvas,newmask,nd,path,newFace)
  seed.update(additions)
 for q in read(OLD/'provenance.json')['records']:
  g=q['gear'];v=q.get('view',q['state'].rsplit('-',1)[1]);oldpath=PREV/q['output'];base=packed.get((g,oldpath.relative_to(R).as_posix()),oldpath);a=arr(base);original=arr(R/q['source']);assert original.shape==a.shape;yy,xx=np.indices(a.shape[:2]);out=a.copy();mask=np.zeros(a.shape[:2],bool);prev=prior[q['output']];detail={'gear':g,'state':q['state'],'frame':q['frame'],'view':v};shared=seed.get((g,pixelkey(original)));faceMask=None
  if shared:
   newpose,newmask,d,path,faceMask=shared;mask=newmask|(np.array(Image.open(PREV/prev['mask']).convert('L'))>0);out[mask]=newpose[mask];detail.update(d);detail.update(gear=g,state=q['state'],frame=q['frame'],view=v,sharedHeadPose=path);detail.pop('foregroundMask',None)
  elif g=='bare' or (v!='north' and not prev['details'].get('noVisibleFace')):
   name=v
   if 'rear-bow' in q['headSource']:name='north-bow'+str({0:45,1:65,2:90}[int(Path(q['headSource']).stem.split('-')[-1])])
   elif 'south-bow' in q['headSource']:name={0:'south-bowed',1:'south-deep',2:'south-fully-bowed'}[int(Path(q['headSource']).stem.split('-')[-1])]
   elif 'repair-side' in q['headSource']:name=v+'-bowed'
   hp=H/'sources'/('clean-bare-'+name+'-native.png');head=Image.open(hp).convert('RGBA');x0,y0,x1,y1=q['headBox'];foreground=np.zeros(a.shape[:2],bool)
   if folder=='water-family':
    row=prev['details'].get('foregroundFromRow')
    if row is not None:foreground=yy>=row
   else:
    foreground=((xx>=x1+5)&(yy<y1+7))|(xx>=x1+25) if v=='east' else ((xx<x0-5)&(yy<y1+7))|(xx<x0-25) if v=='west' else yy>=y1+4 if v=='south' else ((yy>=y1+5)|((xx>x1+12) if v=='se' else (xx<x0-12))) if v in ['se','sw'] else (yy<y0-18)|((xx>x1+8) if v=='ne' else (xx<x0-8)) if v in ['ne','nw'] else np.zeros(a.shape[:2],bool)
    box=prev['details'].get('foregroundGuardExcludesObservedHead')
    if box:bx0,by0,bx1,by1=box;foreground&=~((xx>=bx0)&(xx<bx1)&(yy>=by0)&(yy<by1))
   if g=='bare':
    qr=dict(q);adjust=prev['details'].get('observedWholeHeadRegistration',[0,0]);qr['headPaste']=[q['headPaste'][0]+adjust[0],q['headPaste'][1]+adjust[1]];out,mask,fit=barefit(a,original,qr,prev,PREV,hp,foreground);detail.update(fit)
   else:
    mask=(np.array(Image.open(PREV/prev['mask']).convert('L'))>0)&~foreground;box=prev['details'].get('visorBox')
    if box and prev['details'].get('originalShellRestored'):bx0,by0,bx1,by1=box;mask&=(xx>=bx0)&(xx<bx1)&(yy>=by0)&(yy<by1)
    legacyMask=mask.copy();rgb=original[:,:,:3].astype(float);r,gg,b=[rgb[:,:,i] for i in range(3)];skin=(original[:,:,3]>180)&(r>gg*1.1)&(r>b*1.12)&(b>gg*.55)&(rgb.mean(2)>45)&(xx>=x0-16)&(xx<x1+16)&(yy>=y0-14)&(yy<y1+16);labs,_=label(skin,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;sy,sx=np.where(labs==int(sizes.argmax()));semantic=False
    if len(sx)>=3:
     points=np.column_stack([sx,sy])
     if np.linalg.matrix_rank(points-points.mean(0))==2:
      hull=ConvexHull(points);polygon=[list(map(int,points[i])) for i in hull.vertices];region=Image.new('L',(a.shape[1],a.shape[0]));ImageDraw.Draw(region).polygon([tuple(p) for p in polygon],fill=255);actualFace=np.array(region)>0;foreground&=~actualFace;mask=actualFace;semantic=True;detail['originalSkinVisorPolygon']=polygon;detail['foregroundGuardExcludesObservedVisor']=True
      width=int(sx.max()-sx.min()+1);height=int(sy.max()-sy.min()+1)
      if v in ['east','west'] and width/height>.72:
       name='se' if v=='east' else 'sw';hp=H/'sources'/('clean-bare-'+name+'-native.png');head=Image.open(hp).convert('RGBA');detail['cameraQuarterFromOriginalFaceAspect']=width/height
    sy,sx=np.where(mask);assert len(sx),(folder,g,q['state'],q['frame'],'empty aperture');faceMask=mask.copy();restore=(np.array(Image.open(PREV/prev['mask']).convert('L'))>0)&~mask&~foreground;out[restore]=original[restore];detail['originalShellRestoredPixels']=int(restore.sum());detail['apertureFromOriginalSkin']=semantic
    face=np.array([head.width*(.58 if name=='se' else .42 if name=='sw' else .72 if v in ['east','ne'] else .28 if v in ['west','nw'] else .5),head.height*(.75 if name=='south-fully-bowed' else .63 if name=='south-deep' else .57 if name=='south-bowed' else .46)]);target=np.array([sx.mean(),sy.mean()]);paste=np.rint(target-face).astype(int).tolist();layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.alpha_composite(head,tuple(paste));n=np.array(layer);opaque=n[:,:,3]>0;lining=arr(H/'sources/visor-lining-native.png');backdrop=lining[(yy-paste[1])%32,(xx-paste[0])%32,:3];out[mask,:3]=backdrop[mask];out[mask&opaque,:3]=n[mask&opaque,:3];mask|=restore;detail.update(headSource='res://'+hp.relative_to(R).as_posix(),headHash=sha(hp),paste=paste,liningSource='res://character/krusher-head-fit-v4/sources/visor-lining-native.png',sourceHeadShapeUnscaled=True,nativeFaceLandmark=face.tolist(),apertureFaceCenter=target.tolist(),restoredShellOutsideApertureProtected=True)
   if foreground.any():
    fg=P/'foreground-masks'/g/Path(q['output']).name;fg.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(foreground.astype('uint8')*255).save(fg);detail['foregroundMask']='res://'+fg.relative_to(R).as_posix();assert np.array_equal(a[foreground],out[foreground])
  assert np.array_equal(a[~mask],out[~mask])
  if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3])
  if g=='helmet' and 'headSource' in detail:
   if faceMask is None:faceMask=mask.copy()
   pm=P/'portrait-masks'/g/Path(q['output']).name;pm.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(faceMask.astype('uint8')*255).save(pm);detail['portraitMask']='res://'+pm.relative_to(R).as_posix()
  save(P,base,q['output'],out,mask,detail,records);seed[g,pixelkey(original)]=(out,mask,detail,'res://'+(P/q['output']).relative_to(R).as_posix(),faceMask)
 for f in names:
  for g in ['bare','helmet']:(P/(f+'-'+g+'-manifest.json')).write_bytes((PREV/(f+'-'+g+'-manifest.json')).read_bytes())
 (P/'revision.json').write_text(json.dumps({'status':'unselected v4 repaired underwater identity; full package/native review pending','records':records},indent=2)+'\n');print(json.dumps({'family':folder,'outputs':len(records),'sharedHeadPoses':sum('sharedHeadPose' in q['details'] for q in records),'translations':[(q['state'],q['frame'],q['details'].get('neckRegistrationOffset')) for q in records if q['details'].get('neckRegistrationOffset') not in [None,[0,0]]]}))
