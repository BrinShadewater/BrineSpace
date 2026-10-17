"""Paired source and normal literal-loader admission; world proof is separate."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];source=R/'character/veld-sofa-fall-south-v1';checks=0;bindings={}
def check(value,message):
    global checks
    checks+=1;assert value,message
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
registry=json.loads((R/'character/ACTIVE_ASSETS.json').read_text(encoding='utf-8'));loader=(R/'scripts/grid_canvas.gd').read_text(encoding='utf-8')
for gear in ['bare','helmet']:
    path=P/f'{gear}-manifest.json';manifest=json.loads(path.read_text())
    reference=json.loads((source/f'{gear}-manifest.json').read_text());neutral=json.loads((source/f'{gear}-neutral-manifest.json').read_text())
    check(manifest['states']==reference['states']+neutral['states'],'Exact original and neutral paired source states')
    for field in ['frameWidth','frameHeight','standingHeight','pivot','precomposed','textureFilter','sofaFallDeathMode','equipment']:check(manifest[field]==reference[field],'Exact reviewed '+field)
    check('"res://'+path.relative_to(R).as_posix()+'"' in loader,'Whole literal normal loader path')
    key='equipmentActionOverrides' if gear=='helmet' else 'actionOverrides'
    check(registry[key]['veld-south-sofa-reader-falls']==path.relative_to(R).as_posix(),'Paired registry admission')
    for state in manifest['states']:
        check(state['frameDurationsMs']==[180,180,200,220,240,500] and not state['loop'],'Finite sofa clock')
        for frame in state['frameFiles']:
            check(frame.startswith('res://character/'),'Whole source path');bindings[frame.removeprefix('res://')]=sha(R/frame.removeprefix('res://'))
    bindings[path.relative_to(R).as_posix()]=sha(path)
(P/'source-admission-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'normalLoaderPaths':True,'bindings':bindings,'scope':'paired source/registry/literal-loader admission only; actual world disk and native visual evidence separate'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'uniqueFrames':len(bindings)-2}))
