from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json
import numpy as np

p = Path(__file__).resolve().parent
r = p.parents[1]
indices = list(range(21))
plan = json.loads((p / 'dense-walk-v6-plan.json').read_bytes())
durations = plan['state']['frameDurationsMs']
assert len(durations) == 49 and sum(durations) == 1680

def source(i):
    if i == 3:
        return p / 'walk03-contact-v7.png'
    if i == 12:
        return p / 'walk12-case-master-v5-seam.png'
    return p / (f'walk{i:02d}-case-master-v5.png' if i in (0, 8, 20)
                else f'walk{i:02d}-dense-carry-v6.png')

files, checks, frames = [], [], []
for i in indices:
    f = source(i)
    donor = (p / f'walk{i:02d}-dense-carry-v6-original.png' if i not in (0, 8, 12, 20)
             else r / 'character/james-west-carry-depth-v1/walk12-original.png' if i == 12
             else p / f'walk{i:02d}-carry-original.png')
    a = np.array(Image.open(donor).convert('RGBA'))
    b = np.array(Image.open(f).convert('RGBA'))
    mask = np.ones(a.shape[:2], bool)
    mask[104:169, 88:166] = False
    assert mask.sum() == 60466 and np.array_equal(a[mask], b[mask]), i
    frames.append(Image.fromarray(b))
    files.extend((donor, f))
    checks.append({'phase': i, 'originalOutside60466Exact': True})

boards = []
for start in (0, 7, 14):
    subset = list(zip(indices, frames))[start:start + 7]
    for kind, width, height in (('full', 256, 256), ('upper', 192, 192)):
        board = Image.new('RGBA', (len(subset) * width, height + 26), (48, 59, 63, 255))
        d = ImageDraw.Draw(board)
        for col, (i, im) in enumerate(subset):
            draw = im if kind == 'full' else im.crop((80, 88, 176, 184)).resize((192, 192), Image.Resampling.NEAREST)
            board.alpha_composite(draw, (col * width, 26))
            d.text((col * width + 5, 7), f'phase{i}', fill='white')
        f = p / f'dense-start-v8-{kind}-{start}.png'
        board.convert('RGB').save(f)
        boards.append(f)

for start in (12, 16, 20):
    subset = list(zip(indices, frames))[start:start + 4]
    board = Image.new('RGBA', (900, len(subset) * 205), (48, 59, 63, 255))
    d = ImageDraw.Draw(board)
    for row, (i, im) in enumerate(subset):
        for x, h in zip((140, 410, 620, 790), (148, 82, 54, 27)):
            size = round(256 * h / 148)
            board.alpha_composite(im.resize((size, size), Image.Resampling.LANCZOS),
                                  (round(x - 128 * h / 148), round(row * 205 + 195 - 224 * h / 148)))
            d.text((x - 60, row * 205 + 7), f'phase {i} / {h}', fill='white')
    f = p / f'dense-start-v8-station-{start}.png'
    board.convert('RGB').save(f)
    boards.append(f)

viewer_durations = durations[:21].copy()
viewer_durations[-1] += 600
preview = p / 'dense-start-v8-preview.apng'
frames[0].save(preview, format='PNG', save_all=True, append_images=frames[1:],
               duration=viewer_durations, loop=0, disposal=0, blend=0)
decoded = Image.open(preview)
assert decoded.n_frames == 21
for i, frame in enumerate(frames):
    decoded.seek(i)
    assert decoded.convert('RGBA').tobytes() == frame.tobytes()
    assert decoded.info['duration'] == viewer_durations[i]

def digest(f):
    return hashlib.sha256(f.read_bytes()).hexdigest()

reuse = {}
for kind, start in (('full', 0), ('upper', 0)):
    old = p / f'dense-start-v7-{kind}-{start}.png'
    new = p / f'dense-start-v8-{kind}-{start}.png'
    assert old.read_bytes() == new.read_bytes()
    reuse[new.name] = old.name

report = {'phases': indices, 'sourceSha256': {f.relative_to(r).as_posix(): digest(f) for f in files},
          'checks': checks, 'fullWalkDurationsMs': durations, 'fullWalkDurationMs': 1680,
          'sliceDurationsMs': durations[:21], 'sliceDurationMs': sum(durations[:21]),
          'viewerTerminalHoldMs': 600, 'viewerDurationsMs': viewer_durations,
          'decodedPreviewFramesExact': 21, 'previewSha256': digest(preview),
          'boardSha256': {f.name: digest(f) for f in boards}, 'unchangedBoards': reuse,
          'visualReviewPending': True, 'sourceAcceptance': False, 'selected': False,
          'scope': '21 consecutive actual original-body source poses, finite initial slice. No complete gait, continuous cadence, helmet, native, room or owner acceptance.'}
(p / 'dense-start-v8-review.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(f'21 chronological sources: {sum(durations[:21])}ms source clock; APNG frames/timing exact. Two boards unchanged; seven new boards need visual review.')
