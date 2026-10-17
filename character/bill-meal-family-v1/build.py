from pathlib import Path
import json,copy,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];states=[];root=None;bindings={}
for direction in ['east','south','west','north']:
    source=P.parent/f'bill-meal-{direction}-family-v1/manifest.json'
    m=json.loads(source.read_text());root=root or copy.deepcopy(m)
    assert m['pivot']==[128,224] and m['standingHeight']==148 and len(m['states'])==6
    for state in m['states']:
        s=copy.deepcopy(state);assert len(s['frameFiles'])==7 and sum(s['frameDurationsMs'])==(960 if s['loop'] else 580)
        for file in s['frameFiles']:
            assert file.startswith('res://') and (R/file[6:]).is_file();bindings[file]=hashlib.sha256((R/file[6:]).read_bytes()).hexdigest()
        states.append(s)
root.update(name='Bill cardinal bare meal family',states=states,status='selected_runtime',scope='dry bare Bill meal phases; equipped actors retain inspection')
(P/'manifest.json').write_text(json.dumps(root,indent=2)+'\n',encoding='utf-8')
(P/'verification.json').write_text(json.dumps({'passed':True,'states':24,'frameReferences':168,'uniquePNG':len(bindings),'sha256':bindings,'scope':'density/clock/path source binding; service and visual evidence separate'},indent=2)+'\n',encoding='utf-8')
print('Built24 cardinal bare meal states/168 unchanged frame references')
