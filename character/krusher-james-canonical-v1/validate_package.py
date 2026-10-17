from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
v=json.loads((P/'provenance.json').read_text());errors=[];checks=0
for relative,digest in v['sourceHashes'].items():
 checks+=1
 if sha(R/relative)!=digest:errors.append('source:'+relative)
for t in v['frames']:
 checks+=2
 if sha(P/t['file'])!=t['sha256'] or sha(R/t['source'])!=t['sha256']:errors.append('frame:'+t['file'])
 if Image.open(P/t['file']).size!=(184,184):errors.append('canvas:'+t['file'])
for gear,folder in [('bare','krusher-james-cyan-test-v2'),('helmet','krusher-james-helmet-fit-v2')]:
 m=json.loads((P/(gear+'-manifest.json')).read_text());original=json.loads((R/'character'/folder/'manifest.json').read_text())
 for s in m['states']:
  src=next(t for t in original['states'] if t['id']==s['id'])
  for key,val in src.items():
   if key=='frameFiles':continue
   checks+=1
   if s[key]!=val:errors.append('state:'+s['id']+':'+key)
  checks+=1
  if len(s['frameFiles'])!=len(src['frameFiles']):errors.append('count:'+s['id'])
 for key in ['pivot','standingHeight']:
  checks+=1
  if m[key]!=original[key]:errors.append('registration:'+key)
report={'checks':checks,'errors':errors,'scope':'Current source/output bytes,184px canvases, exact state metadata/clocks and physical registration; selection is owner base choice, not animation artistic acceptance'}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));assert not errors
