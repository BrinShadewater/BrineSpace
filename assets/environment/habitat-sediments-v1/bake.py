"""Package immutable whole habitat fields; no tiling, repainting or grading."""
import hashlib
import json
from pathlib import Path
from PIL import Image

PACK = Path(__file__).resolve().parent
IDS = ('sulfur-ground', 'sponge-ground', 'brine-ground', 'nodules-ground', 'iron-ground')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bake():
    ledger = PACK / 'manifest.json'
    if ledger.exists():
        for a in json.loads(ledger.read_text())['assets']:
            for v in a['versions']:
                if not v['file'].startswith('runtime/'):
                    assert sha(PACK / v['file']) == v['sha256'], 'Immutable source drift'
    (PACK / 'runtime').mkdir(exist_ok=True)
    for identity in IDS:
        im = Image.open(PACK / (identity + '-v2.png')).convert('RGBA')
        assert im.getchannel('A').getextrema() == (255, 255), 'Opaque field required'
        assert im.width == im.height, 'Square material field required'
        im.resize((1024,1024), Image.Resampling.LANCZOS).save(PACK / 'runtime' / (identity + '.png'))
    print('Five 1024-square habitat materials packaged')
if __name__ == '__main__': bake()
