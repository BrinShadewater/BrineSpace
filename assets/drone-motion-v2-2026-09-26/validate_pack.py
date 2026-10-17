"""Check delivered paths, loop geometry, atlas parity and status brightness."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
assert set(d['headings'])=={'north','northeast','east','southeast','south','southwest','west','northwest'}
assert set(d['actions'])=={'mine','collect','weld','repair'}
required={f'work-{action}-{heading}' for action in d['actions'] for heading in ['north','east','south','west']}
assert required <= {s['id'] for s in d['states']},'Missing cardinal work clips'
result={'headings':8,'workActions':4,'bodyFrames':0,'effectFrames':0,'cargoFrames':0,'statusFrames':0,'atlasParitySamples':0,'statusBrightness':{},'sourceHashes':'pass'}
result['cardinalWorkClips']=len(required)
for state in d['states']:
    if state['id'] in required:
        assert state['frameCount']==102 and state['fps']==30
        assert len(state['effectFiles'])==102 and len(state['lamp'])==2
        first=Image.open(ROOT/state['frameFiles'][0])
        active=Image.open(ROOT/state['frameFiles'][35])
        assert first.tobytes()!=active.tobytes(),state['id']+' has no motion'
    for path in state['frameFiles']:
        im=Image.open(ROOT/path)
        assert im.mode=='RGBA' and im.size==(256,256),path
        box=im.getbbox();assert box and min(box[:2])>0 and max(box[2:])<256,path
        result['bodyFrames']+=1
    for path in state.get('effectFiles',[]):
        im=Image.open(ROOT/path);assert im.mode=='RGBA' and im.size==(256,256),path
        result['effectFrames']+=1
    for path in state.get('cargoFiles',[]):
        im=Image.open(ROOT/path);assert im.mode=='RGBA' and im.size==(256,256),path
        result['cargoFrames']+=1
    for kind,paths in [('atlas',state['frameFiles']),('effectAtlas',state.get('effectFiles',[])),('cargoAtlas',state.get('cargoFiles',[]))]:
        if not paths:continue
        atlas=Image.open(ROOT/state[kind]['path'])
        for index in [0,len(paths)//2,len(paths)-1]:
            x=(index%8)*256;y=(index//8)*256
            assert atlas.crop((x,y,x+256,y+256)).tobytes()==Image.open(ROOT/paths[index]).tobytes()
            result['atlasParitySamples']+=1
for name,clip in d['statusClips'].items():
    values=[]
    for path in clip['frameFiles']:
        im=Image.open(ROOT/path);assert im.mode=='RGBA' and im.size==(256,256)
        rgb=np.array(im)[128,128,:3]
        values.append(float(np.dot(rgb,[.2126,.7152,.0722])))
    assert max(values)>min(values)*2.5,(name,min(values),max(values))
    assert values[0]>values[13],name+' pulse must dim, not fade to white'
    result['statusBrightness'][name]={'minimumLuminance':round(min(values),2),'maximumLuminance':round(max(values),2)}
    result['statusFrames']+=len(values)
for entry in d['sourceFiles']:
    assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
result['status']='pass'
(ROOT/'review/pack-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
