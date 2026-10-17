"""Present retained native interruption captures without changing artwork."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parent
report = json.loads((root / 'interruption-probe-evidence.json').read_text())
board = Image.new('RGB', (1100, 6 * 290), '#303b40')
draw = ImageDraw.Draw(board)
for row, case in enumerate(report['results']):
    y = row * 290
    draw.text((8, y + 4), f"{case['mode']} / {case['target']} — source before / after; room before / after", fill='white')
    paths = case['sources'] + [p.removeprefix('res://character/james-east-cargo-heads-v3/') for p in case['captures']]
    for column, path in enumerate(paths):
        im = Image.open(root / path).convert('RGBA')
        im.thumbnail((270, 256), Image.Resampling.NEAREST)
        board.paste(im, (column * 275 + (270 - im.width) // 2, y + 26), im)
board.save(root / 'interruption-before-after-review.png')
print('Six before/after source and room comparisons assembled.')
