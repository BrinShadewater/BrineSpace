"""Extract a reversible locker study; never writes runtime frames."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / 'output/bill-locker-identity-2026-09-22'

def main():
    OUT.mkdir(exist_ok=True)
    source = HERE / 'generated-source.png'
    pixels = np.array(Image.open(source).convert('RGBA'))
    pixels[pixels[:, :, 3] < 128] = 0
    pixels[pixels[:, :, 3] >= 128, 3] = 255
    raw = Image.fromarray(pixels)
    idle = Image.open(ROOT / 'character/major-bill-v3/frames/bare/idle-east/000.png').convert('RGBA')
    geared = Image.open(ROOT / 'character/major-bill-v3/frames/helmet/idle-east/000.png').convert('RGBA')
    palette_pixels = []
    for im in [idle, geared]:
        a = np.array(im)
        palette_pixels.extend(a[a[:, :, 3] == 255, :3].tolist())
    palette = Image.fromarray(np.array(palette_pixels, dtype=np.uint8).reshape(1, -1, 3)).quantize(colors=256)
    scale = 148 / 428
    poses, records = [], []
    for index in range(8):
        box = (index % 4 * 384, index // 4 * 512, index % 4 * 384 + 384, index // 4 * 512 + 512)
        cell = raw.crop(box)
        a = np.array(cell)
        ys, xs = np.where(a[465:482, :, 3] > 0)
        foot_x = (int(xs.min()) + int(xs.max()) + 1) / 2
        scaled = cell.resize((round(384 * scale), round(512 * scale)), Image.Resampling.NEAREST)
        mapped = scaled.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        mapped.putalpha(scaled.getchannel('A'))
        frame = Image.new('RGBA', (184, 208))
        paste = (round(92 - foot_x * scale), round(196 - 482 * scale))
        frame.alpha_composite(mapped, paste)
        poses.append(frame)
        records.append({'cell': box, 'foot': [foot_x, 482], 'paste': paste})
    # Keep the runtime standing endpoints byte-for-byte, only adding transparent headroom.
    for index, im in [(0, idle), (7, geared)]:
        poses[index] = Image.new('RGBA', (184, 208))
        poses[index].alpha_composite(im, (0, 24))
    sequences = {'equip': [0,1,2,2,3,3,3,4,5,6,7,7],
                 'remove': [7,6,5,4,3,3,3,2,2,2,1,0]}
    for name, order in sequences.items():
        folder = OUT / name
        folder.mkdir(exist_ok=True)
        for i, pose in enumerate(order):
            poses[pose].save(folder / f'{i:03}.png')
    board = Image.new('RGBA', (184 * 8, 232), (30, 40, 48, 255))
    draw = ImageDraw.Draw(board)
    for i, frame in enumerate(poses):
        board.alpha_composite(frame, (184 * i, 24))
        draw.text((184 * i + 5, 5), f'pose {i}', fill='white')
    board.save(OUT / 'candidate-board.png')
    recipe = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'canvas': [184,208], 'pivot': [92,196], 'standingHeight':148,
              'scale':scale, 'alpha_threshold':128, 'frames':records,
              'sequences':sequences, 'status':'study only; native handoff and identity review pending'}
    (HERE / 'registration.json').write_text(json.dumps(recipe, indent=2) + '\n')
    print('Extracted eight source poses and two 12-frame studies; runtime unchanged')

if __name__ == '__main__':
    main()
