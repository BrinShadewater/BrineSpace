"""Register sample handling to the corrected north kneeling endpoint."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/veld-identity-correction-v1'


def main():
    source = BASE / 'sources/sample-north-body-01.png'
    raw = binary(chroma(source))
    assert raw.size == (2172, 724)
    endpoint = Image.open(BASE / 'review/north-kneel-body-01/kneel-north-005.png').convert('RGBA')
    scale = 97 / 503
    frames, records = [endpoint], []
    for i in range(4):
        left, right = i * raw.width // 4, (i + 1) * raw.width // 4
        tile = raw.crop((left, 0, right, raw.height))
        box = tile.getbbox()
        assert box[0] > 0 and box[2] < tile.width
        mid = round((box[0] + box[2]) / 2)
        ys, _ = np.where(np.asarray(tile)[:, :mid, 3] > 0)
        sole = int(ys.max())
        _, xs = np.where(np.asarray(tile)[sole - 10:sole + 1, :, 3] > 0)
        xs = xs[xs < mid]
        occupied_feet = np.unique(xs)
        gaps = np.where(np.diff(occupied_feet) > 1)[0]
        if len(gaps):
            xs = xs[xs <= occupied_feet[gaps[0]]]
        support = float((xs.min() + xs.max()) / 2)
        dense = binary(tile.resize((round(tile.width * scale), round(tile.height * scale)), Image.Resampling.BOX), True)
        offset = (round(112 - support * scale), round(222 - sole * scale))
        pose = Image.new('RGBA', (256, 256))
        pose.alpha_composite(dense, offset)
        frames.append(pose)
        records.append(dict(sourceCrop=[left, 0, right, raw.height], support=[support, sole], offset=offset))
    frames.append(endpoint.copy())
    out = BASE / 'review/north-kneel-body-01'
    sheet = Image.new('RGB', (1536, 768), '#293b40')
    for row, action in enumerate(['kneel', 'repair', 'stand']):
        for i in range(6):
            if action == 'repair':
                frame = frames[i]
                frame.save(out / f'repair-north-{i:03}.png')
            else:
                frame = Image.open(out / f'{action}-north-{i:03}.png').convert('RGBA')
            sheet.paste(frame, (i * 256, row * 256), frame)
    sheet.save(out / 'body-chain-contact.png')
    (out / 'sample-registration.json').write_text(json.dumps(dict(
        status='prepared_selection_tracked_in_ledger',
        source=source.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        scale=scale, pivot=[128, 224], records=records,
        joins='kneel5=repair0=repair5=stand0',
        limits=['Fitted helmet variants and native continuous chain review pending.']
    ), indent=2) + '\n')
    print('Prepared north sample action joined to corrected kneeling endpoint.')


if __name__ == '__main__':
    main()
