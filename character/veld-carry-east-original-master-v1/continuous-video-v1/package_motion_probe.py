from pathlib import Path
import json,copy
P=Path(__file__).resolve().parent;R=P.parents[2]
record=json.loads((P/'cycle-study-record.json').read_text(encoding='utf-8'))
for gear in ['bare','helmet']:
    data=json.loads((P.parent/f'{gear}-key-manifest.json').read_text(encoding='utf-8'))
    state=copy.deepcopy(data['states'][0]);count=32
    state.update(frameCount=count,frameFiles=['res://'+(P/f'cycle-study/{gear}/{i:03}.png').relative_to(R).as_posix() for i in range(count)],frameDurationsMs=record['frameDurationsMs'])
    for key,value in [('facings','east'),('waterKinds','carry'),('waterPoses',False),('depthOffsets',0.0)]:state[key]=[value]*count
    data.update(name='Veld East SOURCE motion probe '+gear,status='diagnostic_only_unresolved_contacts',strideDistanceCells={'carry-east':100.13333333333346*(384*.17/148)/384},states=[state]+data['states'][1:])
    (P/f'{gear}-probe-manifest.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('Paired diagnostic manifests written; stride is a sweep midpoint, not accepted calibration.')
