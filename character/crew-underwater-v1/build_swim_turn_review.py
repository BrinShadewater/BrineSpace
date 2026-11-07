"""Compare current directional bodies at equal stroke fractions and scale."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
inventory = json.loads((ROOT / 'revisions/current-swim-coverage.json').read_text(encoding='utf-8'))
rows = {(row['actor'], row['direction']): row for row in inventory['rows']}
out = ROOT / 'revisions/swim-turn-review'
out.mkdir(exist_ok=True)
records = []
for equipped in [False, True]:
    for phase in range(6):
        sheet = Image.new('RGB', (1040, 1020), '#1d252a')
        draw = ImageDraw.Draw(sheet)
        sources = []
        for row, actor in enumerate(['bill', 'veld', 'branforth']):
            for col, direction in enumerate(['east', 'south', 'west', 'north']):
                item = rows[actor, direction]
                folder = ROOT / item['helmet' if equipped else 'body']
                manifest_path = folder / 'manifest.json'
                manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
                clip = manifest['states'][0]
                cursor = sum(clip['frameDurationsMs']) * (phase + 0.5) / 6
                selected = len(clip['frameFiles']) - 1
                for index, duration in enumerate(clip['frameDurationsMs']):
                    if cursor < duration:
                        selected = index
                        break
                    cursor -= duration
                source = (folder / clip['frameFiles'][selected]).resolve()
                assert hashlib.sha256(source.read_bytes()).hexdigest() == item['sourceSha256'][source.relative_to(ROOT).as_posix()]
                image = Image.open(source).convert('RGBA')
                px, py = manifest['pivot']
                image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)
                x, y = col * 260 + 130 - px * 2, row * 340 + 170 - py * 2
                assert col * 260 <= x and x + image.width <= (col + 1) * 260
                assert row * 340 <= y and y + image.height <= (row + 1) * 340
                sheet.paste(image, (x, y), image)
                draw.text((col * 260 + 10, row * 340 + 10), f'{actor} {direction} / phase {selected + 1}', fill='white')
                sources.append({'path': source.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        name = f'{"helmet" if equipped else "bare"}-phase-{phase + 1}.png'
        sheet.save(out / name)
        records.append({'sheet': name, 'fraction': (phase + 0.5) / 6, 'sources': sources})
(out / 'sources.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
print('12 phase-aligned directional comparisons built from hashed current selections; visual review required.')
