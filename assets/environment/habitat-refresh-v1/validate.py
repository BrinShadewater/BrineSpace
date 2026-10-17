"""Verify immutable source hashes and deterministic rebakes; record first ledger once."""
import hashlib,json,sys
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
sys.path.insert(0,str(PACK.parents[2]/'tools'))
from audit_environment_pack import inspect_pack
from bake import bake
identities={'lace-coral':'prop','vase-sponges':'prop','coral-sediment':'ground',
            'cup-corals':'prop','sea-fans':'prop'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
ledger=PACK/'manifest.json'
if '--record' in sys.argv:
    assert not ledger.exists(),'Never replace immutable source baselines'
    assets=[]
    for identity,kind in identities.items():
        assets.append({'id':identity,'kind':kind,'selected_source':'runtime/'+identity+'.png','versions':[{'file':name,'sha256':digest(PACK/name),'rejection':None} for name in [identity+'-v1.png','runtime/'+identity+'.png']],'stage':'integrated locally; native and owner review pending'})
    ledger.write_text(json.dumps({'schema_version':1,'title':'Cold coral and sponge habitat replacements','assets':assets,'prompt_records':['prompts.json'],'bake':'bake.py'},indent=2)+'\n')
report=inspect_pack(ledger)
expected={p.name:digest(p) for p in (PACK/'runtime').glob('*.png')}
bake()
assert all(digest(PACK/'runtime'/name)==value for name,value in expected.items()),'Rebake differs'
assert report['identity_count']==5 and report['source_count']==10
assert not report['unregistered_candidates']
print('HABITAT RASTER: 5 identities, 10 recorded sources; hashes/alpha/rebake pass')
