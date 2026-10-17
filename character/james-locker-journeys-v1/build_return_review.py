from pathlib import Path
import json
from PIL import Image, ImageDraw

P = Path(__file__).resolve().parent
evidence = json.loads((P / 'native-locker-return-evidence.json').read_bytes())
manifest = json.loads((P.parent / 'james-helmet-fitting-east-v1/manifest.json').read_bytes())
frames, durations = [], []
for result in evidence['results']:
    if result['rotation'] != 2:
        continue
    action = result['action']
    row = next(row for row in manifest['states'] if row['id'] == action + '-east')
    remaining = result['return']['startedElapsed'] * 1000
    boundaries = [0]
    for duration in row['frameDurationsMs']:
        boundaries.append(boundaries[-1] + duration)
    for slot in result['return']['slots']:
        image = Image.open(P / 'return-captures' / f'q2-{action}-return-{slot:02d}.png').convert('RGB')
        assert image.size == (432, 432)
        canvas = Image.new('RGB', (240, 324), (45, 58, 63))
        canvas.paste(image.crop((156, 90, 276, 240)).resize((240, 300), Image.Resampling.NEAREST), (0, 24))
        ImageDraw.Draw(canvas).text((5, 5), action + ' / interrupted return', fill='white')
        frames.append(canvas)
        durations.append(max(10, round(min(remaining, boundaries[slot + 1]) - boundaries[slot])) + (600 if slot == 0 else 0))
        remaining = boundaries[slot]
palette_source = Image.new('RGB', (240 * len(frames), 324))
for i, frame in enumerate(frames):
    palette_source.paste(frame, (240 * i, 0))
palette = palette_source.quantize(colors=256)
indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
indexed[0].save(P / 'native-return-review.gif', save_all=True, append_images=indexed[1:], duration=durations, loop=0, disposal=2, optimize=False)
palette_source.save(P / 'native-return-contact.png')
print(f'{len(frames)} native reverse poses; sampled clocks with 600ms endpoint review holds')
