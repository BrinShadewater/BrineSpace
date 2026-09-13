"""Deterministic extraction of edited held/donning helmet source sheets.

Source edits are separate from frozen legacy reconstruction contracts. Extraction
keeps each original sheet's body scale; helmet-raised bounds never set scale.
"""
from functools import lru_cache
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
import rebuild_bill_art as shared

ROOT = shared.ROOT
REVISION = ROOT / 'character/crew-helmet-fit-v2'


@lru_cache(maxsize=None)
def sequence(actor, kind):
    source = REVISION / 'sources' / f'{actor}-{kind}-candidate-01.png'
    raw = shared.chroma(source)
    boxes = shared.SourceRebaker.column_boxes(raw)
    if kind == 'pickup':
        original = shared.read(shared.WATER / 'revisions' / f'{actor}-pickup-helmet-east-v1/registration.json')
        scale = original['scale'] * 2
    else:
        original = shared.read(shared.WATER / 'pilot' / f'{actor}-equip-helmet-east/sources.json')
        scale = original[0]['scale'] * 2
    frames, poses = [], []
    for box in boxes:
        crop = raw.crop(box)
        alpha = np.array(crop.getchannel('A'))
        # Feet occupy the lowest source rows; exclude isolated antialias pixels.
        ys, xs = np.where(alpha[-max(4, round(6 / scale)):] > 128)
        foot_x = (int(xs.min()) + int(xs.max()) + 1) / 2
        size = (round(crop.width * scale), round(crop.height * scale))
        dense = shared.binary(crop.resize(size, Image.Resampling.BOX), True)
        at = (round(92 - foot_x * scale), 196 - size[1])
        frame = Image.new('RGBA', (184, 208))
        frame.alpha_composite(dense, at)
        frames.append(frame)
        poses.append({'sourceBounds': box, 'scale': scale, 'footSourceX': box[0] + foot_x, 'placement': at})
    shared.OPS[source.relative_to(ROOT).as_posix()] = {
        'method': 'Edited fitted helmet source; original body scale; sole registration',
        'filter': 'BOX', 'density': 2, 'poses': poses}
    return frames


def replacement(actor, path):
    """Resolve original locker paths to edited poses, including reversed aliases."""
    path = Path(path)
    folder = path.parent.name
    index = int(path.stem.rsplit('_', 1)[1])
    if folder == f'{actor}-pickup-helmet-east-v1':
        return (sequence(actor, 'pickup')[index] if index < 5 else sequence(actor, 'donning')[0]).copy()
    if folder == f'{actor}-deposit-helmet-east-v1':
        return replacement(actor, shared.WATER / 'revisions' / f'{actor}-pickup-helmet-east-v1' / f'frame_{5-index:03}.png')
    if folder == f'{actor}-equip-helmet-east':
        return sequence(actor, 'donning')[index].copy()
    if folder == f'{actor}-remove-helmet-east':
        return sequence(actor, 'donning')[5-index].copy()
    return None


def review(actor):
    import json
    out = REVISION / 'review' / actor
    out.mkdir(parents=True, exist_ok=True)
    pickup, donning = sequence(actor, 'pickup'), sequence(actor, 'donning')
    poses = pickup[:5] + [donning[0], donning[0]] + donning[1:]
    sheet = Image.new('RGB', (184 * 6, 232 * 2), '#303b40')
    for i, frame in enumerate(poses):
        frame.save(out / f'{i:03}.png')
        x, y = i % 6 * 184, i // 6 * 232
        sheet.paste(frame, (x, y + 20), frame)
        ImageDraw.Draw(sheet).text((x + 8, y + 4), str(i), fill='white')
    sheet.save(out / 'contact.png')
    (out / 'registration.json').write_text(json.dumps({'sourceHashes': shared.SOURCE_HASHES, 'operations': shared.OPS}, indent=2) + '\n')
    print(out.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('actor', choices=['veld', 'branforth'])
    review(parser.parse_args().actor)
