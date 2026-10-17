from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'thigh-crossing-fine-v281';w=p/'thigh-window-v282';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((o/'inputs.json').read_bytes());n=json.loads((w/'native-evidence.json').read_bytes());v=json.loads((w/'native_probe-validation.json').read_bytes());frozen=json.loads((w/'inputs.json').read_bytes());report=json.loads((o/'package-review.json').read_bytes())
assert all(sha(r/f)==h for f,h in d['referenceSha256'].items()) and sha(o/'prompt.txt')==d['promptSha256']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
assert (n['checks'],n['failures'],n['captures'])==(112,0,8)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
for row in d['sources']:
 for mode,item in row['files'].items():
  assert sha(r/item['file'])==item['sha256']
  if row['phase']==31:assert (r/item['file']).read_bytes()==(o/f'phase31/{mode}-head-protected.png').read_bytes()
report.update(disposition='unselected_crossing_stitch_refinement',rawVisuallyReviewed=True,sourceBoardsReviewed=['thigh-detail-review.png','paired-source-review.png'],nativeWindow=282,nativeIncluded=True,findings=['28..30 near-thigh stitching has softer narrower ridges; original alpha/silhouette/full knee and glove guards unchanged in both gears. Generator changed calf seams and reference31 in raw; protected pixels and entire reference31 preserved in package.', 'Same-mask medians move72.50to73.64,73.74to74.85,73.64to75.14; p95 rises29/30. Numerical old-source preservation cannot certify actual master fabric grade; whole moving material still pending.', 'Far-side parallel folds/stripes remain outside these masks; do not certify all thigh cloth. Native112/0/8 verifies26..33 sources/clocks/rulers, not traveling contact or normal controller lifecycle.'])
(o/'package-review.json').write_text(json.dumps(report,indent=2)+'\n')
(o/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='e111d2bf-7b62-4f2b-b2e5-e3675cd8be46',method='builtin_imagegen_three_targets_unchanged_reference',rawSha256=sha(o/'raw.png'),prompt='prompt.txt'),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old)
for phase in [28,29,30]:
 prev=next(s for s in j['thighConstructionStudies'] if s['phase']==phase);j.setdefault('supersededThighConstructionStudies',[]).append(prev)
 j['thighConstructionStudies']=[s for s in j['thighConstructionStudies'] if s['phase']!=phase]+[dict(phase=phase,version=281,sources={mode:dict(file=(o/f'phase{phase}/{mode}-head-protected.png').relative_to(r).as_posix(),sha256=sha(o/f'phase{phase}/{mode}-head-protected.png')) for mode in ['bare','helmet']},selected=False)]
j['nextVisualRepair']='V281 softens near-thigh stitching28..30; examine far-side stripes/folds separately with leg/equipment guards. Whole updated49 motion and seam/equipment-free master material samples remain, then anatomical/contact/helmet comparison and normal cargo lifecycle integration. All-family consistency/polish open.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
(w/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,nativeCaptures=8,sourceIndices=list(range(26,34)),nativeBoardsVisuallyReviewed=[0,1,2],selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
section='''### James crossing stitch refinement with protected neighboring pose - October3,2026

V281 edits current unselected28..30 near-thigh cloth using original master and
unchanged31 reference. Raw/detail/paired boards inspected; softer finer ridges,
215/142/126RGB pixels admitted, source alpha/silhouette/outside, full knee rims
and glove guards preserved for both gears. Generator changed lower-leg seams
and reference31 in raw; local admission excludes these, packaged31 byte-exact.
Same-mask median72.50to73.64/73.74to74.85/73.64to75.14;29/30p95 rises.
These are unselected stitch studies, not final original-master colour acceptance.
V282 original26..33 clock320ms,16paired sources;112native checks0/8captures,
scratch owner unchanged, frozen hashes stable. All three native boards inspected.

Lesson: fine-stitch wording can reduce pronounced ridges yet generation still
redesigns neighboring calf seams. Protect cloth components and unchanged reference
cells locally; paired head/body invariants are separate from whole-master fidelity.
Far-side stripe/fold construction remains outside these masks. Next separate
far-side garment review, whole latest49 moving comparison and seam/equipment-free
master cloth sampling. Whole anatomy/contact/helmet, normal cargo integration and
all-family polish remain. Goal active/incomplete; no normal selection changed.
Handoff: character/james-west-carry-walk-keys-v1/thigh-window-v282/HANDOFF.md.
'''
guides=record_guides(r,section,'### James latest full carrying study and original-cloth reference correction')
handoff='''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James crossing cloth refinement

## Objective and acceptance
Full original-master animation set, then cross-family consistency and polish.

## Accepted decisions and constraints
Fine matte quilting, muted yellow seam, original anatomy/perspective/equipment.
Protect complete knee rims/glove; wrench on belt. Studies remain unselected.

## Current state
V281 three paired revised near-thigh poses28..30; frozen prompt, two references,
raw, package/proofs and review.31 reference retained byte-exact. Latest study ledger
replaces28..30 refs with281, preserving superseded276 refs. Five guides updated.

## Verification
Raw and both source boards viewed.112native checks0/8captures26..33; all three
native boards viewed; scratch isolation/owner unchanged/frozen hashes stable.
Outside masks/alpha/silhouette/knee/glove exact, shared body exact. Not full moving
contact, grade/anatomy acceptance or normal runtime integration.

## Next action
Review far-side stripe/fold surface with component guards; seam/equipment-free
original cloth samples, full latest49 moving comparison, helmet/anatomical/contact
fidelity. Then versioned normal cargo joins, lifecycle/Continue and all-family polish.
'''
for folder in [o,w]:(folder/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [o,w] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(revisedPairedPoses=3,checks=112,failures=0,captures=8,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
