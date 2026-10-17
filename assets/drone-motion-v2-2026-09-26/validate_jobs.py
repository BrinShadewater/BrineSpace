"""Cargo ownership, contact continuity, phase coverage and completed hover checks."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from build_job_sequences import work_setup
from build_rotor_review import spin
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'manifest.json').read_text());states={s['id']:s for s in d['states']}
assert len(d['jobs'])==16
checks=[]
for direction in ['north','east','south','west']:
    for action in ['mine','collect','weld','repair']:
        s=states[d['jobs'][f'{action}-{direction}']];count=s['frameCount']
        assert s['fps']==30 and not s['loop']
        assert len(s['phases'])==len(s['rootOffsets'])==len(s['frameFiles'])==len(s['cargoFiles'])==count
        assert count-s['holdStart']==51
        assert all(p=='Complete' for p in s['phases'][s['holdStart']:])
        if action=='collect':
            assert list(dict.fromkeys(s['phases']))==['Ready','Reach','Grip','Lift','Carry','Lower','Release','Withdraw','Complete']
            events=s['cargoEvents'];assert [e['event'] for e in events]==['attach-cargo','detach-cargo']
            a,b=[e['frame'] for e in events]
            assert all(x=='pickup' for x in s['cargoState'][:a])
            assert all(x=='held' for x in s['cargoState'][a:b])
            assert all(x=='deposited' for x in s['cargoState'][b:])
            item=Image.open(ROOT/s['groundCargo']).convert('RGBA')
            # At transfer the same ore pixels occupy the same world-space contact.
            assert Image.open(ROOT/s['cargoFiles'][a]).tobytes()==item.tobytes()
            assert Image.open(ROOT/s['cargoFiles'][b-1]).tobytes()==item.tobytes()
            assert s['rootOffsets'][a]==[0,0] and s['rootOffsets'][b-1]==s['depositOffset']
            for n,path in enumerate(s['cargoFiles']):assert bool(Image.open(ROOT/path).getbbox())==(a<=n<b)
            assert s['rootOffsets'][-1]!=s['depositOffset'],'drone must clear deposited ore'
            assert max(np.linalg.norm(np.subtract(x,y)) for x,y in zip(s['rootOffsets'],s['rootOffsets'][1:]))<2
        else:
            prepared=work_setup(direction,action,d);mask=np.zeros((256,256),bool)
            for rig in prepared[-1]:mask|=spin(prepared[0],rig,0,1)[1]>0
            # End of reach and start of work are the same pixels outside spinning blades.
            for a,b in [(29,30),(131,132)]:
                left=np.array(Image.open(ROOT/s['frameFiles'][a]));right=np.array(Image.open(ROOT/s['frameFiles'][b]))
                assert not np.any(np.any(left!=right,axis=2)&~mask),(direction,action,'contact join')
            assert Image.open(ROOT/s['effectFiles'][0]).getbbox() is None
            assert Image.open(ROOT/s['effectFiles'][-1]).getbbox() is None
        checks.append({'direction':direction,'action':action,'frames':count,'status':'pass'})
(ROOT/'review/job-validation.json').write_text(json.dumps({'jobs':checks,'cargoTransfers':'same-pixel, same-world-position','finalHoverFrames':51,'status':'pass'},indent=2))
print('16 jobs: phases, transfer continuity, contact joins, root movement and completed hover pass.')
