from pathlib import Path
from PIL import Image
import json,hashlib,numpy as np
P=Path(__file__).resolve().parent;R=P.parent.parent;old=R/'character/krusher-water-family-v2';qs=json.loads((P/'revision.json').read_text())['records'];checks=0;errors=[]
def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for q in qs:
 a=arr(R/q['previousSource'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0;check(sha(R/q['previousSource'][6:])==q['previousHash'],'baseline hash');check(sha(P/q['output'])==q['outputHash'],'output hash');check(a.shape==b.shape==(276,256,4),'source canvas');check(np.array_equal(a[~mask],b[~mask]),'all body outside head area exact '+q['output']);check(np.array_equal(a[q['headBox'][3]+18:],b[q['headBox'][3]+18:]),'lower body exact');yy,xx=np.indices(a.shape[:2]);d=q['state'].rsplit('-',1)[1]
 if d in ['east','west','south']:
  check(sha(R/q['details']['headSource'][6:])==q['details']['headHash'],'new source hash');hands=xx>=168 if d=='east' else xx<=87 if d=='west' else yy>=q['headBox'][3]+(4 if (q['frame'] if q['state'].startswith('swim-start-') else 5-q['frame'] if q['state'].startswith('swim-stop-') else 5 if q['state'].startswith('swim-') else 0)>=2 else 18)
  if d=='south' and q['gear']=='helmet':
   oldq=next(z for z in json.loads((old/'revision.json').read_text())['records'] if z['gear']==q['gear'] and z['state']==q['state'] and z['frame']==q['frame']);hands=yy>=max(q['headBox'][3]+4,oldq['details']['originalFaceBox'][3])
  check(np.array_equal(a[hands],b[hands]),'independent arm/hand extent '+q['state']+' '+str(q['frame'])+' '+q['gear'])
  if q['gear']=='bare':
   head=arr(R/q['details']['headSource'][6:]);x,y=q['details']['paste'];layer=np.zeros_like(a);layer[y:y+head.shape[0],x:x+head.shape[1]]=head;opaque=layer[:,:,3]>0
   if q['details'].get('foregroundFromRow') is not None:opaque[q['details']['foregroundFromRow']:]=False
   check(np.array_equal(b[opaque],layer[opaque]),'entire opaque head/neck exact, no grey original pixels '+q['output']);source=arr(R/q['source']);check(np.any(opaque&(source[:,:,3]>180)),'head overlaps actual original contact, not floating')
  else:check(np.array_equal(a[:,:,3],b[:,:,3]),'helmet alpha exact')
 else:check(np.array_equal(a,b),'other directions unchanged pending review')
for gear in ['bare','helmet']:
 name=f'water-{gear}-manifest.json';m=json.loads((P/name).read_text());check((P/name).read_bytes()==(old/name).read_bytes(),'entire original manifest byte exact');s={s['id']:s for s in m['states']}
 for d in ['east','west','north','south']:
  start=s['swim-start-'+d]['frameFiles'];stop=s['swim-stop-'+d]['frameFiles'];swim=s['swim-'+d]['frameFiles'];tread=s['tread-'+d]['frameFiles']
  for a,b in [(start[0],tread[0]),(start[-1],swim[0]),(stop[0],swim[0]),(stop[-1],tread[0])]:check(np.array_equal(arr(P/a),arr(P/b)),'exact entry/exit join')
  check(start==list(reversed(stop)),'reverse choreography alias exact')
  for fs in [swim,tread]:check(np.array_equal(arr(P/fs[0]),arr(P/fs[-1])),'loop endpoint exact')
r={'checks':checks,'errors':errors,'scope':'All112unique poses; source/output hashes, exact canvas/body outside masks, lower bodies and independent arms/hands; complete inserted opaque bare head-neck pixels exact with overlap at actual original body; helmet alpha; original manifests byte exact;32entry/exit joins,8reversals,16loop endpoints. E/W plus front/bowed South candidate, North retained, does not prove owner visual acceptance or actual station contact.'};(P/'validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':errors}));assert not errors
