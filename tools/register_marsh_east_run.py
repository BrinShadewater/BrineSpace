"""Correct one airborne whole-pose registration; retain all authored artwork pixels."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-east-run-smooth-v1'
SOURCE = ROOT / 'character/marsh-east-run-material-v1/candidate-03/manifest.json'
CATALOG = ROOT / 'character/marsh-v2/catalog.json'
RELATIVE = '../marsh-east-run-smooth-v1/manifest.json'


def build(install=False):
    original = SOURCE.parent / '002.png'
    image = Image.open(original).convert('RGBA')
    assert image.size == (184, 184)
    assert image.getbbox()[0] > 10 and image.getbbox()[3] < 172, 'Only an airborne, unclipped pose may move'
    revised = Image.new('RGBA', image.size)
    revised.paste(image, (-10, 0))
    assert revised.crop((0, 0, 174, 184)).tobytes() == image.crop((10, 0, 184, 184)).tobytes()
    BASE.mkdir(exist_ok=True)
    revised.save(BASE / 'run-east-002-registered.png')
    manifest = json.loads(SOURCE.read_text())
    manifest['revision'] = 'marsh-east-run-airborne-registration-v1'
    state = manifest['states'][0]
    state['frameFiles'] = [
        'res://character/marsh-east-run-material-v1/candidate-03/000.png',
        'res://character/marsh-east-run-material-v1/candidate-03/001.png',
        'res://character/marsh-east-run-smooth-v1/run-east-002-registered.png',
        'res://character/marsh-east-run-material-v1/candidate-03/003.png',
        'res://character/marsh-east-run-material-v1/candidate-03/004.png',
        'res://character/marsh-east-run-material-v1/candidate-03/005.png',
    ]
    (BASE / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    provenance = dict(source=original.relative_to(ROOT).as_posix(), sourceSha256=hashlib.sha256(original.read_bytes()).hexdigest(),
        operation='Translate the complete airborne pose10pixels left on its unchanged184canvas; no resize, alpha threshold, recolour, anatomical edit or interpolated art.',
        reason='Airborne head centers112.5/103px differ9.5px across half-cycles; first becomes102.5px. Largest adjacent excursion13->6.5px.',
        preserved='All source foreground RGBA pixels, vertical placement, five other holds including all planted poses,6x100ms timing, stride, pivot and controller.',
        rejected={'sources/inbetweens-01.png':'Repeated stance and arm phases; not sufficiently intermediate.', 'sources/full-cycle-02.png':'Does not reliably alternate limbs; no replacement-cycle admission.', 'sources/midpoint3-03.png':'Standalone study unnecessary after identifying the specific airborne registration outlier.'})
    (BASE / 'provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
    if install:
        catalog = json.loads(CATALOG.read_text())
        if RELATIVE not in catalog['body']:
            catalog['body'].append(RELATIVE)
            CATALOG.write_text(json.dumps(catalog, indent=2) + '\n')
    print('East run: one whole airborne pose registered; ' + ('installed' if install else 'staged'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true')
    build(parser.parse_args().install)
