"""Non-destructive source inventory and same-scale comparison, not art cleanup."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'rooms/underwater/batch-two'

def main():
    brief = json.loads((BATCH / 'production-briefs.json').read_text())
    sheet = Image.new('RGB', (1500, 660), '#141d24')
    draw = ImageDraw.Draw(sheet)
    records = []
    for index, room in enumerate(brief['rooms']):
        source = BATCH / (room['id'] + '-source-v1.png')
        with Image.open(source) as raw:
            raw.load()
            records.append({'id': room['id'], 'source': source.relative_to(ROOT).as_posix(),
                'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                'native_size': list(raw.size), 'mode': raw.mode,
                'alpha_extrema': list(raw.getchannel('A').getextrema()) if 'A' in raw.getbands() else None})
            # Equal scale comparison only. Source images are never modified.
            tile = raw.convert('RGB').resize((288, 288), Image.Resampling.NEAREST)
            x, y = (index % 5)*300 + 6, (index // 5)*330 + 25
            sheet.paste(tile, (x, y))
            draw.text((x, y-18), room['name'], fill='#e4e9eb')
    target = ROOT / 'output/batch-two-source-review-v1.png'
    target.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(target)
    print(json.dumps(records))

if __name__ == '__main__':
    main()
