"""Remove authorized exterior white only; preserve native canvas and record bounds.

No geometry repair, painting, or per-direction pixel rescaling is performed.
The pilot uses explicit ground-anchored contain-fit registration, not room crops.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from room_art_pipeline import clear_exterior


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    items = {}
    for name in ['jamb', 'rack-south', 'rack-west', 'rack-north', 'rack-east']:
        source = args.directory / (name + '-raw.png')
        destination = args.directory / (name + '.png')
        if destination.exists():
            raise FileExistsError(destination)
        with Image.open(source) as raw:
            result = clear_exterior(raw)
            bounds = result.getchannel('A').getbbox()
            if bounds is None:
                raise ValueError(f'Empty asset: {name}')
            result.save(destination)
            items[name] = {
                'file': destination.name, 'raw_file': source.name,
                'native_size': list(result.size), 'bounds': list(bounds),
                'raw_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'clean_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
                'processing': 'edge-connected neutral-light removal only; canvas preserved',
                'registration': 'contain-fit visible bounds into fixed visual box; bottom-center ground anchor',
                'alpha_corner': result.getpixel((0, 0))[3],
                'enabled_in_pilot': name in ['jamb', 'rack-south'],
                'review': 'Base art registration trial' if name in ['jamb', 'rack-south'] else 'Quarantined: directional transformation not reliable; not approved for rotation',
            }
    manifest = args.directory / 'registration.json'
    if manifest.exists():
        raise FileExistsError(manifest)
    manifest.write_text(json.dumps({'assets': items}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(items, indent=2))


if __name__ == '__main__':
    main()
