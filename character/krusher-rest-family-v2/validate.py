from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;proof=json.load(open(P/'provenance.json'));inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'));checks=0;errors=[];joins=[]
def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
def arr(p):return np.array(Image.open(p).convert('RGBA'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def resolve(mp,f):return R/f[6:] if f.startswith('res://') else mp.parent/f
yy,xx=np.indices((256,256))
for q in proof['records']:
 a=arr(R/q['source']);b=arr(P/q['output']);mask=np.array(Image.open(P/q['allowedMask']))>0
 check(sha(R/q['source'])==q['sourceHash'],'source hash');check(sha(P/q['output'])==q['outputHash'],'output hash');check(sha(R/q['headSource'])==q['headHash'],'head hash');check(b.shape==(256,256,4),'canvas');check(np.array_equal(a[~mask],b[~mask]),'protected pixels '+q['output'])
 x0,y0,x1,y1=q['headBox'];nx,ny=q['neck'];changed=np.any(a!=b,2);headzone=(xx>=x0-25)&(xx<x1+25)&(yy>=y0-25)&(yy<y1+8);upper=((xx-nx)**2+(yy-ny)**2)<75**2
 check(not np.any(changed&~(headzone|upper)),'distant body/equipment preservation '+q['output']);check(np.array_equal(a[:,:,3][~headzone],b[:,:,3][~headzone]),'body geometry preserved')
 if q['gear']=='helmet':check(np.array_equal(a[:,:,3],b[:,:,3]),'helmet shell alpha')
for gear in ['bare','helmet']:
 m=json.load(open(P/(gear+'-manifest.json')));states={s['id']:s for s in m['states']};check(m['pivot']==[128,224] and m['standingHeight']==148,'ruler')
 for s in states.values():
  original=inv['resolved'][gear][s['id']]['state'];check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in original.items() if k not in ['frameFiles','provenance']},'source timing/facing/contact/depth/loop '+s['id'])
 for d in ['east','north','south','west']:
  for left,right in [('lie-down','sleep'),('sleep','get-up')]:
   l=states[left+'-'+d];r=states[right+'-'+d];check(np.array_equal(arr(P/l['frameFiles'][-1]),arr(P/r['frameFiles'][0])),'shared rest endpoint '+gear+d+left);joins.append(gear+' '+d+' '+left+' -> '+right)
  check(states['lie-down-'+d]['frameFiles']==list(reversed(states['get-up-'+d]['frameFiles'])),'exact reversed source choreography '+gear+d)
 for left,right in [('bunk-enter-east','bunk-sleep-east'),('bunk-sleep-east','bunk-exit-east')]:check(np.array_equal(arr(P/states[left]['frameFiles'][-1]),arr(P/states[right]['frameFiles'][0])),'bunk shared endpoint');joins.append(gear+' '+left+' -> '+right)
 check(states['bunk-enter-east']['frameFiles']==list(reversed(states['bunk-exit-east']['frameFiles'])),'bunk exact reverse')
result={'checks':checks,'errors':errors,'joins':joins,'scope':'Source/output/head hashes; native canvas and ruler; protected pixels and distant body; original state timing, facings, depths and furniture flags; exact rest endpoint and reverse choreography. Does not assert identity quality or station furniture contact.'};(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':errors,'joins':len(joins)}));assert not errors
