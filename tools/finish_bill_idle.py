"""Match neutral suit chroma and freeze the approved head for an idle trial."""
import argparse
import json
import shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
args = p.parse_args()
src, out = args.source, args.output
out.mkdir(exist_ok=True)
(out / 'frames').mkdir(exist_ok=True)
ref = np.array(Image.open(src / 'locked-reference.png').convert('RGBA'))
files = sorted((src / 'frames').glob('*.png'))
arrays = [np.array(Image.open(f).convert('RGBA')) for f in files]
yy = np.indices(ref.shape[:2])[0]

def chroma(a):
    rgb = a[..., :3].astype(float)
    mask = (a[..., 3] > 240) & (yy > 56) & (np.ptp(rgb, axis=-1) < 40) & (rgb.mean(-1) > 25) & (rgb.mean(-1) < 140)
    c = rgb[mask]
    return np.median(c - c.mean(-1)[:, None], axis=0)

delta = chroma(ref) - np.median([chroma(a) for a in arrays], axis=0)
head = np.clip((56 - yy) / 5, 0, 1)
for f, a in zip(files, arrays):
    rgb = a[..., :3].astype(float)
    weight = np.clip((48 - np.ptp(rgb, axis=-1)) / 12, 0, 1) * (a[..., 3] > 0)
    b = a.copy()
    b[..., :3] = np.clip(np.rint(rgb + delta * weight[..., None]), 0, 255).astype('uint8')
    b = np.rint(ref * head[..., None] + b * (1 - head[..., None])).astype('uint8')
    assert np.array_equal(b[:52], ref[:52])
    assert np.array_equal(b[56:, :, 3], a[56:, :, 3])
    Image.fromarray(b).save(out / 'frames' / f.name)
shutil.copy2(src / 'locked-reference.png', out / 'locked-reference.png')
html = (src / 'index.html').read_text(encoding='utf-8')
html = html.replace('Right: new full source trial.', 'Right: matched matte suit and completely still locked face.')
html = html.replace('<video src="source.mp4" controls loop></video>', '')
(out / 'index.html').write_text(html, encoding='utf-8')
sheet = Image.new('RGB', (1104, 220), '#303b40')
draw = ImageDraw.Draw(sheet)
for j, n in enumerate(np.linspace(0, len(files)-1, 6).astype(int)):
    im = Image.open(out / 'frames' / files[n].name)
    sheet.paste(im, (j*184, 20), im)
    draw.text((j*184, 0), str(n), fill='white')
sheet.save(out / 'contact.png')
(out / 'checks.json').write_text(json.dumps({'frames':len(files), 'fixedChromaOffset':delta.tolist(), 'headMatchesLockedReference':True, 'bodyAlphaPreserved':True, 'timingUnchanged':True, 'installed':False, 'loopSelected':False}, indent=2))
print('Finished', len(files), 'frames; fixed chroma offset', delta.tolist())
