from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;C=R/'character/krusher-james-canonical-v7';read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for family in ['meal-family','meal-service']:
 P=R/('character/krusher-'+family+'-v4');OLD=R/('character/krusher-'+family+'-v3');records=read(P/'revision.json')['records'];checks=0;errors=[];contacts=[]
 def check(ok,msg):
  global checks
  checks+=1
  if not ok:errors.append(msg)
 for i,q in enumerate(records):
  tag=family+' '+str(i);a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']).convert('L'))>0;d=q['details'];row=d.get('protectedFromRow',141);check(sha(R/q['source'][6:])==q['sourceHash'],'source hash '+tag);check(sha(P/q['output'])==q['outputHash'],'output hash '+tag);check(a.shape==b.shape==(256,256,4),'canvas '+tag);check(np.array_equal(a[~mask],b[~mask]),'body outside head mask '+tag);check(np.array_equal(a[row:],b[row:]),'body below head '+tag)
  if 'headSource' in d:
   hp=R/d['headSource'][6:];head=Image.open(hp).convert('RGBA');check(sha(hp)==d['headHash'],'head hash '+tag);layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(d['paste']));h=np.array(layer);visible=(h[:,:,3]>180)&np.all(h==b,2);hl,_=label(visible,np.ones((3,3)));hs=np.bincount(hl.ravel());hs[0]=0;main=hl==int(hs.argmax());labs,_=label(b[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;detached=int((main&(labs!=int(sizes.argmax()))).sum());check(detached==0 and hs.max()>0,'head attachment '+tag);check(int(main.sum())>int((h[:,:,3]>180).sum())*.6,'head visibility '+tag);contacts.append({'record':i,'detached':detached})
  if 'foregroundMask' in d:
   fg=np.array(Image.open(R/d['foregroundMask'][6:]).convert('L'))>0;check(np.array_equal(a[fg],b[fg]),'original utensils '+tag)
  if 'canonicalTabletPose' in d or 'canonicalEndpoint' in d:
   gear=q['gear'];sid=('interact-'+d['state'].rsplit('-',1)[1]) if 'canonicalTabletPose' in d else 'idle-'+d['canonicalEndpoint'];idx=d.get('canonicalTabletPose',0);s=next(s for s in read(C/(gear+'-manifest.json'))['states'] if s['id']==sid);n=arr(C/s['frameFiles'][idx]);expected=np.zeros((256,256,4),np.uint8);expected[52:236,36:220]=n;check(np.array_equal(expected,b),'exact canonical join '+tag)
   if gear=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'shell alpha '+tag)
 states=refs=0
 for mp in P.glob('*-manifest.json'):
  check(mp.read_bytes()==(OLD/mp.name).read_bytes(),'manifest exact '+mp.name);m=read(mp);states+=len(m['states'])
  for s in m['states']:
   refs+=len(s['frameFiles']);check(all((P/f).is_file() for f in s['frameFiles']),'reference completeness '+s['id'])
 report={'checks':checks,'errors':errors,'states':states,'frameReferences':refs,'uniqueOutputs':len(records),'primaryHeadContacts':contacts,'scope':'All source/output/head hashes, exact body protection and original lower body, all bare head attachment/visibility, recorded utensil foreground masks, exact canonical tablet and idle joins, full original manifest bytes and every frame reference. Offline source evidence; station acceptance pending.'};(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','states','frameReferences','uniqueOutputs']}|{'errors':len(errors),'examples':errors[:5]}))
 if errors:raise SystemExit(1)
