from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];T=R/'character/veld-cargo-turns-master-family-v1';checks=0
for gear in ['bare','helmet']:
 combined=None
 for family in ['north-west-candidate-v4','candidate-v7']:
  m=json.loads((T/family/f'{gear}-manifest.json').read_text())
  if combined is None:combined={k:v for k,v in m.items() if k!='states'};combined['states']=[]
  combined['states']+=m['states']
 (P/f'baseline-{gear}-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
 if gear=='helmet':
  for state in combined['states']:
   family='north-west-candidate-v4' if 'north-west' in state['id'] or 'west-north' in state['id'] else 'candidate-v7'
   state['frameFiles']=['res://'+(P/'mixed-v5-study/pilot'/family/Path(ref).name).relative_to(R).as_posix() for ref in state['frameFiles']]
 combined['name']='Veld shared original helmet four quarter turns '+gear;combined['status']='staged_shared_original_helmet_not_installed'
 for state in combined['states']:
  assert not state['loop'] and sum(state['frameDurationsMs'])==800;checks+=1
  assert all((R/ref[6:]).is_file() for ref in state['frameFiles']);checks+=1
 west=next(s for s in combined['states'] if s['id']=='carry-turn-north-west');southwest=next(s for s in combined['states'] if s['id']=='carry-turn-south-west')
 assert (R/west['frameFiles'][-1][6:]).read_bytes()==(R/southwest['frameFiles'][-1][6:]).read_bytes();checks+=1
 east=json.loads((R/f'character/veld-helmet-original-turntable-v1/{gear}-manifest.json').read_text());combined['states']+=east['states']
 for left,li,right,ri in [('north-west',0,'north-east',0),('south-west',0,'east-south',-1)]:
  a=next(s for s in combined['states'] if s['id']=='carry-turn-'+left);b=next(s for s in combined['states'] if s['id']=='carry-turn-'+right);assert (R/a['frameFiles'][li][6:]).read_bytes()==(R/b['frameFiles'][ri][6:]).read_bytes();checks+=1
 (P/f'{gear}-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
print(str(checks)+' timing/source/shared-cardinal package checks0')
