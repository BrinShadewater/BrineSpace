"""Review preserved source/native endpoint joins without changing artwork."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
source = bank / 'north-unload-chain-v360'
out = bank / 'north-unload-join-audit-v361'
out.mkdir(exist_ok=True)
spec = json.loads((source / 'playback.json').read_text())['unload']
times = [400, 420, 435, 449, 450, 470, 520]
board = Image.new('RGB', (256 * len(times), 2 * 292), (48, 59, 64))
draw = ImageDraw.Draw(board)
observations = []
for row_index, row in enumerate(spec):
    for column, elapsed in enumerate(times):
        index, clock = 0, min(elapsed, sum(row['clocks']) - .001)
        while index < len(row['clocks']) - 1 and clock >= row['clocks'][index]:
            clock -= row['clocks'][index]
            index += 1
        path = root / row['paths'][index].lstrip('/')
        image = Image.open(path).convert('RGBA')
        x, y = column * 256, row_index * 292
        board.paste(image, (x, y + 30), image)
        draw.text((x + 8, y + 8), f"{row['gear']} {elapsed}ms / {index}", fill='white')
        observations.append({'bank': row['gear'], 'timeMs': elapsed, 'index': index,
                             'source': path.relative_to(root).as_posix()})
board.save(out / 'source-end-join.png')
captures = root / 'output/james-unload-playtest-v360/captures'
native = json.loads((captures / 'review.json').read_text())
joined = []
for case_index, case in enumerate(native['cases']):
    active = [r for r in native['captures'] if r['case'] == case['case']
              and r.get('source', {}).get('key') == 'unload-north']
    first_terminal = next(i for i, r in enumerate(active) if r['source']['index'] == 283)
    rows = active[max(0, first_terminal - 3):first_terminal + 2]
    assert len(rows) == 5
    w, h = Image.open(captures / rows[0]['file']).size
    if case_index == 0:
        native_board = Image.new('RGB', (w * 5, (h + 28) * 4), (48, 59, 64))
        native_draw = ImageDraw.Draw(native_board)
    for col, row in enumerate(rows):
        x, y = col * w, case_index * (h + 28)
        native_board.paste(Image.open(captures / row['file']).convert('RGB'), (x, y + 28))
        native_draw.text((x + 3, y + 5), f"R{case['rotation']} slot{row['source']['index']}", fill='white')
    joined.append({'case': case['case'], 'nativeFrames': rows})
native_board.save(out / 'native-end-join.png')
(out / 'evidence.json').write_text(json.dumps({'version': 361, 'selected': False,
    'sourceSamples': observations, 'nativeJoinSamples': joined,
    'scope': 'Preserved V360 source and actual corrected-linear native captures. No new simulation, generation, body alteration or runtime admission.'}, indent=2) + '\n')
print(json.dumps({'sourceSamples': len(observations), 'nativeJoinSamples': 20,
                  'normalChanged': False, 'generationJobs': 0}))
