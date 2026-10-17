"""Register only the verified Veld turn matrix; retain existing clearance."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;R=H.parents[1]
registry=R/'character/ACTIVE_ASSETS.json';out=H/'revisions/pre-install-v1';out.mkdir(parents=True,exist_ok=True)
if not (out/'ACTIVE_ASSETS.json').exists():(out/'ACTIVE_ASSETS.json').write_bytes(registry.read_bytes())
assets=json.loads(registry.read_text());before=json.dumps(assets,sort_keys=True)
for gear,field in [('bare','actionOverrides'),('helmet','equipmentActionOverrides')]:
    path='character/veld-swim-turn-matrix-coherent-v1/'+gear+'-manifest.json';assets[field]['veld-swim-turn-matrix']=path
    binding={'script':'scripts/grid_canvas.gd','contains':'res://'+path}
    if binding not in assets['bindings']:assets['bindings'].append(binding)
if json.dumps(assets,sort_keys=True)!=before:
    temporary=registry.with_name('ACTIVE_ASSETS.veld-install.tmp')
    temporary.write_text(json.dumps(assets,indent=2)+'\n',encoding='utf-8');temporary.replace(registry)
clearance=R/'character/dr-veld-v2/clearance.json';report=json.loads((H/'candidate-clearance-v1.json').read_text())
assert report['undercovered']==0 and report['selectedClearanceSha256']==hashlib.sha256(clearance.read_bytes()).hexdigest()
(H/'selection.json').write_text(json.dumps(dict(status='installed_full_ordinary_swim_turn_matrix_pending_normal_loader_checks_and_full_set_polish',states=24,references=184,normalLoaderScript='scripts/grid_canvas.gd',clearanceUnchanged=True,clearanceSha256=hashlib.sha256(clearance.read_bytes()).hexdigest(),scope='Ordinary swimming turns only; water cargo/actions/distress/death and inherited crew-life remain'),indent=2)+'\n')
print('Two literal normal-loader/registry bindings registered;24states/184refs; clearance unchanged')
