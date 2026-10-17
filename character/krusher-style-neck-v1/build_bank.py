"""Repair each selected drawing once; aliases inherit exactly the same repaired pixels."""
from pathlib import Path
from PIL import Image
from scipy import ndimage
import numpy as np,json,hashlib,math,os
H=Path(__file__).resolve().parent;R=H.parents[1];BASE=R/'character/krusher-animation-package-v8';O=R/'character/krusher-style-neck-bank-v1';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());mapping=read(H/'bank-mapping.json');derived=mapping['derivedSources'];headcache={};records=[];errors=[];replacements={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def anchor(a):
 yy,xx=np.indices(a.shape[:2]);r,g,b=[a[:,:,k].astype(float) for k in range(3)];m=(a[:,:,3]>120)&(yy>=a.shape[0]-5)&(r>g*1.055)&(r>b*1.09)&(r>60);y,x=np.where(m)
 if not len(x):y,x=np.where((a[:,:,3]>120)&(yy>=a.shape[0]-4))
 bottom=int(y.max());return np.array([float(x[y>=bottom-2].mean()),float(bottom)])
def newhead(path):
 path=path.removeprefix('res://').replace('\\','/')
 if path in headcache:return headcache[path]
 if path in derived:
  q=derived[path];im,point,_,source=newhead(q['source']);angle=q['rotationDegrees'];oldsize=np.array(im.size);out=im.rotate(angle,resample=Image.Resampling.BICUBIC,expand=True);t=math.radians(angle);rot=np.array([[math.cos(t),math.sin(t)],[-math.sin(t),math.cos(t)]]);point=rot@(point-oldsize/2)+np.array(out.size)/2;result=(out,point,angle,source)
 else:
  name=Path(path).name.replace('clean-bare-','style-');source=H/'sources'/name
  if not source.exists():raise RuntimeError(('No matching authored head',path,name))
  im=Image.open(source).convert('RGBA');result=(im,anchor(np.array(im)),0,source.relative_to(R).as_posix())
 headcache[path]=result;return result
def pad(a,shape,offset):
 if a.shape[:2]==shape:return a
 out=np.zeros((*shape,*a.shape[2:]),a.dtype);x,y=offset
 if y<0 or x<0 or y+a.shape[0]>shape[0] or x+a.shape[1]>shape[1]:raise RuntimeError(('Original body canvas mismatch',a.shape,shape,offset))
 out[y:y+a.shape[0],x:x+a.shape[1]]=a;return out
def atomic(im,path):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_name(path.name+'.tmp');im.save(tmp,format='PNG');os.replace(tmp,path)
for count,(rel,q) in enumerate(mapping['records'].items()):
 a=arr(BASE/rel);details=q['details'];out=a.copy();mask=np.zeros(a.shape[:2],bool);info={'source':rel,'sourceHash':sha(BASE/rel),'example':q['example'],'exampleFrame':q['exampleFrame'],'gear':q['gear'],'canvas':q['canvas'],'pivot':q['pivot']}
 if not q['noVisibleHead']:
  oldpath=details['headSource'];old=Image.open(R/oldpath[6:]).convert('RGBA');head,neck,angle,newsource=newhead(oldpath);ha=np.array(head);prone_south=q['gear']=='bare' and q['direction']=='south' and q['state'].startswith(('swim-', 'swim-pickup-')) and 'south-bowed' in oldpath
  if prone_south:
   # The authored short neck is behind the jaw in this prone view. Crop its exposed lower end.
   head=head.copy();ha=np.array(head);ha[-3:]=0;head=Image.fromarray(ha)
  offset=np.array(q['pivot'])-np.array([92,172]) if q.get('paddedCanonical') else np.array([0,0]);oldpaste=np.array(details['paste'])+offset
  oldlayer=Image.new('RGBA',(a.shape[1],a.shape[0]));oldlayer.alpha_composite(old,tuple(oldpaste.astype(int)));oldpixels=np.array(oldlayer)
  helmet=q['gear']=='helmet' or bool(details.get('liningSource'))
  if helmet:
   mp=details.get('portraitMask') or q.get('mask')
   if not mp:raise RuntimeError(('No protected helmet aperture',q['example']))
   mp=R/mp.removeprefix('res://');ap=np.array(Image.open(mp).convert('L'))>0
   if ap.shape!=a.shape[:2]:ap=pad(ap,a.shape[:2],offset.astype(int))
   oldface=np.array(details.get('nativeFaceLandmark',[old.width*.5,old.height*.46]),float)
   face=oldface/np.array(old.size)*np.array(head.size);paste=np.rint(oldpaste+oldface-face).astype(int)
   lining=arr(R/details.get('liningSource','res://character/krusher-head-fit-v7/sources/visor-lining-native.png')[6:]);yy,xx=np.indices(a.shape[:2]);back=lining[(yy-paste[1])%lining.shape[0],(xx-paste[0])%lining.shape[1],:3];clean=a.copy();clean[ap,:3]=back[ap]
   layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.alpha_composite(head,tuple(paste));hn=np.array(layer);blend=np.array(Image.alpha_composite(Image.fromarray(clean),layer));out[ap,:3]=blend[ap,:3];mask=ap
   assert np.array_equal(a[:,:,3],out[:,:,3]);info.update({'mode':'Protected visor portrait, proper alpha composite','newHead':newsource,'newPaste':paste.tolist(),'rotationDegrees':angle,'aperturePixels':int(ap.sum())})
  else:
   visible=(oldpixels[:,:,3]>0)&np.all(a==oldpixels,2);target=np.array(details['neck'],float)+offset if details.get('neck') else oldpaste+anchor(np.array(old));paste=np.rint(target-neck).astype(int);yy,xx=np.indices(a.shape[:2]);axis=np.array([0,-1] if prone_south else details.get('bodyAxis',[math.sin(math.radians(angle)),math.cos(math.radians(angle))]));dx=xx-target[0];dy=yy-target[1];along=dx*axis[0]+dy*axis[1];across=dx*axis[1]-dy*axis[0];contact=(along>=-5)&(along<=7)&(abs(across)<=6);clean=a.copy();clean[visible]=0;restore=np.zeros_like(mask)
   if q.get('originalBody'):
    original=arr(R/q['originalBody']);original=pad(original,a.shape[:2],offset.astype(int) if q.get('paddedCanonical') else np.array([36,52]) if original.shape[:2]==(184,184) and a.shape[:2]==(256,256) else np.array([0,96]) if original.shape[0]==276 and a.shape[0]==360 else np.array([0,0]))
    r,g,b=[original[:,:,k].astype(float) for k in range(3)];skin=(original[:,:,3]>120)&(r>g*1.09)&(r>b*1.15)&((r-g)>(g-b)*1.25)&(r>32);restore=skin&contact
    if prone_south:restore[:]=False
    clean[restore]=original[restore]
   occlusion=(a[:,:,3]>180)&~visible&~restore
   def compose(at):
    layer=Image.new('RGBA',(a.shape[1],a.shape[0]));layer.alpha_composite(head,tuple(at));hn=np.array(layer);hn[occlusion]=0;candidate=np.array(Image.alpha_composite(Image.fromarray(clean),Image.fromarray(hn)));hm=(hn[:,:,3]>220);hl,_=ndimage.label(hm,np.ones((3,3)));sizes=np.bincount(hl.ravel());sizes[0]=0;main=hl==sizes.argmax() if len(sizes)>1 and sizes.max() else np.zeros_like(hm);labels,_=ndimage.label(candidate[:,:,3]>180,ndimage.generate_binary_structure(2,1));areas=np.bincount(labels.ravel());areas[0]=0;body=areas.argmax();attached=bool(main.any() and np.all(labels[main]==body));return candidate,hn,main,attached
   out,hn,main,attached=compose(paste);shift=0
   if not attached:
    for distance in [1,2,3]:
     at=paste+np.rint(axis*distance).astype(int);candidate,ch,cm,ok=compose(at)
     if ok:out,hn,main,attached,paste,shift=candidate,ch,cm,True,at,distance;break
   mask=visible|restore|(hn[:,:,3]>0)
   if not attached:errors.append({'source':rel,'example':q['example'],'problem':'Primary visible skull not attached to body after bounded collar registration','headPixels':int(main.sum())})
   info.update({'mode':'Matte head over original body neck; original collar/props occlude foreground','newHead':newsource,'newPaste':paste.tolist(),'rotationDegrees':angle,'originalBody':q.get('originalBody'),'bodyNeckTarget':target.tolist(),'collarRegistrationAlongBody':shift,'restoredOriginalSkinPixels':int(restore.sum()),'oldVisibleHeadPixels':int(visible.sum()),'primaryHeadAttached':attached,'visiblePrimaryHeadPixels':int(main.sum())})
 assert np.array_equal(a[~mask],out[~mask]),q['example']
 digest=hashlib.sha256(str(out.shape).encode()+out.tobytes()).hexdigest();path=O/'frames'/(digest+'.png')
 if not path.exists():atomic(Image.fromarray(out),path)
 maskpath=O/'edit-masks'/(Path(rel).stem+'.png');atomic(Image.fromarray(mask.astype('uint8')*255),maskpath)
 replacements[rel]='res://'+path.relative_to(R).as_posix();info.update({'output':path.relative_to(O).as_posix(),'outputHash':sha(path),'mask':maskpath.relative_to(O).as_posix(),'changedPixels':int(np.any(a!=out,2).sum()),'protectedBodyOutsideMaskExact':True});records.append(info)
 if count%500==0:print(json.dumps({'processed':count+1,'attachmentFindings':len(errors)}),flush=True)
outindex={'candidatePacks':{'bare':[],'helmet':[]}}
for gear,paths in read(BASE/'package.json')['candidatePacks'].items():
 for i,path in enumerate(paths):
  mp=R/path[6:];m=read(mp)
  for s in m['states']:s['frameFiles']=[replacements[(mp.parent/f).resolve().relative_to(BASE.resolve()).as_posix()] for f in s['frameFiles']]
  dest=O/'packs'/f'{gear}-{i:02d}.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(m,indent=2)+'\n');outindex['candidatePacks'][gear].append('res://'+dest.relative_to(R).as_posix())
(O/'candidate-bank-index.json').write_text(json.dumps(outindex,indent=2)+'\n');(O/'revision.json').write_text(json.dumps({'status':'Matte style and anatomical neck candidate; visual/native review pending','records':records,'attachmentFindings':errors},indent=2)+'\n')
print(json.dumps({'sourceDrawings':len(records),'changed':sum(q['changedPixels']>0 for q in records),'attachmentFindings':len(errors),'examples':errors[:10]}))
