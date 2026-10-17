from pathlib import Path
import hashlib
import json
import re
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import label

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
BASE = ROOT / 'character/bill-walk-west-master-repair-v2'
BANK = ROOT / 'character/bill-walk-west-material-v1'

def mask(im):
    a = np.array(im)
    labs, _ = label(a[:, :, 3] >= 180)
    counts = np.bincount(labs.ravel())
    return labs == int(counts[1:].argmax() + 1)

def bounds(m):
    ys, xs = np.where(m)
    return [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)]

freeze = json.loads((OUT / 'input-freeze.json').read_text(encoding='utf-8'))
for path, sha in freeze.items():
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path

images = {}
rows = []
for n in [47, 0, 1]:
    old = Image.open(BANK / f'frames/bare/walk-west/{n:03}.png').convert('RGBA')
    previous = Image.open(BASE / f'canvas-normalized-study-{n:03}.png').convert('RGBA')
    if n == 47:
        candidate = previous.copy()
        generated = False
    else:
        job = json.loads((OUT / f'generation-provenance-{n:03}-v4.json').read_text(encoding='utf-8'))
        assert job['status'] == 'completed'
        rawpath = OUT / f'sources/walk-{n:03}-head-edit-v4.png'
        assert hashlib.sha256(rawpath.read_bytes()).hexdigest() == job['sha256']
        assert hashlib.sha256(Path(job['originalPath']).read_bytes()).hexdigest() == job['sha256']
        assert hashlib.sha256(Path(job['promptFile']).read_bytes()).hexdigest() == job['promptSha256'] == job['submittedPromptSha256']
        for ref in job['references']:
            assert hashlib.sha256(Path(ref['path']).read_bytes()).hexdigest() == ref['sha256']
        raw = Image.open(rawpath).convert('RGBA')
        assert raw.width == raw.height
        # Normalize the whole transparent canvas only. No pose or head fitting.
        candidate = raw.resize((256, 256), Image.Resampling.LANCZOS)
        candidate.save(OUT / f'canvas-normalized-study-{n:03}.png')
        generated = True
    images[n] = [old, previous, candidate]
    om, pm, cm = [mask(im) for im in images[n]]
    bodyp, bodyc = pm.copy(), cm.copy()
    bodyp[:110] = False
    bodyc[:110] = False
    pa, ca = np.array(previous), np.array(candidate)
    rows.append({
        'frame': n, 'newSourceEdit': generated,
        'selectedBounds': bounds(om), 'previousBounds': bounds(pm), 'candidateBounds': bounds(cm),
        'candidateVsSelectedIoU': float((om & cm).sum()/(om | cm).sum()),
        'bodyBelow110VsPreviousIoU': float((bodyp & bodyc).sum()/(bodyp | bodyc).sum()),
        'bodyBelow110ChangedRgbaPixels': int(np.any(pa[110:] != ca[110:], axis=2).sum()),
        'bodyBelow110MaxChannelDifference': int(np.abs(pa[110:].astype(int)-ca[110:].astype(int)).max()),
        'scope': 'Body/crown diagnostic only; face, collar, contact and full-loop acceptance require visual and motion review.'
    })

poseboard = Image.new('RGB', (768, 930), (23, 42, 51))
headboard = Image.new('RGB', (1200, 780), (23, 42, 51))
pd, hd = ImageDraw.Draw(poseboard), ImageDraw.Draw(headboard)
for col, n in enumerate([47, 0, 1]):
    for row, (name, im) in enumerate(zip(['Selected', 'Previous material', 'Head correction'], images[n])):
        pd.text((col*256+8, row*300+5), f'{name} {n:03}', fill='white')
        poseboard.paste(im, (col*256, row*300+25), im)
        crop = im.crop((108, 70, 143, 111)).resize((210, 246), Image.Resampling.NEAREST)
        headboard.paste(crop, (col*400, row*260+15), crop)
        hd.text((col*400+220, row*260+15), f'{name}\n{n:03}', fill='white')
