from pathlib import Path
import json,hashlib
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[2]
source=json.loads((P/'SOURCE_REVIEW.json').read_bytes());assert source['frameCount']==142
assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in source['bindings'].items())
bindings=dict(source['bindings']);inventory_path=R/'character/veld-master-consistency-current-v2/selected-library.json';inventory=json.loads(inventory_path.read_bytes())
shell_path=R/'character/veld-helmet-original-turntable-v1/v3-study/shells/000.png';shell=Image.open(shell_path).convert('RGBA')
def fitted(im):
 im=im.copy();im.paste((0,0,0,0),(115,77,143,103));im.alpha_composite(shell,(112,68));return im
for gear in ['bare','helmet']:
 data=json.loads((P/f'{gear}-source-manifest.json').read_bytes())
 for name,filename in [('reference-north','original-idle-master.png'),('prepared-north','prepared-idle-master.png')]:
  im=Image.open(P/filename).convert('RGBA');im=im if gear=='bare' else fitted(im);dest=P/f'{gear}-{name}.png';im.save(dest)
  data['states'].append(dict(id=name,frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
 entry=inventory['resolved'][gear]['idle-north'];selected=R/entry['frameFiles'][0];assert hashlib.sha256(selected.read_bytes()).hexdigest()==inventory['sourceBindings'][entry['frameFiles'][0]]
 im=Image.open(selected).convert('RGBA');plate=Image.new('RGBA',(256,256));px,py=entry['pivot'];plate.alpha_composite(im,(128-round(px),224-round(py)));dest=P/f'{gear}-selected-idle.png';plate.save(dest)
 data['states'].append(dict(id='idle-north',frameCount=1,frameFiles=['res://'+dest.relative_to(R).as_posix()],frameDurationsMs=[1000],loop=True))
 path=P/f'{gear}-native-manifest.json';path.write_text(json.dumps(data,indent=2)+'\n')
 for state in data['states']:
  for ref in state['frameFiles']:
   p=R/ref[6:];bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 for p in [path,selected,R/entry['manifest']]:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in [inventory_path,P/'prepare_native.py',P/'SOURCE_REVIEW.json',P/'generation.json']:bindings[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(P/'full-source-record.json').write_text(json.dumps(dict(bindings=bindings,scope='Complete North quiet idle source comparison only; finite, no loop or integration acceptance.'),indent=2)+'\n')
print('Quiet North native comparison prepared')
