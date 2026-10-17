"""Package selected immutable painted masters, without paint or colour grading."""
import hashlib,json
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
SOURCES={'mining':'mining-v1.png','frame':'frame-v2.png','cable':'cable-v1.png'}
def bake():
    ledger=PACK/'manifest.json'
    if ledger.exists():
        for asset in json.loads(ledger.read_text())['assets']:
            for v in asset['versions']:
                if not v['file'].startswith('runtime/'):
                    assert hashlib.sha256((PACK/v['file']).read_bytes()).hexdigest()==v['sha256'],'Immutable source drift: '+v['file']
    (PACK/'runtime').mkdir(exist_ok=True)
    for identity,name in SOURCES.items():
        im=Image.open(PACK/name).convert('RGBA')
        assert im.getchannel('A').getextrema()[0]==0
        im=im.crop(im.getchannel('A').getbbox())
        im.resize((512,round(im.height*512/im.width)),Image.Resampling.LANCZOS).save(PACK/'runtime'/(identity+'.png'))
    print('3 sprites packaged at 512px width; transparent-margin trim and isotropic resampling')
if __name__=='__main__':bake()
