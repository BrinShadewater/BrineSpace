"""Package immutable plant sources with margin trim and isotropic sizing only."""
import hashlib,json
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
IDS=('emerald-reed-kelp','sea-white-reed-kelp','violet-reed-kelp')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bake():
    ledger=PACK/'manifest.json'
    if ledger.exists():
        for a in json.loads(ledger.read_text())['assets']:
            for v in a['versions']:
                if not v['file'].startswith('runtime/'):
                    assert sha(PACK/v['file'])==v['sha256'],'Master drift'
    (PACK/'runtime').mkdir(exist_ok=True)
    for identity in IDS:
        version='v2' if identity=='violet-reed-kelp' else 'v1'
        im=Image.open(PACK/(identity+'-'+version+'.png')).convert('RGBA')
        assert im.getchannel('A').getextrema()[0]==0,'Transparent exterior required'
        im=im.crop(im.getchannel('A').getbbox())
        im.resize((round(1024*im.width/im.height),1024),Image.Resampling.LANCZOS).save(PACK/'runtime'/(identity+'.png'))
    print('Three 1024px-high upright kelp sprites packaged; no grade or alpha repaint')
if __name__=='__main__':bake()
