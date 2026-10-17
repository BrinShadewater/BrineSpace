from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import json,hashlib,numpy as np,sys
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;C=R/'character/krusher-james-canonical-v7'
read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for family in ['water-family','water-cargo-turns','water-interruptions']:
 newVersion=3 if family=='water-interruptions' else 4;oldVersion=2 if family=='water-interruptions' else 3;P=R/f'character/krusher-{family}-v{newVersion}';OLD=R/f'character/krusher-{family}-v{oldVersion}';records=read(P/'revision.json')['records'];checks=0;errors=[];contacts=[];oldPortraitPixels=0
 def check(ok,msg):
  global checks
  checks+=1
  if not ok:errors.append(msg)
 for q in records:
  tag=q['gear']+' '+q['state']+' '+str(q['frame']);src=R/q['source'][6:];out=P/q['output'];a=arr(src);b=arr(out);mask=np.array(Image.open(P/q['mask']).convert('L'))>0
  check(sha(src)==q['sourceHash'],'source hash '+tag);check(sha(out)==q['outputHash'],'output hash '+tag);check(a.shape==b.shape,'canvas '+tag);check(np.array_equal(a[~mask],b[~mask]),'protected body and shell '+tag)
  if q['gear']=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'original shell alpha '+tag)
  d=q['details']
  if 'canonicalEndpoint' in d:
   gear=q['gear'];st=next(st for st in read(C/(gear+'-manifest.json'))['states'] if st['id']=='idle-'+d['canonicalEndpoint']);expected=np.zeros_like(b);expected[52:236,36:220]=arr(C/st['frameFiles'][0]);check(np.array_equal(b,expected),'exact canonical endpoint '+tag)
  if 'foregroundMask' in d:
   fg=np.array(Image.open(R/d['foregroundMask'][6:]).convert('L'))>0;check(np.array_equal(a[fg],b[fg]),'tool foreground '+tag)
  if 'headSource' not in d:continue
  hp=R/d['headSource'][6:];head=Image.open(hp).convert('RGBA');check(sha(hp)==d['headHash'],'source head hash '+tag);layer=Image.new('RGBA',(b.shape[1],b.shape[0]));layer.paste(head,tuple(d['paste']));h=np.array(layer)
  if q['gear']=='bare':
   visible=(h[:,:,3]>180)&np.all(h==b,axis=2)
   vlabs,_=label(visible,np.ones((3,3)));vs=np.bincount(vlabs.ravel());vs[0]=0;main=vlabs==int(vs.argmax())
   labs,_=label(b[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;body=int(sizes.argmax());detached=int((main&(labs!=body)).sum())
   check(detached==0,'primary head detached '+tag);check(int(main.sum())>int((h[:,:,3]>180).sum())*.60,'face excessively occluded '+tag)
   contacts.append({'state':q['state'],'frame':q['frame'],'detachedPrimaryHeadPixels':detached,'visibleHeadPixels':int(visible.sum()),'registrationOffset':d['neckRegistrationOffset']})
  else:
   if 'portraitMask' in d:mask=np.array(Image.open(R/d['portraitMask'][6:]).convert('L'))>0
   yy,xx=np.indices(b.shape[:2]);lining=arr(R/d['liningSource'][6:]);expected=lining[(yy-d['paste'][1])%32,(xx-d['paste'][0])%32,:3].copy();opaque=h[:,:,3]>0;expected[opaque]=h[opaque,:3];wrong=int((mask&np.any(b[:,:,:3]!=expected,axis=2)).sum());oldPortraitPixels+=wrong;check(wrong==0,'non-v4 portrait pixels inside aperture '+tag)
 refs=states=0
 for mp in P.glob('*-manifest.json'):
  check(mp.read_bytes()==(OLD/mp.name).read_bytes(),'all original manifest metadata exact '+mp.name);m=read(mp);states+=len(m['states'])
  for st in m['states']:
   refs+=len(st['frameFiles']);check(all((P/f).is_file() for f in st['frameFiles']),'all references '+mp.name+' '+st['id'])
 for rel,d in read(P/'revision.json').get('derivedSources',{}).items():
  src=R/d['source'][6:];check(sha(src)==d['sourceHash'],'rigid source hash '+rel);expected=Image.open(src).convert('RGBA').rotate(d['rotationDegrees'],resample=Image.Resampling.NEAREST,expand=True);check(np.array_equal(np.array(expected),arr(P/rel)),'rigid nearest rotation '+rel);check(sha(P/rel)==d['outputHash'],'rigid output hash '+rel)
 report={'checks':checks,'errors':errors,'states':states,'frameReferences':refs,'uniqueOutputs':len(records),'primaryHeadContactRecords':contacts,'oldPortraitPixelsInsideRevisedApertures':oldPortraitPixels,'scope':'Every unique source/output hash and protected pixel, full manifest/profile/clock preservation, every reference, all bare primary head contacts, all helmet face/lining pixels, and recorded canonical/tool/rigid-rotation joins. Offline source validation; station and owner acceptance remain separate.'};(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','states','frameReferences','uniqueOutputs','oldPortraitPixelsInsideRevisedApertures']}|{'errors':len(errors),'examples':errors[:8]}))
 if errors:raise SystemExit(1)
