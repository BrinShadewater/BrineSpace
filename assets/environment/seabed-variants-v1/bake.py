"""Rebuild selected sprites from immutable masters; alpha trim and isotropic resize."""
import hashlib,json
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
SOURCES={'rounded-boulders':'rounded-boulders-v1.png','pale-driftwood':'pale-driftwood-v2.png'}
def bake():
    ledger=PACK/'manifest.json'
    if ledger.exists():
        for asset in json.loads(ledger.read_text())['assets']:
            for version in asset['versions']:
                if not version['file'].startswith('runtime/'):
                    assert hashlib.sha256((PACK/version['file']).read_bytes()).hexdigest()==version['sha256'], 'Immutable source drift: '+version['file']
    (PACK/'runtime').mkdir(exist_ok=True)
    for identity,name in SOURCES.items():
        im=Image.open(PACK/name).convert('RGBA')
        assert im.getchannel('A').getextrema()[0]==0
        im=im.crop(im.getchannel('A').getbbox())
        im.resize((512,round(im.height*512/im.width)),Image.Resampling.LANCZOS).save(PACK/'runtime'/(identity+'.png'))
    print('2 selected sprites packaged at 512px width; original RGB/alpha, margin trim only')
if __name__=='__main__':bake()
