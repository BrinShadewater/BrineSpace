"""Candidate packaging checks; does not establish animation/runtime acceptance."""
import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parent
m = json.loads((root / 'manifest.json').read_text())
expected = {'lantern-bell-body.png': (1280, 960), 'lantern-bell-core.png': (1280, 960),
            'ribbon-swimmer.png': (640, 768), 'ribbon-head.png': (640, 768),
            'tidewalker-body.png': (1600, 420), 'tidewalker-fin.png': (320, 256),
            'tidewalker-sail.png': (160, 160), 'tidewalker-lights.png': (1600, 420)}
expected.update({n+'-'+layer+'.png':(1024,512) for n in ['glass-choir','veil-kite'] for layer in ['body','core']})
checks = 0
for entry in m['files'] + m['sources']:
    p = root / entry['path']
    assert p.is_file(), p
    assert hashlib.sha256(p.read_bytes()).hexdigest() == entry['sha256'], p
    with Image.open(p) as im:
        assert list(im.size) == entry['dimensions'], p
        assert im.mode == 'RGBA', p
        lo, hi = im.getchannel('A').getextrema()
        assert lo == 0 and hi > 0, p
        assert im.getchannel('A').histogram()[1:255] != [0]*254, p
        if entry['path'] in expected:
            assert im.size == expected[entry['path']], p
            checks += 1
    checks += 6
assert len(m['tidewalker']['light_positions']) == 26
assert len(set(map(tuple, m['tidewalker']['light_positions']))) == 26
assert len(m['tidewalker']['fin_roots']) == 6
assert len(m['tidewalker']['sail_roots']) == 7
assert isinstance(m['runtime_wired'],bool) and isinstance(m['owner_accepted'],bool)
checks += 5
print(f'PASS: {checks} candidate packaging checks; motion/native acceptance remains pending.')
