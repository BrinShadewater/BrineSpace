from pathlib import Path
import base64
import hashlib
import json
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
checks = []
for item in manifest['views']:
    path = root / 'rotations' / (item['direction'] + '.png')
    im = Image.open(path)
    im.load()
    assert im.mode == 'RGBA' and im.size == (184, 184)
    assert im.getchannel('A').getextrema() == (0, 255)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
    bounds = im.getbbox()
    assert bounds and all([bounds[0] > 0, bounds[1] > 0, bounds[2] < 184, bounds[3] < 184])
    checks.append({'direction': item['direction'], 'rgba_canvas': True, 'real_transparency': True,
                   'hash_matches': True, 'unclipped_bounds': True})
def data_image(path):
    return 'data:image/png;base64,' + base64.b64encode(path.read_bytes()).decode('ascii')
cards = ''.join('<figure><img src="' + data_image(root / 'rotations' / (n + '.png')) + '" alt="Kris ' + n + '"><figcaption>' + n.title() + '</figcaption></figure>' for n in ['south','east','north','west'])
html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Kris Krüg — Standing references</title>
<style>body{margin:0;background:#202529;color:#e0e5e8;font:18px system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:24px}h1{font-size:32px;margin-bottom:6px}p{line-height:1.5;color:#bac8ce}.views{display:grid;grid-template-columns:repeat(auto-fit,minmax(184px,1fr));gap:16px}figure{margin:0;background:#30373c;border-radius:8px;text-align:center;padding:8px}figure img{width:100%;max-width:368px;image-rendering:pixelated}figcaption{padding:6px}img.board{width:100%;height:auto}a{color:#b4d6da}</style>
<main><h1>Kris Krüg</h1><p>Cognitive Concordance Specialist<br>AI &amp; Robotics · Intent Harmonisation</p>
<p>Four transparent standing candidates. Hat-free tied hair, wrap suit, diagonal recorder harness and consistent flat data-wafer pouch.</p>
<div class="views">''' + cards + '''</div><p>Static references: 184 × 184 canvas, foot pivot (92,172), common front-derived standing scale. No motion or in-game installation.</p>
<img class="board" src="''' + data_image(root / 'review.png') + '''" alt="Native-size and enlarged references with crew comparison and labelled static room composite">
<p>The room inset is a historical screenshot with a static character composite. Visual selection and animation remain separate.</p></main></html>'''
(root / 'index.html').write_text(html, encoding='utf-8')
(root / 'validation.json').write_text(json.dumps({'standing_candidates': checks, 'failures': 0,
    'visual_review': 'Agent reviewed raw atlas and review.png; likeness, wrap silhouette, wafer pouch, matte material and standing stature remain readable. South remains slightly three-quarter; cardinal camera refinement may be needed for motion.',
    'native_runtime': 'not run: static-source scope', 'owner_acceptance': 'pending'}, indent=2), encoding='utf-8')
with ZipFile(root / 'Kris-Krug-standing-preview.zip', 'w', ZIP_DEFLATED) as bundle:
    for name in ['index.html', 'review.png', 'manifest.json', 'README.md']:
        bundle.write(root / name, name)
    for item in manifest['views']:
        name = 'rotations/' + item['direction'] + '.png'
        bundle.write(root / name, name)
print('Four RGBA candidates validated; standalone review and 8-file preview ZIP saved.')
