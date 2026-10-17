import json
from pathlib import Path

from PIL import Image, ImageDraw

root = Path.cwd()
review = root / 'character/james-west-carry-walk-keys-v1/north-unload-chain-v360'
captures = root / 'output/james-unload-playtest-v360/captures'
data = json.loads((captures / 'review.json').read_text())
assert data['failures'] == 0 and len(data['cases']) == 4
for case in data['cases']:
    rows = [r for r in data['captures'] if r['case'] == case['case']]
    active = [r for r in rows if r.get('source', {}).get('key') == 'unload-north']
    assert active and max(r['source']['index'] for r in active) == 283
    selected = [(f'candidate {slot}', min(active, key=lambda r: abs(r['source']['index'] - slot))) for slot in [0, 70, 141, 210, 277, 283]]
    selected = [('arrival', rows[rows.index(active[0]) - 1])] + selected + [('idle', rows[-1])]
    width, height = Image.open(captures / active[0]['file']).size
    board = Image.new('RGB', (4 * width, 2 * (height + 24)), (48, 59, 64))
    draw = ImageDraw.Draw(board)
    for i, (label, row) in enumerate(selected):
        x, y = i % 4, i // 4
        board.paste(Image.open(captures / row['file']).convert('RGB'), (x * width, y * (height + 24) + 24))
        draw.text((x * width + 4, y * (height + 24) + 5), label, fill='white')
    board.save(review / (case['case'] + '-native.png'))
    unload = [r for r in rows if r['stage'] == 'workshop_unload'] + [rows[-1]]
    images = [Image.open(captures / r['file']).convert('RGB') for r in unload]
    clocks = [max(1, round((unload[i + 1]['time'] - r['time']) * 1000)) if i + 1 < len(unload) else 400 for i, r in enumerate(unload)]
    images[0].save(review / (case['case'] + '-native-motion.png'), save_all=True, append_images=images[1:], duration=clocks, loop=0, disposal=0, blend=0)
(review / 'native-review.json').write_text(json.dumps(data, indent=2) + '\n')
print(json.dumps({'checks': data['checks'], 'failures': 0, 'cases': 4, 'captures': len(data['captures']), 'actualCandidateTerminalSlot': 283}))
