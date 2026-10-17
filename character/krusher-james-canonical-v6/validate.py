from pathlib import Path
import hashlib,json,numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation,label
P=Path(__file__).resolve().parent;R=P.parent.parent;old=R/'character/krusher-james-canonical-v5';records=json.loads((P/'revision.json').read_text())['records'];checks=0;errors=[];contacts=[]
def check(ok,msg):
 global checks
 checks+=1
 if not ok:errors.append(msg)
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for q in records:
 if q['alias']:continue
 a=arr(R/q['source'][6:]);b=arr(P/q['output']);mask=np.array(Image.open(P/q['mask']))>0
 check(sha(R/q['source'][6:])==q['sourceHash'],'source hash');check(sha(P/q['output'])==q['outputHash'],'output hash');check(b.shape==(184,184,4),'original canvas');check(np.array_equal(a[~mask],b[~mask]),'outside head mask '+q['output']);check(np.array_equal(a[q['protectedFromRow']:],b[q['protectedFromRow']:]),'protected lower body '+q['output'])
 details=q['details']
 if 'headSource' not in details:check(np.array_equal(a,b),'rear untouched');continue
 check(sha(R/details['headSource'][6:])==details['headHash'],'generated source hash')
 if q['gear']=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'helmet shell alpha exact');continue
 head=arr(R/details['headSource'][6:]);x,y=details['paste'];layer=np.zeros_like(a);layer[y:y+head.shape[0],x:x+head.shape[1]]=head;opaque=layer[:,:,3]>180;tablet=None
 if 'tabletMask' in details:tablet=np.array(Image.open(R/details['tabletMask'][6:]))>0;opaque&=~tablet;check(np.array_equal(a[tablet],b[tablet]),'independent original tablet foreground '+q['output'])
 check(np.array_equal(b[opaque],layer[opaque]),'inserted opaque full head/neck exact, no inherited grey pixels '+q['output']);body=(b[:,:,3]>180)&~opaque;lower=opaque.copy();lower[:y+head.shape[0]*3//4]=False;edge=int((binary_dilation(lower)&body).sum());lab,n=label(b[:,:,3]>180);largest=np.bincount(lab.ravel())[1:].argmax()+1;joined=bool(np.all(lab[opaque]==largest));contacts.append({'gear':q['gear'],'state':q['state'],'index':q['index'],'output':q['output'],'edge':edge,'headJoinedToMainBody':joined});check(edge>0,'neck edge '+q['output']);check(joined,'head joined '+q['output'])
for gear in ['bare','helmet']:
 name=gear+'-manifest.json';check((P/name).read_bytes()==(old/name).read_bytes(),'whole original manifest byte identical '+gear);m=json.loads((P/name).read_text());states={s['id']:s for s in m['states']}
 for d in ['east','north','south','west']:
  action=states['interact-'+d];idle=states['idle-'+d]
  for i in [0,-1]:check(np.array_equal(arr(P/action['frameFiles'][i]),arr(P/idle['frameFiles'][0])),'exact tablet/idle endpoint '+gear+d)
 check(all((P/f).is_file() for s in m['states'] for f in s['frameFiles']),'all original frame slots present')
result={'checks':checks,'errors':errors,'uniqueOutputs':sum(not q['alias'] for q in records),'bareContacts':contacts,'scope':'All1675unique outputs and2122source slots through exact manifests, protected original bodies/hashes, helmet alpha and visible bare generated head sources/tablet occlusion. Every changed bare pose tested for complete silhouette contact and lower-neck adjacency;16exact action-idle joins. Technical checks do not certify owner likeness or final all-family animation/station acceptance.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');bad=[q for q in contacts if not q['edge'] or not q['headJoinedToMainBody']];print(json.dumps({'checks':checks,'errors':len(errors),'examples':errors[:12],'bareContactPoses':len(contacts),'badContactExamples':bad[:8]}));assert not errors
