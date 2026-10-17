"""Rebuild the accepted idle tone override without modifying its source."""
import json
from pathlib import Path
from PIL import Image
from build import helmet_tone
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=ROOT/'character/veld-shared-helmet-v1'
m=json.loads((source/'manifest.json').read_text())
state=dict(next(s for s in m['states'] if s['id']=='idle-east'))
files=[]
for i,f in enumerate(state['frameFiles']):
    im=Image.open(source/f).convert('RGBA')
    head,_=helmet_tone(im.crop((82,17,116,55)))
    im.paste(head,(82,17))
    name=f'frames/equipped-idle-east/{i:03}.png'
    (HERE/name).parent.mkdir(parents=True,exist_ok=True)
    im.save(HERE/name);files.append(name)
state['frameFiles']=files
out={k:v for k,v in m.items() if k!='states'}
out.update(name='Veld approved fitting matching equipped east idle',status='owner_accepted_installed',states=[state])
(HERE/'equipped-idle-manifest.json').write_text(json.dumps(out,indent=2)+'\n')
