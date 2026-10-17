from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];reg=json.loads((P/'family-registration.json').read_text());checks=0
for file,key in [(P/reg['source'],'sourceSHA256'),(R/reg['helmetSource'],'helmetSourceSHA256'),(R/reg['sharedMaterialRecipe'],'sharedMaterialRecipeSHA256')]:assert hashlib.sha256(file.read_bytes()).hexdigest()==reg[key];checks+=1
for gear in ['bare','helmet']:
 data=json.loads((P/f'{gear}-manifest.json').read_text());
 unload=next(s for s in data['states'] if s['id']=='unload-north');pickup=next(s for s in data['states'] if s['id']=='pickup-north');assert pickup['frameFiles']==list(reversed(unload['frameFiles']));checks+=1
 for state in [unload,pickup]:
  old=json.loads((R/f"character/veld-{state['id'].split('-')[0]}-north-consistent-v1/original-state.json").read_text());assert {k:v for k,v in state.items() if k not in ['frameFiles','frameCount']}=={k:v for k,v in old.items() if k not in ['frameFiles','frameCount']};checks+=1;assert sum(state['frameDurationsMs'])==520 and not state['loop'];checks+=1
  for ref in state['frameFiles']:
   assert ref.startswith('res://');checks+=1;path=R/ref.removeprefix('res://');assert hashlib.sha256(path.read_bytes()).hexdigest()==reg['newFrameBindings'][path.relative_to(R).as_posix()];checks+=1;im=Image.open(path);assert im.mode=='RGBA' and im.size==(256,256);checks+=1
 first=np.array(Image.open(R/unload['frameFiles'][0].removeprefix('res://')));held=np.array(Image.open(R/reg['heldAliasDirectory']/'frames'/gear/'000.png'));assert np.array_equal(first,held);checks+=1
(P/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'scope':'Exact source/master/shell bindings, whole paths, finite action metadata/reverse aliases/exact canonical held endpoint; not native/contact/world acceptance.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0}))
