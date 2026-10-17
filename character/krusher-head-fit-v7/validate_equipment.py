from pathlib import Path
from PIL import Image
from scipy.ndimage import label
import json,numpy as np,hashlib
R=Path(__file__).resolve().parents[2];P=R/'character/krusher-helmet-transition-v5';OLD=R/'character/krusher-helmet-transition-v3';C=R/'character/krusher-james-canonical-v9';read=lambda p:json.loads(p.read_text());arr=lambda p:np.array(Image.open(p).convert('RGBA'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=0;errors=[];outputs={}
def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
for q in read(P/'revision.json')['records']:
 d=q['details'];i=d['pose'];a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']).convert('L'))>0;check(sha(R/q['source'][6:])==q['sourceHash'],'source hash '+str(i));check(sha(P/q['output'])==q['outputHash'],'output hash '+str(i));check(a.shape==b.shape==(256,256,4),'canvas '+str(i));check(np.array_equal(a[~mask],b[~mask]),'protected pixels '+str(i));check(np.array_equal(a[138:,:,3],b[138:,:,3]) if 'canonicalGearEndpoint' in d else np.array_equal(a[138:],b[138:]),'lower body or exact canonical alpha '+str(i));outputs[i]=b
 if 'canonicalGearEndpoint' in d:
  g=d['canonicalGearEndpoint'];s=next(s for s in read(C/(g+'-manifest.json'))['states'] if s['id']=='idle-east');expected=np.zeros((256,256,4),np.uint8);expected[52:236,36:220]=arr(C/s['frameFiles'][0]);check(np.array_equal(b,expected),'exact gear endpoint '+str(i))
 else:
  head=Image.open(R/d['headSource'][6:]).convert('RGBA');check(sha(R/d['headSource'][6:])==d['headHash'],'head hash '+str(i));layer=Image.new('RGBA',(256,256));layer.paste(head,tuple(d['paste']));h=np.array(layer)
  if 'visorBox' in d:
   y,x=np.indices(b.shape[:2]);lining=arr(R/d['liningSource'][6:]);expected=lining[(y-d['paste'][1])%32,(x-d['paste'][0])%32,:3].copy();opaque=h[:,:,3]>0;expected[opaque]=h[opaque,:3];check(np.array_equal(b[mask,:3],expected[mask]),'natural head and lining only '+str(i));check(np.array_equal(a[:,:,3],b[:,:,3]),'helmet original alpha '+str(i))
  else:
   visible=(h[:,:,3]>180)&np.all(h==b,2);hl,_=label(visible,np.ones((3,3)));hs=np.bincount(hl.ravel());hs[0]=0;main=hl==int(hs.argmax());labs,_=label(b[:,:,3]>180,np.ones((3,3)));sizes=np.bincount(labs.ravel());sizes[0]=0;check(hs.max()>0 and np.all(labs[main]==int(sizes.argmax())),'bare head attachment '+str(i))
check((P/'manifest.json').read_bytes()==(OLD/'manifest.json').read_bytes(),'all manifest metadata exact');m=read(P/'manifest.json');refs=0
for s in m['states']:
 for f,i in zip(s['frameFiles'],s['sourcePoseIndices']):refs+=1;check((P/f).is_file() and np.array_equal(arr(P/f),outputs[i]),'indexed equip/remove pose '+s['id']+' '+str(i))
report={'checks':checks,'errors':errors,'states':len(m['states']),'frameReferences':refs,'uniqueOutputs':len(outputs),'scope':'All source/output hashes, head shape and alpha/mask protection, bare attachment, natural visor/lining pixels, exact both canonical gear endpoints, original full manifest and indexed equip/removal correspondence. Offline source evidence; native station review pending.'};(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['checks','states','frameReferences','uniqueOutputs']}|{'errors':len(errors),'examples':errors[:5]}))
if errors:raise SystemExit(1)

