from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;read=lambda p:json.loads(p.read_text())
progress=read(R/'character/krusher-complete-animation-v1/progress.json');coverage=read(R/'character/krusher-complete-animation-v1/source-coverage.json')
mapping={'krusher-james-canonical-v4':'krusher-james-canonical-v6','krusher-helmet-transition-v1':'krusher-helmet-transition-v3','krusher-meal-family-v1':'krusher-meal-family-v3','krusher-meal-service-v1':'krusher-meal-service-v3','krusher-inspection-family-v1':'krusher-inspection-family-v3','krusher-repair-family-v1':'krusher-repair-family-v3','krusher-torch-family-v1':'krusher-torch-family-v3','krusher-seated-family-v1':'krusher-seated-family-v3','krusher-cargo-family-v1':'krusher-cargo-family-v3','krusher-rest-family-v2':'krusher-rest-family-v4','krusher-recovery-salvage-v1':'krusher-recovery-salvage-v2','krusher-death-family-v1':'krusher-death-family-v2','krusher-water-family-v1':'krusher-water-family-v3','krusher-water-cargo-turns-v2':'krusher-water-cargo-turns-v3','krusher-water-interruptions-v1':'krusher-water-interruptions-v2','krusher-cargo-settle-profile-v1':'krusher-cargo-settle-profile-v3'}
index={'candidatePacks':{},'status':'all-H3-families-staged-palette-and-full-bank-review-pending','scope':'Audit input only; does not modify selected full bank or normal gameplay.'};report={'gears':{},'errors':[]};unique={};totalrefs=0
for gear,paths in progress['candidatePacks'].items():
 staged=[];states={};overrides=[]
 for path in paths:
  for old,new in mapping.items():path=path.replace(old,new)
  staged.append(path);mp=R/path[6:];m=read(mp)
  for s in m['states']:
   if s['id'] in states:overrides.append({'state':s['id'],'previous':states[s['id']]['manifest'],'override':path})
   states[s['id']]={'manifest':path,'state':s,'profile':{k:v for k,v in m.items() if k!='states'}}
 index['candidatePacks'][gear]=staged
 required=set(coverage['resolved'][gear]);missing=sorted(required-set(states));extra=sorted(set(states)-required)
 for key,q in states.items():
  mp=R/q['manifest'][6:]
  for f in q['state']['frameFiles']:
   fp=R/f[6:] if f.startswith('res://') else mp.parent/f;totalrefs+=1
   if not fp.exists():report['errors'].append('missing file: '+str(fp));continue
   if str(fp) not in unique:
    im=Image.open(fp);im.verify();unique[str(fp)]={'sha256':hashlib.sha256(fp.read_bytes()).hexdigest(),'size':list(Image.open(fp).size)}
 if missing:report['errors'].append(gear+' missing states: '+str(missing))
 report['gears'][gear]={'requiredStates':len(required),'stagedStates':len(states),'missing':missing,'extra':extra,'overrides':overrides}
report.update(frameReferences=totalrefs,uniqueFiles=len(unique),scope='All corrected candidate manifests resolve required source states and readable PNGs. Coverage is not anatomical/palette, coherent shared joins, native full-bank admission, station lifecycle or owner acceptance. Selected bank/package unchanged.')
(H/'candidate-bank-index.json').write_text(json.dumps(index,indent=2)+'\n');(H/'candidate-bank-audit.json').write_text(json.dumps(report,indent=2)+'\n');(H/'candidate-bank-file-hashes.json').write_text(json.dumps(unique,indent=2)+'\n')
print(json.dumps({'gears':{g:{k:v for k,v in q.items() if k!='overrides'} for g,q in report['gears'].items()},'frameReferences':totalrefs,'uniqueFiles':len(unique),'errors':report['errors']}));assert not report['errors']
