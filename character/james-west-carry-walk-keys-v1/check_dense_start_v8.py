from pathlib import Path
from PIL import Image
import hashlib, json, subprocess
import numpy as np

p = Path(__file__).resolve().parent
r = p.parents[1]
def digest(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def stable(d):
    assert all(digest(r / f) == sha for f, sha in d['preCallSha256'].items())

plan = json.loads((p / 'dense-walk-v6-plan.json').read_bytes())
assert digest(r / plan['sourceManifest']) == plan['sourceManifestSha256']
for i in plan['remainingAuthoredPhases']:
    stable(json.loads((p / f'walk{i:02d}-dense-carry-v6-inputs.json').read_bytes()))

namespace = {'__file__': str(p / 'audit_case_components_v5.py')}
exec((p / 'audit_case_components_v5.py').read_text().split('results=[]')[0], namespace)
components = namespace['components']
results = []
for i in range(13, 20):
    n = f'walk{i:02d}-dense-carry-v6'
    inputs = json.loads((p / f'{n}-inputs.json').read_bytes())
    review = json.loads((p / f'{n}-review.json').read_bytes())
    assert digest(p / f'{n}-raw.png') == review['rawSha256']
    a = np.array(Image.open(p / inputs['baseFile']).convert('RGBA'))
    b = np.array(Image.open(p / f'{n}.png').convert('RGBA'))
    mask = np.ones(a.shape[:2], bool)
    mask[104:169, 88:166] = False
    assert np.array_equal(a[mask], b[mask]) and mask.sum() == 60466
    results.append({'phase': i, 'outside60466Exact': True,
                    'originalComponents': components(p / inputs['baseFile']),
                    'candidateComponents': components(p / f'{n}.png')})

review = json.loads((p / 'dense-start-v8-review.json').read_bytes())
assert all(digest(r / f) == sha for f, sha in review['sourceSha256'].items())
assert digest(p / 'dense-start-v8-preview.apng') == review['previewSha256']
assert review['decodedPreviewFramesExact'] == 21
rasters = [f.relative_to(r).as_posix() for f in p.iterdir() if f.suffix in ('.png', '.apng')]
attrs = subprocess.run(['git', 'check-attr', '-z', 'filter', '--stdin'],
                       input=b'\0'.join(s.encode() for s in rasters) + b'\0',
                       cwd=r, capture_output=True, check=True).stdout.split(b'\0')
assert len(attrs) == len(rasters) * 3 + 1 and all(x == b'lfs' for x in attrs[2:-1:3])
report = {'all41PreparedInputsStable': True, 'newSources': results,
          'newSingleAlpha128Component': all(len(d['candidateComponents']) == 1 for d in results),
          'twentyOneOriginalGuardsExact': True, 'sourceClockMs': review['sliceDurationMs'],
          'fullClockMs': 1680, 'decodedPreviewFramesExact': 21, 'rastersLfs': len(rasters),
          'normalChanged': False, 'nativeRun': False, 'fullGoalComplete': False}
(p / 'dense-start-v8-checks.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k != 'newSources'}))
for d in results:
    if len(d['candidateComponents']) != 1:
        print('Detached silhouette:', d['phase'], d['candidateComponents'][1:])
