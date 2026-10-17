"""Package immutable opaque whole fields; no painting, grading or repeated tiles."""
import hashlib,json
from pathlib import Path
from PIL import Image
PACK=Path(__file__).resolve().parent
IDS=('brine-ripples','coral-shell-sand','iron-clay')
def bake():
    ledger=PACK/'manifest.json'
    if ledger.exists():
        for a in json.loads(ledger.read_text())['assets']:
            for v in a['versions']:
                if not v['file'].startswith('runtime/'):
                    assert hashlib.sha256((PACK/v['file']).read_bytes()).hexdigest()==v['sha256'],'Immutable master drift'
    (PACK/'runtime').mkdir(exist_ok=True)
    for identity in IDS:
        im=Image.open(PACK/(identity+'-v2.png')).convert('RGBA')
        assert im.getchannel('A').getextrema()==(255,255),'Opaque field required'
        # Centre-crop a square if the generator supplied a landscape master.
        edge=min(im.size);x=(im.width-edge)//2;y=(im.height-edge)//2
        im=im.crop((x,y,x+edge,y+edge))
        im.resize((1024,1024),Image.Resampling.LANCZOS).save(PACK/'runtime'/(identity+'.png'))
    print('Three opaque 1024-square biome variants packaged without grading')
if __name__=='__main__':bake()
