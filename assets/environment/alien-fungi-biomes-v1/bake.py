"""Immutable generation sources -> alpha-margin trim/isotropic runtime rasters."""
import hashlib,json
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
SOURCES={'fungal-shelves':'fungal-shelves-v2.png','spore-rosettes':'spore-rosettes-v1.png','alien-sieve-pod':'alien-sieve-pod-v1.png','kelp-sediment':'kelp-sediment-v1.png','fungal-sediment':'fungal-sediment-v1.png'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bake():
    ledger=PACK/'manifest.json'
    if ledger.exists():
        for asset in json.loads(ledger.read_text())['assets']:
            for v in asset['versions']:
                if not v['file'].startswith('runtime/'):
                    assert sha(PACK/v['file'])==v['sha256'],'Immutable source drift: '+v['file']
    (PACK/'runtime').mkdir(exist_ok=True)
    for id,name in SOURCES.items():
        im=Image.open(PACK/name).convert('RGBA')
        ground=id.endswith('sediment')
        if not ground:
            assert im.getchannel('A').getextrema()[0]==0
            im=im.crop(im.getchannel('A').getbbox())
        width=1024 if ground else 512
        im.resize((width,round(width*im.height/im.width)),Image.Resampling.LANCZOS).save(PACK/'runtime'/(id+'.png'))
    print(len(SOURCES),'runtime rasters; no RGB grade or alpha repaint')
if __name__=='__main__':bake()
