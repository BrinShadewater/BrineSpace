from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent;d=json.loads((R/'manifest.json').read_text());count=0
for e in d['states']:
    body=Image.open(R/e['atlas']['path']).convert('RGBA');cargo=Image.open(R/e['cargoAtlas']['path']).convert('RGBA')
    assert len(e['frameFiles'])==len(e['cargoFiles'])==e['frameCount']
    frames=[]
    for n,(bp,cp) in enumerate(zip(e['frameFiles'],e['cargoFiles'])):
        b=Image.open(R/bp).convert('RGBA');c=Image.open(R/cp).convert('RGBA');box=(n%6*512,n//6*512,(n%6+1)*512,(n//6+1)*512)
        assert b.size==c.size==(512,512) and b.tobytes()==body.crop(box).tobytes() and c.tobytes()==cargo.crop(box).tobytes()
        bounds=b.getbbox();assert min(bounds[:2])>0 and max(bounds[2:])<512
        frames.append(np.array(b));count+=1
    if e['loop']:
        changes=[np.abs(frames[(n+1)%len(frames)].astype(float)-f).mean() for n,f in enumerate(frames)]
        assert changes[-1]<max(changes[:-1])*1.2+1e-8,(e['id'],'loop spike')
for source in d['sourceFiles']:assert hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256']
states={e['state']:e for e in d['states']}
for left,ln,right,rn in [('retrieve',119,'carry',59),('carry',0,'release',0),('release',119,'idle',59)]:
    a=Image.open(R/states[left]['frameFiles'][ln]);b=Image.open(R/states[right]['frameFiles'][rn])
    # Different propulsion rates can change only the rotor texture; claw geometry must agree.
    assert a.getchannel('A').tobytes()==b.getchannel('A').tobytes(),(left,right)
result={'clips':5,'heading':'south','bodyFrames':count,'cargoFrames':count,'atlasParity':'pass','clipping':'none','loopSpikes':'none','clawEndpointSilhouettes':'pass','sourceHashes':'pass','scope':'pilot, not complete directional pack'}
(R/'review/validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))
