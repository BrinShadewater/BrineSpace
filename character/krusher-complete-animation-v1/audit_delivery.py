from pathlib import Path
from PIL import Image
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent;inv=json.load(open(P/'source-coverage.json'));progress=json.load(open(P/'progress.json'));checks=0;errors=[];counts={};hashes={};registeredPadding=[];imageSizes={};proofCache={}
def check(ok,why):
 global checks
 checks+=1
 if not ok:errors.append(why)
for gear in ['bare','helmet']:
 staged={}
 for path in progress['candidatePacks'][gear]:
  mp=R/path[6:];m=json.load(open(mp));hashes[path]=hashlib.sha256(mp.read_bytes()).hexdigest()
  for s in m['states']:staged[s['id']]=(mp,m,s)
 check(set(staged)==set(inv['resolved'][gear]),gear+' exact required state set')
 refs=0;unique=set()
 for key,(mp,m,s) in staged.items():
  source=inv['resolved'][gear][key];original=source['state'];profile=source['profile']
  check(len(s['frameFiles'])==len(original['frameFiles']),gear+' pose count '+key)
  for field,value in original.items():
   if field not in ['frameFiles','provenance']:check(s.get(field)==value,gear+' state field '+key+':'+field)
  delta=[m['pivot'][i]-profile['pivot'][i] for i in range(2)]
  padded=(delta==[36,52] and m['frameWidth']==256 and m['frameHeight']==256 and profile['frameWidth']==184 and profile['frameHeight'] in [184,192])
  if padded:
   pp=mp.parent/'provenance.json'
   if pp not in proofCache:proofCache[pp]=json.load(open(pp))['records']
   rows={q['output']:q for q in proofCache[pp]}
   for frame in s['frameFiles']:
    row=rows[frame];check(row.get('sourcePadding')==delta,gear+' explicit registered padding '+key)
   registeredPadding.append({'gear':gear,'state':key,'delta':delta,'sourceCanvas':[profile['frameWidth'],profile['frameHeight']],'outputCanvas':[256,256]})
  for field in ['frameWidth','frameHeight','pivot','standingHeight','textureFilter','precomposed']:
   if padded and field in ['frameWidth','frameHeight','pivot']:continue
   check(m.get(field,'nearest' if field=='textureFilter' else None)==profile.get(field,'nearest' if field=='textureFilter' else None),gear+' render profile '+key+':'+field)
  for f in s['frameFiles']:
   file=R/f[6:] if f.startswith('res://') else mp.parent/f;check(file.is_file(),gear+' pose file '+key);refs+=1;unique.add(str(file))
   if file not in imageSizes:imageSizes[file]=Image.open(file).size
   check(imageSizes[file]==(m['frameWidth'],m['frameHeight']),gear+' native canvas '+key)
  check(len(s.get('frameDurationsMs',[]))==len(s['frameFiles']),gear+' duration count '+key)
 counts[gear]={'states':len(staged),'references':refs,'uniqueFiles':len(unique)}
report={'checks':checks,'errors':errors,'coverage':counts,'registeredPadding':registeredPadding,'manifestHashes':hashes,'scope':'Exact frozen state set, source pose counts/state metadata, canvas/pivot/ruler/filter/precomposition and every referenced file. Does not establish all native station contexts or final visual consistency.'};(P/'delivery-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'checks':checks,'errors':len(errors),'firstErrors':errors[:12],'coverage':counts}))

assert not errors
