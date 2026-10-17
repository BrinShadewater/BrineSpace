from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'far-thigh-v283';w=p/'thigh-window-v284';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((o/'inputs.json').read_bytes());n=json.loads((w/'native-evidence.json').read_bytes());v=json.loads((w/'native_probe-validation.json').read_bytes());frozen=json.loads((w/'inputs.json').read_bytes());report=json.loads((o/'package-review.json').read_bytes())
assert all(sha(r/f)==s for f,s in d['referenceSha256'].items()) and sha(o/'prompt.txt')==d['promptSha256']
assert all(sha(r/f)==s for f,s in frozen['preLaunchSha256'].items())
assert (n['checks'],n['failures'],n['captures'])==(112,0,8)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
for row in d['sources']:
 for mode,item in row['files'].items():
  assert sha(r/item['file'])==item['sha256']
  if row['phase']==31:assert (r/item['file']).read_bytes()==(o/f'phase31/{mode}-head-protected.png').read_bytes()
report.update(disposition='unselected_far_thigh_construction_refinement',rawVisuallyReviewed=True,sourceBoardsReviewed=['thigh-detail-review.png','paired-source-review.png'],nearThighProtectedBothGears=True,nativeWindow=284,nativeIncluded=True,findings=['Far-side cloth28..30 has softer folds/fine stitching, reduced bold parallel stripes.65/102/63RGB pixels admitted; original alpha/silhouette/full knee/glove/near-thigh polygons remain exact. Entire31 reference byte-exact.', 'Raw authoring changed belt details and lower-leg seams; excluded from packaged sources. Near/far separation and outline remain from originals; physical moving contact/anatomy not proven by pixel guards.', 'Same-mask medians54.28to64.64/46.36to55.17/45.28to57.43. Material lighter than old folds but these old pixels alone are not master-colour target. Full temporal/master grade and remaining transitions pending.'])
(o/'package-review.json').write_text(json.dumps(report,indent=2)+'\n');(o/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='bea3a6bf-b758-44bb-89c6-c812c1ec79ad',method='builtin_imagegen_far_component_three_targets_with_region_guide',rawSha256=sha(o/'raw.png'),prompt='prompt.txt'),indent=2)+'\n')
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();j=json.loads(old)
for phase in [28,29,30]:
 prev=next(s for s in j['thighConstructionStudies'] if s['phase']==phase);j.setdefault('supersededThighConstructionStudies',[]).append(prev)
 j['thighConstructionStudies']=[s for s in j['thighConstructionStudies'] if s['phase']!=phase]+[dict(phase=phase,version=283,sources={mode:dict(file=(o/f'phase{phase}/{mode}-head-protected.png').relative_to(r).as_posix(),sha256=sha(o/f'phase{phase}/{mode}-head-protected.png')) for mode in ['bare','helmet']},selected=False)]
j['nextVisualRepair']='Far-thigh283 softens stripe folds28..30 while preserving281 near-leg pixels. Full latest49 moving/master/seam comparison, late44..46 equipment chronology and seam-free cloth grade needed. Whole anatomy/contact/helmet, versioned normal cargo lifecycle and cross-family consistency/polish remain.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(j,indent=2)+'\n')
(w/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,nativeCaptures=8,sourceIndices=list(range(26,34)),nativeBoardsVisuallyReviewed=[0,1,2],selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
section='''### James separate far-thigh cloth and near-leg identity guard - October3,2026

V283 separate far-side cloth28..30 authoring, original fine-quilt master, explicit
cyan region guide and unchanged31 reference. Current281 near-thigh polygons,
full knees/gloves and original silhouette remain byte-exact both gears.65/102/63
RGB pixels admitted; raw/detail/paired boards inspected. Bold parallel far-side
stripes soften while original near/far overlap boundary remains. Raw belt details
and calf seams changed despite prompt, excluded from packaged components.
Original31 reference byte-exact. Medians54.28to64.64/46.36to55.17/45.28to57.43;
these old folds alone cannot establish original-master grade acceptance.
V28426..33 clock320ms,16paired sources;112native checks0/8captures, all three
native boards inspected. Scratch owner profile unchanged; frozen hashes stable.
Candidates unselected, no normal bank change or whole moving fidelity acceptance.

Lesson: protect previously repaired near-leg polygons as well as hardware when
editing far-leg cloth. A region guide does not stop generator equipment drift;
exclude every non-admitted pixel. Preserved overlap proves source geometry stayed,
not that physical root travel/contact is correct. Next whole latest49 moving/master
comparison, late equipment chronology and seam-free master material sampling;
then normal cargo lifecycle/Continue and cross-family polish. Goal incomplete.
Handoff: character/james-west-carry-walk-keys-v1/thigh-window-v284/HANDOFF.md.
'''
guides=record_guides(r,section,'### James crossing stitch refinement with protected neighboring pose')
handoff='''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James far-thigh refinement

## Objective and acceptance
Full James master-matched animation set, integrated and cross-family polished.

## Accepted decisions and constraints
Matte fine quilt, muted yellow seam. Wrench remains on belt, tablet diagnostics,
forward torch repairs. Near-leg refinements and complete knee/glove protected.

## Current state
Far-thigh-v283 revises only far cloth28..30;31 reference byte-exact. Frozen prompt,
three references, raw, package/invariant evidence. Latest unselected study ledger
uses283 for28..30; older281 refs preserved. Five guides updated. Normal bank unchanged.

## Verification
Raw/detail/paired source and three native boards inspected.112checks0/8captures
26..33. Scratch profile, real owner unchanged, frozen hashes stable; source alpha,
silhouette, outside masks, near-leg polygons/knees/glove/shared body exact.
Full moving contact, master colour/anatomy and normal lifecycle remain unproven.

## Next action
Whole latest49 moving/master comparison and seam-free fabric sample review;
resolve late44..46 belt equipment identity before edits. Whole helmet/proportion/
contact acceptance, versioned normal pickup/carry/turn/unload, interruptions and
Continue, complete action coverage and all-family consistency/polish remain.
'''
for folder in [o,w]:(folder/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in [o,w] for f in folder.rglob('*') if f.suffix.lower() in ['.png','.apng']];attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(revisedPairedPoses=3,checks=112,failures=0,captures=8,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
