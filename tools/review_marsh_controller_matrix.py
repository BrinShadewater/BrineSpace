"""Compare a generated directional matrix to independent identity references."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw
from rebuild_bill_art import binary, chroma

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/crew-action-detail-v2'

def main():
    source = BASE / 'sources/marsh-role-controller-matrix-01.png'
    raw = binary(chroma(source))
    out = BASE / 'review/marsh-controller-matrix-01'
    out.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (920, 624), '#293b40')
    records = []
    for row, direction in enumerate(['north', 'south', 'west']):
        reference = Image.open(BASE / f'sources/marsh-role-interact-{direction}-reference-01.png').convert('RGBA')
        sheet.paste(reference, (0, row * 208 + 24), reference)
        tiles = [raw.crop((col * raw.width // 4, row * raw.height // 3,
                          (col + 1) * raw.width // 4, (row + 1) * raw.height // 3)) for col in range(4)]
        # One standing ruler per direction avoids stretching each animated pose.
        height = max(t.getbbox()[3] - t.getbbox()[1] for t in tiles)
        scale = 148 / height
        for col, tile in enumerate(tiles):
            box = tile.getbbox()
            _, x = np.where(np.asarray(tile)[box[3]-6:box[3], :, 3] > 0)
            support = float((x.min() + x.max()) / 2) if direction != 'west' else float(np.median(x))
            dense = binary(tile.resize((round(tile.width * scale), round(tile.height * scale)), Image.Resampling.BOX), True)
            pose = Image.new('RGBA', (184, 184))
            pose.alpha_composite(dense, (round(92 - support * scale), round(172 - (box[3]-1) * scale)))
            pose.save(out / f'{direction}-{col:03}.png')
            sheet.paste(pose, ((col+1)*184, row*208+24), pose)
            records.append(dict(direction=direction, frame=col, bounds=box, scale=scale, support=[support, box[3]-1]))
        ImageDraw.Draw(sheet).text((4, row*208+4), direction + ': original idle | four generated interiors', fill='white')
    sheet.save(out / 'comparison.png')
    report = dict(status='rejected_not_selected', source=source.relative_to(ROOT).as_posix(),
                  sha256=hashlib.sha256(source.read_bytes()).hexdigest(), sourceSize=raw.size,
                  reason='Enlarged head and simplified suit shading relative to independent identity references; correct grid and directions do not establish identity continuity.',
                  frames=records, next='Author one direction at a time with original idle and accepted representative pose references.')
    (out / 'review.json').write_text(json.dumps(report, indent=2)+'\n')
    print('Saved twelve registered review frames, comparison and rejection record; no runtime changes.')

if __name__ == '__main__':
    main()
