"""Read-only Veld selection audit and bounded transition review."""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / 'character/dr-veld-v2'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def rel(path):
    return path.resolve().relative_to(ROOT).as_posix()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    catalog = read(BASE / 'catalog.json')
    selected = {'bare': {}, 'helmet': {}}
    manifests = []
    def load(path, variant):
        data = read(path)
        manifests.append({'path': rel(path), 'sha256': digest(path), 'variant': variant})
        for state in data['states']:
            files = [(path.parent / f).resolve() for f in state['frameFiles']]
            selected[variant][state['id']] = {
                'manifest': rel(path), 'files': [rel(f) for f in files],
                'hashes': [digest(f) for f in files],
                'durations': state['frameDurationsMs'], 'loop': state.get('loop', False),
                'pivot': data['pivot'], 'canvas': list(Image.open(files[0]).size),
                'selection': 'retained' if 'dr-veld-v2' in str(path) else 'revised_installed',
            }
    for variant, key in [('bare', 'body'), ('helmet', 'equipment')]:
        for entry in catalog[key]:
            load(BASE / entry, variant)
    loader = (ROOT / 'scripts/grid_canvas.gd').read_text(encoding='utf-8')
    block = loader.split('if actor == "veld":', 1)[1].split('elif actor == "branforth":', 1)[0]
    for line in block.splitlines():
        match = re.search(r'"res://([^"]+manifest.json)"', line)
        if match:
            load(ROOT / match[1], 'helmet' if 'load_equipment_manifest' in line else 'bare')
    report = {
        'scope': 'Catalog plus explicit Veld overrides in _load_replacement_crew_animations; runtime-derived joins are separate, not flattened here.',
        'loader_sha256': digest(ROOT / 'scripts/grid_canvas.gd'),
        'manifests': manifests, 'selected': selected,
        'counts': {v: {s: sum(r['selection'] == s for r in rows.values()) for s in ['retained', 'revised_installed']} for v, rows in selected.items()},
    }
    (HERE / 'inventory.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    actions = ['equip-helmet-east', 'remove-helmet-east', 'pickup-helmet-east', 'putdown-helmet-east']
    panels = []
    for key in actions:
        if key not in selected['bare']:
            continue
        row = selected['bare'][key]
        sequence = [selected['bare']['idle-east'], row, selected['helmet']['idle-east']]
        if key == 'remove-helmet-east':
            sequence = [selected['helmet']['idle-east'], row, selected['bare']['idle-east']]
        images = []
        durations = []
        for index, item in enumerate(sequence):
            files = item['files'] if index == 1 else item['files'][:1]
            for f in files:
                # Ground-register canvases at the original pivot; no pose-height normalization.
                frame = Image.open(ROOT / f).convert('RGBA')
                canvas = Image.new('RGBA', (224, 232))
                canvas.alpha_composite(frame, (round(112-item['pivot'][0]), round(208-item['pivot'][1])))
                images.append(canvas)
            durations.extend(item['durations'] if index == 1 else [650])
        sheet = Image.new('RGB', (224 * len(images), 256), '#202a30')
        draw = ImageDraw.Draw(sheet)
        for index, frame in enumerate(images):
            sheet.paste(frame, (224*index, 24), frame)
            draw.text((224*index+5, 5), 'idle join' if index in [0, len(images)-1] else f'{key} {index-1:02}', fill='white')
        sheet.save(HERE / f'{key}-contact.png')
        gif = []
        for frame in images:
            bg = Image.new('RGB', frame.size, '#202a30')
            bg.paste(frame, (0, 0), frame)
            gif.append(bg)
        gif[0].save(HERE / f'{key}.gif', save_all=True, append_images=gif[1:], duration=durations, loop=0)
        payload = json.dumps({'files': [rel(HERE/f'{key}.gif')], 'frames': row['files'], 'durations': row['durations']})
        panels.append(f'<section><h2>{key} — retained selection</h2><p>Accepted idle bookends; foot pivot registered. Endpoints are context, not proof of action semantics.</p><img src="{key}.gif" height="232"><img src="{key}.gif" height="128"><img src="{key}.gif" height="85"><img src="{key}.gif" height="42"><p><a href="{key}-contact.png">Every frame and joins</a></p><script type="application/json">{payload}</script></section>')
    html = '<!doctype html><meta charset="utf-8"><title>Veld remaining animation audit</title><style>body{background:#202a30;color:#e2e8eb;font:16px sans-serif;margin:32px}section{border-top:1px solid #687580;padding:16px}img{margin:12px;image-rendering:auto}</style><h1>Veld: retained helmet transitions</h1><p>Read-only review. Existing artwork; no runtime binding or generation change. Smaller views approximate 82/54/27px standing heights.</p>' + ''.join(panels)
    (HERE / 'index.html').write_text(html, encoding='utf-8')
    print(json.dumps({'counts': report['counts'], 'transition_reviews': len(panels), 'output': str(HERE)}))

if __name__ == '__main__':
    main()
