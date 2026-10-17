"""One-time immutable source registration; refuses to overwrite a ledger."""
import json
from PIL import Image
from bake import PACK,SELECTED,digest
ledger=PACK/'manifest.json'
assert not ledger.exists(),'Existing hashes must never be refreshed'
groups={k:[] for k in SELECTED}
groups.update({'mantle-grazer-study':[],'sieve-colony-study':[]})
for path in sorted(PACK.glob('*.png')):
    name=path.stem
    if name.startswith('brittle-stars') or name.startswith('brine-star'): identity='brine-star'
    elif name.startswith('mantle-grazer'): identity='mantle-grazer-study'
    elif name.startswith('sieve-colony'): identity='sieve-colony-study'
    else: identity=next(k for k in SELECTED if name==k or name.startswith(k+'-v'))
    selected=SELECTED.get(identity)==path.name
    reason=None if selected else 'Rejected: exterior haze / shadow, or superseded source; never installed'
    if identity=='mantle-grazer-study' and 'white' in name: reason='Opaque white extraction source; no transparent runtime selection'
    groups[identity].append({'file':path.name,'sha256':digest(path),'native_size':list(Image.open(path).size),'rejection':reason})
assets=[]
for identity,versions in groups.items():
    runtime=identity in SELECTED
    selected='runtime/'+identity+'.png' if runtime else versions[-1]['file']
    if runtime:
        path=PACK/selected
        versions.append({'file':selected,'sha256':digest(path),'native_size':list(Image.open(path).size),'rejection':None})
    assets.append({'id':identity,'kind':('ground' if identity in ['fractured-stone','mineral-vein'] else ('prop' if runtime else 'study')),'selected_source':selected,'runtime_selected':runtime,'stage':'integrated; native review pending; owner acceptance pending' if runtime else 'REJECTED study only; catalogue source selection does not indicate runtime selection','cell_width':{'brine-star':.28,'tube-worms':.4,'seagrass':.3,'ribbon-seaweed':.55,'mycelium-mat':.65,'shell-silt':.25}.get(identity),'versions':versions})
ledger.write_text(json.dumps({'schema_version':1,'title':'Ocean-floor expansion: eight runtime assets; two rejected identities','generator':'built-in image_gen','processing':'alpha-margin trim and isotropic LANCZOS packaging; no RGB/alpha repaint, thresholds or color transfer','assets':assets},indent=2)+'\n')
print('Registered',len(assets),'identities,',sum(len(a['versions']) for a in assets),'rasters, 8 runtime selections')
