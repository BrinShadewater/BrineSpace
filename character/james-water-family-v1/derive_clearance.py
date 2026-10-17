"""Selected alpha bounds at the production65.28px world standing height."""
from pathlib import Path
import json,hashlib,copy,math
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];base=R/'character/chief-engineer-branforth-v2/clearance.json'
baseline=P/'retained-clearance.json'
old=json.loads((baseline if baseline.exists() else base).read_bytes());out=copy.deepcopy(old);evidence={'scope':'Exact new loop alpha envelopes; transition union includes actual retained water-turn pixels and prior conservative contract','worldStandingHeight':65.28,'rendererAnchor':'main.get_chief_branforth_position subtracts0.038 cells; grid draw adds0.038 cells, net actor.foot','manifests':{},'frames':{},'selected':{},'retainedTurns':{},'prior':copy.deepcopy(old)}
def union(boxes):return [min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
for mode in ['bare','helmet']:
 mf=P/(mode+'-manifest.json');m=json.loads(mf.read_bytes());evidence['manifests'][mf.name]=hashlib.sha256(mf.read_bytes()).hexdigest();scale=65.28/m['standingHeight'];pivot=m['pivot'];bounds={}
 for s in m['states']:
  boxes=[]
  for rel in s['frameFiles']:
   f=P/rel;a=np.array(Image.open(f).convert('RGBA'));y,x=np.where(a[:,:,3]>0);assert len(x);boxes.append([(x.min()-pivot[0])*scale,(y.min()-pivot[1])*scale,(x.max()+1-pivot[0])*scale,(y.max()+1-pivot[1])*scale]);evidence['frames'][rel]=hashlib.sha256(f.read_bytes()).hexdigest()
  bounds[s['id']]=union(boxes)
 evidence['selected'][mode]=bounds
 turn_bounds={d:[] for d in ['east','south','west','north']};catalog=json.loads((base.parent/'catalog.json').read_bytes())
 for rel in catalog['body' if mode=='bare' else 'equipment']:
  manifest=base.parent/rel;cm=json.loads(manifest.read_bytes());cs=65.28/cm['standingHeight'];cp=cm['pivot']
  for state in cm['states']:
   if not state['id'].startswith('swim-turn-'):continue
   boxes=[]
   for file in state['frameFiles']:
    f=manifest.parent/file;a=np.array(Image.open(f).convert('RGBA'));y,x=np.where(a[:,:,3]>0);boxes.append([(x.min()-cp[0])*cs,(y.min()-cp[1])*cs,(x.max()+1-cp[0])*cs,(y.max()+1-cp[1])*cs]);evidence['frames'][f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
   bound=union(boxes);evidence['retainedTurns'][mode+'/'+state['id']]=bound
   for direction in state['id'].split('-')[2:]:turn_bounds[direction].append(bound)
 for d in ['east','south','west','north']:
  for action in ['swim','tread']:out[action][mode][d]=bounds[action+'-'+d]
  out['actions'][mode]['transition-'+d]=union([old['actions'][mode]['transition-'+d],bounds['swim-start-'+d],bounds['swim-stop-'+d]]+turn_bounds[d])
(P/'clearance.json').write_text(json.dumps(out,indent=2)+'\n');(P/'clearance-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({mode:{a:out[a][mode] for a in ['swim','tread']} for mode in ['bare','helmet']},indent=2))
