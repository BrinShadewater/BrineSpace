"""Review current normal gait joins at native density and recorded pivots."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/marsh-movement-joins-v1'
INV = ROOT / 'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
inventory = json.loads(INV.read_text())
inputs = {INV.relative_to(ROOT).as_posix(): sha(INV)}
for entry in [inventory['catalog'], *inventory['orderedBodyManifests']]:
    assert sha(ROOT / entry['path']) == entry['sha256'], entry['path']
    inputs[entry['path']] = entry['sha256']
OUT.mkdir(exist_ok=True)
records = []
boards = []
pages = []
for direction in ['east', 'west', 'north', 'south']:
    keys = [f'idle-{direction}', f'walk-start-{direction}', f'walk-{direction}',
            f'walk-step-{direction}', f'run-{direction}']
    stops = [k for k in inventory['states'] if k.startswith('walk-stop') and k.endswith('-' + direction)]
    keys += stops
    board = Image.new('RGB', (8 * 184, (len(keys) + 1) * 214), '#293b40')
    draw = ImageDraw.Draw(board)
    master_path = ROOT / f'character/marsh-motion-polish-v1/sources/{direction}-standing-identity-01.png'
    master = Image.open(master_path).convert('RGBA')
    # Fixed historical master display ruler. Never derive scaling from pose bounds.
    factor = 147 / 1232
    master = master.resize((round(master.width * factor), round(master.height * factor)), Image.Resampling.LANCZOS)
    board.paste(master, (31, 25 + round(172 - 1393 * factor)), master)
    inputs[master_path.relative_to(ROOT).as_posix()] = sha(master_path)
    draw.text((4, 4), direction + ' original master', fill='white')
    draw.text((188, 8), 'Native sprite pixels; foot pivots aligned. No occupied-pose fitting.', fill='white')
    for row, key in enumerate(keys, 1):
        state = inventory['states'][key]
        assert state['standingHeight'] == 148
        for slot, entry in enumerate(state['frames']):
            assert slot < 8
            p = ROOT / entry['path']
            assert sha(p) == entry['sha256'], entry['path']
            inputs[entry['path']] = entry['sha256']
            im = Image.open(p).convert('RGBA')
            alpha = np.asarray(im)[:, :, 3]
            bounds = Image.fromarray((alpha >= 128).astype('uint8') * 255).getbbox()
            px, py = state['pivot']
            dx, dy = round(92 - px), round(172 - py)
            visible = im.getbbox()
            assert visible and visible[0] + dx >= 0 and visible[1] + dy >= 0
            assert visible[2] + dx <= 184 and visible[3] + dy <= 184, (key, slot, visible)
            board.paste(im, (slot * 184 + dx, row * 214 + 25 + dy), im)
            draw.text((slot * 184 + 3, row * 214 + 3), f'{key} / {slot}', fill='white')
            records.append({'state': key, 'slot': slot, 'path': entry['path'], 'sha256': entry['sha256'],
                'canvas': list(im.size), 'pivot': state['pivot'], 'displayTranslation': [dx, dy],
                'opaqueBounds': bounds, 'height': bounds[3] - bounds[1],
                'width': bounds[2] - bounds[0], 'crownFromPivot': bounds[1] - py,
                'soleFromPivot': bounds[3] - 1 - py,
                'holdMs': state['state']['frameDurationsMs'][slot]})
    output = OUT / f'{direction}-joins.png'
    board.save(output)
    boards.append({'path': output.relative_to(ROOT).as_posix(), 'sha256': sha(output), 'reviewed': False})
    if direction in ['north', 'south']:
        for number, (top, bottom) in enumerate([(0, 856), (856, 1712), (1712, 2568)]):
            page = OUT / f'{direction}-page-{number}.png'
            board.crop((0, top, 1472, bottom)).save(page)
            pages.append({'path': page.relative_to(ROOT).as_posix(), 'sha256': sha(page),
                          'rows': [top // 214, bottom // 214], 'reviewed': False})
report = {'scope': 'Complete current dry idle/start/walk/short-step/run and every authored stop bank in four directions; held source review, not motion/native acceptance.',
    'masterDisplayScale': 147 / 1232, 'normalArtChanged': False, 'inputs': inputs,
    'states': len(set(r['state'] for r in records)), 'slots': len(records), 'records': records, 'boards': boards,
    'nativeDensityPages': pages}
(OUT / 'review.json').write_text(json.dumps(report, indent=2) + '\n')
print(f"{report['states']} states / {report['slots']} slots; four complete pivot-aligned boards; {len(inputs)} frozen inputs")
