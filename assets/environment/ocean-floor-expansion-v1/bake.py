"""Reproducible margin trim/isotropic packaging; no painting or color changes."""
import hashlib,json
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
SELECTED={'brine-star':'brine-star-v4.png','tube-worms':'tube-worms.png','seagrass':'seagrass.png','ribbon-seaweed':'ribbon-seaweed-v3.png','mycelium-mat':'mycelium-mat-v3.png','shell-silt':'shell-silt.png','fractured-stone':'fractured-stone.png','mineral-vein':'mineral-vein.png'}
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def bake():
    ledger=PACK/'manifest.json'
    if ledger.exists():
        for a in json.loads(ledger.read_text())['assets']:
            for v in a['versions']:
                if not v['file'].startswith('runtime/'):
                    assert digest(PACK/v['file'])==v['sha256'],'Immutable source changed: '+v['file']
    (PACK/'runtime').mkdir(exist_ok=True)
    for identity,name in SELECTED.items():
        im=Image.open(PACK/name).convert('RGBA')
        if identity not in ('fractured-stone','mineral-vein'):
            assert im.getchannel('A').getextrema()[0]==0
            im=im.crop(im.getchannel('A').getbbox())
        # 512 visible source pixels per prop width; geology retains 1024/4-cell density.
        width=1024 if identity in ('fractured-stone','mineral-vein') else 512
        im.resize((width,round(im.height*width/im.width)),Image.Resampling.LANCZOS).save(PACK/'runtime'/(identity+'.png'))
    print('8 sources packaged; original RGB/alpha retained, margins/isotropic resize only')
if __name__=='__main__': bake()
