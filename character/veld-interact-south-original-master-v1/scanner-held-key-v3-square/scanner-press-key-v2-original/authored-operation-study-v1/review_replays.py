from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[4];O=R/'output/veld-south-scanner-authored-keys-v1'
checks=0
for gear in ['bare','helmet']:
 for mode in ['source','native']:
  with Image.open(P/f'{gear}-{mode}-key-study.png') as apng:
   assert apng.n_frames==3
   for i,name in enumerate(['held','press','held']):
    im=Image.open(P/f'{gear}-{name}.png' if mode=='source' else O/f'{gear}-{i:03}-native.png').convert('RGBA')
    apng.seek(i);assert apng.convert('RGBA').tobytes()==im.tobytes();checks+=1
    assert round(apng.info['duration'])==[450,200,450][i];checks+=1
bindings=json.loads((O/'inputs-after.json').read_bytes());assert all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in bindings.items())
print(json.dumps(dict(checks=checks,failures=0,nativeInputsStillStable=len(bindings),scope='Two real keys, three semantic slots, exact source/native APNG holds; not smooth full scanner motion.')))
