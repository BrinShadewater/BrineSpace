from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json
import numpy as np

p = Path(__file__).resolve().parent
r = p.parents[1]
plan = json.loads((p / 'dense-walk-v6-plan.json').read_bytes())
manifest = r / plan['sourceManifest']
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == plan['sourceManifestSha256']
m = json.loads(manifest.read_bytes())
state = next(s for s in m['states'] if s['id'] == 'walk-west')
assert state == plan['state'] and m['pivot'] == [92, 172]
durations = state['frameDurationsMs']
assert len(durations) == 49 and sum(durations) == 1680
keys = set(plan['originalKeys'])

def source(i):
    if i == 3: return p / 'walk03-contact-v7.png'
    if i == 12: return p / 'walk12-case-master-v5-seam.png'
    return p / (f'walk{i:02d}-case-master-v5.png' if i in keys else f'walk{i:02d}-dense-carry-v6.png')

frames, files, checks, boards = [], [manifest], [], []
for i in range(49):
    f = source(i)
    donor = manifest.parent / state['frameFiles'][i]
    original = Image.open(donor).convert('RGBA')
    assert original.size == (184, 184)
    base = Image.new('RGBA', (256, 256))
    base.paste(original, (36, 52))
    candidate = Image.open(f).convert('RGBA')
    assert candidate.size == (256, 256)
    a, b = np.array(base), np.array(candidate)
    mask = np.ones((256, 256), bool)
    mask[104:169, 88:166] = False
    assert mask.sum() == 60466 and np.array_equal(a[mask], b[mask]), i
    frames.append(candidate)
    files.extend((f, donor))
    checks.append({'phase': i, 'originalOutside60466Exact': True,
                   'headAbove104AndLegsBelow169Exact': True,
                   'originalNativeSize': [184, 184], 'translation': [36, 52]})

for start in range(0, 49, 7):
    subset = list(enumerate(frames))[start:start + 7]
    for kind, width, height in (('full', 256, 256), ('upper', 192, 192)):
        board = Image.new('RGBA', (len(subset) * width, height + 26), (48, 59, 63, 255))
        d = ImageDraw.Draw(board)
        for col, (i, im) in enumerate(subset):
            draw = im if kind == 'full' else im.crop((80, 88, 176, 184)).resize((192, 192), Image.Resampling.NEAREST)
            board.alpha_composite(draw, (col * width, 26))
            d.text((col * width + 5, 7), f'phase{i}', fill='white')
        f = p / f'dense-cycle-v9-{kind}-{start}.png'
        board.convert('RGB').save(f)
        boards.append(f)

for start in range(20, 49, 4):
    subset = list(enumerate(frames))[start:start + 4]
    board = Image.new('RGBA', (900, len(subset) * 205), (48, 59, 63, 255))
    d = ImageDraw.Draw(board)
    for row, (i, im) in enumerate(subset):
        for x, h in zip((140, 410, 620, 790), (148, 82, 54, 27)):
            size = round(256 * h / 148)
            board.alpha_composite(im.resize((size, size), Image.Resampling.LANCZOS),
                                  (round(x - 128 * h / 148), round(row * 205 + 195 - 224 * h / 148)))
            d.text((x - 60, row * 205 + 7), f'phase {i} / {h}', fill='white')
    f = p / f'dense-cycle-v9-station-{start}.png'
    board.convert('RGB').save(f)
    boards.append(f)

preview = p / 'dense-cycle-v9-preview.apng'
frames[0].save(preview, format='PNG', save_all=True, append_images=frames[1:],
               duration=durations, loop=0, disposal=0, blend=0)
decoded = Image.open(preview)
assert decoded.n_frames == 49
for i, frame in enumerate(frames):
    decoded.seek(i)
    assert decoded.convert('RGBA').tobytes() == frame.tobytes()
    assert decoded.info['duration'] == durations[i]

def digest(f): return hashlib.sha256(f.read_bytes()).hexdigest()
reuse = {}
for kind in ('full', 'upper'):
    for start in (0, 7, 14):
        old = p / f'dense-start-v8-{kind}-{start}.png'
        new = p / f'dense-cycle-v9-{kind}-{start}.png'
        assert old.read_bytes() == new.read_bytes()
        reuse[new.name] = old.name

report = {'sourceSha256': {f.relative_to(r).as_posix(): digest(f) for f in files},
          'checks': checks, 'phases': list(range(49)), 'frameDurationsMs': durations,
          'sourceDurationMs': 1680, 'viewerTerminalHoldMs': 0,
          'decodedPreviewFramesExact': 49, 'previewSha256': digest(preview),
          'boardSha256': {f.name: digest(f) for f in boards}, 'unchangedBoards': reuse,
          'visualReviewPending': True, 'sourceAcceptance': False, 'selected': False,
          'scope': 'Complete49 actual chronological original-body carrying sources. Source coverage complete only; full temporal/art/helmet/native/room/owner acceptance unproven.'}
(p / 'dense-cycle-v9-review.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('49 chronological sources; 1680ms exact decoded APNG, no review hold. Six boards byte-identical to reviewed v8; 16 new boards need visual review.')
