"""Register source hashes once after generation."""
import json
from PIL import Image
from bake import IDS, PACK, sha
assert not (PACK/'manifest.json').exists(), 'Never refresh expected hashes'
assets=[]
for identity in IDS:
    files=sorted(PACK.glob(identity+'-v*.png'))+sorted((PACK/'archive').glob(identity+'-v*.png'))+[PACK/'runtime'/(identity+'.png')]
    versions=[{'file':p.relative_to(PACK).as_posix(),'sha256':sha(p),'native_size':list(Image.open(p).size),'rejection':'Oversized ground chips at native full-habitat scale; unselected' if p.name==identity+'-v1.png' else None} for p in files]
    assets.append({'id':identity,'kind':'ground','selected_source':'runtime/'+identity+'.png','stage':'generated; native review pending','versions':versions})
(PACK/'manifest.json').write_text(json.dumps({'schema_version':1,'title':'Five quiet habitat sediment fields','generator':'built-in image_gen','processing':'Isotropic LANCZOS packaging only; no grading or repaint','assets':assets},indent=2)+'\n')
print('Registered five identities /',sum(len(a['versions']) for a in assets),'rasters')
