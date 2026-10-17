from pathlib import Path
import json,copy
P=Path(__file__).resolve().parent
bowl=P.parent/'james-meal-pickup-north-v1'
cup=json.loads((P/'manifest.json').read_bytes())
meal=json.loads((bowl/'manifest.json').read_bytes())
states=copy.deepcopy(cup['states'])
for action,pack,folder in [('meal-deposit',meal,bowl),('cup-deposit',cup,P)]:
    row=copy.deepcopy(pack['states'][0]);row['id']=action+'-north'
    row['frameFiles']=['res://character/'+folder.name+'/'+path for path in reversed(row['frameFiles'])]
    row['frameDurationsMs'].reverse()
    row['provenance']['derivation']='Exact whole acquisition source figures in reverse, matching accepted held-to-empty counter return; no mirroring or body edits.'
    states.append(row)
cup['states']=states;cup['name']='James North meal counter handoffs';cup['status']='native_choreography_review_pending'
(P/'handoffs-manifest.json').write_text(json.dumps(cup,indent=2)+'\n')
assert all(sum(s['frameDurationsMs'])==900 for s in states)
print('Cup acquisition, bowl deposit and cup deposit; exact reverse whole-source returns900ms each')
