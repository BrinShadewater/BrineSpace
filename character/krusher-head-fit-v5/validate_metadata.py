from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];H=Path(__file__).resolve().parent;P=R/'character/krusher-james-canonical-v8';O=R/'character/krusher-animation-package-v3/packs'
checks=0
for g in ['bare','helmet']:
 a=json.loads((O/(g+'-00.json')).read_text());b=json.loads((P/(g+'-manifest.json')).read_text())
 assert {k:v for k,v in a.items() if k not in ['states','status']}=={k:v for k,v in b.items() if k not in ['states','status']};checks+=1
 assert len(a['states'])==len(b['states']);checks+=1
 for x,y in zip(a['states'],b['states']):
  assert {k:v for k,v in x.items() if k!='frameFiles'}=={k:v for k,v in y.items() if k!='frameFiles'},x['id']
  assert len(x['frameFiles'])==len(y['frameFiles']);checks+=2
report=json.loads((H/'canonical-review.json').read_text());report['metadataChecks']=checks;report['metadataResult']='Original canvas, physical pivot, H148 ruler, pose clocks, strides, loops, and other fields unchanged. Only frame paths and authoring status replaced.'
(H/'canonical-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'metadataChecks':checks,'errors':0}))
