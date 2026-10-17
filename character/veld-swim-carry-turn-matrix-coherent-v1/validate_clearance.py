from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1];live=R/'character/dr-veld-v2/clearance.json';archived=H/'revisions/before-runtime-selection-v1/selected-clearance.json';base=archived if archived.exists() else live;old=json.loads(base.read_text());candidate=json.loads((H/'candidate-clearance-profile-v1.json').read_text());report=json.loads((H/'candidate-clearance-v1.json').read_text());checks=0;changed=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(v):
 global checks
 assert v;checks+=1
def covers(a,b):return all(a[i]<=b[i] if i<2 else a[i]>=b[i] for i in range(4))
check(sha(base)==report['selectedClearanceSha256'])
if archived.exists():check(json.loads(live.read_text())==candidate)
for section in ['swim','tread','actions','life']:
 for g,values in old[section].items():
  for key,b in values.items():
   c=candidate[section][g][key];check(covers(c,b))
   if c!=b:changed.append(dict(section=section,gear=g,key=key,before=b,after=c))
check(candidate['tread']==old['tread'])
for r in report['records']:
 g=r['gear'];d=r['state'].split('-')[-1];action=candidate[r['actionSection']][g][r['actionKey']];move=candidate['swim'][g][d];effective=[min(action[i],move[i]) if i<2 else max(action[i],move[i]) for i in range(4)]
 for f in r['frames']:
  check(sha(R/f['file'])==f['sha256']);check(covers(effective,f['nativeBounds']))
  if r['state'].startswith('swim-carry-') and not r['state'].startswith('swim-carry-turn-'):check(covers(move,f['nativeBounds']))
(H/'candidate-clearance-checks-v1.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=archived.exists(),changedBounds=changed,selectedClearanceSha256=sha(base),candidateProfileSha256=sha(H/'candidate-clearance-profile-v1.json'),measurementSha256=sha(H/'candidate-clearance-v1.json'),scope='Conservative no-shrink profile,all336candidate frame hashes/effective actual gate coverage;48cargo movement frames covered. No world clearance claim.'),indent=2)+'\n',encoding='utf-8');print(f'{checks} candidate envelope/hash/no-shrink checks PASS;{len(changed)} bounds expanded;original bounds preserved; installed profile verified when selected.')
