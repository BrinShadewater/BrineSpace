from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1]
source=json.loads((P/'SOURCE_REVIEW.json').read_bytes())
assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in source['bindings'].items())
inventory_path=R/'character/veld-master-consistency-current-v2/selected-library.json'
inventory=json.loads(inventory_path.read_bytes());bindings=dict(source['bindings'])
shell=Image.open(R/'character/veld-shared-helmet-south-v1/fitted-helmet.png').convert('RGBA')
for gear in ['bare','helmet']:
    data=json.loads((P/f'{gear}-source-manifest.json').read_bytes())
    im=Image.open(P/'original-idle-master.png').convert('RGBA')
    if gear=='helmet':
        im.paste((0,0,0,0),(111,77,143,102));im.alpha_composite(shell,(110,69))
    dest=P/f'{gear}-reference-south.png';im.save(dest)
    data['states'].append(dict(id='reference-south',frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
    entry=inventory['resolved'][gear]['idle-south'];selected=R/entry['frameFiles'][0]
    assert hashlib.sha256(selected.read_bytes()).hexdigest()==inventory['sourceBindings'][entry['frameFiles'][0]]
    plate=Image.new('RGBA',(256,256));px,py=entry['pivot']
    plate.alpha_composite(Image.open(selected).convert('RGBA'),(128-round(px),224-round(py)))
    dest=P/f'{gear}-selected-idle.png';plate.save(dest)
    data['states'].append(dict(id='idle-south',frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
    path=P/f'{gear}-native-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    for state in data['states']:
        for ref in state['frameFiles']:
            p=R/ref[6:];bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    for p in [path,selected,R/entry['manifest']]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in [inventory_path,Path(__file__),P/'SOURCE_REVIEW.json',P/'generation.json']:
    bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(P/'full-source-record.json').write_text(json.dumps(dict(frameCount=source['frameCount'],durationMs=source['durationMs'],bindings=bindings,scope='Complete finite South scanner source paired to original front helmet and original/current idle references. Appearance comparison only; not controller or final motion acceptance.'),indent=2)+'\n',encoding='utf-8')
print('South native source comparison prepared.')