poseboard.save(OUT/'whole-pose-review.png')
headboard.save(OUT/'face-collar-review.png')

oldy = [r['selectedBounds'][1] for r in rows]
prevy = [r['previousBounds'][1] for r in rows]
newy = [r['candidateBounds'][1] for r in rows]
report = {
    'status': 'head_correction_source_study_unselected', 'poses': rows,
    'frames': [47, 0, 1], 'selectedCrownY': oldy, 'previousCrownY': prevy, 'candidateCrownY': newy,
    'candidateCrownMatchesSelected': newy == oldy,
    'boundedInputsUnchanged': len(freeze), 'newSourceEdits': 2,
    'distinctBareStudiesIncludingV2': 6, 'remainingBare': 42, 'remainingHelmet': 48,
    'normalAdmission': False, 'nativeAcceptance': False,
    'scope': 'Two revisions of existing poses plus an unchanged frame47 context. No new complete gait or standing density proof.'
}
if (OUT/'rejection.json').exists():
    report['status'] = 'rejected_head_motion_source_study'
    report['rejection'] = 'rejection.json'
(OUT/'review.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')

holds = json.loads((BANK/'manifest.json').read_text(encoding='utf-8'))['states'][0]['frameDurationsMs']
assert len(holds) == 48 and sum(holds) == 2000
segments = {'wrap': {'frames': [47, 0, 1], 'holds': [holds[n] for n in [47, 0, 1]]}}
paths = {}
for n in [47, 0, 1]:
    previous = f'/character/bill-walk-west-master-repair-v2/canvas-normalized-study-{n:03}.png'
    paths[str(n)] = {'old': previous, 'new': previous if n == 47 else f'canvas-normalized-study-{n:03}.png'}
html = (BASE/'sources/context-template.html').read_text(encoding='utf-8')
html = re.sub(r'const segments=.*?;const paths=.*?;', lambda m: 'const segments='+json.dumps(segments)+';const paths='+json.dumps(paths)+';', html, count=1)
html = html.replace('<option value="adjacent">Adjacent poses Ã‚Â· 34 Ã¢â€ â€™ 35</option>', '')
html = html.replace('Bill West walking continuity', 'Bill West head continuity correction')
html = html.replace('Selected walking<canvas', 'Previous material edit<canvas').replace('Material edit<canvas', 'Head correction<canvas')
html = html.replace('six-pose-context-review.png', 'whole-pose-review.png')
html = html.replace('Six authored source studies', 'Whole pose and head attachment review')
html = html.replace('Selected and edited frames47,0,1,28,34,35 with head closeups', 'Selected, previous and corrected poses at47,0,1')
html = html.replace('6 of48bare phases authored; helmet version and full-loop continuity still pending.', 'Two revisions of existing poses. Full48phase gait and helmet continuity remain pending.')
html = html.replace('</script>', '</script><h2>Face and collar</h2><img src="face-collar-review.png" alt="Face and collar comparison at the loop boundary">')
(OUT/'index.html').write_text(html, encoding='utf-8')
print(json.dumps({'selectedCrownY': oldy, 'previousCrownY': prevy, 'candidateCrownY': newy, 'bodyDiagnostics': rows, 'boundedInputs': len(freeze)}))

if (OUT/'rejection.json').exists():
    p=OUT/'index.html'
    text=p.read_text(encoding='utf-8').replace('<h1>Bill West head continuity correction</h1>', '<h1>Bill West head continuity study — rejected</h1><p>Rejected source experiment. Head motion does not match the intended trajectory; do not install.</p>')
    p.write_text(text,encoding='utf-8')

p=OUT/'index.html'
html=p.read_text(encoding='utf-8')
html=re.sub(r'<select id="segment">.*?</select>', '<select id="segment"><option value="wrap">Loop boundary: 47 to 0 to 1</option></select>',html,count=1,flags=re.S)
p.write_text(html,encoding='utf-8')
