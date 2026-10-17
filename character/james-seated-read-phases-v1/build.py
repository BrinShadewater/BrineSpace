"""Draw/held/stow phases from exact current whole seated reading sources."""
from pathlib import Path
import json,copy,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
baseline=P/'source-bindings.json'
if not baseline.exists():
    coverage=json.loads((R/'character/james-animation-coverage-2026-09-30/runtime-coverage.json').read_text());bindings=[]
    for mode,group in [('bare','body'),('helmet','equipment')]:
        for direction in ['north','south','east','west']:
            key='read-seated-'+direction;f=R/coverage[group][key]['path'];m=json.loads(f.read_text());state=next(s for s in m['states'] if s['id']==key)
            paths=[R/x[6:] if x.startswith('res://') else (f.parent/x).resolve() for x in state['frameFiles']]
            bindings.append({'mode':mode,'direction':direction,'manifest':str(f.relative_to(R)),'header':{k:v for k,v in m.items() if k!='states'},'state':state,'sources':[{'path':x.relative_to(R).as_posix(),'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in paths]})
    baseline.write_text(json.dumps(bindings,indent=2)+'\n')
bindings=json.loads(baseline.read_text());records=[]
for mode in ['bare','helmet']:
    own=[x for x in bindings if x['mode']==mode];pack=copy.deepcopy(own[0]['header']);pack['states']=[];pack['name']='James seated tablet draw/held/stow '+mode
    pack['status']=json.loads((P/'selection.json').read_text()).get('status','staged_phase_review_pending') if (P/'selection.json').exists() else 'staged_phase_review_pending'
    for binding in own:
        for source in binding['sources']:assert hashlib.sha256((R/source['path']).read_bytes()).hexdigest()==source['sha256']
        for action,poses,durations,loop in [('read-seated-enter',[0,4,4,3,2,2],[80]*6,False),('read-seated',[2,3,2,3,2,3],[600]*6,True),('read-seated-exit',[2,2,3,4,4,0],[80]*6,False)]:
            state=copy.deepcopy(binding['state']);state['id']=action+'-'+binding['direction'];state['frameFiles']=['res://'+binding['sources'][i]['path'] for i in poses];state['frameCount']=6;state['frameDurationsMs']=durations;state['loop']=loop
            for key in ['depthOffsets']:
                if key in state:state[key]=[binding['state'][key][i] for i in poses]
            state['provenance'].update(phaseSourcePoses=poses,derivation='Exact current whole authored seated source aliases. Entry0/4/3/2, held2/3, exact reverse exit. Repeated aliases are holds, not newly authored drawings. No pixels/scale/grade/foot edits.')
            pack['states'].append(state);records.append({'mode':mode,'key':state['id'],'sourcePoses':poses,'durationMs':sum(durations),'loop':loop})
    (P/(mode+'-manifest.json')).write_text(json.dumps(pack,indent=2)+'\n')
(P/'phase-evidence.json').write_text(json.dumps({'records':records,'references':144,'frozenOriginalSourceReferences':48,'usedSourcePoseReferences':32,'uniqueSourcePosesPerFacing':4,'scope':'Existing source0/2/3/4 only; holds/reverse aliases, no new authored art. Original12second observation budget: .48entry +11.04held +.48exit.'},indent=2)+'\n')
print('Paired12states/144references, exact authored whole-source aliases; no new artwork.')
