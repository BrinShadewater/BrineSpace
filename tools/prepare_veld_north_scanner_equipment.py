"""Fit Veld's authored north-facing helmet poses to the new scanner body."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from rebuild_bill_art import binary, chroma

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/veld-identity-correction-v1'


def main():
    source = BASE / 'sources/scanner-north-helmet-heads-01.png'
    raw = binary(chroma(source))
    assert raw.size == (2043, 770)
    out = BASE / 'review/north-scanner-body-01'
    idle = Image.open(BASE / 'review/directional-movement-01/helmet-idle-north-000.png').convert('RGBA')
    frames, records = [idle], []
    scale = .09
    for i, slot in enumerate([0, 0, 1, 0], 1):
        body = Image.open(out / f'interact-north-{i:03}.png').convert('RGBA')
        tile = raw.crop((slot * raw.width // 2, 0, (slot + 1) * raw.width // 2, raw.height))
        bottom = tile.getbbox()[3] - 1
        _, xs = np.where(np.asarray(tile)[bottom - 8:bottom + 1, :, 3] > 0)
        neck = float((xs.min() + xs.max()) / 2)
        head = binary(tile.resize((round(tile.width * scale), round(tile.height * scale)), Image.Resampling.BOX), True)
        offset = (round(128 - neck * scale), 108 - (head.getbbox()[3] - 1))
        pose = body.copy()
        pose.paste((0, 0, 0, 0), (111, 75, 147, 103))
        pose.paste((0, 0, 0, 0), (114, 103, 143, 107))
        pose.alpha_composite(head, offset)
        assert pose.crop((0, 109, 256, 256)).tobytes() == body.crop((0, 109, 256, 256)).tobytes(), i
        frames.append(pose)
        records.append(dict(slot=i, headSourceSlot=slot, offset=offset))
    frames.append(idle.copy())
    sheet = Image.new('RGB', (1536, 512), '#293b40')
    for i, frame in enumerate(frames):
        frame.save(out / f'helmet-interact-north-{i:03}.png')
        sheet.paste(frame, (i * 256, 256), frame)
        body = Image.open(out / f'interact-north-{i:03}.png')
        sheet.paste(body, (i * 256, 0), body)
    sheet.save(out / 'paired-contact.png')
    (out / 'equipment-registration.json').write_text(json.dumps(dict(
        status='prepared_source_selection_recorded_in_ledger',
        source=source.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        scale=scale, records=records, protectedBelow=109,
        limits=['Exact corrected equipped idle endpoints; body, hands and scanner below collar preserved.']
    ), indent=2) + '\n')
    print('Prepared north scanner fitted helmet variants.')


if __name__ == '__main__':
    main()
