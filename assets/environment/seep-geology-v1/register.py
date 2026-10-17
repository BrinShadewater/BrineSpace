"""Create immutable source ledger once, after selecting reviewed masters."""
import json
from PIL import Image
from bake import PACK, IDS, SOURCES, sha

assert not (PACK / 'manifest.json').exists(), 'Do not overwrite expected hashes'
assets = []
for identity in IDS:
    files = sorted(PACK.glob(identity + '-v*.png')) + [PACK / 'runtime' / (identity + '.png')]
    versions = []
    for path in files:
        relative = path.relative_to(PACK).as_posix()
        rejected = not relative.startswith('runtime/') and relative != SOURCES[identity]
        versions.append({'file': relative, 'sha256': sha(path), 'native_size': list(Image.open(path).size), 'rejection': 'Diffuse exterior haze; unselected' if rejected else None})
    assets.append({'id': identity, 'kind': 'prop', 'selected_source': 'runtime/' + identity + '.png', 'stage': 'source selection pending native review', 'versions': versions})
(PACK / 'manifest.json').write_text(json.dumps({'schema_version': 1, 'title': 'Brine, nodule and iron seep geology', 'generator': 'built-in image_gen', 'processing': 'Alpha margin trim and isotropic LANCZOS only', 'assets': assets}, indent=2) + '\n')
print('Registered', len(assets), 'identities /', sum(len(a['versions']) for a in assets), 'rasters')
