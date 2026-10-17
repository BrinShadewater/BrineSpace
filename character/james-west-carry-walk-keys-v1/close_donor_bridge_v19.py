from pathlib import Path
import hashlib, json, os, subprocess, uuid
import numpy as np
from PIL import Image

p = Path(__file__).resolve().parent
r = p.parents[1]
out = p / 'donor-bridge-v19'
def sha(f): return hashlib.sha256(f.read_bytes()).hexdigest()
def save(f, d): f.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')

generations = []
for i in (1, 2):
    name = f'start-{i:03}'
    inputs = json.loads((out / f'{name}-inputs.json').read_bytes())
    assert all(sha(r / f) == v for f, v in inputs['preCallSha256'].items())
    base = np.array(Image.open(r / inputs['baseFile']).convert('RGBA'))
    candidate = np.array(Image.open(out / f'{name}.png').convert('RGBA'))
    mask = np.ones((256, 256), bool)
    mask[104:228, 88:166] = False
    mask[62:110, 102:155] = True
    assert mask.sum() == 56182 and np.array_equal(base[mask], candidate[mask])
    review = json.loads((out / f'{name}-review.json').read_bytes())
    assert review['rawSha256'] == sha(out / f'{name}-raw.png')
    generation = json.loads((out / f'{name}-generation.json').read_bytes())
    assert generation['terminal']
    review.update(visualReviewPending=False, sourceAcceptance=False, selected=False,
        disposition='rejected_nonprogressive_stance_and_equipment_drift',
        findings=[
            'Raw and donor/native comparison reviewed; whole and body four-pose paired boards reviewed.',
            'Pose1 lowers the knees and retains a conspicuous long near-side yellow belt item. Pose2 returns toward the broad standing stance instead of the intended narrower profile donor.',
            'Ordered standing/pose1/pose2/walk0 chain does not progressively approach the walking stance. Case face, latch geometry and equipment change across the chain.',
            'Master head identity and protected pixels pass, but generated legs are not original-donor-exact. Do not infer motion acceptance from those guards.',
            'No finite clip or runtime adoption. Both full-body endpoint edits and full-body donor repairs failed; next isolate lower-body stance authoring from the fixed case, grip and upper-body reference.'
        ])
    save(out / f'{name}-review.json', review)
    generations.append(dict(slot=i, tool='builtin_image_gen', prompt=f'{name}-prompt.txt',
        raw=f'{name}-raw.png', rawSha256=review['rawSha256'], terminal=True, used=False,
        disposition=review['disposition']))
save(out / 'generation-index.json', dict(generations=generations, allTerminalAndCopied=True))
chain = json.loads((out / 'chain-review.json').read_bytes())
chain.update(visualReviewPending=False, sourceAcceptance=False, selected=False,
    reviewedBoards=['chain-whole.png', 'chain-body.png'],
    disposition='rejected_nonprogressive_stance_and_equipment_drift',
    nativeRun=False, normalChanged=False, fullGoalComplete=False)
save(out / 'chain-review.json', chain)
rasters = [f.relative_to(r).as_posix() for f in out.iterdir() if f.suffix == '.png']
attrs = subprocess.run(['git', 'check-attr', '-z', 'filter', '--stdin'], cwd=r,
    input=b'\0'.join(x.encode() for x in rasters) + b'\0', capture_output=True, check=True).stdout.split(b'\0')
assert len(attrs) == len(rasters)*3+1 and all(x == b'lfs' for x in attrs[2:-1:3])
section = '''### James actual-pose carrying bridge rejection — October 2, 2026

V19 two actual West settle donor repairs generated, terminal/copied, both raw and
native comparisons reviewed plus whole/body four-pose paired boards. Rejected:
pose1 lowers knees and retains a long near-side belt item; pose2 returns toward
the broad standing stance. Neither ordered chain progressively reaches walk0.
Case face/latch geometry and equipment change. Exact master head and56182 outside
body/restored-head pixels pass, but generated legs are not donor-exact. Technical
guards cannot establish motion or equipment acceptance. No finite bridge/native
run/adoption. V16 walk candidate and normal runtime remain unchanged.
Lesson: old donor poses carry old equipment/material assumptions; a full-body
master repair can regenerate stance despite explicit donor-preservation prompts.
After endpoint and full-body donor failures, isolate the lower-body stance region
and keep case/grip/upper-body fixed to a named master source; review pelvis/knee/
boot chronology before spending on material repair. Do not repeat the same broad
repair with another fractional yaw instruction. Height must be assessed at the
declared pivot/ruler, never corrected by fitting each silhouette.
Full James master/cardinal consistency, cargo joins, actual room dispatch and
interruptions/Continue remain incomplete. Evidence and prompts:
character/james-west-carry-walk-keys-v1/donor-bridge-v19/generation-index.json.
'''
paths = [r/'docs/CURRENT_STATUS.md', r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',
    r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',
    Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in paths:
    old = path.read_bytes(); entry = section.encode()
    if entry.split(b'\n', 1)[0] in old: continue
    if path.name == 'CURRENT_STATUS.md':
        at = old.index(b'### James full primary-source inventory and stance reference audit')
        new = old[:at] + entry + b'\n' + old[at:]
    else: new = old + b'\n' + entry
    temp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        temp.write_bytes(new)
        assert path.read_bytes() == old
        os.replace(temp, path)
    finally:
        if temp.exists(): temp.unlink()
f = p / 'HANDOFF.md'
old = f.read_text(encoding='utf-8')
marker = '## V19 actual-pose donor review\n'
if marker not in old:
    at = old.index('## Next action\n')
    old = old[:at] + marker + '''Two actual settle donor master repairs terminal/copied and rejected after raw,
comparison and paired chain review: knees/stance do not progress toward walk0,
case/latches and equipment drift.56182 protected pixels and frozen inputs exact.
Generated legs are not donor-exact. No finite bridge/native adoption. All five
guides updated. Prompts/dispositions:donor-bridge-v19/generation-index.json.
Next stance attempt should isolate lower-body authoring while keeping the named
master case/grip/upper body fixed, and first establish credible leg chronology.

''' + old[at:]
    f.write_text(old, encoding='utf-8')
print(json.dumps(dict(rejectedTrials=2, reviewedRawImages=2, reviewedComparisons=2,
    reviewedChainBoards=2, frozenInputsStable=True, protectedPixels=56182,
    guides=5, lfsRasters=len(rasters), nativeRun=False, normalChanged=False)))
