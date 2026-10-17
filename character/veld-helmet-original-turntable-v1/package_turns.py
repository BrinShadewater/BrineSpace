from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1];T=R/'character/veld-cargo-turns-master-family-v1';checks=0
for gear in ['bare','helmet']:
 combined=None
 for family in ['north-east-candidate-v5','east-south-candidate-v3']:
  m=json.loads((T/family/f'{gear}-manifest.json').read_text())
  if combined is None:combined={k:v for k,v in m.items() if k!='states'};combined['states']=[]
  combined['states']+=m['states']
 (P/f'baseline-{gear}-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
 if gear=='helmet':
  for state in combined['states']:
   family='north-east-candidate-v5' if 'north-east' in state['id'] or 'east-north' in state['id'] else 'east-south-candidate-v3'
   state['frameFiles']=['res://'+(P/'v3-study/pilot'/family/Path(ref).name).relative_to(R).as_posix() for ref in state['frameFiles']]
 combined['name']='Veld shared original helmet NE ES turns '+gear;combined['status']='staged_shared_original_helmet_not_installed'
 for state in combined['states']:
  assert not state['loop'] and sum(state['frameDurationsMs'])==800;checks+=1
  assert all((R/ref[6:]).is_file() for ref in state['frameFiles']);checks+=1
 ne=next(s for s in combined['states'] if s['id']=='carry-turn-north-east');es=next(s for s in combined['states'] if s['id']=='carry-turn-east-south')
 assert (R/ne['frameFiles'][-1][6:]).read_bytes()==(R/es['frameFiles'][0][6:]).read_bytes();checks+=1
 (P/f'{gear}-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
print(str(checks)+' timing/source/shared-East package checks0')
