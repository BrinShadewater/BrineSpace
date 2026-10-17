from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np,sys
from scipy.ndimage import label,binary_dilation
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;C=R/'character/krusher-james-canonical-v9';BANK=R/'character/krusher-animation-package-v3'
read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
index=read(BANK/'package.json');packed={}
inventory=read(R/'character/krusher-complete-animation-v1/source-coverage.json')['resolved']
for k,q in index['states'].items():
 g,key=k.split(':',1);mp=BANK/q['manifest'];m=read(mp);s=next(s for s in m['states'] if s['id']==key)
 for old,new in zip(q['sourceFrames'],s['frameFiles']):packed[g,old]=(mp.parent/new).resolve()
idle={(g,d):arr(C/next(s for s in read(C/(g+'-manifest.json'))['states'] if s['id']=='idle-'+d)['frameFiles'][0]) for g in ['bare','helmet'] for d in ['south','east','north','west']}
def neckaxis(h):
 y,x=np.where((h[:,:,3]>150)&(np.indices(h.shape[:2])[0]>=h.shape[0]-4));return round((int(x.min())+int(x.max()))/2)
def connected(candidate,headlayer):
 opaque=candidate[:,:,3]>180;labs,_=label(opaque,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;body=int(sizes.argmax());head=(headlayer[:,:,3]>180)&np.all(candidate==headlayer,axis=2)
 return int((head&(labs!=body)).sum())<=2
for family in sys.argv[1:] or ['repair','torch','seated']:
 O=R/f'character/krusher-{family}-family-v1';PREV=R/f'character/krusher-{family}-family-v3';P=R/f'character/krusher-{family}-family-v5';P.mkdir(exist_ok=True);prior={q['output']:q for q in read(PREV/'revision.json')['records']};records=[]
 for q in read(O/'provenance.json')['records']:
  g=q['gear'];d=q['state'].rsplit('-',1)[1];oldpath=PREV/q['output'];basepath=packed.get((g,oldpath.relative_to(R).as_posix()),oldpath);a=arr(basepath);original=arr(R/q['source']);hh,ww=a.shape[:2]
  assert a.shape==original.shape,(family,q['state'],q['frame'],'canvas')
  out=a.copy();yy,xx=np.indices((hh,ww));mask=np.zeros((hh,ww),bool);details={};prev=prior[q['output']]
  if q['method'].startswith('Exact complete'):
   out=np.zeros_like(a);out[:184,:184]=idle[g,d];mask=np.any(a!=out,2);details={'canonicalEndpoint':d}
  elif g=='bare':
   bowed=('side-heads' in q['headSource'] or 'bow-heads' in q['headSource']);kind=f'clean-bare-{d}'+('-bowed' if bowed else '');hp=H/'sources'/(kind+'-native.png');head=Image.open(hp).convert('RGBA');h=np.array(head);old=arr(R/q['headSource']);ax,ay=q['headPaste']
   # The legacy bowed east cutout's lower-alpha midpoint tracked beard,
   # not the rear skin neck. Calibrate this source's nape consistently to
   # the original collar (see bowed-neck-diagnostic.png), before any
   # small per-pose registration correction. This avoids a 4px pose jump.
   authoredOffset=[-4,0] if bowed and d=='east' else [0,0]
   paste=(ax+neckaxis(old)-neckaxis(h)+authoredOffset[0],ay+old.shape[0]-head.height)
   x0,y0,x1,y1=q['headBox'];bottom=y1+(2 if d=='north' else 3);axis=round((x0+x1)/2)
   if d=='east':region=(xx>=min(x0-4,ax-1))&(xx<x1+8)
   elif d=='west':region=(xx>=x0-8)&(xx<max(x1+4,ax+old.shape[1]+1))
   else:region=(xx>=axis-17)&(xx<axis+18)
   region&=(yy>=min(y0-9,ay-1))&(yy<bottom)
   collar=(yy>=bottom-5)&(original[:,:,3]>0)
   if d=='east':collar=(yy>=y0-2)&(xx<x0)&(original[:,:,3]>0)
   elif d=='west':collar=(yy>=y0-2)&(xx>=x1)&(original[:,:,3]>0)
   else:collar&=(xx<axis-8)|(xx>axis+8)
   # Recover original rigid collar pixels within the observed neck band.
   # Prior enlarged portraits erased this hardware and hid the resulting gap.
   r,gg,b=[original[:,:,c].astype(float) for c in range(3)]
   warmSkin=(r>b*1.15)&(gg>b*1.12)&(r>35)&(gg>r*.65)
   paired=inventory['helmet'][q['state']];pairedmp=R/paired['manifest'].removeprefix('res://');pairedrel=paired['state']['frameFiles'][q['frame']];pairedpath=R/pairedrel[6:] if pairedrel.startswith('res://') else pairedmp.parent/pairedrel;pairedarray=arr(pairedpath)
   shared=(original[:,:,3]>0)&np.all(original==pairedarray,axis=2)
   rigid=(original[:,:,3]>0)&~warmSkin&(yy>=y1)&(yy<y1+10)&(xx>=x0-10)&(xx<x1+10)
   rigid|=shared&(yy>=y0-2)&(yy<y1+10)&(xx>=x0-10)&(xx<x1+10)
   collar=rigid
   # Remove the actual prior inserted head plus its measured original window.
   oldlayer=Image.new('RGBA',(ww,hh))
   if 'headSource' in prev['details']:
    oldhead=Image.open(R/prev['details']['headSource'][6:]).convert('RGBA');oldlayer.paste(oldhead,tuple(prev['details']['paste']))
   else:oldlayer.paste(Image.fromarray(old),(ax,ay))
   prioralpha=np.array(oldlayer)[:,:,3]>0;region|=prioralpha;region&=~collar
   foreground=np.zeros_like(region)
   if family in ['torch','seated']:
    # Protect opaque cyan tools/screens, not the original cutout's faint
    # green matte fringe or nearly black hair pixels inside the new head.
    rgb=original[:,:,:3].astype(float);foreground=(original[:,:,3]>180)&(rgb[:,:,2]>60)&(rgb[:,:,1]>60)&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(rgb[:,:,1]>rgb[:,:,0]*1.2)
   region&=~foreground;out[region]=0
   layer=Image.new('RGBA',(ww,hh));layer.alpha_composite(head,paste);n=np.array(layer);opaque=n[:,:,3]>0;admitted=opaque&~collar&~foreground;out[admitted]=n[admitted];mask=region|admitted
   # Restore observed collar hardware erased by the earlier full-head layer.
   restore=rigid&region|rigid&prioralpha;out[restore]=original[restore];mask|=restore
   r,gg,b=[original[:,:,c].astype(float) for c in range(3)];gold=restore&(r>gg*1.015)&(r<gg*1.8)&(gg>b*1.08)&(gg>35);lum=(r*.2126+gg*.7152+b*.0722)/145;colour=np.clip(lum[:,:,None]*np.array([82,124,128]),0,177).astype('uint8');out[gold,:3]=colour[gold]
   offset=[0,0]
   if not connected(out,n):
    # Rigidly register the authored skin neck to the observed original collar.
    # Only a bounded translation is allowed; neither head nor body is deformed.
    clean=a.copy();clean[region]=0;clean[restore]=out[restore];found=False
    offsets=sorted([(dx,dy) for dx in range(-6,7) for dy in range(-3,5)],key=lambda z:(abs(z[0])+abs(z[1]),abs(z[1]),abs(z[0]),z[0],z[1]))
    necklocal=(h[:,:,3]>180)&(np.indices(h.shape[:2])[0]>=head.height-6)
    for dx,dy in offsets:
     candidatePaste=(paste[0]+dx,paste[1]+dy);layer=Image.new('RGBA',(ww,hh));layer.alpha_composite(head,candidatePaste);candidateHead=np.array(layer);candidateOpaque=candidateHead[:,:,3]>0;candidateAdmit=candidateOpaque&~collar&~foreground;candidate=clean.copy();candidate[candidateAdmit]=candidateHead[candidateAdmit]
     neckImage=Image.new('L',(ww,hh));neckImage.paste(Image.fromarray(necklocal.astype('uint8')*255),candidatePaste);neck=(np.array(neckImage)>0)&candidateAdmit;contact=int((binary_dilation(neck,np.ones((3,3)))&(clean[:,:,3]>180)).sum())
     if contact>=2 and connected(candidate,candidateHead):
      out=candidate;mask=region|candidateAdmit|restore;paste=candidatePaste;offset=[dx,dy];found=True;break
    if not found:raise RuntimeError((family,q['state'],q['frame'],'no bounded anatomical neck registration'))
   details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'paste':paste,'bowed':bowed,'collarRestoredPixels':int(restore.sum()),'sourceHeadShapeUnscaled':True,'authoredNeckOffset':authoredOffset,'neckRegistrationOffset':offset}
  elif d!='north':
   bowed=('side-heads' in q['headSource'] or 'bow-heads' in q['headSource']);hp=H/'sources'/f'clean-bare-{d}{"-bowed" if bowed else ""}-native.png';head=Image.open(hp).convert('RGBA')
   mask=np.array(Image.open(PREV/prev['mask']).convert('L'))>0
   x0,y0,x1,y1=q['headBox'];px=x1+2-head.width if d=='east' else x0 if d=='west' else round((x0+x1-head.width)/2);paste=(px,y0-5)
   layer=Image.new('RGBA',(ww,hh));layer.alpha_composite(head,paste);n=np.array(layer);opaque=n[:,:,3]>0
   lining=arr(H/'sources/visor-lining-native.png');backdrop=lining[(yy-paste[1])%32,(xx-paste[0])%32,:3]
   out[mask,:3]=backdrop[mask];out[mask&opaque,:3]=n[mask&opaque,:3]
   details={'headSource':'res://'+hp.relative_to(R).as_posix(),'headHash':sha(hp),'paste':paste,'bowed':bowed,'liningPixels':int((mask&~opaque).sum()),'oldPortraitPixelsRetainedInAperture':0,'liningSource':'res://character/krusher-head-fit-v7/sources/visor-lining-native.png','sourceHeadShapeUnscaled':True}
  assert np.array_equal(a[~mask],out[~mask]),(family,g,q['state'],q['frame'],'body protection')
  if g=='helmet':assert np.array_equal(a[:,:,3],out[:,:,3]),(family,g,q['state'],q['frame'],'shell alpha')
  target=P/q['output'];target.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(out).save(target);mr='head-masks/'+g+'/'+target.name;(P/mr).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(mask.astype('uint8')*255).save(P/mr)
  records.append({'gear':g,'state':q['state'],'frame':q['frame'],'source':'res://'+basepath.relative_to(R).as_posix(),'sourceHash':sha(basepath),'originalBody':'res://'+q['source'],'output':q['output'],'outputHash':sha(target),'mask':mr,'changedPixels':int(np.any(a!=out,2).sum()),'details':details})
 for g in ['bare','helmet']:(P/(g+'-manifest.json')).write_bytes((PREV/(g+'-manifest.json')).read_bytes())
 (P/'revision.json').write_text(json.dumps({'status':'v4 head candidate; full-library propagation and native station review pending','records':records,'scope':'Natural complete heads/skin necks on preserved cyan original bodies; original manifests exact; helmet head clipped without stretching.'},indent=2)+'\n')
 print(json.dumps({'family':family,'outputs':len(records),'apertureUncovered':sum(q['details'].get('uncoveredAperturePixels',0) for q in records)}))
