"""Extract a provisional whole-body cycle from the preserved Veld motion video."""
from pathlib import Path
import hashlib
import json
import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw
from rebuild_bill_art import binary

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/veld-identity-correction-v1'


def main(direction='east'):
    if direction not in ['east','west','south','north']:raise ValueError('Unsupported video direction')
    source = BASE / ('sources/walk-video-01.mp4' if direction=='east' else f'sources/walk-{direction}-video-01.mp4')
    if direction=='north':source=BASE/'sources/walk-north-video-02.mp4'
    out = BASE / ('review/walk-video-cycle-01' if direction=='east' else f'review/walk-{direction}-video-cycle-01')
    out.mkdir(exist_ok=True)
    # Visually matched full-cycle contacts at 29 and 56; sample the existing
    # six-slot time boundaries. One transform preserves torso rise and rotation.
    slots = [29, 34, 38, 43, 48, 52]
    durations = [170, 130, 150, 170, 130, 150]
    scale = 140 / 1369
    position = (round(128 - 610 * scale), round(223 - 1522 * scale))
    cycle=[29,56]
    if direction=='west':
        slots=[28,33,36,40,45,48]
        scale=140/1282
        position=(round(128-650*scale),round(223-1498*scale))
        cycle=[28,52]
    if direction=='south':
        slots=[24,29,32,36,41,44]
        scale=140/1454
        position=(round(128-624*scale),round(223-1564*scale))
        cycle=[24,48]
    if direction=='north':
        slots=[26,31,34,38,43,46]
        scale=140/1284
        position=(round(128-624*scale),round(223-1534*scale))
        cycle=[26,50]
    reader = imageio.get_reader(str(source), format='ffmpeg')
    assert reader.get_meta_data()['size'] == (1248, 1664)
    poses = []
    records = []
    for slot, frame in enumerate(slots):
        rgb = np.asarray(reader.get_data(frame))[:, :, :3]
        r, g, b = rgb.astype(int).transpose(2, 0, 1)
        keep = ~((r > g + 35) & (b > g + 35))
        rgba = np.dstack([rgb, keep.astype(np.uint8) * 255])
        rgba[~keep] = 0
        raw = Image.fromarray(rgba)
        Image.fromarray(rgb).save(out / f'raw-{frame:03}.png')
        dense = binary(raw.resize((round(raw.width * scale), round(raw.height * scale)), Image.Resampling.BOX), True)
        pose = Image.new('RGBA', (256, 256))
        pose.alpha_composite(dense, position)
        pose.save(out / f'walk-{direction}-{slot:03}.png')
        poses.append(pose)
        records.append(dict(slot=slot, sourceFrame=frame, bounds=pose.getbbox()))
    reader.close()
    sheet = Image.new('RGB', (1536, 256), '#293b40')
    previews = []
    for slot, pose in enumerate(poses):
        sheet.paste(pose, (slot * 256, 0), pose)
        canvas = Image.new('RGB', (256, 256), '#293b40')
        ImageDraw.Draw(canvas).line((0, 224, 256, 224), fill='#839597')
        canvas.paste(pose, (0, 0), pose)
        previews.append(canvas)
    sheet.save(out / 'contact.png')
    previews[0].save(out / 'stationary-loop.gif', save_all=True, append_images=previews[1:], duration=durations, loop=0)
    report = dict(status='prepared_selection_tracked_in_ledger', direction=direction, source=source.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(source.read_bytes()).hexdigest(), sourceCycle=cycle, sourceFps=24, scale=scale, position=position, pivot=[128, 224], durations=durations, records=records, limits=['Single transform intentionally retains any camera drift for review.', 'Six-slot resampling and sole contact require native movement review.', 'Fitted helmet and selection evidence are tracked in the companion registration and clip ledger.'])
    (out / 'registration.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Prepared six video-derived study frames; selection and contact evidence tracked in the clip ledger.')


if __name__ == '__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('direction',choices=['east','west','south','north'],default='east',nargs='?')
    main(parser.parse_args().direction)
