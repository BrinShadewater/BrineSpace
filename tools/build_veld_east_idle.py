"""West idle study from its own locked pose, using accepted east breathing."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

root = Path('character/crew-runtime-matte-v1/veld')
manifest = json.loads((root / 'manifest.json').read_text())
state = next(s for s in manifest['states'] if s['id'] == 'idle-east')
source = root / state['frameFiles'][0]
out = Path('character/veld-idle-east-readable-v1')
out.mkdir(exist_ok=True)
(out / 'frames').mkdir(exist_ok=True)
a = np.array(Image.open(source).convert('RGBA'))
Image.fromarray(a).save(out / 'locked-reference.png')
yy, xx = np.indices(a.shape[:2])
v = a.astype(float) / 255
prem = v.copy()
prem[..., :3] *= prem[..., 3:]
envelope = np.where((yy > 53) & (yy < 121), np.sin(np.pi * np.clip((yy-53)/68, 0, 1))**2, 0)
side = np.tanh((xx-92)/8)
for i in range(72):
    phase = (1-np.cos(2*np.pi*i/72))/2
    dx = 1.25*phase*envelope*side
    dy = -.65*phase*envelope
    b = np.stack([map_coordinates(prem[..., k], [yy-dy, xx-dx], order=1, mode='constant', cval=0) for k in range(4)], axis=-1)
    b[..., :3] = np.divide(b[..., :3], b[..., 3:], out=np.zeros_like(b[..., :3]), where=b[..., 3:] > 0)
    b = np.clip(np.rint(b*255), 0, 255).astype('uint8')
    b[yy <= 53] = a[yy <= 53]
    b[yy >= 121] = a[yy >= 121]
    assert np.array_equal(b[:54], a[:54])
    assert np.array_equal(b[121:], a[121:])
    Image.fromarray(b).save(out / 'frames' / f'{i:03}.png')
html = Path('character/bill-idle-east-readable-v1/index.html').read_text(encoding='utf-8')
html = html.replace('Bill east breathing idle', 'Veld east breathing idle').replace('Bill — clearer breathing and brown hair', 'James — south breathing idle').replace('Left: corrected dark-brown hair.', 'Left: locked east pose.').replace('Right: stronger local breathing motion;', 'Right: matching breathing motion;')
(out / 'index.html').write_text(html, encoding='utf-8')
(out / 'checks.json').write_text(json.dumps({'source': source.as_posix(), 'frames':72, 'fps':24, 'durationMs':3000, 'method':'Accepted east procedural breathing applied to independent east pose', 'headAndFeetExact':True, 'paletteUnchanged':True, 'installed':False, 'generationSpendUSD':0}, indent=2))
print('72 west frames exported; head and feet exact; independent east reference.')
