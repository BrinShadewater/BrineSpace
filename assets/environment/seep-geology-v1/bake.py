"""Package immutable overhead geology masters without repainting or grading."""
import hashlib
import json
from pathlib import Path
from PIL import Image

PACK = Path(__file__).resolve().parent
IDS = ('seep-stones', 'nodule-cluster', 'mineral-ledges')
SOURCES = {'seep-stones': 'seep-stones-v4.png', 'nodule-cluster': 'nodule-cluster-v1.png', 'mineral-ledges': 'mineral-ledges-v4.png'}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bake():
    ledger = PACK / 'manifest.json'
    if ledger.exists():
        for asset in json.loads(ledger.read_text())['assets']:
            for version in asset['versions']:
                if not version['file'].startswith('runtime/'):
                    assert sha(PACK / version['file']) == version['sha256'], 'Master changed'
    (PACK / 'runtime').mkdir(exist_ok=True)
    for identity in IDS:
        source = Image.open(PACK / SOURCES[identity]).convert('RGBA')
        assert source.getchannel('A').getextrema()[0] == 0, 'Transparent exterior required'
        source = source.crop(source.getchannel('A').getbbox())
        source.resize((512, round(source.height * 512 / source.width)), Image.Resampling.LANCZOS).save(PACK / 'runtime' / (identity + '.png'))
    print('3 runtime rasters packaged; no grading or alpha repaint')

if __name__ == '__main__':
    bake()
