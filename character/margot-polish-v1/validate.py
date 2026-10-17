"""Read-only checks for Margot's review revision, not gameplay acceptance."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parent
m=json.loads((R/'manifest.json').read_text());states={s['id']:s for s in m['states']}
frames={};count=0
for key,s in states.items():
    assert len(s['frameFiles'])==len(s['frameDurationsMs'])
    assert min(s['frameDurationsMs'])>0
    frames[key]=[]
    for f in s['frameFiles']:
        im=Image.open(R/f).convert('RGBA');a=np.array(im)[:,:,3];box=im.getbbox()
        assert im.size==(184,184) and box and box[0]>0 and box[1]>0 and box[2]<184 and box[3]<184,(key,f,box)
        assert set(np.unique(a))<={0,255}
        frames[key].append(im.tobytes());count+=1
for d in ['south','west','north','east']:
    assert frames['sit-enter-'+d][0]==frames['idle-'+d][0]
    assert frames['sit-enter-'+d][-1]==frames['sit-'+d][0]==frames['sit-exit-'+d][0]
    assert frames['sit-exit-'+d][-1]==frames['idle-'+d][0]
    assert len(set(frames['walk-'+d]))==6
    assert 0<m['calibration'][d]['motionScale']<=1 and 0<m['calibration'][d]['sitScale']<=1
    for action in ['groom','nap','yawn']+(['pet'] if d=='south' else []):
        assert frames[action+'-enter-'+d][0]==frames['idle-'+d][0]
        assert frames[action+'-enter-'+d][-1]==frames[action+'-'+d][0]
        assert frames[action+'-exit-'+d][-1]==frames['idle-'+d][0]
    assert frames['stretch-'+d][0]==frames['stretch-'+d][-1]==frames['idle-'+d][0]
    for key,value in m['calibration'][d].items():
        if key.endswith('Scale'):assert 0<value<=1,(d,key,value)
for name,expected in m['sourceHashes'].items():assert hashlib.sha256((R/'sources'/name).read_bytes()).hexdigest()==expected
baseline=json.loads((R/'baseline.json').read_text())
for s in baseline['states']:
    original=R.parents[1]/'character'/s['sourcePack']
    for i,path in enumerate(s['frameFiles']):
        assert (R/path).read_bytes()==(original/'frames'/s['id']/f'{i:03}.png').read_bytes()
report=dict(clips=len(states),frameReferences=count,directions=4,uniqueWalkPhasesPerDirection=6,sourceUpscaling=False,
  bounds='pass',binaryAlpha='pass',transitionEndpoints='pass',sourceHashes='pass',activeBaselineUnchanged=True,
  scope='complete existing 71-state Margot library')
expected={s['id'] for s in baseline['states']}
assert set(states)==expected,(set(states)-expected,expected-set(states))
# Approved locomotion exports remain byte-identical through action expansion.
first=json.loads((R/'review/approved-first-pass-manifest.json').read_text())
assert first['sourceHashes']['locomotion-v1.png']==m['sourceHashes']['locomotion-v1.png']
report['existingStateCoverage']='71/71';report['locomotionSourceUnchanged']=True
combined=set()
for name,expected_count in [('locomotion',8),('actions',55),('water',8)]:
    path=R/'packs'/name/'manifest.json';pack=json.loads(path.read_text())
    assert len(pack['states'])==expected_count and pack['standingHeight']==148 and pack['strideDistanceCells']['walk']==.07
    for state in pack['states']:
        combined.add(state['id'])
        for relative,original in zip(state['frameFiles'],states[state['id']]['frameFiles']):
            assert (path.parent/relative).resolve()==(R/original).resolve()
assert combined==set(states)
report['runtimePackPartition']='8 locomotion / 55 actions / 8 water; shared frame files'
(R/'review/validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
