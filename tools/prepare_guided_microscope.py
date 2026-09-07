"""Register guided views on one shared canvas transform; never tight-fit each view."""
import hashlib
import json
from pathlib import Path
from PIL import Image
from room_art_pipeline import clear_exterior

root = Path(__file__).resolve().parents[1] / 'rooms/modular/microscope-guided-01'
manifest = root / 'registration.json'
if manifest.exists():
    raise FileExistsError(manifest)
assets = {}
for q in range(4):
    raw = root / f'microscope-{q}-raw.png'
    output = root / f'microscope-{q}.png'
    if output.exists():
        raise FileExistsError(output)
    with Image.open(raw) as source:
        image = clear_exterior(source)
    image.save(output)
    assets[f'microscope_{q}'] = {
        'file': output.name, 'bounds': [0, 0, image.width, image.height],
        'native_size': list(image.size), 'alpha_bounds': list(image.getbbox()),
        'pivot_normalized': [0.5, 0.7], 'world_size': [60, 60],
        'directions': [q], 'enabled_in_pilot': True,
        'raw_sha256': hashlib.sha256(raw.read_bytes()).hexdigest(),
        'clean_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'processing': 'edge-connected neutral light background removal; native canvas retained; no tight fitting',
        'stage': 'registered candidate for native review; not final production approval'
    }
manifest.write_text(json.dumps({'assets': assets}, indent=2)+'\n', encoding='utf-8')
print(json.dumps(assets, indent=2))
