from pathlib import Path
import json,copy
P=Path(__file__).resolve().parent;R=P.parent.parent;inv=json.load(open(R/'character/krusher-complete-animation-v1/source-coverage.json'))
for gear in ['bare','helmet']:
 oldpath=R/f'character/krusher-cargo-family-v1/{gear}-manifest.json';old=json.load(open(oldpath));state=copy.deepcopy(next(s for s in old['states'] if s['id']=='carry-settle-west'));source=inv['resolved'][gear]['carry-settle-west'];m=copy.deepcopy(source['profile']);m['name']='Krusher Dom West cargo settle '+gear;m['status']='candidate-not-installed';m['identity']=old['identity'];state['frameFiles']=['res://'+(oldpath.parent/f).relative_to(R).as_posix() for f in state['frameFiles']];state['provenance']['sourceManifest']=source['manifest'];state['provenance']['profileRepair']='Exact frozen original root filter profile, no raster or clock change';m['states']=[state];(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('Two source-profile-preserving override manifests, no new raster.')
