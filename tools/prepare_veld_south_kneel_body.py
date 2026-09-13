"""Prepare the female Veld south kneeling transition at one anatomical scale."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/veld-identity-correction-v1'


def main():
    source = BASE / 'sources/kneel-south-body-01.png'
    raw = binary(chroma(source))
    assert raw.size == (2172, 724)
    scale = 145 / 556  # Source standing pose is the common anatomical ruler.
    frames, records = [], []
    for i in range(6):
        tile = raw.crop((i * 362, 0, (i + 1) * 362, 724))
        box = tile.getbbox()
        assert box[0] > 0 and box[2] < 362
        sole = box[3] - 1
        _, xs = np.where(np.asarray(tile)[sole - 10:sole + 1, :, 3] > 0)
        xs = xs[xs > (box[0] + box[2]) / 2]
        support = float((xs.min() + xs.max()) / 2)
        dense = binary(tile.resize((round(362 * scale), round(724 * scale)), Image.Resampling.BOX), True)
        offset = (round(148 - support * scale), round(223 - sole * scale))
        pose = Image.new('RGBA', (256, 256))
        pose.alpha_composite(dense, offset)
        frames.append(pose)
        records.append(dict(sourceCrop=[i * 362, 0, (i + 1) * 362, 724], support=[support, sole], offset=offset))
    frames[0] = Image.open(BASE / 'review/directional-movement-01/idle-south-000.png').convert('RGBA')
    out = BASE / 'review/south-kneel-body-01'
    out.mkdir(exist_ok=True)
    sheet = Image.new('RGB', (1536, 512), '#293b40')
    for row, (action, poses) in enumerate([('kneel', frames), ('stand', list(reversed(frames)))]):
        for i, frame in enumerate(poses):
            frame.save(out / f'{action}-south-{i:03}.png')
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
    print('Prepared south kneel/stand chain with one body ruler.')


if __name__ == '__main__':
    main()
