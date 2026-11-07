"""Register sample handling to the corrected south kneeling endpoint."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/veld-identity-correction-v1'


def main():
    source = BASE / 'sources/sample-south-body-01.png'
    raw = binary(chroma(source))
    assert raw.size == (2079, 756)
    endpoint = Image.open(BASE / 'review/south-kneel-body-01/kneel-south-005.png').convert('RGBA')
    scale = 110 / 502
    frames, records = [endpoint], []
    for i in range(4):
        left, right = i * raw.width // 4, (i + 1) * raw.width // 4
        tile = raw.crop((left, 0, right, raw.height))
        box = tile.getbbox()
        assert box[0] > 0 and box[2] < tile.width
        sole = box[3] - 1
        _, xs = np.where(np.asarray(tile)[sole - 10:sole + 1, :, 3] > 0)
        xs = xs[xs > (box[0] + box[2]) / 2]
        support = float((xs.min() + xs.max()) / 2)
        dense = binary(tile.resize((round(tile.width * scale), round(tile.height * scale)), Image.Resampling.BOX), True)
        offset = (round(148 - support * scale), round(223 - sole * scale))
        pose = Image.new('RGBA', (256, 256))
        pose.alpha_composite(dense, offset)
        frames.append(pose)
        records.append(dict(sourceCrop=[left, 0, right, raw.height], support=[support, sole], offset=offset))
    frames.append(endpoint.copy())
    out = BASE / 'review/south-kneel-body-01'
    sheet = Image.new('RGB', (1536, 768), '#293b40')
    for row, action in enumerate(['kneel', 'repair', 'stand']):
        for i in range(6):
            if action == 'repair':
                frame = frames[i]
                frame.save(out / f'repair-south-{i:03}.png')
            else:
                frame = Image.open(out / f'{action}-south-{i:03}.png').convert('RGBA')
            sheet.paste(frame, (i * 256, row * 256), frame)
    sheet.save(out / 'body-chain-contact.png')
    (out / 'sample-registration.json').write_text(json.dumps(dict(
        status='prepared_selection_tracked_in_ledger',
        source=source.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        scale=scale, pivot=[128, 224], records=records,
        joins='kneel5=repair0=repair5=stand0',
        limits=['Fitted helmet variants and native continuous chain review pending.']
    ), indent=2) + '\n')
    print('Prepared south sample action joined to corrected kneeling endpoint.')


if __name__ == '__main__':
    main()
