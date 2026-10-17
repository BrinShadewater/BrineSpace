from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent
checks=0
def check(ok,message):
 global checks
 assert ok,message
 checks+=1
legacy=json.loads((HERE.parent/'major-bill-v3/clearance.json').read_text(encoding='utf-8'))
for gear in ['bare','helmet']:
 p=json.loads((HERE/f'{gear}-manifest.json').read_text(encoding='utf-8'));hashes=json.loads((HERE/f'{gear}-hashes.json').read_text(encoding='utf-8'))
 check(len(p['states'])==4,'complete direction coverage')
 for state in p['states']:
  direction=state['facings'][0];folder=(HERE/state['frameFiles'][0]).resolve().parents[2];bounds=[]
  check(state['loop'] and state['frameDurationsMs']==[160]*6,'retained loop clock')
  check(state['waterKinds']==['swim']*6 and state['waterPoses']==[True]*6 and state['facings']==[direction]*6,'water contract')
  for file in state['frameFiles']:
   im=Image.open(HERE/file).convert('RGBA');check(im.size==(256,256),'canvas');check(hashlib.sha256((HERE/file).read_bytes()).hexdigest()==hashes[file],'referenced pixel hash');bounds.append(im.getchannel('A').getbbox())
  authority=HERE.parent/('bill-swim-'+('helmet-' if gear=='helmet' else '')+direction+'-coherent-v1/frames/swim-'+direction+'/000.png');pad={'east':(6,40),'west':(42,40),'north':(24,56),'south':(24,-24)}[direction];expected=Image.new('RGBA',(256,256));expected.alpha_composite(Image.open(authority).convert('RGBA'),pad)
  for index in [0,5]:check(np.array_equal(np.array(Image.open(HERE/state['frameFiles'][index])),np.array(expected)),'exact selected join')
  union=[min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds)];extent=[(v-128)*65.28/148 for v in union];life=legacy['life'][gear][state['id']];swim=legacy['swim'][gear][direction];allowed=[min(life[0],swim[0]),min(life[1],swim[1]),max(life[2],swim[2]),max(life[3],swim[3])];contained=all(extent[i]>=allowed[i] for i in [0,1]) and all(extent[i]<=allowed[i] for i in [2,3]);check(contained,'effective retained clearance')
  (folder/'clearance-review.json').write_text(json.dumps({'alphaUnion':union,'worldExtent':extent,'retainedLifeClearance':life,'retainedSwimClearance':swim,'effectiveRetainedClearance':allowed,'effectiveContained':contained,'scope':'whole alpha union against actual ordinary-swim plus distress extent;not a route journey'},indent=2)+'\n',encoding='utf-8')
(HERE/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'aggregate hashes,coverage,clocks,exact joins,effective clearance;runtime selection separately'},indent=2)+'\n',encoding='utf-8');print(f'{checks} aggregate distress checks PASS')
