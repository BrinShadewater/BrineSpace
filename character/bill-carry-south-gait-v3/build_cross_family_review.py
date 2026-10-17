from pathlib import Path
import json
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
R = P.parent.parent
profiles = {
    'east': 'bill-carry-east-gait-v3',
    'south': 'bill-carry-south-gait-v3',
    'west': 'bill-carry-west-gait-v2',
    'north': 'bill-carry-north-gait-v2',
}
for gear in ['bare', 'helmet']:
    board = Image.new('RGB', (768, 1200), '#22343e')
    draw = ImageDraw.Draw(board)
    for row, (direction, bank) in enumerate(profiles.items()):
        manifest = json.loads((R / 'character' / bank / f'{gear}-manifest.json').read_text(encoding='utf-8'))
        frames = manifest['states'][0]['frameFiles']
        master_manifest = R / 'character' / f'bill-cargo-{direction}-master-head-v1' / ('manifest.json' if gear == 'bare' else 'helmet-manifest.json')
        master = json.loads(master_manifest.read_text(encoding='utf-8'))
        held = next(state for state in master['states'] if state['id'] == 'pickup-' + direction)['frameFiles'][-1]
        for col, path in enumerate([held, frames[0], frames[len(frames) // 2]]):
            source = Image.open(R / path.removeprefix('res://')).convert('RGBA')
            board.paste(source, (col * 256, row * 300), source)
            draw.text((col * 256 + 8, row * 300 + 265), direction + ' ' + ['master', 'contact0', 'opposite half'][col], fill='white')
    board.save(P / f'{gear}-cross-family-review.png')
