"""Compare pending axial bodies at a fixed trial scale; never select clips."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label, binary_dilation

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCALE = .26
sheet = Image.new('RGBA', (1536, 620), '#202a30')
draw = ImageDraw.Draw(sheet)
records = []
for row, direction in enumerate(['north', 'south']):
    source = HERE / f'{direction}-transition-source-v1.png'
    pixels = np.array(Image.open(source).convert('RGBA'))
    labels, count = label(pixels[:, :, 3] > 160)
    sizes = np.bincount(labels.ravel())
    ids = sorted(range(1, count + 1), key=lambda k: sizes[k], reverse=True)[:4]
    ids.sort(key=lambda k: np.where(labels == k)[1].mean())
    images = [Image.open(HERE / f'frames/bare/tread-{direction}/000.png').convert('RGBA')]
    names = ['selected candidate tread']
    for slot, component in enumerate(ids):
        keep = binary_dilation(labels == component, iterations=2)
        cut = pixels.copy()
        cut[~keep] = 0
        y, x = np.where(labels == component)
        box = [int(x.min()), int(y.min()), int(x.max() + 1), int(y.max() + 1)]
        raw = Image.fromarray(cut).crop(box)
        image = raw.resize((round(raw.width * SCALE), round(raw.height * SCALE)), Image.Resampling.LANCZOS)
        images.append(image)
        names.append(f'raw interior {slot + 1} / scale .26')
        records.append({'direction': direction, 'interior': slot + 1, 'sourceBox': box,
                        'fixedTrialScale': SCALE, 'projectedTrialSize': list(image.size),
                        'sourceSha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    images.append(Image.open(HERE / f'frames/bare/swim-{direction}/000.png').convert('RGBA'))
    names.append('selected candidate swim')
    for column, image in enumerate(images):
        image = image.crop(image.getbbox())
        position = (column * 256 + (256 - image.width) // 2,
                    row * 310 + 45 + (256 - image.height) // 2)
        sheet.alpha_composite(image, position)
        draw.text((column * 256 + 7, row * 310 + 8), direction + ' / ' + names[column], fill='white')
        draw.text((column * 256 + 7, row * 310 + 25),
                  f'silhouette {image.width}x{image.height}; centers aligned', fill='#b1c2cc')
sheet.save(HERE / 'axial-source-scale-audit-v1.png')
heads = Image.new('RGBA', (768, 330), '#202a30')
draw = ImageDraw.Draw(heads)
for row, direction in enumerate(['north', 'south']):
    upright = ('character/veld-shared-helmet-v1/fitted-north.png' if direction == 'north'
               else 'character/veld-shared-helmet-south-v1/fitted-helmet.png')
    paths = [upright, f'character/veld-water-master-audit-v1/fitted-swim-{direction}-head.png']
    for column, path in enumerate(paths):
        image = Image.open(ROOT / path).convert('RGBA')
        heads.alpha_composite(image.resize((image.width * 3, image.height * 3), Image.Resampling.NEAREST),
                              (column * 384 + 130, row * 165 + 35))
        title = 'upright shared component' if column == 0 else 'pitched swim component'
        draw.text((column * 384 + 20, row * 165 + 10),
                  f'{direction}: {title} {image.width}x{image.height}', fill='white')
heads.save(HERE / 'axial-helmet-master-audit-v1.png')
findings = [
    'Both axial sources enlarge head/shoulder mass at the side-source trial scale .26; calibrate physical rulers independently.',
    'North rear shell pitch and south crown/visor progression need authored intermediates between exact endpoint heads.',
    'Upright and prone helmet components retain neutral construction and widths 33 north / 35 south.',
    'Centered silhouettes are an anatomy diagnostic, not registered motion; no pending interiors are selected.'
]
(HERE / 'axial-source-audit-v1.json').write_text(json.dumps({
    'status': 'raw_sources_pending_anatomical_scale_and_pitch_fitting', 'installed': False,
    'trialScale': SCALE, 'registration': 'centered silhouettes, not motion registration',
    'records': records, 'visualFindings': findings}, indent=2) + '\n', encoding='utf-8')
print('8 raw body samples and 4 master head components saved; selection unchanged.')
