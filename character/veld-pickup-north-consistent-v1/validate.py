from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt

here = Path(__file__).resolve().parent
original = json.loads((here / 'original-state.json').read_text())
checks = 0
for variant in ['bare', 'helmet']:
    manifest = json.loads((here / f'{variant}-manifest.json').read_text())
    state = manifest['states'][0]
    assert all(state[k] == original[k] for k in ['id', 'frameDurationsMs', 'loop', 'facings', 'waterKinds', 'waterPoses', 'depthOffsets'])
    checks += 1
    assert manifest['pivot'] == [128, 224] and manifest['standingHeight'] == 148
    checks += 1
    frames = []
    with Image.open(here / f'{variant}-pickup-north-v1.gif') as gif:
        assert gif.n_frames == 6
        checks += 1
        for i in range(6):
            pixels = np.array(Image.open(here / state['frameFiles'][i]).convert('RGBA'))
            assert pixels.shape == (256, 256, 4)
            checks += 1
            alpha = pixels[:, :, 3]
            assert not np.any(np.concatenate([alpha[0], alpha[-1], alpha[:, 0], alpha[:, -1]]) > 20)
            checks += 1
            gif.seek(i)
            rgb = np.array(gif.convert('RGB')).astype(int)
            outside = (alpha == 0) & (distance_transform_edt(alpha < 200) > 2)
            assert np.abs(rgb[outside] - [32, 42, 48]).max() <= 3
            checks += 1
            source = np.array(Image.open(here.parent / 'veld-unload-north-consistent-v1' / f'frames/{variant}/{5-i:03}.png').convert('RGBA'))
            assert np.array_equal(pixels, source)
            checks += 1
            frames.append(pixels)
    idle = np.array(Image.open(here.parent / 'veld-unload-north-consistent-v1' / f'frames/{variant}/005.png').convert('RGBA'))
    assert np.array_equal(frames[0], idle)
    checks += 1
(here / 'packaging-checks.json').write_text(json.dumps({'checks': checks, 'failures': 0, 'original_metadata_exact': True, 'accepted_idle_entry_exact': True, 'decoded_gif_frames': 12}, indent=2))
print(f'{checks} packaging checks, 0 failures')
