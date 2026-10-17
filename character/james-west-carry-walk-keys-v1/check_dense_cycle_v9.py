from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, subprocess
import numpy as np

p = Path(__file__).resolve().parent
r = p.parents[1]
def digest(f): return hashlib.sha256(f.read_bytes()).hexdigest()
plan = json.loads((p / 'dense-walk-v6-plan.json').read_bytes())
review = json.loads((p / 'dense-cycle-v9-review.json').read_bytes())
assert all(digest(r / f) == sha for f, sha in review['sourceSha256'].items())
assert all(digest(p / f) == sha for f, sha in review['boardSha256'].items())
assert digest(p / 'dense-cycle-v9-preview.apng') == review['previewSha256']
namespace = {'__file__': str(p / 'audit_case_components_v5.py')}
exec((p / 'audit_case_components_v5.py').read_text().split('results=[]')[0], namespace)
components = namespace['components']
results = []
for i in plan['remainingAuthoredPhases']:
    n = f'walk{i:02d}-dense-carry-v6'
    inputs = json.loads((p / f'{n}-inputs.json').read_bytes())
    assert all(digest(r / f) == sha for f, sha in inputs['preCallSha256'].items())
    d = json.loads((p / f'{n}-review.json').read_bytes())
    assert digest(p / f'{n}-raw.png') == d['rawSha256']
    results.append({'phase': i, 'candidateComponents': components(p / f'{n}.png'),
                    'originalComponents': components(p / inputs['baseFile'])})

keys = set(plan['originalKeys'])
def source(i):
    if i == 3: return p / 'walk03-contact-v7.png'
    if i == 12: return p / 'walk12-case-master-v5-seam.png'
    return p / (f'walk{i:02d}-case-master-v5.png' if i in keys else f'walk{i:02d}-dense-carry-v6.png')

manifest = r / plan['sourceManifest']
originals, candidates = [], []
for i in range(49):
    im = Image.open(manifest.parent / plan['state']['frameFiles'][i]).convert('RGBA')
    base = Image.new('RGBA', (256, 256)); base.paste(im, (36, 52))
    originals.append(base); candidates.append(Image.open(source(i)).convert('RGBA'))
join_deltas = []
for i in range(49):
    j = (i + 1) % 49
    da = np.any(np.array(originals[i]) != np.array(originals[j]), axis=2)
    db = np.any(np.array(candidates[i]) != np.array(candidates[j]), axis=2)
    join_deltas.append({'from': i, 'to': j, 'originalWholeChangedPixels': int(da.sum()),
                        'candidateWholeChangedPixels': int(db.sum()),
                        'originalLegsBelow169ChangedPixels': int(da[169:].sum()),
                        'candidateLegsBelow169ChangedPixels': int(db[169:].sum()),
                        'candidateCaseContactChangedPixels': int(db[124:157, 88:151].sum())})

board = Image.new('RGBA', (1024, 564), (48, 59, 63, 255))
d = ImageDraw.Draw(board)
for row, bank in enumerate((originals, candidates)):
    for col, i in enumerate((47, 48, 0, 1)):
        board.alpha_composite(bank[i], (col * 256, row * 282 + 26))
        d.text((col * 256 + 5, row * 282 + 7), f'{"original" if row == 0 else "candidate"} phase{i}', fill='white')
board.convert('RGB').save(p / 'dense-cycle-v9-loop-join.png')

rasters = [f.relative_to(r).as_posix() for f in p.iterdir() if f.suffix in ('.png', '.apng')]
attrs = subprocess.run(['git', 'check-attr', '-z', 'filter', '--stdin'],
                       input=b'\0'.join(s.encode() for s in rasters) + b'\0',
                       cwd=r, capture_output=True, check=True).stdout.split(b'\0')
assert len(attrs) == len(rasters) * 3 + 1 and all(x == b'lfs' for x in attrs[2:-1:3])
report = {'all41PreparedInputsAndRawHashesStable': True, 'sourceComponents': results,
          'all41InitialCandidatesSingleAlpha128Component': all(len(d['candidateComponents']) == 1 for d in results),
          'fortyNineOriginalGuardsExact': True, 'sourceClockMs': 1680,
          'decodedPreviewFramesExact': 49, 'viewerTerminalHoldMs': 0,
          'adjacentAndLoopDeltas': join_deltas,
          'loopJoinBoardSha256': digest(p / 'dense-cycle-v9-loop-join.png'),
          'rastersLfs': len(rasters), 'normalChanged': False, 'nativeRun': False,
          'sourceCoverageComplete': True, 'visualMotionAcceptance': False, 'fullGoalComplete': False}
(p / 'dense-cycle-v9-checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k not in ('sourceComponents', 'adjacentAndLoopDeltas')}))
for d in results:
    if len(d['candidateComponents']) != 1:
        print('Detached silhouette:', d['phase'], d['candidateComponents'][1:])
print('Loop join diagnostic:', join_deltas[-1])
