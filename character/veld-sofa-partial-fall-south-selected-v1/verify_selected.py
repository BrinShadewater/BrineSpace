from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];S=R/'character/veld-sofa-partial-fall-south-v1';checks=0
def check(ok,why):
    global checks
    assert ok,why
    checks+=1
registry=json.loads((R/'character/ACTIVE_ASSETS.json').read_text(encoding='utf-8'));grid=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
bindings=json.loads((P/'source-bindings.json').read_text(encoding='utf-8'))
for gear,key in [('bare','actionOverrides'),('helmet','equipmentActionOverrides')]:
    file=P/f'{gear}-manifest.json';data=json.loads(file.read_text(encoding='utf-8'));candidate=json.loads((S/f'{gear}-manifest.json').read_text(encoding='utf-8'))
    check({k:v for k,v in data.items() if k not in ['name','status']}=={k:v for k,v in candidate.items() if k not in ['name','status']},'Exact runtime source/profile/timing metadata')
    relative=file.relative_to(R).as_posix();check(registry[key]['veld-south-sofa-partial-falls']==relative,'Paired registry admission')
    check('"res://'+relative+'"' in grid,'Whole literal normal loader')
    check({'script':'scripts/grid_canvas.gd','contains':'res://'+relative} in registry['bindings'],'Maintained loader binding')
    for state in data['states']:
        check(not state['loop'] and state['terminalFrame']==5 and len(state['frameFiles'])==6,'Finite six-source family')
        for source in state['frameFiles']:
            check(source.startswith('res://'),'Whole source path')
            im=Image.open(R/source[6:]);check(im.size==(256,272) and im.mode=='RGBA','Same raw source/profile')
for relative,digest in bindings.items():check(hashlib.sha256((R/relative).read_bytes()).hexdigest()==digest,'Retained staged source metadata')
(P/'selection-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'statesPerGear':6,'sourceSlots':72,'sourceArtChanged':False,'scope':'paired normal loader/registry/exact candidate profile/source paths/finite clocks; actual normal world/Continue verification separate'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'sourceSlots':72}))
