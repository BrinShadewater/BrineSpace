"""Normal q2 South drain05 study, preserving original per-manifest metadata."""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
B = ROOT / 'character/marsh-water-transition-material-v1'
read = lambda p: json.loads(p.read_text())
old = read(B / 'cardinal03-cross-review/family-manifest.json')
new = read(B / 'drain-south-05-unselected/manifest.json')
for key in ['frameWidth', 'frameHeight', 'pivot', 'standingHeight', 'textureFilter']:
    assert old[key] == new[key]
family = old.copy()
family['revision'] = 'marsh-cardinal-water-transitions-04-staged'
family['sources'] = ['drain-south-05' if n == 'drain-south-04' else n for n in old['sources']]
family['states'] = [new['states'][0] if s['id'] == 'cargo-drain-south' else s for s in old['states']]
out = B / 'cardinal04-cross-review'
out.mkdir(exist_ok=True)
(out / 'family-manifest.json').write_text(json.dumps(family, indent=2) + '\n')
combined = read(B / 'combined05-cross-review/manifest-list.json')
combined['manifests'] = [n.replace('cardinal03-cross-review', 'cardinal04-cross-review') for n in combined['manifests']]
out = B / 'combined06-cross-review'
out.mkdir(exist_ok=True)
(out / 'manifest-list.json').write_text(json.dumps(combined, indent=2) + '\n')
source = (ROOT / 'tools/review_marsh_water_transition_world07.gd').read_text()
source = source.replace('water-transition-world-07', 'water-transition-world-08').replace('WORLD07', 'WORLD08').replace('cardinal03-cross-review', 'cardinal04-cross-review').replace('Southdrain04', 'Southdrain05')
fixture = ROOT / 'tools/review_marsh_water_transition_world08.gd'
fixture.write_text(source)
fixture.with_suffix('.gd.uid').write_text('uid://cy6n8pq4mv3h\n')
fingerprint = (ROOT / 'tools/fingerprint_marsh_water_transition_world07.py').read_text().replace('water_transition_world07', 'water_transition_world08')
(ROOT / 'tools/fingerprint_marsh_water_transition_world08.py').write_text(fingerprint)
out = B / 'drain-south05-cross-review'
out.mkdir(exist_ok=True)
board = Image.new('RGB', (1792, 476), '#293b40')
for row, rev in enumerate(['04', '05']):
    board.paste(Image.open(B / f'drain-south-{rev}-unselected/whole-transition-comparison.png'), (0, row * 238))
board.save(out / 'revisions-04-05.png')
states = {s['id']: s for n in combined['manifests'] for s in read(ROOT / n)['states']}
assert len(states) == 48 and sum(len(s['frameFiles']) for s in states.values()) == 272
print('q2 Southdrain05 private study prepared; 48 states/272 slots, original metadata retained.')
