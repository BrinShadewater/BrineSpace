"""Prepare the female Veld west kneeling transition at one anatomical scale."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/veld-identity-correction-v1'


def main():
    source = BASE / 'sources/kneel-west-body-01.png'
    raw = binary(chroma(source))
    assert raw.size == (2172, 724)
    scale = 147 / 519  # Source standing pose is the common anatomical ruler.
    frames, records = [], []
    occupied = np.asarray(raw)[:, :, 3].any(axis=0)
    edges = np.diff(np.r_[False, occupied, False].astype(int))
    starts, ends = np.where(edges == 1)[0], np.where(edges == -1)[0]
    assert len(starts) == len(ends) == 6
    for i, (start, end) in enumerate(zip(starts, ends)):
        left, right = int(start)-2, int(end)+2
        tile = raw.crop((left, 0, right, 724))
        box = tile.getbbox()
        assert box[0] > 0 and box[2] < tile.width
        sole = box[3] - 1
        _, xs = np.where(np.asarray(tile)[sole - 10:sole + 1, :, 3] > 0)
        occupied_feet = np.unique(xs)
        gaps = np.where(np.diff(occupied_feet) > 1)[0]
        if len(gaps):
            xs = xs[xs <= occupied_feet[gaps[0]]]
        support = float((xs.min() + xs.max()) / 2)
        dense = binary(tile.resize((round(tile.width * scale), round(724 * scale)), Image.Resampling.BOX), True)
        offset = (round(128 - support * scale), round(223 - sole * scale))
        pose = Image.new('RGBA', (256, 256))
        pose.alpha_composite(dense, offset)
        frames.append(pose)
        records.append(dict(sourceCrop=[left, 0, right, 724], support=[support, sole], offset=offset))
    frames[0] = Image.open(BASE / 'review/directional-movement-01/idle-west-000.png').convert('RGBA')
    out = BASE / 'review/west-kneel-body-01'
    out.mkdir(exist_ok=True)
    sheet = Image.new('RGB', (1536, 512), '#293b40')
    for row, (action, poses) in enumerate([('kneel', frames), ('stand', list(reversed(frames)))]):
        for i, frame in enumerate(poses):
            frame.save(out / f'{action}-west-{i:03}.png')
            sheet.paste(frame, (i * 256, row * 256), frame)
    sheet.save(out / 'contact.png')
    (out / 'registration.json').write_text(json.dumps(dict(
        status='prepared_selection_tracked_in_ledger',
        source=source.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        scale=scale, pivot=[128, 224], records=records,
        derived='Stand reverses authored kneel poses; timing must remain original.',
        limits=['Sample action and fitted helmets must connect before selection.',
                'Corrected idle endpoint retained; full native motion and workplace review pending.']
    ), indent=2) + '\n')
    print('Prepared west kneel/stand chain with one body ruler.')


if __name__ == '__main__':
    main()
