from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;proof=json.loads((P/'provenance.json').read_text());m=json.loads((P/'bare-manifest.json').read_text());checks=0;errors=[]
def check(ok,label):
 global checks
 checks+=1
 if not ok:errors.append(label)
records={r['sourceHash']:r for r in proof['records']}
for r in proof['records']:
 check(hashlib.sha256((R/r['source']).read_bytes()).hexdigest()==r['sourceHash'],'source hash')
 if r['headSource']:check(hashlib.sha256((R/r['headSource']).read_bytes()).hexdigest()==r['headHash'],'head hash')
 check(hashlib.sha256((P/r['output']).read_bytes()).hexdigest()==r['outputHash'],'output hash')
 a0=Image.open(R/r['source']).convert('RGBA');pad=Image.new('RGBA',(256,256));pad.alpha_composite(a0,tuple(r['sourcePadding']));a=np.array(pad);b=np.array(Image.open(P/r['output']).convert('RGBA'));allowed=np.array(Image.open(P/r['allowedMask']))>0
 check(b.shape==(256,256,4),'canvas');check(np.array_equal(a[~allowed],b[~allowed]),'protected body');check(np.array_equal(a[r['protectedFromRow']:],b[r['protectedFromRow']:]),'lower body/boot protection')
for s in m['states']:
 source=proof['sourceStates'][s['id']];mp=R/source['manifest'].removeprefix('res://');check(hashlib.sha256(mp.read_bytes()).hexdigest()==source['sha256'],'manifest hash');old=next(row for row in json.loads(mp.read_text())['states'] if row['id']==s['id'])
 check({k:v for k,v in s.items() if k not in ['frameFiles','provenance']}=={k:v for k,v in old.items() if k not in ['frameFiles','provenance']},'clock/events/chronology metadata')
 for i,f in enumerate(old['frameFiles']):
  path=R/f.removeprefix('res://') if f.startswith('res://') else mp.parent/f;h=hashlib.sha256(path.read_bytes()).hexdigest();check(s['frameFiles'][i]==records[h]['output'],'exact shared source derivation')
cm=json.loads((R/'character/krusher-james-canonical-v4/bare-manifest.json').read_text());idle_hashes={}
for direction,j in [('north',0),('south',9)]:
 idle=next(s for s in cm['states'] if s['id']=='idle-'+direction);pad=Image.new('RGBA',(256,256));pad.alpha_composite(Image.open(R/'character/krusher-james-canonical-v4'/idle['frameFiles'][0]).convert('RGBA'),(36,52));expected=np.array(pad);endpoint=next(r for r in proof['records'] if r['newSourceIndex']==j);check(np.array_equal(expected,np.array(Image.open(P/endpoint['output']).convert('RGBA'))),'complete canonical idle:'+direction);idle_hashes[direction]=endpoint['outputHash']
returns=[s for s in m['states'] if s['id'].startswith('meal-return-')];exact_returns=sum(hashlib.sha256((P/s['frameFiles'][-1]).read_bytes()).hexdigest()==idle_hashes[s['id'].rsplit('-',1)[1]] for s in returns)
check(exact_returns==len(returns),'all interrupted returns end at canonical idle')
result={'checks':checks,'errors':errors,'states':len(m['states']),'uniquePoses':len(records),'indexedReturns':len(returns),'exactIdleReturnTails':exact_returns};(P/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not errors
