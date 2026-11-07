"""Prepare and register the generated Construction matte wall candidate."""
import json
import shutil
from pathlib import Path
from PIL import Image
from build_clone_overhead_directions import remove_exterior_neutral, sha

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'assets/rooms/construction-drone-bay/material'
RAW = Path('C:/Users/Alex/.codex/generated_images/01a097fe-5111-7cf1-96a5-7e19609bde1e/exec-7de8de89-8538-419e-931e-8711c4a461fb.png')
REG = ROOT / 'rooms/full-wall-v1/registrations'

def main():
    PACK.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(RAW, PACK / 'construction-south-refined-raw.png')
    clean, removed = remove_exterior_neutral(Image.open(RAW))
    south = clean.crop(clean.getchannel('A').getbbox())
    directions = {'south': south, 'north': south.transpose(Image.Transpose.ROTATE_180),
                  'east': south.transpose(Image.Transpose.ROTATE_90),
                  'west': south.transpose(Image.Transpose.ROTATE_270)}
    outputs = {}
    for direction, image in directions.items():
        path = PACK / f'{direction}-overhead.png'
        image.save(path)
        name = 'construction-fabrication-wall.json' if direction == 'north' else f'side-construction-fabrication-wall-{direction}.json'
        backup = PACK / (name + '.before')
        if not backup.exists():
            shutil.copyfile(REG / name, backup)
        w, h = image.size
        data = {'source': 'res://' + path.relative_to(ROOT).as_posix(), 'sha256': sha(path),
                'method': 'Generated matte south repaint; exterior-neutral cleanup; exact quarter turns',
                'region': [0, 0, w, h], 'pieces': [[[0, 0], [w, 0], [w, h], [0, h]]],
                'direction': direction,
                'wall_contact': {'side': direction, 'purpose': 'Fixed chassis wall-side; tool grips and catches inward'}}
        (REG / name).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        outputs[direction] = {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path), 'size': [w, h]}
    (PACK / 'build.json').write_text(json.dumps({'status': 'candidate pending native review',
        'source': 'assets/construction-directional-v1/construction-south.png',
        'raw_sha256': sha(RAW), 'exterior_pixels_removed': removed,
        'directions': outputs, 'remaining': ['roller and spool sheen', 'independent floor equipment material repair']}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'removed': removed, 'size': list(south.size), 'directions': 4}))

if __name__ == '__main__':
    main()
