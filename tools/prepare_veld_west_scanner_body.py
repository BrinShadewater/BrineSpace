"""Register authored west scanner bodies against corrected Veld idle anatomy."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/veld-identity-correction-v1'


def main():
    source = BASE / 'sources/scanner-west-body-01.png'
    raw = binary(chroma(source))
    assert raw.size == (2112, 744)
    idle = Image.open(BASE / 'review/directional-movement-01/idle-west-000.png').convert('RGBA')
    scale = 147 / 568
    frames = [idle]
    records = []
    for i in range(4):
        left, right = i * 528, (i + 1) * 528
        tile = raw.crop((left, 0, right, raw.height))
        assert not tile.getchannel('A').crop((0, 0, 1, tile.height)).getbbox()
        assert not tile.getchannel('A').crop((527, 0, 528, tile.height)).getbbox()
        sole = 673
        _, xs = np.where(np.asarray(tile)[sole - 20:sole + 1, :, 3] > 0)
        support = float((xs.min() + xs.max()) / 2)
        dense = binary(tile.resize((round(tile.width * scale), round(tile.height * scale)), Image.Resampling.BOX), True)
        offset = (round(128 - support * scale), round(223 - sole * scale))
        pose = Image.new('RGBA', (256, 256))
        pose.alpha_composite(dense, offset)
        frames.append(pose)
        records.append(dict(sourceCrop=[left, 0, right, raw.height], support=[support, sole], offset=offset))
    frames.append(idle.copy())
    out = BASE / 'review/west-scanner-body-01'
    out.mkdir(exist_ok=True)
    sheet = Image.new('RGB', (1536, 256), '#293b40')
    for i, frame in enumerate(frames):
        frame.save(out / f'interact-west-{i:03}.png')
        sheet.paste(frame, (i * 256, 0), frame)
    sheet.save(out / 'contact.png')
    (out / 'registration.json').write_text(json.dumps(dict(
        status='prepared_source_selection_recorded_in_ledger',
        source=source.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        scale=scale, pivot=[128, 224], records=records,
        limits=['Exact corrected idle endpoints; source body proportions and action progression require paired native review.']
    ), indent=2) + '\n')
    print('Registered four west body interiors and exact corrected idle endpoints.')


if __name__ == '__main__':
    main()
