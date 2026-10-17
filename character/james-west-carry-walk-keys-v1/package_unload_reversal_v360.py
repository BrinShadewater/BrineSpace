import json
from pathlib import Path

from PIL import Image

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
output = bank / 'north-unload-chain-v360'
base = json.loads((bank / 'release-motion-review-v356/playback.json').read_text())
current = next(x for x in base['unload'] if x['gear'] == 'bare' and x['direction'] == 'north')
frames = sorted((output / 'bend/frames/bare').glob('*.png'))
assert len(frames) == 142
ordered = frames + frames[-2::-1]
endpoint = root / current['paths'][-1].lstrip('/')
paths = ['/' + x.relative_to(root).as_posix() for x in ordered] + [current['paths'][-1]]
assert len(paths) == 284
metadata = [{'pivot': [128, 224], 'size': [256, 256], 'standingHeight': 148}] * len(paths)
clocks = [(round((i + 1) * 450 / len(ordered)) - round(i * 450 / len(ordered))) for i in range(len(ordered))] + [70]
assert sum(clocks) == 520 and min(clocks) > 0
candidate = {'gear': 'candidate', 'direction': 'north', 'paths': paths, 'meta': metadata, 'clocks': clocks, 'loop': False}
current['gear'] = 'current'
(output / 'playback.json').write_text(json.dumps({'unload': [current, candidate]}, indent=2) + '\n')
images = [Image.open(x).convert('RGBA') for x in ordered] + [Image.open(endpoint).convert('RGBA')]
source_clocks = [round((i + 1) * 1000 / 24) - round(i * 1000 / 24) for i in range(len(ordered))] + [800]
images[0].save(output / 'reversed-source-chain.png', save_all=True, append_images=images[1:], duration=source_clocks, loop=0, disposal=0, blend=0)
images[0].save(output / 'game-clock-chain.png', save_all=True, append_images=images[1:], duration=clocks, loop=0, disposal=0, blend=0)
page = (bank / 'release-motion-review-v356/index.html').read_text()
page = page.replace('James release motion review', 'James unload reversal study')
page = page.replace('James - selected animation playback', 'James - unload reversal comparison')
page = page.replace('All directions, bare above and helmet below. Original source pixels, fixed foot anchors and selected clocks. Finite actions hold their endpoint. This is source playback, not station collision or furniture acceptance.', 'Current unload and unselected reversal candidate. Both use the 520ms game clock and fixed source registration. The candidate reverses the lowering source, then holds the existing empty-handed standing endpoint. This is source review, not native cargo contact acceptance.')
page = page.replace("const x=128+256*['west','east','north','south'].indexOf(row.direction),y=row.gear==='bare'?180:390", "const x=row.gear==='current'?256:768,y=280")
(output / 'reversal.html').write_text(page, encoding='utf8')
(output / 'reversal-provenance.json').write_text(json.dumps({'version': 360, 'authoredLoweringFrames': 142, 'derivedReverseIndices': list(range(140, -1, -1)), 'standingEndpoint': current['paths'][-1], 'runtimeDurationMs': 520, 'sourceDurationMs': sum(source_clocks), 'newFramesAuthoredForRise': 0, 'rgbAltered': False, 'selected': False, 'normalChanged': False, 'limits': 'Reversed lowering can retain a carrying arm posture. Cargo release/contact and final neutral join must be reviewed in actual gameplay before installation. Original material consistency still unproven.'}, indent=2) + '\n')
print(json.dumps({'candidateSlots': 284, 'gameClockMs': 520, 'reusedLoweringSource': True, 'normalChanged': False}))
