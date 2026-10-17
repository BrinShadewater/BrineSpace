from pathlib import Path
import hashlib,json
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent;R=P.parents[1];O=P/'paired-package-v1';reg=json.loads((O/'package-registration.json').read_text());original=json.loads((R/reg['originalManifest']).read_text());checks=0
for key,hashkey in [('originalManifest','originalManifestSHA256'),('helmetSource','helmetSourceSHA256')]:
 assert hashlib.sha256((R/reg[key]).read_bytes()).hexdigest()==reg[hashkey];checks+=1
for gear in ['bare','helmet']:
 data=json.loads((O/f'{gear}-manifest.json').read_text());assert {k:v for k,v in data.items() if k not in ['name','status','states']}=={k:v for k,v in original.items() if k not in ['name','status','states']};checks+=1
 state=data['states'][0];assert {k:v for k,v in state.items() if k!='frameFiles'}=={k:v for k,v in original['states'][0].items() if k!='frameFiles'};checks+=1
 for i,path in enumerate(state['frameFiles']):
  assert path.startswith('res://');checks+=1;file=R/path.removeprefix('res://');assert hashlib.sha256(file.read_bytes()).hexdigest()==reg['sourceBindings'][file.relative_to(O).as_posix()];checks+=1
  a=np.array(Image.open(file));assert a.shape==(256,256,4);checks+=1
  body=np.array(Image.open(R/reg['bareSourceDirectory']/f'{i:03}.png'))
  assert np.array_equal(a,body) if gear=='bare' else np.array_equal(a[110:],body[110:]);checks+=1
(O/'package-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'scope':'Exact frozen body/shell hashes, full original metadata, whole res paths and protected body; native/world/motion acceptance separate.'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0}))
