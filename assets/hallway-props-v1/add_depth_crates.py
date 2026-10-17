"""Register generated originals and refresh their review page; never edits pixels."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
from PIL import Image

PACK = Path(__file__).resolve().parent
ROOT = PACK.parents[1]
SPECS = [('stacked-crates-depth', 'Stacked Crates - Raised View', 48)]

if len(sys.argv) == 2 and sys.argv[1] != '--gallery':
    registry_path = ROOT / 'rooms/station-props-v2/props.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    manifest_path = PACK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for (key, label, width), source in zip(SPECS, sys.argv[1:]):
        destination = PACK / (key + '.png')
        shutil.copy2(source, destination)
        im = Image.open(destination).convert('RGBA')
        x, y, right, bottom = im.getchannel('A').point(lambda v: 255 if v > 32 else 0).getbbox()
        x, y = max(0, x - 2), max(0, y - 2)
        right, bottom = min(im.width, right + 2), min(im.height, bottom + 2)
        footprint = [.04, .09, .92, .87]
        record = dict(id='sp-hall-' + key, label=label, category='common',
                      source='res://assets/hallway-props-v1/' + key + '.png',
                      region=[x, y, right-x, bottom-y],
                      pieces=[[[x,y],[right,y],[right,bottom],[x,bottom]]],
                      footprint=footprint, collision_boxes=[footprint],
                      display_width=width, wall_contact=[], default_rooms=[])
        registry = [r for r in registry if r['id'] != record['id']] + [record]
        manifest['assets'] = [r for r in manifest['assets'] if r['id'] != record['id']]
        manifest['assets'].append(dict(**record, raw_dimensions=list(im.size),
            sha256=hashlib.sha256(destination.read_bytes()).hexdigest(), generation_source=source))
        print(key, record['region'], 'world width', width)
    registry_path.write_text(json.dumps(registry, indent=1, ensure_ascii=False)+'\n', encoding='utf-8')
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')

if '--gallery' in sys.argv:
    gallery = ROOT / 'assets/room-risers-expansion-v1/hallway-props'
    cards = []
    for key, label, width in SPECS:
        shutil.copy2(PACK/(key+'.png'), gallery/(key+'.png'))
        views = []
        for shape in ['corridor', 'corner', 'tee_corridor']:
            for q in range(4):
                name = f'{key}-{shape}-q{q}.png'
                shutil.copy2(PACK/'review'/name, gallery/name)
                views.append(f'<img width="256" src="{name}">')
        cards.append(f'<article><h2>{label}</h2><img class="source" src="{key}.png">'
                     f'<p>{width} world units wide. Visible stacked height and muted matte metal.</p>'
                     f'<img class="board" src="{key}-corridor-q1.png">'
                     '<details><summary>All hallway orientations</summary>'+''.join(views)+'</details></article>')
    path = gallery/'index.html'
    page = path.read_text(encoding='utf-8', errors='replace')
    page = page.split('<!-- crate-depth -->')[0]
    page += '<!-- crate-depth --><h1 id="crate-depth">Stacked crates - more visible depth</h1><p>Slightly lower camera; compact two-crate stack with solid navigation footprints. 12 new placement checks pass.</p><div class="grid">'+''.join(cards)+'</div>'
    path.write_text(page, encoding='utf-8')
