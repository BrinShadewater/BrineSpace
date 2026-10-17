from pathlib import Path
import json
import numpy as np
from PIL import Image, ImageDraw

R=Path(__file__).resolve().parents[2]
H=R/'character/krusher-continuous-playback-v1'
def read(p): return json.loads(p.read_text())
def rgba(p): return np.array(Image.open(R/p).convert('RGBA'))
records=[]
for q in read(H/'bunk-registration.json'):
    a,b=rgba(q['source']),rgba(q['output'])
    mask=np.array(Image.open(R/q['mask']).convert('L'))>0
    assert np.array_equal(a[~mask],b[~mask])
    assert q['opaqueContactPixels']>=20
    records.append(dict(q,kind='helmet/collar registration',bodyOutsideMaskExact=True))
style={q['source']:q for q in read(R/'character/krusher-style-neck-bank-v1/revision.json')['records']}
for q in read(H/'visor-pilot.json'):
    a,b=rgba(q['source']),rgba(q['output'])
    mask=Image.open(R/'character/krusher-style-neck-bank-v1'/style[q['sourceRaw']]['mask']).convert('L')
    ImageDraw.Draw(mask).polygon([tuple(p) for p in q['polygon']],fill=255)
    m=np.array(mask)>0
    assert np.array_equal(a[~m],b[~m])
    assert np.array_equal(a[:,:,3],b[:,:,3])
    records.append(dict(q,kind='visor interior',bodyOutsideMaskExact=True,alphaExact=True))
assert len(records)==21
(H/'repair-validation.json').write_text(json.dumps({'correctedDrawings':len(records),'failures':0,'records':records},indent=2))
a,b=read(H/'library-v10.json')['states'],read(H/'library.json')['states']
changes=[]; mapping={}
for k in a:
    assert len(a[k]['files'])==len(b[k]['files'])
    n=0
    for x,y in zip(a[k]['files'],b[k]['files']):
        if Path(x).name!=Path(y).name:
            n+=1
            assert mapping.setdefault(x,y)==y
    if n: changes.append({'key':k,'holds':n})
scope={'changedDrawings':len(mapping),'changedStates':len(changes),'changedHolds':sum(x['holds'] for x in changes),'unchangedStates':len(a)-len(changes),'consistentSourceReplacements':True,'states':changes}
(H/'changed-scope.json').write_text(json.dumps(scope,indent=2))
print({k:v for k,v in scope.items() if k!='states'})
