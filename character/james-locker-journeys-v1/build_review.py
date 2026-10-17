from pathlib import Path
import json
from PIL import Image, ImageDraw
P = Path(__file__).resolve().parent
manifest = json.loads((P.parent / 'james-helmet-fitting-east-v1/manifest.json').read_bytes())
def crop(path):
    im = Image.open(path).convert('RGB')
    assert im.size == (432, 432), (path, im.size)
    return im.crop((156, 90, 276, 240)).resize((240, 300), Image.Resampling.NEAREST)
files = [(0, 'equip-helmet', 0), (0, 'equip-helmet', 6), (0, 'equip-helmet', 11),
         (0, 'remove-helmet', 0), (0, 'remove-helmet', 6), (0, 'remove-helmet', 11),
         (1, 'equip-helmet', 6), (2, 'equip-helmet', 6), (3, 'equip-helmet', 6)]
board = Image.new('RGB', (720, 972), (45, 58, 63))
draw = ImageDraw.Draw(board)
for i, (q, action, slot) in enumerate(files):
    label = f'q{q}-{action}-{slot:02d}'
    board.paste(crop(P / 'captures' / (label + '.png')), ((i % 3) * 240, (i // 3) * 324 + 24))
    draw.text(((i % 3) * 240 + 4, (i // 3) * 324 + 5), label, fill='white')
board.save(P / 'native-contact.png')
frames, durations = [], []
for row in manifest['states']:
    action = row['id'].removesuffix('-east')
    for slot, duration in enumerate(row['frameDurationsMs']):
        canvas = Image.new('RGB', (240, 324), (45, 58, 63))
        canvas.paste(crop(P / 'captures' / f'q0-{action}-{slot:02d}.png'), (0, 24))
        ImageDraw.Draw(canvas).text((5, 5), action + ' / actual locker', fill='white')
        frames.append(canvas)
        durations.append(int(duration) + (600 if slot in [0, 11] else 0))
palette = board.quantize(colors=256)
indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
indexed[0].save(P / 'native-review.gif', save_all=True, append_images=indexed[1:],
                duration=durations, loop=0, disposal=2, optimize=False)
print('Nine native comparisons; 24-slot fitting/removal review with endpoint holds')
