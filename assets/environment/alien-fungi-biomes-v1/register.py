"""Register original generation hashes exactly once; never refresh expected bytes."""
import json
from PIL import Image
from bake import PACK,SOURCES,sha
assert not (PACK/'manifest.json').exists()
assets=[]
for identity,source in SOURCES.items():
    files=[p for p in PACK.glob(identity+'-v*.png')]+[PACK/'runtime'/(identity+'.png')]
    selected='runtime/'+identity+'.png'
    versions=[{'file':p.relative_to(PACK).as_posix(),'sha256':sha(p),'native_size':list(Image.open(p).size),'rejection':'Exterior cloud; superseded by clean v2' if p.name=='fungal-shelves-v1.png' else None} for p in files]
    assets.append({'id':identity,'kind':'ground' if identity.endswith('sediment') else 'prop','selected_source':selected,'stage':'integrated; native review pending; owner acceptance separate','versions':versions})
(PACK/'manifest.json').write_text(json.dumps({'schema_version':1,'title':'Alien fungi, sieve organism and biome sediments','generator':'built-in image_gen','processing':'Transparent margin trim and isotropic LANCZOS packaging only','assets':assets},indent=2)+'\n')
print('Registered 5 identities /',sum(len(a['versions']) for a in assets),'rasters')
