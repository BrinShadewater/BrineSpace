"""Package painted mineral habitat masters without repainting or grading."""
import hashlib,json
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
SOURCES={'anhydrite':'anhydrite-v1.png','bacterial-mat':'bacterial-mat-v1.png','salt-plates':'salt-plates-v1.png'}
def bake():
    ledger=PACK/'manifest.json'
    if ledger.exists():
        for asset in json.loads(ledger.read_text())['assets']:
            for v in asset['versions']:
                if not v['file'].startswith('runtime/'):
                    assert hashlib.sha256((PACK/v['file']).read_bytes()).hexdigest()==v['sha256'],'Immutable source drift: '+v['file']
    (PACK/'runtime').mkdir(exist_ok=True)
    for identity,name in SOURCES.items():
        im=Image.open(PACK/name).convert('RGBA');alpha=im.getchannel('A')
        assert alpha.getextrema()[0]==0
        bounds=alpha.point(lambda a:255 if a>=16 else 0).getbbox()
        im=im.crop((max(0,bounds[0]-2),max(0,bounds[1]-2),min(im.width,bounds[2]+2),min(im.height,bounds[3]+2)))
        im.resize((512,round(im.height*512/im.width)),Image.Resampling.LANCZOS).save(PACK/'runtime'/(identity+'.png'))
    print('3 mineral habitat props packaged at 512px; significant-alpha bounds + 2px margin, preserved colour/alpha')
if __name__=='__main__':bake()
