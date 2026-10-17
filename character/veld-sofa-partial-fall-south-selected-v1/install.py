from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];P=Path(__file__).resolve().parent
path=R/'character/ACTIVE_ASSETS.json';original=path.read_bytes();d=json.loads(original)
for key,gear in [('actionOverrides','bare'),('equipmentActionOverrides','helmet')]:
    d[key]['veld-south-sofa-partial-falls']=f'character/veld-sofa-partial-fall-south-selected-v1/{gear}-manifest.json'
    literal=f'res://character/veld-sofa-partial-fall-south-selected-v1/{gear}-manifest.json'
    binding={'script':'scripts/grid_canvas.gd','contains':literal}
    if binding not in d['bindings']:d['bindings'].append(binding)
    assert literal in (R/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
temp=path.with_name('ACTIVE_ASSETS.veld-partial-selection.tmp')
temp.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert path.read_bytes()==original,'Concurrent registry changes; retry with current bytes'
temp.replace(path)
print('Normal registry selects both partial-fall manifests, other actor selections retained')
