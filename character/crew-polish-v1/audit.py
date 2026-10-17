"""Read the selected crew catalogs; freeze a reproducible pre-polish inventory."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
CAST = {'bill': 'major-bill-v3', 'veld': 'dr-veld-v2',
        'branforth': 'chief-engineer-branforth-v2', 'marsh': 'marsh-v2'}
KEYS = ['idle-south', 'walk-south', 'walk-east', 'kneel-west', 'repair-west', 'swim-east']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    report = {}
    board = Image.new('RGBA', (1320, 920), '#242b2e')
    draw = ImageDraw.Draw(board)
    for row, (who, folder) in enumerate(CAST.items()):
        root = REPO / 'character' / folder
        catalog = root / 'catalog.json'
        cat = json.loads(catalog.read_text())
        selected = {}
        for relative in cat['body']:
            manifest = root / relative
            data = json.loads(manifest.read_text())
            for state in data['states']:
                selected[state['id']] = (manifest, data, state)
        records = {}
        for key, (manifest, data, state) in selected.items():
            paths = [(manifest.parent / p).resolve() for p in state['frameFiles']]
            records[key] = dict(manifest=manifest.relative_to(REPO).as_posix(),
                pivot=data.get('pivot'), standingHeight=data.get('standingHeight', 74),
                durations=state['frameDurationsMs'], loop=state['loop'],
                frames=[dict(path=p.relative_to(REPO).as_posix(), sha256=sha(p)) for p in paths])
        report[who] = dict(catalog=catalog.relative_to(REPO).as_posix(),
                           sha256=sha(catalog), bodyStates=records)
        for col, key in enumerate(KEYS):
            if key not in selected:
                continue
            manifest, data, state = selected[key]
            im = Image.open((manifest.parent / state['frameFiles'][0]).resolve()).convert('RGBA')
            scale = 148 / data.get('standingHeight', 74)
            if scale != 1:
                im = im.resize((round(im.width*scale), round(im.height*scale)), Image.Resampling.LANCZOS)
            px, py = data.get('pivot', [46, 86])
            board.alpha_composite(im, (round(col*220+110-px*scale), round(row*230+212-py*scale)))
            draw.text((col*220+8, row*230+8), who+' / '+key, fill='white')
    target = ROOT / 'review/baseline.json'
    if target.exists():
        assert json.loads(target.read_text()) == report, 'Frozen baseline changed; do not overwrite it.'
    else:
        target.write_text(json.dumps(report, indent=2)+'\n')
    board.save(ROOT / 'review/current-actions.png')
    print(json.dumps({k: {'bodyStates':len(v['bodyStates']),
        'frameReferences':sum(len(s['frames']) for s in v['bodyStates'].values())} for k,v in report.items()}))

if __name__ == '__main__':
    main()
